# WAFT Being Test - Empirica Integration

React app to test the Being system with Empirica integration.

## Features

- ✨ Spawn the first Being (automatically uses Empirica)
- 🎲 Make decisions (auto or manual)
- 🧠 View Empirica gate results
- 📊 Monitor Being state (stamina, fatigue, etc.)
- 📝 Activity log

## Setup

1. **Install dependencies:**
```bash
cd react-being-test
npm install
```

2. **Start the API server** (in the project root):
```bash
# From the waft project root
uvicorn src.waft.api.main:app --reload --port 8000
```

3. **Start the React app** (in react-being-test directory):
```bash
npm run dev
```

4. **Open your browser:**
```
http://localhost:3000
```

## Testing Empirica Integration

1. Click "✨ Spawn First Being" - This creates a Being with Empirica enabled
2. Click "🎲 Make Auto Decision" - The Being will make a decision using Empirica thinking
3. Watch the activity log for Empirica gate results (PROCEED/HALT/BRANCH/REVISE)
4. Try "⚡ Make 5 Decisions" to see multiple decisions in sequence
5. Check the "Recent Decisions" section to see Empirica gate results

## What to Look For

- ✅ **Empirica Badge**: Should appear next to the Being ID when Empirica is enabled
- 🧠 **Empirica Gate**: Each decision should show a gate result (PROCEED/HALT/BRANCH/REVISE)
- 📊 **Preflight/Postflight**: Empirica assessments happen automatically (check backend logs)
- 🔍 **Findings/Unknowns**: Logged automatically based on decision quality

## API Endpoints

- `POST /api/being/spawn` - Spawn a new Being
- `POST /api/being/{being_id}/decision` - Make a decision
- `GET /api/being/{being_id}` - Get Being state
- `GET /api/being/{being_id}/decisions/make-multiple?count=5` - Make multiple decisions

## Troubleshooting

- **CORS errors**: Make sure the API server is running on port 8000
- **Empirica not enabled**: Check that Empirica is initialized in the project (`.empirica-project` exists)
- **Being not found**: Make sure you spawn a Being first
