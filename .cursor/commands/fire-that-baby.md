# Fire That Baby

**Launch the D&D Campaign Desktop App and start collecting first-time startup data.**

Starts the Electron app, which spawns the Python backend, and begins monitoring data collection. This command is specifically designed to capture first-time startup metrics and system information.

**Use when:** You want to launch the desktop app for the first time and collect startup data, or test the complete system.

---

## Purpose

This command provides:
- **App Launch**: Starts the Electron desktop application
- **Backend Startup**: Spawns Python backend process
- **Monitoring Activation**: Begins data collection
- **First-Time Detection**: Captures first startup metrics
- **System Information**: Collects platform, versions, performance data

---

## What Gets Collected

### First-Time Startup Data

1. **System Information**:
   - Platform (macOS, Windows, Linux)
   - Platform version
   - Architecture
   - Python version
   - Node.js version (if available)
   - CPU count
   - Total memory

2. **Startup Metrics**:
   - Total startup time
   - Backend startup time
   - Electron startup time
   - Health check duration
   - Health check result (passed/failed)

3. **Events**:
   - Backend start event
   - Backend ready event
   - Health check events
   - Error events (if any)
   - Feature access events

4. **Performance Metrics**:
   - Health check response times
   - API response times
   - Campaign creation times
   - Other runtime metrics

---

## Execution Steps

### Step 1: Verify Prerequisites
**Purpose**: Ensure everything is ready

**Actions**:
1. Check backend dependencies installed
2. Check Electron dependencies installed
3. Verify Python 3 available
4. Verify Node.js available
5. Check monitoring directory exists

**Output**: Prerequisites status

---

### Step 2: Start Backend
**Purpose**: Launch Python backend server

**Actions**:
1. Navigate to backend directory
2. Activate virtual environment (if exists)
3. Start FastAPI server
4. Verify server starts on port 8000
5. Record backend start time

**Output**: Backend server running

---

### Step 3: Start Electron
**Purpose**: Launch Electron desktop app

**Actions**:
1. Navigate to electron directory
2. Start Electron app (`npm start`)
3. Electron spawns Python backend
4. Record Electron start time
5. Verify window opens

**Output**: Electron app running

---

### Step 4: Verify Monitoring
**Purpose**: Confirm data collection is active

**Actions**:
1. Check monitoring directory created
2. Verify startup_data.json exists (if first startup)
3. Check events.jsonl is being written
4. Check metrics.jsonl is being written
5. Verify health checks are being recorded

**Output**: Monitoring status

---

### Step 5: Collect Initial Data
**Purpose**: Trigger first data collection

**Actions**:
1. Wait for backend to be ready
2. Perform health check
3. Record first startup data (if applicable)
4. Capture system information
5. Record initial metrics

**Output**: First-time startup data collected

---

## What Happens

1. **Backend Starts**:
   - FastAPI server launches on `localhost:8000`
   - Monitoring system initializes
   - Checks if first startup
   - Collects system information
   - Records backend start event

2. **Electron Starts**:
   - Electron app launches
   - Spawns Python backend process
   - Monitors backend health
   - Records Electron start time
   - Connects to backend API

3. **Monitoring Begins**:
   - First startup data collected (if first time)
   - System info captured
   - Startup times recorded
   - Health checks monitored
   - Events logged to JSONL files

4. **Data Storage**:
   - `_pyrite/.waft/monitoring/startup_data.json` - First startup data
   - `_pyrite/.waft/monitoring/events.jsonl` - Runtime events
   - `_pyrite/.waft/monitoring/metrics.jsonl` - Performance metrics

---

## Usage Examples

### Basic Usage
```
/fire-that-baby
```

Launches the app and starts monitoring.

### With Verification
```
/fire-that-baby --verify
```

Launches app and verifies monitoring is working.

### With Logs
```
/fire-that-baby --logs
```

Launches app and shows monitoring logs in real-time.

---

## Monitoring Data Location

**Directory**: `_pyrite/.waft/monitoring/`

**Files**:
- `startup_data.json` - First-time startup data (created once)
- `events.jsonl` - Runtime events (appended continuously)
- `metrics.jsonl` - Performance metrics (appended continuously)

---

## API Endpoints

Once backend is running, monitoring data is available via:

- `GET /api/monitoring/startup-data` - Get first-time startup data
- `GET /api/monitoring/is-first-startup` - Check if first startup
- `GET /api/monitoring/stats` - Get monitoring statistics

---

## What Gets Monitored

### Events
- Backend start/stop
- Electron start/ready
- Health checks
- Campaign creation/start/completion
- Errors
- Restarts
- Shutdowns

### Metrics
- Health check duration
- API response times
- Campaign operation times
- System resource usage
- Performance benchmarks

### Features
- Which features are accessed
- Feature usage frequency
- Feature access patterns

---

## Integration

- **`/checkpoint`**: Create checkpoint after first startup
- **`/verify`**: Verify monitoring data collection
- **`/check-assumptions`**: Validate monitoring assumptions

---

## When to Use

**Use `/fire-that-baby` when**:
- ✅ First time launching the app
- ✅ Want to collect startup metrics
- ✅ Testing the complete system
- ✅ Need to verify monitoring works
- ✅ Want to capture baseline performance

**Don't use `/fire-that-baby` when**:
- ❌ Just need to start backend (use `python campaign_server.py`)
- ❌ Just need to start Electron (use `npm start`)
- ❌ Monitoring not needed

---

## Troubleshooting

### Backend Won't Start
- Check Python 3 installed: `python3 --version`
- Check dependencies: `pip install -r requirements.txt`
- Check port 8000 available

### Electron Won't Start
- Check Node.js installed: `node --version`
- Check dependencies: `npm install`
- Check backend is running first

### Monitoring Not Working
- Check monitoring directory exists: `_pyrite/.waft/monitoring/`
- Check file permissions
- Check backend logs for errors
- Verify monitoring module imported correctly

---

**This command launches the complete desktop app system and begins comprehensive data collection for first-time startup analysis.**
