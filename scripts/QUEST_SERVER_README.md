# 🎮 Quest Guide Server

A FastAPI web server for the Quest Guide Implementation system.

## Overview

The Quest Guide Server provides a REST API for managing quests, checkpoints, and tests. It can run standalone or be integrated into the main WAFT API.

## Quick Start

### Standalone Server

Run the standalone quest server:

```bash
# Default port 8001
python3 scripts/quest_server.py

# Custom port
python3 scripts/quest_server.py --port 8080

# Development mode with auto-reload
python3 scripts/quest_server.py --reload
```

### Integrated with WAFT API

The quest routes are automatically included in the main WAFT API when you start the server:

```bash
# Start main WAFT API (includes quest routes)
waft serve

# Or directly with uvicorn
uvicorn src.waft.api.main:app --reload
```

## API Endpoints

### Quest Status

```bash
GET /api/quests/status
```

Returns overall quest system status:
- Total quests
- Completed/in progress/available/locked counts
- Total XP earned
- Completion percentage

### List Quests

```bash
GET /api/quests
GET /api/quests?status_filter=available
```

List all quests, optionally filtered by status.

### Get Quest Details

```bash
GET /api/quests/{quest_id}
```

Get detailed information about a specific quest.

### Start Quest

```bash
POST /api/quests/{quest_id}/start
```

Start a quest (marks it as in_progress).

### Complete Quest

```bash
POST /api/quests/{quest_id}/complete
```

Complete a quest (validates checkpoints and tests).

### Check Checkpoint

```bash
POST /api/quests/checkpoints/{checkpoint_id}/check
GET /api/quests/checkpoints/{checkpoint_id}
```

Check or get information about a checkpoint.

### Run Test

```bash
POST /api/quests/tests/{test_id}/run
GET /api/quests/tests/{test_id}
```

Run or get information about a test.

### Get Quest Checkpoints

```bash
GET /api/quests/{quest_id}/checkpoints
```

Get all checkpoints for a quest with their status.

### Get Quest Tests

```bash
GET /api/quests/{quest_id}/tests
```

Get all tests for a quest with their status.

## Example Usage

### Using curl

```bash
# Get quest status
curl http://localhost:8001/api/quests/status

# List all quests
curl http://localhost:8001/api/quests

# Get quest details
curl http://localhost:8001/api/quests/quest_1

# Start a quest
curl -X POST http://localhost:8001/api/quests/quest_1/start

# Check a checkpoint
curl -X POST http://localhost:8001/api/quests/checkpoints/cp_guide_file/check

# Run a test
curl -X POST http://localhost:8001/api/quests/tests/test_init/run

# Complete a quest
curl -X POST http://localhost:8001/api/quests/quest_1/complete
```

### Using Python requests

```python
import requests

base_url = "http://localhost:8001/api/quests"

# Get status
status = requests.get(f"{base_url}/status").json()
print(f"Completed: {status['completed']}/{status['total_quests']}")

# List quests
quests = requests.get(f"{base_url}").json()
for quest in quests['quests']:
    print(f"{quest['quest_id']}: {quest['name']} ({quest['status']})")

# Start quest
response = requests.post(f"{base_url}/quest_1/start")
print(response.json())

# Check checkpoint
checkpoint = requests.post(f"{base_url}/checkpoints/cp_guide_file/check").json()
print(f"Checkpoint: {checkpoint['passed']} - {checkpoint['message']}")

# Complete quest
complete = requests.post(f"{base_url}/quest_1/complete").json()
print(f"XP Earned: {complete['xp_earned']}")
print(f"Achievements: {complete['achievements_unlocked']}")
```

## API Documentation

When the server is running, visit:

- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc
- **OpenAPI JSON**: http://localhost:8001/openapi.json

## Response Models

### QuestStatusResponse

```json
{
  "status": "active",
  "total_quests": 17,
  "completed": 0,
  "in_progress": 0,
  "available": 1,
  "locked": 16,
  "total_xp": 0,
  "completion_percentage": 0.0
}
```

### QuestResponse

```json
{
  "quest_id": "quest_1",
  "name": "🏗️ Foundation: Create TheGuide Skeleton",
  "description": "Create the basic structure...",
  "difficulty": 2,
  "xp_reward": 50,
  "status": "available",
  "prerequisites": [],
  "checkpoints": ["cp_guide_file", "cp_guide_class"],
  "tests": ["test_init"],
  "achievements": ["🏗️ Foundation Builder"],
  "started_at": null,
  "completed_at": null,
  "progress": {
    "checkpoints_passed": [],
    "tests_passed": [],
    "current_step": "",
    "notes": []
  }
}
```

### QuestCompleteResponse

```json
{
  "success": true,
  "message": "🎉 Quest completed: ... (+50 XP)!",
  "xp_earned": 50,
  "achievements_unlocked": ["🏗️ Foundation Builder"]
}
```

## Integration with Claude Code Cloud

The API is perfect for LLM-guided development:

1. **Check status**: `GET /api/quests/status` to see what's available
2. **Get quest details**: `GET /api/quests/{quest_id}` to understand requirements
3. **Start quest**: `POST /api/quests/{quest_id}/start` to begin work
4. **Check checkpoints**: `POST /api/quests/checkpoints/{checkpoint_id}/check` to validate progress
5. **Run tests**: `POST /api/quests/tests/{test_id}/run` to verify correctness
6. **Complete quest**: `POST /api/quests/{quest_id}/complete` when done

The API provides clear feedback on what needs to be done and validates progress automatically.

## Development

### Running in Development Mode

```bash
# Auto-reload on code changes
python3 scripts/quest_server.py --reload
```

### Testing the API

```bash
# Start server
python3 scripts/quest_server.py --port 8001 &

# Test endpoints
curl http://localhost:8001/api/quests/status
curl http://localhost:8001/api/quests

# Stop server
pkill -f quest_server.py
```

## Troubleshooting

**Import errors?**
- Make sure you're running from the project root
- Check that `scripts/quest_guide_implementation.py` exists

**Port already in use?**
- Use a different port: `--port 8002`
- Or stop the existing server

**CORS issues?**
- The standalone server allows all origins
- If integrated with WAFT API, check CORS settings in `src/waft/api/main.py`

## Next Steps

1. Start the server: `python3 scripts/quest_server.py`
2. Visit http://localhost:8001/docs for interactive API docs
3. Use the API to guide LLM development
4. Track progress through the quest system

Happy questing! 🎮✨
