"""
FastAPI Backend for Typst Demo Web App
Serves PDF demos and provides Typst compilation API
"""

import os
import subprocess
import tempfile
import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

app = FastAPI(
    title="Typst Demo API",
    description="API for compiling Typst documents and serving PDF demos",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths
BASE_DIR = Path(__file__).parent.parent.parent
TYPST_DEMOS_DIR = BASE_DIR / "typst-demos"
TEMP_DIR = Path(tempfile.gettempdir()) / "typst-webapp"
TEMP_DIR.mkdir(exist_ok=True)


class CompileRequest(BaseModel):
    content: str
    filename: str = "document"


class TemplateInfo(BaseModel):
    name: str
    description: str
    package: str
    version: str
    url: str


TEMPLATES = {
    "drafting": TemplateInfo(
        name="Drafting Demo",
        description="Margin notes and annotations for document review",
        package="drafting",
        version="0.2.2",
        url="https://typst.app/universe/package/drafting",
    ),
    "s6t5-page-bordering": TemplateInfo(
        name="Page Bordering Demo",
        description="Professional page borders with headers and footers",
        package="s6t5-page-bordering",
        version="1.0.0",
        url="https://typst.app/universe/package/s6t5-page-bordering",
    ),
    "scaffolder": TemplateInfo(
        name="Scaffolder Demo",
        description="Layout debugging borders for text area, header and footer",
        package="scaffolder",
        version="0.2.1",
        url="https://typst.app/universe/package/scaffolder",
    ),
    "codly": TemplateInfo(
        name="Codly Demo",
        description="Beautiful code blocks with line numbers, highlighting, and language icons",
        package="codly",
        version="1.3.0",
        url="https://typst.app/universe/package/codly",
    ),
    "pinit": TemplateInfo(
        name="Pinit Demo",
        description="Relative positioning by pins for annotations, arrows, and slides",
        package="pinit",
        version="0.2.2",
        url="https://typst.app/universe/package/pinit",
    ),
    "showybox": TemplateInfo(
        name="Showybox Demo",
        description="Colorful and customizable boxes for callouts and notes",
        package="showybox",
        version="2.0.4",
        url="https://typst.app/universe/package/showybox",
    ),
    "stack-pointer": TemplateInfo(
        name="Stack Pointer Demo",
        description="Program execution and call stack visualization for CS education",
        package="stack-pointer",
        version="0.1.0",
        url="https://typst.app/universe/package/stack-pointer",
    ),
}


@app.get("/")
async def root():
    return {
        "message": "Typst Demo API",
        "endpoints": {
            "templates": "/api/templates",
            "pdf": "/api/pdf/{template_name}",
            "source": "/api/source/{template_name}",
            "compile": "/api/compile",
        },
    }


@app.get("/api/templates")
async def list_templates():
    return {"templates": {k: v.model_dump() for k, v in TEMPLATES.items()}}


@app.get("/api/pdf/{template_name}")
async def get_pdf(template_name: str):
    if template_name not in TEMPLATES:
        raise HTTPException(status_code=404, detail=f"Template '{template_name}' not found")
    
    pdf_path = TYPST_DEMOS_DIR / f"{template_name}-demo.pdf"
    if not pdf_path.exists():
        raise HTTPException(status_code=404, detail=f"PDF file not found at {pdf_path}")
    
    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=f"{template_name}-demo.pdf",
    )


@app.get("/api/source/{template_name}")
async def get_source(template_name: str):
    if template_name not in TEMPLATES:
        raise HTTPException(status_code=404, detail=f"Template '{template_name}' not found")
    
    typ_path = TYPST_DEMOS_DIR / f"{template_name}-demo.typ"
    if not typ_path.exists():
        raise HTTPException(status_code=404, detail=f"Source file not found at {typ_path}")
    
    content = typ_path.read_text()
    return {"content": content, "filename": f"{template_name}-demo.typ"}


@app.post("/api/compile")
async def compile_typst(request: CompileRequest):
    # Create unique filename
    unique_id = str(uuid.uuid4())[:8]
    typ_file = TEMP_DIR / f"{request.filename}_{unique_id}.typ"
    pdf_file = TEMP_DIR / f"{request.filename}_{unique_id}.pdf"
    
    try:
        typ_file.write_text(request.content)
        
        result = subprocess.run(
            ["typst", "compile", str(typ_file), str(pdf_file)],
            capture_output=True,
            text=True,
            timeout=30,
        )
        
        if result.returncode != 0:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": result.stderr or "Compilation failed",
                    "stdout": result.stdout,
                },
            )
        
        if not pdf_file.exists():
            return JSONResponse(
                status_code=500,
                content={"success": False, "error": "PDF file was not created"},
            )
        
        return FileResponse(
            pdf_file,
            media_type="application/pdf",
            filename=f"{request.filename}.pdf",
        )
    
    except subprocess.TimeoutExpired:
        return JSONResponse(
            status_code=408,
            content={"success": False, "error": "Compilation timed out"},
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)},
        )
    finally:
        if typ_file.exists():
            typ_file.unlink()


@app.get("/health")
async def health_check():
    typst_available = subprocess.run(
        ["which", "typst"], capture_output=True
    ).returncode == 0
    
    return {
        "status": "healthy",
        "typst_available": typst_available,
        "demos_dir": str(TYPST_DEMOS_DIR),
        "demos_exist": TYPST_DEMOS_DIR.exists(),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
