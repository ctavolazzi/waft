---
name: Intellectual Obstacle Course Benchmark Suite
overview: Create a comprehensive benchmark suite with progressively complex tasks ranging from trivial file operations to complex multi-system orchestration, stored in a new benchmarks/ directory with both markdown documentation and an executable Python runner.
todos:
  - id: create-structure
    content: Create benchmarks/ directory structure with subdirectories for tasks, results, and configuration
    status: pending
  - id: create-readme
    content: Create README.md with overview, quick start guide, and usage instructions
    status: pending
  - id: create-obstacle-course
    content: Create obstacle_course.md with all tasks organized by difficulty level (0-5)
    status: pending
  - id: create-runner
    content: Create runner.py executable script for running and validating benchmarks
    status: pending
  - id: create-config
    content: Create config.yaml with benchmark execution settings and requirements
    status: pending
  - id: create-task-definitions
    content: Create individual task definition files in tasks/ subdirectories with metadata
    status: pending
  - id: add-examples
    content: Add example task definitions showing the format and structure
    status: pending
  - id: security-hardening
    content: Add input validation, sandboxing, and security measures to runner
    status: pending
  - id: error-handling
    content: Implement comprehensive error handling and cleanup mechanisms
    status: pending
  - id: testing-strategy
    content: Add tests for runner and validation logic
    status: pending
  - id: result-analysis
    content: Create tools for analyzing benchmark trends and comparing runs
    status: pending
---

# Intellectual Obstacle Course Benchmark Suite

## Overview

Create a comprehensive benchmark suite to test system capabilities as it evolves. Tasks progress from trivial operations to complex multi-system orchestration.

## Structure

### Directory Layout

```
benchmarks/
├── README.md                    # Overview and usage guide
├── obstacle_course.md          # Complete task catalog (markdown)
├── runner.py                   # Executable benchmark runner
├── config.yaml                 # Benchmark configuration
├── results/                    # Benchmark execution results
│   ├── latest.json            # Latest run results
│   └── history/               # Historical results
└── tasks/                      # Individual task definitions
    ├── level_0_trivial/       # Trivial tasks
    ├── level_1_basic/         # Basic tasks
    ├── level_2_intermediate/   # Intermediate tasks
    ├── level_3_advanced/      # Advanced tasks
    ├── level_4_expert/        # Expert tasks
    └── level_5_master/         # Master tasks
```

## Task Organization

### Level 0: Trivial (File/Folder Operations)

**Purpose**: Test basic file system operations and simple commands

1. **Create a file** - Create a text file with specific content
2. **Create a folder** - Create a directory structure
3. **Read a file** - Read and display file contents
4. **List directory** - List files in a directory
5. **Delete a file** - Safely delete a file
6. **Copy a file** - Copy file to new location
7. **Move a file** - Move file to new location
8. **Write to file** - Append text to existing file
9. **Create nested folders** - Create multi-level directory structure
10. **Find files** - Search for files matching pattern

### Level 1: Basic (Simple Scripts & Operations)

**Purpose**: Test basic scripting, environment setup, and simple logic

1. **Hello World script** - Create and run a simple script
2. **Environment variable** - Read and use environment variable
3. **Command execution** - Execute shell command and capture output
4. **Simple calculator** - Create script that performs basic math
5. **File counter** - Count files in directory
6. **Text processor** - Read file, process text, write output
7. **Simple config parser** - Parse JSON/YAML config file
8. **Log file generator** - Create timestamped log entries
9. **Basic error handling** - Script with try/except blocks
10. **Simple CLI tool** - CLI with argument parsing

### Level 2: Intermediate (Single-Component Apps)

**Purpose**: Test single-framework applications and basic integrations

1. **Static HTML page** - Create HTML page with CSS
2. **Simple Python web server** - HTTP server serving static files
3. **REST API endpoint** - Single endpoint returning JSON
4. **Database connection** - Connect to SQLite and query
5. **File upload handler** - Accept file upload via HTTP
6. **Basic authentication** - Simple login system
7. **Template rendering** - Render HTML from template
8. **JSON API client** - Fetch data from public API
9. **Scheduled task** - Script that runs on schedule
10. **Configuration management** - Multi-environment config system

### Level 3: Advanced (Full-Stack Applications)

**Purpose**: Test full-stack development and framework integration

1. **MERN stack app** - MongoDB, Express, React, Node.js app displaying data
2. **Open in browser** - Launch app and open in default browser
3. **CRUD operations** - Full Create, Read, Update, Delete interface
4. **User authentication** - JWT-based auth system
5. **Database migrations** - Schema versioning and migrations
6. **API documentation** - Auto-generated API docs (Swagger/OpenAPI)
7. **Error logging** - Centralized error logging system
8. **File storage** - Upload and serve files
9. **Real-time updates** - WebSocket or SSE implementation
10. **Testing suite** - Unit and integration tests

### Level 4: Expert (Complex Integrations)

**Purpose**: Test complex system integrations and platform conversions

1. **Electron desktop app** - Convert web app to Electron
2. **Docker containerization** - Containerize application
3. **Docker Compose setup** - Multi-container orchestration
4. **API rate limiting** - Implement rate limiting middleware
5. **Public API integration** - Integrate with external API
6. **API rule compliance** - Respect API terms and rate limits
7. **Data collection system** - Collect and store API data
8. **Background workers** - Queue-based job processing
9. **Caching layer** - Redis or in-memory caching
10. **Monitoring dashboard** - Metrics and health monitoring

### Level 5: Master (Multi-System Orchestration)

**Purpose**: Test complex multi-system coordination and advanced patterns

1. **Docker orchestration** - Launch Docker from Electron dashboard
2. **Multi-service architecture** - Microservices with service discovery
3. **Event-driven system** - Event bus with pub/sub
4. **Distributed data collection** - Multiple API sources with coordination
5. **Rate limit coordination** - Manage rate limits across multiple APIs
6. **Data pipeline** - ETL pipeline with transformation
7. **CI/CD pipeline** - Automated testing and deployment
8. **Infrastructure as code** - Terraform or similar IaC
9. **Multi-region deployment** - Deploy across regions
10. **System monitoring** - Full observability stack

## Task Metadata Structure

Each task includes:

- **ID**: Unique identifier (e.g., `L0-T001`)
- **Title**: Task name
- **Description**: Detailed task description
- **Difficulty**: 0-5 (Trivial to Master)
- **Estimated Time**: Minutes to complete
- **Dependencies**: Required tools/libraries
- **Success Criteria**: How to verify completion
- **Example Output**: Expected result
- **Tags**: Categories (file-ops, web, api, docker, etc.)

## Implementation Details

### obstacle_course.md

- Markdown file with all tasks organized by level
- Each task has full description, requirements, and examples
- Includes difficulty progression visualization
- Links to related tasks and dependencies

### runner.py

Python script that can:

- List all available benchmarks
- Run specific benchmark or level
- Validate task completion
- Generate execution reports
- Track benchmark history
- Compare results across runs
- Export results to JSON/CSV

**Security Features:**

- Input validation and sanitization for all task definitions
- Sandboxed execution environment (isolated directories, resource limits)
- Timeout limits per task and per level
- Resource limits (memory, CPU, disk)
- Automatic cleanup of temporary files and processes
- Result signing/verification to prevent tampering

**Error Handling:**

- Comprehensive try/except blocks for all operations
- Graceful degradation when dependencies missing
- Clear error messages with actionable guidance
- Rollback mechanisms for failed tasks
- Logging of all errors for debugging

### config.yaml

Configuration for:

- Benchmark execution settings
- Timeout values per level (defaults: L0=30s, L1=60s, L2=120s, L3=300s, L4=600s, L5=1800s)
- Resource limits (memory, CPU, disk)
- Required tools check
- Output directory settings
- Result retention policy
- Sandbox settings (isolated directories, cleanup policies)
- Security settings (input validation, result signing)

## Success Criteria

Each task defines:

1. **Functional Requirements**: What must work
2. **Quality Requirements**: Code quality standards
3. **Performance Requirements**: Speed/efficiency targets
4. **Verification Steps**: How to validate completion

## Example Task Definition

```yaml
id: L3-T001
title: "MERN Stack App - Display Data"
difficulty: 3
estimated_time: 60
dependencies:
  - node
  - npm
  - mongodb
description: |
  Create a full-stack MERN application that:
  - Connects to MongoDB database
  - Serves REST API with Express
  - Displays data in React frontend
  - Opens automatically in browser
success_criteria:
  - App runs without errors
  - Data displays correctly in browser
  - API endpoints respond correctly
  - Database connection works
tags:
  - web
  - full-stack
  - mern
  - database
```

## Security & Safety

### Input Validation

- All task definitions validated against schema before execution
- File paths sanitized to prevent path traversal attacks
- Command arguments validated and sanitized
- No shell=True in subprocess calls (use list arguments)

### Sandboxing

- Tasks execute in isolated temporary directories
- Resource limits enforced (memory, CPU, disk space)
- Network access controlled (can be restricted per task)
- File system access scoped to task directory

### Timeouts & Resource Limits

- Per-task timeouts based on difficulty level
- Memory limits (default: 512MB per task, configurable)
- CPU limits (default: 1 core per task, configurable)
- Disk space limits (default: 100MB per task, configurable)

### Cleanup

- Automatic cleanup of temporary files after task completion
- Process cleanup (zombie process prevention)
- Resource monitoring and cleanup on timeout/failure
- Configurable cleanup policies

## Error Handling Strategy

### Error Categories

1. **Dependency Errors**: Missing tools/libraries - clear error with installation instructions
2. **Execution Errors**: Task execution failures - detailed error logs with context
3. **Validation Errors**: Task definition issues - schema validation errors with fixes
4. **Resource Errors**: Timeout/memory/disk - resource limit exceeded with suggestions
5. **Network Errors**: API/network failures - connectivity issues with retry logic

### Error Recovery

- Automatic retry for transient failures (network, timeouts)
- Graceful degradation when optional dependencies missing
- Partial result capture on failure
- Rollback mechanisms for state-changing tasks

## Testing Strategy

### Runner Tests

- Unit tests for validation logic
- Integration tests for task execution
- Security tests for input validation and sandboxing
- Performance tests for resource limits
- Error handling tests for all error categories

### Task Validation Tests

- Schema validation for task definitions
- Dependency checking tests
- Success criteria validation tests
- Example output verification tests

## Result Analysis & Tracking

### Analysis Tools

- `analyze.py`: Analyze benchmark trends over time
- `compare.py`: Compare results across runs
- `baseline.py`: Establish and compare against baseline performance
- `visualize.py`: Generate charts/graphs for progress tracking

### Metrics Tracked

- Success rate per level
- Average completion time per task
- Resource usage (memory, CPU, disk)
- Error rates and types
- Progress over time (improvement trends)

### Baseline Establishment

- Initial baseline capture on first run
- Baseline comparison for each subsequent run
- Progress metrics (improvement/degradation)
- Historical trend analysis

## Task Versioning

- Tasks include version numbers
- Version tracking in task definitions
- Change log for task modifications
- Backward compatibility considerations
- Migration path for task updates

## Implementation Priorities

### Phase 1: Core Structure (Critical)

1. Create directory structure
2. Create README.md with overview
3. Create obstacle_course.md with task catalog
4. Create basic config.yaml

### Phase 2: Security & Safety (Critical)

1. Implement input validation in runner
2. Add sandboxing (isolated directories)
3. Add timeout and resource limits
4. Implement cleanup mechanisms
5. Add error handling framework

### Phase 3: Runner Implementation (High)

1. Implement task execution engine
2. Add validation logic
3. Add result storage
4. Add basic reporting

### Phase 4: Testing & Validation (High)

1. Add tests for runner
2. Add tests for validation logic
3. Add security tests
4. Test error handling

### Phase 5: Analysis Tools (Medium)

1. Create analyze.py for trends
2. Create compare.py for run comparison
3. Create baseline.py for baseline management
4. Create visualize.py for charts

### Phase 6: Documentation (Medium)

1. Create SECURITY.md
2. Create TASK_AUTHORING.md
3. Add examples and tutorials
4. Complete task documentation

## Integration Points

- Can integrate with existing test infrastructure (pytest, test_suite.py patterns)
- Results can feed into WAFT evolution system (fitness scores)
- Can track performance over time (historical analysis)
- Supports both manual and automated execution
- Integrates with Empirica for epistemic tracking

## Documentation

- README.md: Quick start and overview
- obstacle_course.md: Complete task catalog
- SECURITY.md: Security guidelines and best practices
- TASK_AUTHORING.md: Guide for creating new tasks
- Each task folder: Detailed task documentation
- Results analysis: Tools to analyze benchmark trends