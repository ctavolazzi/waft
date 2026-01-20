"""
Scribe: Hand of the Librarian

The Scribe writes records into the Library Realm under the Librarian's direction.
Creates timestamped script files for audit trail.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class Scribe:
    """
    Scribe: Hand of the Librarian

    Writes records into the Library Realm, creating timestamped script files
    for audit trail and record keeping.

    Storage:
    - Scripts: _pantheon/library/scripts/[timestamp]_[description].json
    """

    def __init__(self, scripts_dir: Path):
        """
        Initialize the Scribe.

        Args:
            scripts_dir: Directory where scripts are written
        """
        self.scripts_dir = Path(scripts_dir)
        self.scripts_dir.mkdir(parents=True, exist_ok=True)

    def write_script(
        self, description: str, data: dict[str, Any], script_type: str = "record"
    ) -> Path:
        """
        Write a script (timestamped record file).

        Args:
            description: Description of the script
            data: Data to record
            script_type: Type of script (record, catalog, archive, etc.)

        Returns:
            Path to written script file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Create safe filename from description
        safe_desc = "".join(c if c.isalnum() or c in (" ", "-", "_") else "" for c in description)
        safe_desc = safe_desc.replace(" ", "_")[:50]  # Limit length

        filename = f"{timestamp}_{safe_desc}.json"
        script_path = self.scripts_dir / filename

        script_data = {
            "script_type": script_type,
            "description": description,
            "timestamp": timestamp,
            "iso_timestamp": datetime.now().isoformat(),
            "data": data,
        }

        script_path.write_text(json.dumps(script_data, indent=2), encoding="utf-8")

        return script_path

    def write_catalog_script(self, action: str, count: int, source: str) -> Path:
        """Write a cataloging script."""
        return self.write_script(
            f"Cataloged {count} records from {source}",
            {"action": action, "count": count, "source": source},
            script_type="catalog",
        )

    def write_record_script(
        self, record_type: str, record_id: str, metadata: dict[str, Any]
    ) -> Path:
        """Write a record script."""
        return self.write_script(
            f"Recorded {record_type}: {record_id}",
            {"record_type": record_type, "record_id": record_id, "metadata": metadata},
            script_type="record",
        )
