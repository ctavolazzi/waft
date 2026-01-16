# 🧪 Cute Test Runner

A simple, cute HTML/CSS/JavaScript test runner with a FastAPI backend.

## Features

- ✨ Beautiful, animated UI
- 🚀 Run tests with one click
- 📊 Real-time test results
- 🎨 Cute design with emojis
- 📱 Responsive layout

## Setup

1. Install dependencies (if needed):
```bash
pip install fastapi uvicorn pytest pytest-json-report
```

2. Start the server:
```bash
python3 cute_test_runner/server.py
```

3. Open in browser:
```
http://localhost:8002
```

## Usage

1. Click "🚀 Run Tests" button
2. Watch the cute animations while tests run
3. See results with color-coded test status
4. Click "🧹 Clear" to reset

## Architecture

- **Frontend**: Pure HTML/CSS/JavaScript (no frameworks)
- **Backend**: FastAPI (Python)
- **Test Runner**: pytest

## Files

- `index.html` - Main HTML page
- `style.css` - Cute styling with animations
- `script.js` - Frontend JavaScript
- `server.py` - FastAPI backend
- `README.md` - This file

## Customization

You can customize:
- Colors in `style.css` (CSS variables)
- API endpoint in `script.js` (API_URL)
- Test runner in `server.py` (run_pytest function)

Enjoy your cute test runner! 🎉
