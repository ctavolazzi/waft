/**
 * WAFT Desktop - Electron Main Process
 *
 * Manages WAFT Python backend process and provides IPC communication
 * with the SvelteKit frontend renderer process.
 */

const { app, BrowserWindow, ipcMain, Menu } = require('electron');
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
   * A WAFT project must have _pyrite directory and pyproject.toml
   */
  findWaftPath() {
    const fs = require('fs');

    // Check environment variable
    if (process.env.WAFT_PATH) {
      const envPath = path.resolve(process.env.WAFT_PATH);
      if (fs.existsSync(path.join(envPath, '_pyrite')) && fs.existsSync(path.join(envPath, 'pyproject.toml'))) {
        return envPath;
      }
    }

    // Check parent directory (if running from waft_desktop/electron)
    // __dirname is waft_desktop/electron, so go up two levels to get to waft project root
    const projectRoot = path.resolve(__dirname, '../..');
    if (fs.existsSync(path.join(projectRoot, '_pyrite')) && fs.existsSync(path.join(projectRoot, 'pyproject.toml'))) {
      return projectRoot;
    }

    // Try to find by walking up from current working directory
    let currentPath = process.cwd();
    const pathParts = currentPath.split(path.sep);

    for (let i = pathParts.length; i > 0; i--) {
      const testPath = pathParts.slice(0, i).join(path.sep);
      if (fs.existsSync(path.join(testPath, '_pyrite')) && fs.existsSync(path.join(testPath, 'pyproject.toml'))) {
        return testPath;
      }
    }

    // Fallback to parent directory (may not be valid, but better than nothing)
    console.warn(`Warning: Could not find valid WAFT project. Using: ${projectRoot}`);
    return projectRoot;
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
    // Use 'inherit' for stdio to avoid EPIPE errors - let backend write directly to console
    this.backendProcess = spawn('waft', ['serve', '--port', this.backendPort.toString()], {
      cwd: waftPath,
      stdio: ['ignore', 'inherit', 'inherit'], // Changed from 'pipe' to 'inherit' to avoid EPIPE
      shell: true,
      env: {
        ...process.env,
        ELECTRON_START_TIME: Date.now().toString(),
      },
      detached: false
    });

    this.startTime = Date.now();

    // #region agent log
    fetch('http://127.0.0.1:7248/ingest/ceee6b95-45b6-41a1-900d-ebc6e869bf02',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'main.js:77',message:'Backend process spawned',data:{pid:this.backendProcess.pid,waftPath:waftPath,port:this.backendPort},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'A'})}).catch(()=>{});
    // #endregion

    // Note: Using 'inherit' for stdio means we can't capture stdout/stderr directly
    // Backend output will go to Electron's console instead
    // For log capture, we'd need to use 'pipe' but handle EPIPE errors gracefully

    // Handle process errors
    this.backendProcess.on('error', (err) => {
      // #region agent log
      fetch('http://127.0.0.1:7248/ingest/ceee6b95-45b6-41a1-900d-ebc6e869bf02',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'main.js:90',message:'process spawn error',data:{error:err.message,code:err.code},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'F'})}).catch(()=>{});
      // #endregion
      console.error(`[Backend spawn error] ${err.message}`);
      this.backendProcess = null;
      this.isHealthy = false;

      if (mainWindow && !mainWindow.isDestroyed()) {
        mainWindow.webContents.send('backend-status', {
          status: 'error',
          error: err.message
        });
      }
    });

    // Handle process exit
    this.backendProcess.on('exit', (code, signal) => {
      // #region agent log
      fetch('http://127.0.0.1:7248/ingest/ceee6b95-45b6-41a1-900d-ebc6e869bf02',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'main.js:107',message:'process exit',data:{code:code,signal:signal,restartAttempts:this.restartAttempts},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'G'})}).catch(()=>{});
      // #endregion
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

  // Create context menu that works in DevTools (enables copy-paste)
  // This MUST be set up BEFORE DevTools opens to work properly
  mainWindow.webContents.on('context-menu', (e, params) => {
      // #region agent log
      fetch('http://127.0.0.1:7248/ingest/ceee6b95-45b6-41a1-900d-ebc6e869bf02',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'main.js:302',message:'Context menu event',data:{hasSelection:!!params.selectionText,isEditable:params.isEditable,linkURL:params.linkURL||'none'},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'J'})}).catch(()=>{});
      // #endregion

      const template = [];

      // Always show copy if there's selection (works in DevTools console)
      if (params.selectionText) {
        template.push({ role: 'copy', label: 'Copy', enabled: true });
      }

      // Show cut/paste if in editable area
      if (params.isEditable) {
        template.push(
          { role: 'cut', label: 'Cut', enabled: true },
          { role: 'copy', label: 'Copy', enabled: true },
          { role: 'paste', label: 'Paste', enabled: true }
        );
      }

      // If no selection but we're in DevTools, still show copy (for console text)
      // DevTools console text might not register as selectionText, so we always show copy
      if (!params.selectionText && !params.isEditable) {
        template.push({ role: 'copy', label: 'Copy', enabled: true });
      }

      // Show select all if in editable area or if there's text
      if (params.isEditable || params.selectionText) {
        if (template.length > 0) template.push({ type: 'separator' });
        template.push({ role: 'selectAll', label: 'Select All', enabled: true });
      }

      // Always show these for DevTools
      if (template.length > 0) template.push({ type: 'separator' });
      template.push(
        { role: 'reload', label: 'Reload', enabled: true },
        { role: 'forceReload', label: 'Force Reload', enabled: true },
        { role: 'toggleDevTools', label: 'Toggle Developer Tools', enabled: true }
      );

      // If we have menu items, show the menu
      if (template.length > 0) {
        const menu = Menu.buildFromTemplate(template);
        // Use popup with window reference to ensure it works in DevTools
        menu.popup({ window: mainWindow });
      }
    });

  // Load frontend
  if (isDev) {
    // Development: Load from Vite dev server (try 5173, fallback to 5174)
    const devPort = 5173;
    mainWindow.loadURL(`http://localhost:${devPort}`).catch(() => {
      // If 5173 fails, try 5174
      mainWindow.loadURL('http://localhost:5174');
    });
    // Open DevTools in development (AFTER context menu is set up)
    mainWindow.webContents.openDevTools({
      mode: 'right', // Dock DevTools to the right
      activate: true
    });
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
  // #region agent log
  fetch('http://127.0.0.1:7248/ingest/ceee6b95-45b6-41a1-900d-ebc6e869bf02',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'main.js:290',message:'App ready',data:{isDev:process.argv.includes('--dev')},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'H'})}).catch(()=>{});
  // #endregion

  createWindow();

  // Start backend after window is ready
  mainWindow.webContents.once('did-finish-load', () => {
    // #region agent log
    fetch('http://127.0.0.1:7248/ingest/ceee6b95-45b6-41a1-900d-ebc6e869bf02',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'main.js:298',message:'Window loaded, starting backend',data:{},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'I'})}).catch(()=>{});
    // #endregion
    backendManager.startBackend();
  });

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
