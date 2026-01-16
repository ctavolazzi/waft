/**
 * Electron Main Process - D&D Campaign Desktop App
 *
 * Manages Python backend process, health monitoring, and auto-restart.
 * Based on Electron best practices and recap_review_app structure.
 */

const { app, BrowserWindow, ipcMain } = require('electron/main');
const path = require('path');
const { spawn } = require('child_process');
const axios = require('axios');

// Configuration
const API_URL = 'http://127.0.0.1:8000';
const BACKEND_HEALTH_CHECK_INTERVAL = 5000; // 5 seconds
const MAX_RESTART_ATTEMPTS = 5;
const RESTART_DELAY = 2000; // 2 seconds

let mainWindow = null;
let pythonProcess = null;
let restartCount = 0;
let healthCheckInterval = null;
let isShuttingDown = false;

// Single instance lock
const gotTheLock = app.requestSingleInstanceLock();

if (!gotTheLock) {
  app.quit();
} else {
  app.on('second-instance', () => {
    if (mainWindow) {
      if (mainWindow.isMinimized()) mainWindow.restore();
      mainWindow.focus();
    }
  });

  // App lifecycle
  app.whenReady().then(() => {
    createWindow();
    startBackend();
  });

  app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
      app.quit();
    }
  });

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });

  app.on('before-quit', () => {
    isShuttingDown = true;
    stopBackend();
  });
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1000,
    minHeight: 700,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true,
      sandbox: false,
    },
    show: false,
    titleBarStyle: 'default',
    backgroundColor: '#1a1a2e',
    frame: true,
    transparent: false,
    hasShadow: true,
  });

  mainWindow.once('ready-to-show', () => {
    mainWindow.show();

    if (process.platform === 'darwin') {
      app.dock.show();
    }
    mainWindow.focus();
  });

  // Load SvelteKit dev server or built app
  if (process.env.NODE_ENV === 'development' || !app.isPackaged) {
    // Development: Connect to SvelteKit dev server
    mainWindow.loadURL('http://localhost:5173');
    mainWindow.webContents.openDevTools();
  } else {
    // Production: Load built SvelteKit app
    mainWindow.loadFile(path.join(__dirname, '../frontend/build/index.html'));
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

class BackendManager {
  constructor() {
    this.process = null;
    this.restartCount = 0;
    this.maxRestarts = MAX_RESTART_ATTEMPTS;
    this.isRunning = false;
  }

  start() {
    if (this.process) {
      console.log('Backend already running');
      return;
    }

    console.log('Starting Python backend...');

    const electronStartTime = Date.now();

    // Determine Python path
    const pythonCommand = process.platform === 'win32' ? 'python' : 'python3';
    const backendPath = path.join(__dirname, '../backend/campaign_server.py');
    const projectPath = path.resolve(__dirname, '../..');

    // Spawn Python backend process
    this.process = spawn(pythonCommand, [backendPath], {
      cwd: projectPath,
      env: {
        ...process.env,
        WAFT_PROJECT_PATH: projectPath,
        PYTHONUNBUFFERED: '1',
        ELECTRON_START_TIME: electronStartTime.toString(),
      },
      stdio: ['pipe', 'pipe', 'pipe'],
    });

    this.isRunning = true;

    // Handle stdout
    this.process.stdout.on('data', (data) => {
      const output = data.toString();
      console.log(`[Backend] ${output}`);
      if (mainWindow) {
        mainWindow.webContents.send('backend-log', { type: 'stdout', message: output });
      }
    });

    // Handle stderr
    this.process.stderr.on('data', (data) => {
      const output = data.toString();
      console.error(`[Backend Error] ${output}`);
      if (mainWindow) {
        mainWindow.webContents.send('backend-log', { type: 'stderr', message: output });
      }
    });

    // Handle process exit
    this.process.on('exit', (code, signal) => {
      console.log(`Backend process exited with code ${code}, signal ${signal}`);
      this.process = null;
      this.isRunning = false;

      if (!isShuttingDown && code !== 0) {
        this.handleCrash();
      }
    });

    // Handle process error
    this.process.on('error', (error) => {
      console.error('Backend process error:', error);
      this.isRunning = false;
      if (mainWindow) {
        mainWindow.webContents.send('backend-error', { error: error.message });
      }

      if (!isShuttingDown) {
        this.handleCrash();
      }
    });

    // Start health monitoring
    this.startHealthMonitoring();
  }

  handleCrash() {
    if (this.restartCount >= this.maxRestarts) {
      console.error(`Backend crashed ${this.maxRestarts} times. Stopping restart attempts.`);
      if (mainWindow) {
        mainWindow.webContents.send('backend-fatal', {
          message: `Backend crashed ${this.maxRestarts} times. Please check logs.`,
        });
      }
      return;
    }

    this.restartCount++;
    console.log(`Backend crashed, restarting... (${this.restartCount}/${this.maxRestarts})`);

    if (mainWindow) {
      mainWindow.webContents.send('backend-restart', {
        attempt: this.restartCount,
        maxAttempts: this.maxRestarts,
      });
    }

    setTimeout(() => {
      this.start();
    }, RESTART_DELAY);
  }

  async healthCheck() {
    try {
      const response = await axios.get(`${API_URL}/api/health`, {
        timeout: 3000,
      });

      if (response.data.status === 'healthy') {
        // Reset restart count on successful health check
        if (this.restartCount > 0) {
          console.log('Backend recovered, resetting restart count');
          this.restartCount = 0;
        }

        if (mainWindow) {
          mainWindow.webContents.send('backend-health', {
            status: 'healthy',
            metrics: response.data.metrics,
          });
        }
        return true;
      } else {
        throw new Error('Backend unhealthy');
      }
    } catch (error) {
      console.error('Health check failed:', error.message);

      if (mainWindow) {
        mainWindow.webContents.send('backend-health', {
          status: 'unhealthy',
          error: error.message,
        });
      }

      // If process is running but health check fails, restart
      if (this.isRunning && !isShuttingDown) {
        console.log('Health check failed, restarting backend...');
        this.stop();
        this.handleCrash();
      }

      return false;
    }
  }

  startHealthMonitoring() {
    if (healthCheckInterval) {
      clearInterval(healthCheckInterval);
    }

    healthCheckInterval = setInterval(() => {
      if (!isShuttingDown) {
        this.healthCheck();
      }
    }, BACKEND_HEALTH_CHECK_INTERVAL);
  }

  stop() {
    if (healthCheckInterval) {
      clearInterval(healthCheckInterval);
      healthCheckInterval = null;
    }

    if (this.process) {
      console.log('Stopping Python backend...');
      this.isRunning = false;

      // Try graceful shutdown
      if (process.platform === 'win32') {
        this.process.kill();
      } else {
        this.process.kill('SIGTERM');
      }

      // Force kill after timeout
      setTimeout(() => {
        if (this.process) {
          console.log('Force killing backend process...');
          this.process.kill('SIGKILL');
          this.process = null;
        }
      }, 5000);
    }
  }
}

const backendManager = new BackendManager();

function startBackend() {
  backendManager.start();
}

function stopBackend() {
  backendManager.stop();
}

// IPC handlers
ipcMain.handle('backend-status', async () => {
  return {
    isRunning: backendManager.isRunning,
    restartCount: backendManager.restartCount,
  };
});

ipcMain.handle('backend-restart', async () => {
  backendManager.stop();
  setTimeout(() => {
    backendManager.start();
  }, 1000);
  return { success: true };
});

ipcMain.handle('backend-health-check', async () => {
  return await backendManager.healthCheck();
});
