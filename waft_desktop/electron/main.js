/**
 * WAFT Desktop - Electron Main Process
 *
 * Manages WAFT Python backend process and provides IPC communication
 * with the SvelteKit frontend renderer process.
 */

const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const http = require('http');

// Backend management
class BackendManager {
  constructor() {
    this.backendProcess = null;
    this.backendPort = 8000;
    this.healthCheckInterval = null;
    this.restartAttempts = 0;
    this.maxRestartAttempts = 5;
    this.isHealthy = false;
    this.startTime = null;
  }

  /**
   * Find WAFT installation path
   */
  findWaftPath() {
    // Check environment variable
    if (process.env.WAFT_PATH) {
      return process.env.WAFT_PATH;
    }

    // Check parent directory (if running from waft_desktop/electron)
    const parentPath = path.resolve(__dirname, '../..');
    const waftPath = path.join(parentPath, 'waft');

    // Try to find waft command
    try {
      const { execSync } = require('child_process');
      const result = execSync('which waft', { encoding: 'utf-8' });
      if (result.trim()) {
        // Extract path from command location
        const waftBin = result.trim();
        return path.dirname(path.dirname(waftBin));
      }
    } catch (e) {
      // Fallback to parent directory
    }

    return parentPath;
  }

  /**
   * Start WAFT backend process
   */
  startBackend() {
    if (this.backendProcess) {
      console.log('Backend already running');
      return;
    }

    const waftPath = this.findWaftPath();
    console.log(`Starting WAFT backend from: ${waftPath}`);

    // Spawn WAFT serve command
    this.backendProcess = spawn('waft', ['serve', '--port', this.backendPort.toString()], {
      cwd: waftPath,
      stdio: ['ignore', 'pipe', 'pipe'],
      shell: true,
      env: {
        ...process.env,
        ELECTRON_START_TIME: Date.now().toString(),
      }
    });

    this.startTime = Date.now();

    // Handle stdout
    this.backendProcess.stdout.on('data', (data) => {
      const message = data.toString();
      console.log(`[Backend] ${message}`);
      // Send to renderer if window exists
      if (mainWindow && !mainWindow.isDestroyed()) {
        mainWindow.webContents.send('backend-log', { type: 'stdout', message });
      }
    });

    // Handle stderr
    this.backendProcess.stderr.on('data', (data) => {
      const message = data.toString();
      console.error(`[Backend Error] ${message}`);
      if (mainWindow && !mainWindow.isDestroyed()) {
        mainWindow.webContents.send('backend-log', { type: 'stderr', message });
      }
    });

    // Handle process exit
    this.backendProcess.on('exit', (code, signal) => {
      console.log(`Backend process exited with code ${code}, signal ${signal}`);
      this.backendProcess = null;
      this.isHealthy = false;

      if (mainWindow && !mainWindow.isDestroyed()) {
        mainWindow.webContents.send('backend-status', {
          status: 'stopped',
          code,
          signal
        });
      }

      // Auto-restart if not intentional shutdown
      if (code !== 0 && this.restartAttempts < this.maxRestartAttempts) {
        this.restartAttempts++;
        console.log(`Auto-restarting backend (attempt ${this.restartAttempts}/${this.maxRestartAttempts})...`);
        setTimeout(() => this.startBackend(), 2000);
      } else if (this.restartAttempts >= this.maxRestartAttempts) {
        console.error('Max restart attempts reached. Backend will not restart automatically.');
      }
    });

    // Start health checks
    this.startHealthChecks();

    if (mainWindow && !mainWindow.isDestroyed()) {
      mainWindow.webContents.send('backend-status', {
        status: 'starting',
        pid: this.backendProcess.pid
      });
    }
  }

  /**
   * Stop backend process
   */
  stopBackend() {
    if (this.healthCheckInterval) {
      clearInterval(this.healthCheckInterval);
      this.healthCheckInterval = null;
    }

    if (this.backendProcess) {
      console.log('Stopping backend process...');
      this.backendProcess.kill();
      this.backendProcess = null;
      this.isHealthy = false;
      this.restartAttempts = 0;
    }
  }

  /**
   * Restart backend process
   */
  restartBackend() {
    console.log('Restarting backend...');
    this.restartAttempts = 0;
    this.stopBackend();
    setTimeout(() => this.startBackend(), 1000);
  }

  /**
   * Start health checks
   */
  startHealthChecks() {
    if (this.healthCheckInterval) {
      return;
    }

    this.healthCheckInterval = setInterval(() => {
      this.checkHealth();
    }, 5000); // Check every 5 seconds
  }

  /**
   * Check backend health
   */
  checkHealth() {
    const options = {
      hostname: 'localhost',
      port: this.backendPort,
      path: '/api/health',
      method: 'GET',
      timeout: 2000
    };

    const req = http.request(options, (res) => {
      const wasHealthy = this.isHealthy;
      this.isHealthy = res.statusCode === 200;

      if (wasHealthy !== this.isHealthy && mainWindow && !mainWindow.isDestroyed()) {
        mainWindow.webContents.send('backend-health', {
          healthy: this.isHealthy,
          statusCode: res.statusCode,
          uptime: this.startTime ? Date.now() - this.startTime : 0
        });
      }
    });

    req.on('error', (err) => {
      const wasHealthy = this.isHealthy;
      this.isHealthy = false;

      if (wasHealthy !== this.isHealthy && mainWindow && !mainWindow.isDestroyed()) {
        mainWindow.webContents.send('backend-health', {
          healthy: false,
          error: err.message
        });
      }
    });

    req.on('timeout', () => {
      req.destroy();
      const wasHealthy = this.isHealthy;
      this.isHealthy = false;

      if (wasHealthy !== this.isHealthy && mainWindow && !mainWindow.isDestroyed()) {
        mainWindow.webContents.send('backend-health', {
          healthy: false,
          error: 'Health check timeout'
        });
      }
    });

    req.end();
  }

  /**
   * Get backend status
   */
  getStatus() {
    return {
      running: this.backendProcess !== null,
      healthy: this.isHealthy,
      port: this.backendPort,
      pid: this.backendProcess ? this.backendProcess.pid : null,
      restartAttempts: this.restartAttempts,
      uptime: this.startTime ? Date.now() - this.startTime : 0
    };
  }
}

// Global backend manager
const backendManager = new BackendManager();

// Main window
let mainWindow = null;

/**
 * Create main application window
 */
function createWindow() {
  const isDev = process.argv.includes('--dev');

  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: false
    },
    titleBarStyle: 'hiddenInset', // macOS
    show: false // Don't show until ready
  });

  // Load frontend
  if (isDev) {
    // Development: Load from Vite dev server
    mainWindow.loadURL('http://localhost:5173');
    // Open DevTools in development
    mainWindow.webContents.openDevTools();
  } else {
    // Production: Load from build
    mainWindow.loadFile(path.join(__dirname, '../frontend/build/index.html'));
  }

  // Show window when ready
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
  });

  // Handle window closed
  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

// App lifecycle
app.whenReady().then(() => {
  createWindow();

  // Start backend
  backendManager.startBackend();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  // Stop backend before quitting
  backendManager.stopBackend();

  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('before-quit', () => {
  // Ensure backend is stopped
  backendManager.stopBackend();
});

// IPC Handlers
ipcMain.handle('backend-get-status', () => {
  return backendManager.getStatus();
});

ipcMain.handle('backend-restart', () => {
  backendManager.restartBackend();
  return { success: true };
});

ipcMain.handle('backend-health-check', () => {
  backendManager.checkHealth();
  return backendManager.getStatus();
});

// Single instance lock
const gotTheLock = app.requestSingleInstanceLock();

if (!gotTheLock) {
  app.quit();
} else {
  app.on('second-instance', () => {
    // Focus existing window
    if (mainWindow) {
      if (mainWindow.isMinimized()) mainWindow.restore();
      mainWindow.focus();
    }
  });
}
