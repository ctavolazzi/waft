---
name: OpenAPI Directory Integration Service
overview: Build a comprehensive API service that integrates the APIs-guru/openapi-directory into WAFT, providing search, fetch, validate, transform, generate, and catalog capabilities for OpenAPI specifications to help integrate APIs into WAFT and other projects.
todos:
  - id: "1"
    content: Create core service module (openapi_directory.py) with directory access and indexing
    status: pending
  - id: "2"
    content: Create GitHub API client (openapi_client.py) for fetching specs
    status: pending
  - id: "3"
    content: Create Pydantic models (openapi.py) for requests/responses
    status: pending
  - id: "4"
    content: Create FastAPI router (openapi_directory.py) with all endpoints
    status: pending
  - id: "5"
    content: Implement search functionality with filtering and pagination
    status: pending
  - id: "6"
    content: Implement fetch functionality for OpenAPI specs
    status: pending
  - id: "7"
    content: Implement validation using openapi-spec-validator
    status: pending
  - id: "8"
    content: Implement transformation between OpenAPI versions
    status: pending
  - id: "9"
    content: Implement code generation for multiple languages
    status: pending
  - id: "10"
    content: Implement catalog browsing with metadata
    status: pending
  - id: "11"
    content: Register router in main.py and add dependencies to pyproject.toml
    status: pending
  - id: "12"
    content: Add error handling and rate limiting for GitHub API
    status: pending
---

# OpenAPI Directory Integration Service

## Overview
Create a new FastAPI service route (`/api/openapi-directory`) that provides comprehensive OpenAPI specification management capabilities using the APIs-guru/openapi-directory repository. This service will enable WAFT users to discover, fetch, validate, transform, and generate code from OpenAPI specs.

## Architecture

### Service Components
1. **OpenAPIDirectoryService** - Core service class managing OpenAPI directory operations
2. **OpenAPIRoute** - FastAPI router with endpoints for all operations
3. **OpenAPIModels** - Pydantic models for requests/responses
4. **OpenAPIClient** - HTTP client for fetching specs from openapi-directory
5. **OpenAPIValidator** - Validates OpenAPI 2.0/3.x specs
6. **OpenAPITransformer** - Converts between OpenAPI versions
7. **OpenAPIGenerator** - Generates code/clients from specs

### Data Flow
```
User Request → FastAPI Route → OpenAPIDirectoryService →
  ├─ OpenAPIClient (fetch from GitHub/API)
  ├─ OpenAPIValidator (validate specs)
  ├─ OpenAPITransformer (convert versions)
  └─ OpenAPIGenerator (generate code)
→ Response (JSON/File)
```

## Implementation Plan

### Phase 1: Core Infrastructure

#### 1.1 Create Service Module
- **File**: `src/waft/api/services/openapi_directory.py`
- **Purpose**: Core service class with business logic
- **Features**:
  - Clone/sync openapi-directory repository (or use GitHub API)
  - Index APIs by name, category, tags
  - Cache frequently accessed specs
  - Handle rate limiting for GitHub API

#### 1.2 Create Route Module
- **File**: `src/waft/api/routes/openapi_directory.py`
- **Purpose**: FastAPI router with all endpoints
- **Endpoints**:
  - `GET /api/openapi-directory/catalog` - List all APIs
  - `GET /api/openapi-directory/search` - Search APIs
  - `GET /api/openapi-directory/{api_name}` - Fetch specific API spec
  - `POST /api/openapi-directory/validate` - Validate OpenAPI spec
  - `POST /api/openapi-directory/transform` - Transform spec version
  - `POST /api/openapi-directory/generate` - Generate client code

#### 1.3 Create Models
- **File**: `src/waft/api/models/openapi.py`
- **Purpose**: Pydantic models for requests/responses
- **Models**:
  - `APICatalogResponse` - List of APIs with metadata
  - `APISearchRequest` - Search parameters
  - `APISearchResponse` - Search results
  - `APISpecResponse` - OpenAPI spec content
  - `ValidationRequest` - Spec to validate
  - `ValidationResponse` - Validation results
  - `TransformRequest` - Transformation parameters
  - `TransformResponse` - Transformed spec
  - `GenerateRequest` - Code generation parameters
  - `GenerateResponse` - Generated code/files

### Phase 2: Directory Access

#### 2.1 GitHub API Integration
- **File**: `src/waft/api/services/openapi_client.py`
- **Purpose**: Fetch OpenAPI specs from openapi-directory via GitHub API
- **Features**:
  - Use GitHub API to fetch files (avoid cloning entire repo)
  - Cache responses locally
  - Handle rate limiting
  - Support both OpenAPI 2.0 (swagger.yaml) and 3.x (openapi.yaml)

#### 2.2 Directory Indexing
- **Purpose**: Build searchable index of all APIs
- **Storage**: In-memory cache or local JSON file
- **Index Fields**:
  - API name
  - Provider/owner
  - Categories/tags
  - OpenAPI version
  - Endpoint count
  - Last updated date

### Phase 3: Core Features

#### 3.1 Search Functionality
- **Endpoint**: `GET /api/openapi-directory/search?q={query}&category={cat}&tags={tags}`
- **Features**:
  - Full-text search on API names/descriptions
  - Filter by category
  - Filter by tags
  - Pagination support
  - Sort by relevance/name/updated

#### 3.2 Fetch Functionality
- **Endpoint**: `GET /api/openapi-directory/{provider}/{api_name}?version={v}`
- **Features**:
  - Fetch OpenAPI spec by provider and name
  - Support version selection
  - Return raw YAML/JSON or parsed object
  - Include metadata (x-origin, x-providerName, etc.)

#### 3.3 Validation
- **Endpoint**: `POST /api/openapi-directory/validate`
- **Purpose**: Validate OpenAPI 2.0/3.x specifications
- **Library**: Use `openapi-spec-validator` or `swagger-spec-validator`
- **Features**:
  - Validate structure
  - Check required fields
  - Validate JSON Schema references
  - Return detailed error messages

#### 3.4 Transformation
- **Endpoint**: `POST /api/openapi-directory/transform`
- **Purpose**: Convert between OpenAPI versions
- **Library**: Use `openapi-core` or custom transformer
- **Features**:
  - OpenAPI 2.0 → 3.0.x
  - OpenAPI 3.0.x → 3.1.x
  - Preserve as much information as possible
  - Report conversion warnings

#### 3.5 Code Generation
- **Endpoint**: `POST /api/openapi-directory/generate`
- **Purpose**: Generate API clients from specs
- **Options**:
  - Python (httpx/requests)
  - TypeScript/JavaScript
  - cURL commands
  - Postman collection
- **Library**: Consider `openapi-generator` or custom templates

### Phase 4: Catalog Feature

#### 4.1 Browsable Catalog
- **Endpoint**: `GET /api/openapi-directory/catalog`
- **Features**:
  - List all APIs with pagination
  - Group by provider/category
  - Include metadata (logo, description, etc.)
  - Filter and sort options

#### 4.2 API Details
- **Endpoint**: `GET /api/openapi-directory/{provider}/{api_name}/info`
- **Features**:
  - Full API metadata
  - Available versions
  - Categories and tags
  - Related APIs

### Phase 5: Integration with WAFT

#### 5.1 Register Route
- **File**: `src/waft/api/main.py`
- **Action**: Add `openapi_directory` router to FastAPI app
- **Prefix**: `/api/openapi-directory`

#### 5.2 CLI Command (Optional)
- **File**: `src/waft/cli/openapi.py`
- **Command**: `waft openapi search <query>`
- **Purpose**: CLI access to OpenAPI directory features

#### 5.3 Work Effort Integration
- **Purpose**: Track API integrations in work efforts
- **Action**: Link API specs to work efforts for documentation

## Dependencies

### Required Packages
- `httpx` or `requests` - HTTP client for GitHub API
- `pyyaml` - YAML parsing for OpenAPI specs
- `openapi-spec-validator` - OpenAPI validation
- `openapi-core` (optional) - OpenAPI processing
- `pydantic` - Already in use for FastAPI

### Optional Packages
- `openapi-generator-cli` - For code generation (or use API)
- `jsonschema` - For JSON Schema validation

## File Structure

```
src/waft/api/
├── routes/
│   └── openapi_directory.py      # FastAPI router
├── services/
│   ├── openapi_directory.py      # Core service logic
│   └── openapi_client.py         # GitHub API client
└── models/
    └── openapi.py                # Pydantic models
```

## API Endpoints Summary

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/openapi-directory/catalog` | List all APIs |
| GET | `/api/openapi-directory/search` | Search APIs |
| GET | `/api/openapi-directory/{provider}/{api}` | Fetch API spec |
| GET | `/api/openapi-directory/{provider}/{api}/info` | Get API metadata |
| POST | `/api/openapi-directory/validate` | Validate spec |
| POST | `/api/openapi-directory/transform` | Transform spec version |
| POST | `/api/openapi-directory/generate` | Generate client code |

## Error Handling

- Handle GitHub API rate limits (429 responses)
- Handle missing APIs (404)
- Handle invalid OpenAPI specs (validation errors)
- Handle transformation failures with detailed messages

## Caching Strategy

- Cache API catalog/index locally (update daily)
- Cache frequently accessed specs (TTL: 1 hour)
- Cache validation results for identical specs

## Testing Considerations

- Mock GitHub API responses
- Test with sample OpenAPI specs
- Test validation with invalid specs
- Test transformation edge cases

## Future Enhancements

- Webhook support for catalog updates
- Integration with WAFT's being system for API discovery
- Automatic client generation for discovered APIs
- API usage analytics/tracking