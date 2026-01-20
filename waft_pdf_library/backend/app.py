import hashlib
import json
import os
import shutil
import sqlite3
import subprocess
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "library.db"
CONFIG_PATH = BASE_DIR / "config" / "library.json"
TYPST_TEMPLATES_DIR = BASE_DIR / "typst" / "templates"
GENERATED_DIR = DATA_DIR / "generated"
VERSIONS_DIR = DATA_DIR / "versions"

DATA_DIR.mkdir(parents=True, exist_ok=True)
GENERATED_DIR.mkdir(parents=True, exist_ok=True)
VERSIONS_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="WAFT PDF Library")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4433", "http://127.0.0.1:4433"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class CompileRequest(BaseModel):
    template: str
    output_name: str | None = None


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def read_config():
    if not CONFIG_PATH.exists():
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        CONFIG_PATH.write_text(
            json.dumps({"roots": [str(BASE_DIR.parent.parent)], "ignore_dirs": []}, indent=2)
            + "\n"
        )
    return json.loads(CONFIG_PATH.read_text())


def init_db():
    with get_db() as conn:
        conn.execute(
            """
            create table if not exists pdfs (
                id text primary key,
                name text,
                path text,
                size integer,
                mtime real,
                sha256 text,
                missing integer default 0,
                created_at text,
                updated_at text
            )
            """
        )
        conn.execute(
            """
            create table if not exists pdf_versions (
                id integer primary key autoincrement,
                pdf_id text,
                version_label text,
                path text,
                size integer,
                mtime real,
                sha256 text,
                created_at text
            )
            """
        )


def sha256_file(path: Path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def scan_library():
    config = read_config()
    roots = config.get("roots", [])
    ignore_dirs = set(config.get("ignore_dirs", []))
    now_iso = datetime.utcnow().isoformat()

    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("update pdfs set missing = 1")

        total = 0
        new_files = 0
        updated_files = 0
        for root in roots:
            root_path = Path(root)
            if not root_path.exists():
                continue

            for dirpath, dirnames, filenames in os.walk(root_path):
                dirnames[:] = [d for d in dirnames if d not in ignore_dirs]
                for filename in filenames:
                    if not filename.lower().endswith(".pdf"):
                        continue

                    full_path = Path(dirpath) / filename
                    try:
                        stat = full_path.stat()
                    except OSError:
                        continue

                    doc_id = hashlib.sha256(str(full_path).encode()).hexdigest()[:16]
                    size = stat.st_size
                    mtime = stat.st_mtime
                    row = cur.execute(
                        "select sha256, size, mtime from pdfs where id = ?",
                        (doc_id,),
                    ).fetchone()

                    if row and row["size"] == size and row["mtime"] == mtime:
                        cur.execute("update pdfs set missing = 0 where id = ?", (doc_id,))
                        total += 1
                        continue

                    file_hash = sha256_file(full_path)
                    version_label = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
                    version_path = VERSIONS_DIR / doc_id / f"{version_label}_{file_hash[:8]}.pdf"
                    version_path.parent.mkdir(parents=True, exist_ok=True)

                    if row is None:
                        new_files += 1
                        cur.execute(
                            """
                            insert into pdfs (id, name, path, size, mtime, sha256, missing, created_at, updated_at)
                            values (?, ?, ?, ?, ?, ?, 0, ?, ?)
                            """,
                            (
                                doc_id,
                                filename,
                                str(full_path),
                                size,
                                mtime,
                                file_hash,
                                now_iso,
                                now_iso,
                            ),
                        )
                    else:
                        updated_files += 1
                        cur.execute(
                            """
                            update pdfs
                            set name = ?, path = ?, size = ?, mtime = ?, sha256 = ?, missing = 0, updated_at = ?
                            where id = ?
                            """,
                            (
                                filename,
                                str(full_path),
                                size,
                                mtime,
                                file_hash,
                                now_iso,
                                doc_id,
                            ),
                        )

                    if row is None or row["sha256"] != file_hash:
                        try:
                            shutil.copy2(full_path, version_path)
                        except OSError:
                            version_path = full_path
                        cur.execute(
                            """
                            insert into pdf_versions (pdf_id, version_label, path, size, mtime, sha256, created_at)
                            values (?, ?, ?, ?, ?, ?, ?)
                            """,
                            (
                                doc_id,
                                version_label,
                                str(version_path),
                                size,
                                mtime,
                                file_hash,
                                now_iso,
                            ),
                        )

                    total += 1

        conn.commit()

    return {"total": total, "new": new_files, "updated": updated_files}


@app.on_event("startup")
def startup_event():
    init_db()
    scan_library()


@app.get("/api/health")
def health_check():
    return {"status": "ok", "time": datetime.utcnow().isoformat()}


@app.get("/api/config")
def get_config():
    return read_config()


@app.post("/api/scan")
def scan_endpoint():
    return scan_library()


@app.get("/api/pdfs")
def list_pdfs(query: str | None = None):
    with get_db() as conn:
        if query:
            rows = conn.execute(
                """
                select id, name, path, size, mtime, sha256, updated_at
                from pdfs
                where missing = 0 and (name like ? or path like ?)
                order by updated_at desc
                """,
                (f"%{query}%", f"%{query}%"),
            ).fetchall()
        else:
            rows = conn.execute(
                """
                select id, name, path, size, mtime, sha256, updated_at
                from pdfs
                where missing = 0
                order by updated_at desc
                """
            ).fetchall()

    items = []
    for row in rows:
        items.append(
            {
                "id": row["id"],
                "name": row["name"],
                "path": row["path"],
                "size": row["size"],
                "mtime": row["mtime"],
                "updated_at": row["updated_at"],
            }
        )

    return {"items": items, "count": len(items)}


@app.get("/api/pdfs/{pdf_id}")
def get_pdf(pdf_id: str):
    with get_db() as conn:
        row = conn.execute(
            """
            select id, name, path, size, mtime, sha256, updated_at, missing
            from pdfs where id = ?
            """,
            (pdf_id,),
        ).fetchone()

    if not row or row["missing"]:
        raise HTTPException(status_code=404, detail="PDF not found")

    return {
        "id": row["id"],
        "name": row["name"],
        "path": row["path"],
        "size": row["size"],
        "mtime": row["mtime"],
        "updated_at": row["updated_at"],
    }


@app.get("/api/pdfs/{pdf_id}/file")
def get_pdf_file(pdf_id: str):
    with get_db() as conn:
        row = conn.execute(
            "select path, missing from pdfs where id = ?",
            (pdf_id,),
        ).fetchone()

    if not row or row["missing"]:
        raise HTTPException(status_code=404, detail="PDF not found")

    path = Path(row["path"])
    if not path.exists():
        raise HTTPException(status_code=404, detail="PDF missing on disk")

    return FileResponse(path, media_type="application/pdf")


@app.get("/api/pdfs/{pdf_id}/versions")
def list_versions(pdf_id: str):
    with get_db() as conn:
        rows = conn.execute(
            """
            select id, version_label, path, size, mtime, sha256, created_at
            from pdf_versions
            where pdf_id = ?
            order by created_at desc
            """,
            (pdf_id,),
        ).fetchall()

    items = []
    for row in rows:
        items.append(
            {
                "id": row["id"],
                "version_label": row["version_label"],
                "path": row["path"],
                "size": row["size"],
                "mtime": row["mtime"],
                "sha256": row["sha256"],
                "created_at": row["created_at"],
            }
        )

    return {"items": items, "count": len(items)}


@app.get("/api/typst/templates")
def list_templates():
    if not TYPST_TEMPLATES_DIR.exists():
        return {"items": []}

    items = []
    for path in sorted(TYPST_TEMPLATES_DIR.glob("*.typ")):
        items.append({"name": path.stem, "path": str(path)})

    return {"items": items}


@app.post("/api/typst/compile")
def compile_typst(request: CompileRequest):
    template_name = request.template.strip()
    if not template_name:
        raise HTTPException(status_code=400, detail="Template name required")

    template_path = TYPST_TEMPLATES_DIR / f"{template_name}.typ"
    if not template_path.exists():
        raise HTTPException(status_code=404, detail="Template not found")

    if shutil.which("typst") is None:
        raise HTTPException(status_code=500, detail="typst CLI not installed")

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    output_name = request.output_name or f"{template_name}_{timestamp}.pdf"
    output_path = GENERATED_DIR / output_name

    result = subprocess.run(
        ["typst", "compile", str(template_path), str(output_path)],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        detail = result.stderr.strip() or "Typst compilation failed"
        raise HTTPException(status_code=500, detail=detail)

    with get_db() as conn:
        doc_id = hashlib.sha256(str(output_path).encode()).hexdigest()[:16]
        stat = output_path.stat()
        file_hash = sha256_file(output_path)
        now_iso = datetime.utcnow().isoformat()

        conn.execute(
            """
            insert or replace into pdfs (id, name, path, size, mtime, sha256, missing, created_at, updated_at)
            values (?, ?, ?, ?, ?, ?, 0, ?, ?)
            """,
            (
                doc_id,
                output_path.name,
                str(output_path),
                stat.st_size,
                stat.st_mtime,
                file_hash,
                now_iso,
                now_iso,
            ),
        )
        conn.execute(
            """
            insert into pdf_versions (pdf_id, version_label, path, size, mtime, sha256, created_at)
            values (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                doc_id,
                timestamp,
                str(output_path),
                stat.st_size,
                stat.st_mtime,
                file_hash,
                now_iso,
            ),
        )
        conn.commit()

    return {
        "id": doc_id,
        "name": output_path.name,
        "path": str(output_path),
        "size": stat.st_size,
        "mtime": stat.st_mtime,
        "updated_at": now_iso,
    }
