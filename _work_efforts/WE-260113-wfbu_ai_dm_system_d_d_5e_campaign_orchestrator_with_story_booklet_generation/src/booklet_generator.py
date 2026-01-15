"""
Universal Booklet Generator

Generates comprehensive booklets from ANY input data, including:
- Data structure analysis
- API documentation (if applicable)
- Usage examples
- Reference documentation
- Statistics and insights

Works with:
- JSON files
- Python objects
- API endpoints
- Database schemas
- Configuration files
- Any structured data
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
import json
import inspect
import ast
from dataclasses import dataclass, field, asdict
from enum import Enum
import requests
from urllib.parse import urlparse

# Import PDF generator - handle path issues
import sys
from pathlib import Path
_project_root = Path(__file__).parent.parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))
if str(_project_root / "src") not in sys.path:
    sys.path.insert(0, str(_project_root / "src"))

try:
    from waft.evolution.pdf_generator import PDFGenerator
except ImportError:
    # Fallback: direct import
    import importlib.util
    pdf_gen_path = _project_root / "src" / "waft" / "evolution" / "pdf_generator.py"
    if pdf_gen_path.exists():
        spec = importlib.util.spec_from_file_location("pdf_generator", pdf_gen_path)
        pdf_generator = importlib.util.module_from_spec(spec)
        sys.modules["pdf_generator"] = pdf_generator
        spec.loader.exec_module(pdf_generator)
        PDFGenerator = pdf_generator.PDFGenerator
    else:
        raise ImportError("Could not find PDFGenerator")


class DataType(Enum):
    """Types of data that can be processed."""
    JSON_FILE = "json_file"
    JSON_STRING = "json_string"
    PYTHON_OBJECT = "python_object"
    API_ENDPOINT = "api_endpoint"
    CONFIG_FILE = "config_file"
    UNKNOWN = "unknown"


@dataclass
class DataStructure:
    """Analyzed data structure."""
    data_type: DataType
    structure: Dict[str, Any]
    schema: Dict[str, Any] = field(default_factory=dict)
    statistics: Dict[str, Any] = field(default_factory=dict)
    api_info: Optional[Dict[str, Any]] = None
    examples: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class BookletConfig:
    """Configuration for booklet generation."""
    title: str
    author: str = "WAFT Booklet Generator"
    include_apis: bool = True
    include_examples: bool = True
    include_statistics: bool = True
    include_reference: bool = True
    style: str = "clinical_standard"


class BookletGenerator:
    """Universal booklet generator for any input data."""
    
    def __init__(self, config: BookletConfig):
        """Initialize booklet generator."""
        self.config = config
        self.data_structure: Optional[DataStructure] = None
    
    def generate_from_data(
        self,
        data: Any,
        output_path: Optional[Path] = None
    ) -> Path:
        """
        Generate booklet from any input data.
        
        Args:
            data: Any data structure (dict, list, file path, API URL, etc.)
            output_path: Optional output path for PDF
            
        Returns:
            Path to generated PDF
        """
        # Analyze data
        self.data_structure = self._analyze_data(data)
        
        # Generate markdown content
        markdown = self._generate_markdown()
        
        # Generate PDF
        if output_path is None:
            output_path = Path(f"booklet_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
        
        PDFGenerator.from_content(
            content=markdown,
            title=self.config.title,
            style=self.config.style,
            author=self.config.author,
            subject=f"Booklet: {self.config.title}"
        ).save(str(output_path), open_pdf=False)
        
        return output_path
    
    def _analyze_data(self, data: Any) -> DataStructure:
        """Analyze input data and extract structure."""
        # Detect data type
        data_type = self._detect_data_type(data)
        
        # Extract actual data
        raw_data = self._extract_data(data, data_type)
        
        # Analyze structure
        structure = self._analyze_structure(raw_data)
        
        # Extract schema
        schema = self._extract_schema(raw_data)
        
        # Calculate statistics
        statistics = self._calculate_statistics(raw_data)
        
        # Check for API info
        api_info = None
        if data_type == DataType.API_ENDPOINT:
            api_info = self._analyze_api(data)
        
        # Generate examples
        examples = self._generate_examples(raw_data)
        
        return DataStructure(
            data_type=data_type,
            structure=structure,
            schema=schema,
            statistics=statistics,
            api_info=api_info,
            examples=examples
        )
    
    def _detect_data_type(self, data: Any) -> DataType:
        """Detect the type of input data."""
        if isinstance(data, str):
            # Check if it's a file path
            if Path(data).exists():
                if data.endswith('.json'):
                    return DataType.JSON_FILE
                return DataType.CONFIG_FILE
            
            # Check if it's a URL
            try:
                parsed = urlparse(data)
                if parsed.scheme in ('http', 'https'):
                    return DataType.API_ENDPOINT
            except:
                pass
            
            # Try to parse as JSON
            try:
                json.loads(data)
                return DataType.JSON_STRING
            except:
                pass
        
        # Python object
        if isinstance(data, (dict, list, object)):
            return DataType.PYTHON_OBJECT
        
        return DataType.UNKNOWN
    
    def _extract_data(self, data: Any, data_type: DataType) -> Any:
        """Extract actual data based on type."""
        if data_type == DataType.JSON_FILE:
            with open(data, 'r') as f:
                return json.load(f)
        
        elif data_type == DataType.JSON_STRING:
            return json.loads(data)
        
        elif data_type == DataType.API_ENDPOINT:
            try:
                response = requests.get(data, timeout=10)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                return {"error": str(e), "url": data}
        
        elif data_type == DataType.PYTHON_OBJECT:
            # Convert to dict if possible
            if isinstance(data, dict):
                return data
            elif isinstance(data, list):
                return {"items": data}
            elif hasattr(data, '__dict__'):
                # Check if it's a dataclass
                try:
                    from dataclasses import is_dataclass
                    if is_dataclass(data):
                        return asdict(data)
                except:
                    pass
                # Fallback to __dict__
                return data.__dict__
            else:
                return {"value": str(data), "type": type(data).__name__}
        
        return data
    
    def _analyze_structure(self, data: Any) -> Dict[str, Any]:
        """Analyze the structure of data."""
        structure = {
            "type": type(data).__name__,
            "is_container": isinstance(data, (dict, list)),
            "size": len(data) if isinstance(data, (dict, list, str)) else 1
        }
        
        if isinstance(data, dict):
            structure["keys"] = list(data.keys())
            structure["key_count"] = len(data.keys())
            structure["nested"] = any(
                isinstance(v, (dict, list)) for v in data.values()
            )
        
        elif isinstance(data, list):
            structure["item_count"] = len(data)
            if data:
                structure["item_type"] = type(data[0]).__name__
                structure["uniform"] = all(
                    type(item) == type(data[0]) for item in data
                )
        
        return structure
    
    def _extract_schema(self, data: Any) -> Dict[str, Any]:
        """Extract schema information from data."""
        schema = {}
        
        if isinstance(data, dict):
            schema["type"] = "object"
            schema["properties"] = {}
            for key, value in data.items():
                schema["properties"][key] = {
                    "type": type(value).__name__,
                    "example": str(value)[:100] if not isinstance(value, (dict, list)) else "..."
                }
                if isinstance(value, dict):
                    schema["properties"][key]["nested"] = True
                    schema["properties"][key]["keys"] = list(value.keys())[:10]
        
        elif isinstance(data, list):
            schema["type"] = "array"
            if data:
                schema["items"] = {
                    "type": type(data[0]).__name__
                }
                if isinstance(data[0], dict):
                    schema["items"]["properties"] = list(data[0].keys())[:10]
        
        return schema
    
    def _calculate_statistics(self, data: Any) -> Dict[str, Any]:
        """Calculate statistics about the data."""
        stats = {}
        
        if isinstance(data, dict):
            stats["key_count"] = len(data)
            stats["has_nested"] = any(
                isinstance(v, (dict, list)) for v in data.values()
            )
            stats["value_types"] = {}
            for value in data.values():
                vtype = type(value).__name__
                stats["value_types"][vtype] = stats["value_types"].get(vtype, 0) + 1
        
        elif isinstance(data, list):
            stats["item_count"] = len(data)
            if data:
                stats["item_types"] = {}
                for item in data:
                    itype = type(item).__name__
                    stats["item_types"][itype] = stats["item_types"].get(itype, 0) + 1
        
        return stats
    
    def _analyze_api(self, url: str) -> Dict[str, Any]:
        """Analyze API endpoint."""
        api_info = {
            "url": url,
            "method": "GET",  # Default
            "endpoints": []
        }
        
        try:
            # Try to get API documentation
            response = requests.get(url, timeout=10)
            api_info["status_code"] = response.status_code
            api_info["content_type"] = response.headers.get("Content-Type", "unknown")
            
            # Try to detect API format
            if "application/json" in response.headers.get("Content-Type", ""):
                api_info["format"] = "JSON"
            elif "application/xml" in response.headers.get("Content-Type", ""):
                api_info["format"] = "XML"
            
        except Exception as e:
            api_info["error"] = str(e)
        
        return api_info
    
    def _generate_examples(self, data: Any) -> List[Dict[str, Any]]:
        """Generate usage examples from data."""
        examples = []
        
        if isinstance(data, dict):
            # Example: Accessing data
            examples.append({
                "title": "Accessing Data",
                "code": f"data['{list(data.keys())[0] if data.keys() else 'key'}']",
                "description": "Access a value by key"
            })
            
            # Example: Iterating
            if len(data) > 1:
                examples.append({
                    "title": "Iterating Over Data",
                    "code": "for key, value in data.items():\n    print(key, value)",
                    "description": "Iterate over all key-value pairs"
                })
        
        elif isinstance(data, list):
            examples.append({
                "title": "Accessing Items",
                "code": "data[0]",
                "description": "Access first item"
            })
            
            examples.append({
                "title": "Iterating",
                "code": "for item in data:\n    print(item)",
                "description": "Iterate over all items"
            })
        
        return examples
    
    def _generate_markdown(self) -> str:
        """Generate markdown content for booklet."""
        md = f"""# {self.config.title}

**Generated**: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}  
**Author**: {self.config.author}

---

## Part I: Overview

### What is This Data?

This booklet documents the structure, usage, and API information for the provided data.

**Data Type**: {self.data_structure.data_type.value}  
**Structure Type**: {self.data_structure.structure.get('type', 'unknown')}

"""
        
        # Structure section
        md += "## Part II: Data Structure\n\n"
        md += self._format_structure()
        
        # Schema section
        if self.config.include_reference:
            md += "\n## Part III: Schema Reference\n\n"
            md += self._format_schema()
        
        # Statistics section
        if self.config.include_statistics:
            md += "\n## Part IV: Statistics\n\n"
            md += self._format_statistics()
        
        # API documentation section
        if self.config.include_apis and self.data_structure.api_info:
            md += "\n## Part V: API Documentation\n\n"
            md += self._format_api_docs()
        
        # Examples section
        if self.config.include_examples:
            md += "\n## Part VI: Usage Examples\n\n"
            md += self._format_examples()
        
        # Reference section
        if self.config.include_reference:
            md += "\n## Part VII: Complete Reference\n\n"
            md += self._format_reference()
        
        return md
    
    def _format_structure(self) -> str:
        """Format structure information."""
        s = self.data_structure.structure
        md = f"""
**Type**: `{s.get('type', 'unknown')}`  
**Is Container**: {s.get('is_container', False)}  
**Size**: {s.get('size', 0)}

"""
        
        if 'keys' in s:
            md += f"**Keys** ({s.get('key_count', 0)} total):\n"
            for key in s['keys'][:20]:  # Limit to 20
                md += f"- `{key}`\n"
            if s.get('key_count', 0) > 20:
                md += f"- ... and {s.get('key_count', 0) - 20} more\n"
        
        if 'item_count' in s:
            md += f"**Items**: {s['item_count']}\n"
            if 'item_type' in s:
                md += f"**Item Type**: `{s['item_type']}`\n"
            if 'uniform' in s:
                md += f"**Uniform Types**: {s['uniform']}\n"
        
        return md
    
    def _format_schema(self) -> str:
        """Format schema information."""
        schema = self.data_structure.schema
        md = "```json\n"
        md += json.dumps(schema, indent=2)
        md += "\n```\n"
        return md
    
    def _format_statistics(self) -> str:
        """Format statistics."""
        stats = self.data_structure.statistics
        md = ""
        
        for key, value in stats.items():
            if isinstance(value, dict):
                md += f"**{key.replace('_', ' ').title()}**:\n"
                for k, v in value.items():
                    md += f"- `{k}`: {v}\n"
            else:
                md += f"**{key.replace('_', ' ').title()}**: {value}\n"
        
        return md
    
    def _format_api_docs(self) -> str:
        """Format API documentation."""
        api = self.data_structure.api_info
        if not api:
            return "No API information available.\n"
        
        md = f"""
### API Endpoint

**URL**: `{api.get('url', 'unknown')}`  
**Method**: {api.get('method', 'GET')}

"""
        
        if 'status_code' in api:
            md += f"**Status Code**: {api['status_code']}\n"
        if 'content_type' in api:
            md += f"**Content Type**: {api['content_type']}\n"
        if 'format' in api:
            md += f"**Format**: {api['format']}\n"
        
        md += "\n### Usage\n\n"
        md += f"```python\n"
        md += f"import requests\n\n"
        md += f"response = requests.get('{api.get('url', '')}')\n"
        md += f"data = response.json()\n"
        md += f"```\n"
        
        return md
    
    def _format_examples(self) -> str:
        """Format usage examples."""
        md = ""
        
        for i, example in enumerate(self.data_structure.examples, 1):
            md += f"### Example {i}: {example['title']}\n\n"
            md += f"{example['description']}\n\n"
            md += f"```python\n{example['code']}\n```\n\n"
        
        return md
    
    def _format_reference(self) -> str:
        """Format complete reference."""
        md = "### Data Structure\n\n"
        md += "```python\n"
        md += json.dumps(self.data_structure.structure, indent=2)
        md += "\n```\n"
        return md


# Convenience function
def generate_booklet(
    data: Any,
    title: str,
    output_path: Optional[Path] = None,
    author: str = "WAFT Booklet Generator",
    include_apis: bool = True,
    include_examples: bool = True
) -> Path:
    """
    Generate booklet from any data.
    
    Args:
        data: Any data structure (dict, list, file path, API URL, etc.)
        title: Booklet title
        output_path: Optional output path
        author: Booklet author
        include_apis: Include API documentation
        include_examples: Include usage examples
        
    Returns:
        Path to generated PDF
    """
    config = BookletConfig(
        title=title,
        author=author,
        include_apis=include_apis,
        include_examples=include_examples
    )
    
    generator = BookletGenerator(config)
    return generator.generate_from_data(data, output_path)
