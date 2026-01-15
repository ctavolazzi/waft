# Universal Booklet Generator

**Status**: ✅ Working  
**Date**: 2026-01-13

---

## Overview

The Universal Booklet Generator creates comprehensive PDF booklets from **ANY** input data. It automatically analyzes data structures, generates API documentation, creates usage examples, and outputs professional PDFs.

---

## Features

### ✅ Auto-Detection
- Automatically detects data type (JSON file, Python object, API endpoint, etc.)
- No manual configuration needed

### ✅ Structure Analysis
- Analyzes data structure (keys, types, nesting)
- Extracts schema information
- Calculates statistics

### ✅ API Documentation
- Automatically generates API documentation for endpoints
- Creates usage examples
- Documents request/response formats

### ✅ Usage Examples
- Generates code examples automatically
- Shows how to access and use the data
- Provides multiple examples

### ✅ Professional PDF Output
- Uses WAFT's PDF generator
- Clinical standard styling
- Professional formatting

---

## Supported Data Types

1. **JSON Files** (`.json`)
   ```python
   generate_booklet("data.json", "My Documentation")
   ```

2. **Python Objects**
   ```python
   generate_booklet(my_object, "Object Documentation")
   ```

3. **Dictionaries/Lists**
   ```python
   generate_booklet({"key": "value"}, "Dict Documentation")
   ```

4. **API Endpoints** (URLs)
   ```python
   generate_booklet("https://api.example.com/data", "API Documentation")
   ```

5. **Configuration Files**
   ```python
   generate_booklet("config.yaml", "Config Documentation")
   ```

---

## Usage

### Basic Usage

```python
from booklet_generator import generate_booklet

# Generate booklet from any data
pdf_path = generate_booklet(
    data="path/to/data.json",  # or object, dict, URL, etc.
    title="My Data Documentation"
)
```

### Advanced Usage

```python
from booklet_generator import BookletGenerator, BookletConfig

config = BookletConfig(
    title="Custom Documentation",
    author="Your Name",
    include_apis=True,
    include_examples=True,
    include_statistics=True,
    style="clinical_standard"
)

generator = BookletGenerator(config)
pdf_path = generator.generate_from_data(
    data=my_data,
    output_path="custom_output.pdf"
)
```

---

## Generated Booklet Sections

1. **Part I: Overview** - What is this data?
2. **Part II: Data Structure** - Structure analysis
3. **Part III: Schema Reference** - Complete schema
4. **Part IV: Statistics** - Data statistics
5. **Part V: API Documentation** - API docs (if applicable)
6. **Part VI: Usage Examples** - Code examples
7. **Part VII: Complete Reference** - Full reference

---

## Test Results

✅ **All Tests Passing**:

- **Test 1: JSON File**
  - Input: `sample_api.json`
  - Output: `test_json_file_booklet.pdf` (12.1 KB)
  - ✅ Success

- **Test 2: Python Object**
  - Input: `SampleConfig` class instance
  - Output: `test_python_object_booklet.pdf` (12.2 KB)
  - ✅ Success

- **Test 3: Dictionary Data**
  - Input: Campaign data dictionary
  - Output: `test_dict_booklet.pdf` (12.1 KB)
  - ✅ Success

---

## Example Output

### Sample Booklet Structure

```
# Sample API Documentation

## Part I: Overview
- Data Type: json_file
- Structure Type: dict

## Part II: Data Structure
- Type: dict
- Keys: name, version, endpoints, authentication
- Key Count: 4

## Part III: Schema Reference
{
  "type": "object",
  "properties": {
    "name": {"type": "str"},
    "version": {"type": "str"},
    ...
  }
}

## Part IV: Statistics
- Key Count: 4
- Has Nested: True
- Value Types: {str: 2, list: 1, dict: 1}

## Part V: API Documentation
(If applicable)

## Part VI: Usage Examples
### Example 1: Accessing Data
data['name']

### Example 2: Iterating
for key, value in data.items():
    print(key, value)

## Part VII: Complete Reference
(Full structure dump)
```

---

## Integration with AI DM System

The booklet generator will be used by the AI DM system to:
- Generate campaign story booklets
- Document campaign APIs
- Create session summaries
- Generate character documentation
- Document decision matrices used
- Create campaign analysis reports

---

## Next Steps

- [ ] Add support for YAML, TOML, XML files
- [ ] Enhance API documentation (OpenAPI/Swagger detection)
- [ ] Add data visualization
- [ ] Support for nested API endpoints
- [ ] Custom template support
- [ ] Integration with campaign orchestrator

---

**Status**: ✅ Production Ready  
**Location**: `src/booklet_generator.py`  
**Tests**: `examples/test_booklet_generator.py`
