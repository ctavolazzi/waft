# Being Empirica Integration Testing Guide

## Quick Start

### Option 1: React App (Recommended)

1. **Install React dependencies:**
```bash
cd react-being-test
npm install
```

2. **Start API server** (from project root):
```bash
uvicorn src.waft.api.main:app --reload --port 8000
```

3. **Start React app** (in another terminal):
```bash
cd react-being-test
npm run dev
```

4. **Open browser:**
```
http://localhost:3000
```

### Option 2: Python Test Script

```bash
python examples/test_being_empirica.py
```

### Option 3: Use the startup script

```bash
./scripts/start_being_test.sh
```

## What to Test

### 1. Empirica Initialization
- ✅ Spawn first Being - should show "Empirica enabled"
- ✅ Check for Empirica session ID in Being state
- ✅ Verify `.empirica-project` directory exists

### 2. Decision Making with Empirica
- ✅ Make single decision - check for Empirica gate result
- ✅ Make multiple decisions - verify gates are consistent
- ✅ Check activity log for Empirica-related messages

### 3. Empirica Gate Results
Look for these gate results in decision responses:
- **PROCEED**: Decision approved, proceeding normally
- **HALT**: Decision halted, Being will rest instead
- **BRANCH**: Decision requires investigation
- **REVISE**: Decision needs revision

### 4. Preflight/Postflight Assessments
- Check backend logs for Empirica preflight/postflight submissions
- Verify epistemic vectors are calculated correctly
- Check that assessments happen before/after each decision

### 5. Finding/Unknown Logging
- Excellent decisions should log findings
- Stamina depletion should log unknowns
- Check Empirica logs for these entries

## Expected Behavior

### First Being (with Empirica)
- ✅ Empirica session created automatically
- ✅ Preflight assessment before each decision
- ✅ Check gate evaluates decision safety
- ✅ Postflight assessment after each decision
- ✅ Findings/unknowns logged automatically

### Subsequent Beings (without Empirica)
- ✅ No Empirica session
- ✅ Decisions work normally without Empirica
- ✅ No gate results in decision responses

## Troubleshooting

### Empirica Not Enabled
- Check that `.empirica-project` exists in project root
- Verify Empirica CLI is installed: `empirica --version`
- Check Python version (Empirica requires 3.11+)

### API Errors
- Verify API server is running on port 8000
- Check CORS settings in `src/waft/api/main.py`
- Verify Being routes are registered

### React App Issues
- Clear `node_modules` and reinstall: `rm -rf node_modules && npm install`
- Check that Vite proxy is configured correctly
- Verify API base URL in `App.jsx`

## API Endpoints

### Spawn Being
```bash
POST /api/being/spawn
{
  "reality_id": "test_reality",
  "initial_skills": {"reasoning": 30.0}
}
```

### Make Decision
```bash
POST /api/being/{being_id}/decision
{
  "decision_type": "learn_skill",
  "stamina_cost": 5.0
}
```

### Get Being State
```bash
GET /api/being/{being_id}
```

### Make Multiple Decisions
```bash
GET /api/being/{being_id}/decisions/make-multiple?count=5
```

## Success Criteria

✅ First Being spawns with Empirica enabled
✅ Decisions show Empirica gate results
✅ Preflight/postflight assessments work
✅ Findings/unknowns are logged
✅ Being state updates correctly
✅ React app displays all information
✅ No errors in console or logs
