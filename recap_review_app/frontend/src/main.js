/**
 * Electron Main Process
 * 
 * Main entry point for the Recap and Review Electron application.
 * 
 * Implements best practices from Electron documentation:
 * - Single instance lock
 * - Proper app lifecycle management
 * - Window state management
 * - Error handling
 */

// Use electron/main for main process modules (tutorial best practice)
const { app, BrowserWindow, ipcMain, shell, dialog, Menu, Notification, nativeTheme } = require('electron/main');
const path = require('path');
const fs = require('fs');
const axios = require('axios');

// API URL - use backend service name in Docker, localhost otherwise
const API_URL = process.env.API_URL || 'http://127.0.0.1:8000';

let mainWindow = null;
let campaignWindow = null;
let recentDocuments = [];
let campaignState = null;
let campaignProcess = null;

// Single instance lock - prevent multiple instances
const gotTheLock = app.requestSingleInstanceLock();

if (!gotTheLock) {
  app.quit();
} else {
  app.on('second-instance', () => {
    // Someone tried to run a second instance, focus our window
    if (mainWindow) {
      if (mainWindow.isMinimized()) mainWindow.restore();
      mainWindow.focus();
    }
  });

  // App lifecycle
  app.whenReady().then(() => {
    createWindow();
    createMenu();
  });

  app.on('window-all-closed', () => {
    // On macOS, keep app running even when all windows are closed
    if (process.platform !== 'darwin') {
      app.quit();
    }
  });

  app.on('activate', () => {
    // On macOS, re-create window when dock icon is clicked
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });

  app.on('before-quit', (event) => {
    // Handle cleanup before quit if needed
    // event.preventDefault() to cancel quit
  });

  app.on('will-quit', (event) => {
    // Final cleanup before quit
  });
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 800,
    minHeight: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true,
      sandbox: false, // Set to true if you want sandbox mode
    },
    show: false, // Don't show until ready
    titleBarStyle: 'default',
    backgroundColor: '#667eea', // Match gradient background
    // Window customization
    frame: true,
    transparent: false,
    hasShadow: true,
  });

  // Show window when ready to prevent visual flash
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
    
    // Focus window
    if (process.platform === 'darwin') {
      app.dock.show();
    }
    mainWindow.focus();
  });

  // Check if DnD campaign mode is requested
  const campaignMode = process.env.DND_CAMPAIGN === '1' || process.argv.includes('--dnd-campaign');
  
  if (campaignMode) {
    // Open DnD campaign window directly
    mainWindow.loadFile(path.join(__dirname, 'renderer', 'dnd-campaign.html'));
    mainWindow.setTitle('Self-Playing DnD Campaign');
  } else {
    // Check if PDF viewer mode is requested
    const pdfPath = process.env.PDF_PATH || process.argv.find(arg => arg.startsWith('--pdf='))?.split('=')[1];
    
    if (pdfPath) {
      // Open PDF viewer with PDF path
      const pdfUrl = `file://${path.join(__dirname, 'renderer', 'pdf-viewer.html')}?file=${encodeURIComponent(pdfPath)}`;
      mainWindow.loadURL(pdfUrl);
      mainWindow.setTitle(`PDF Viewer - ${path.basename(pdfPath)}`);
    } else {
      // Open main app (default)
      mainWindow.loadFile(path.join(__dirname, 'renderer', 'index.html'));
    }
  }

  // Open DevTools in development
  if (process.env.NODE_ENV === 'development' || !app.isPackaged) {
    mainWindow.webContents.openDevTools();
  }

  // Progress bar support
  mainWindow.webContents.on('did-start-loading', () => {
    mainWindow.setProgressBar(0.1);
  });

  mainWindow.webContents.on('did-finish-load', () => {
    mainWindow.setProgressBar(-1); // Remove progress bar
  });

  mainWindow.webContents.on('did-fail-load', () => {
    mainWindow.setProgressBar(-1);
  });

  // Handle window closed
  mainWindow.on('closed', () => {
    mainWindow = null;
  });
  
  // Load recent documents
  loadRecentDocuments();

  // Handle window close
  mainWindow.on('close', (event) => {
    // Add any cleanup logic here
    // event.preventDefault() to cancel close
  });

  // Handle errors
  mainWindow.webContents.on('did-fail-load', (event, errorCode, errorDescription) => {
    console.error('Failed to load:', errorCode, errorDescription);
    dialog.showErrorBox('Load Error', `Failed to load: ${errorDescription}`);
  });

  // Handle unresponsive
  mainWindow.on('unresponsive', () => {
    dialog.showMessageBox(mainWindow, {
      type: 'warning',
      title: 'Application Unresponsive',
      message: 'The application is not responding. Would you like to wait or close it?',
      buttons: ['Wait', 'Close'],
    }).then((result) => {
      if (result.response === 1) {
        mainWindow.destroy();
      }
    });
  });
}

function createMenu() {
  const template = [
    {
      label: 'File',
      submenu: [
        {
          label: 'Generate Review',
          accelerator: 'CmdOrCtrl+G',
          click: () => {
            if (mainWindow) {
              mainWindow.webContents.send('menu-generate-review');
            }
          },
        },
        { type: 'separator' },
        {
          label: 'Recent Documents',
          submenu: (() => {
            // Refresh recent documents before building menu
            loadRecentDocuments();
            return recentDocuments.length > 0 
              ? recentDocuments.slice(0, 5).map((doc, index) => ({
                  label: doc.name,
                  accelerator: index < 9 ? `CmdOrCtrl+${index + 1}` : undefined,
                  click: () => {
                    shell.openPath(doc.path);
                  },
                }))
              : [{ label: 'No recent documents', enabled: false }];
          })(),
        },
        {
          label: 'Clear Recent Documents',
          click: () => {
            recentDocuments = [];
            saveRecentDocuments();
            if (process.platform === 'darwin') {
              app.clearRecentDocuments();
            }
            createMenu(); // Refresh menu
          },
        },
        { type: 'separator' },
        {
          label: 'Quit',
          accelerator: process.platform === 'darwin' ? 'Cmd+Q' : 'Ctrl+Q',
          click: () => {
            app.quit();
          },
        },
      ],
    },
    {
      label: 'Edit',
      submenu: [
        { role: 'undo', label: 'Undo' },
        { role: 'redo', label: 'Redo' },
        { type: 'separator' },
        { role: 'cut', label: 'Cut' },
        { role: 'copy', label: 'Copy' },
        { role: 'paste', label: 'Paste' },
      ],
    },
    {
      label: 'View',
      submenu: [
        { role: 'reload', label: 'Reload' },
        { role: 'forceReload', label: 'Force Reload' },
        { role: 'toggleDevTools', label: 'Toggle Developer Tools' },
        { type: 'separator' },
        { role: 'resetZoom', label: 'Actual Size' },
        { role: 'zoomIn', label: 'Zoom In' },
        { role: 'zoomOut', label: 'Zoom Out' },
        { type: 'separator' },
        { role: 'togglefullscreen', label: 'Toggle Full Screen' },
      ],
    },
    {
      label: 'Help',
      submenu: [
        {
          label: 'About',
          click: () => {
            dialog.showMessageBox(mainWindow, {
              type: 'info',
              title: 'About Recap and Review',
              message: 'Recap and Review',
              detail: 'Version 1.0.0\n\nA desktop application for capturing mindspace and generating review documents.',
            });
          },
        },
      ],
    },
  ];

  // macOS specific menu adjustments
  if (process.platform === 'darwin') {
    template.unshift({
      label: app.getName(),
      submenu: [
        { role: 'about', label: 'About ' + app.getName() },
        { type: 'separator' },
        { role: 'services', label: 'Services' },
        { type: 'separator' },
        { role: 'hide', label: 'Hide ' + app.getName() },
        { role: 'hideOthers', label: 'Hide Others' },
        { role: 'unhide', label: 'Show All' },
        { type: 'separator' },
        { role: 'quit', label: 'Quit ' + app.getName() },
      ],
    });
  }

  const menu = Menu.buildFromTemplate(template);
  Menu.setApplicationMenu(menu);
}

function openDnDCampaignWindow() {
  if (campaignWindow && !campaignWindow.isDestroyed()) {
    campaignWindow.focus();
    return;
  }
  
  campaignWindow = new BrowserWindow({
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
    backgroundColor: '#1e3c72',
  });
  
  campaignWindow.once('ready-to-show', () => {
    campaignWindow.show();
    campaignWindow.focus();
  });
  
  campaignWindow.loadFile(path.join(__dirname, 'renderer', 'dnd-campaign.html'));
  campaignWindow.setTitle('Self-Playing DnD Campaign');
  
  // Open DevTools in development
  if (process.env.NODE_ENV === 'development' || !app.isPackaged) {
    campaignWindow.webContents.openDevTools();
  }
  
  campaignWindow.on('closed', () => {
    campaignWindow = null;
    stopCampaignPolling();
  });
}

// IPC Handlers

ipcMain.handle('recap-and-review', async (event, data) => {
  try {
    // Show progress
    if (mainWindow) {
      mainWindow.setProgressBar(0.3);
    }
    
    const response = await axios.post(`${API_URL}/api/recap-and-review`, {
      project_path: data.project_path || null,
      output_path: data.output_path || null,
    }, {
      timeout: 60000, // 60 second timeout
    });
    
    // Update progress
    if (mainWindow) {
      mainWindow.setProgressBar(0.8);
    }
    
    // Add to recent documents if successful
    if (response.data.success && response.data.pdf_file) {
      addToRecentDocuments(response.data.pdf_file);
      
      // Show notification
      if (Notification.isSupported()) {
        new Notification({
          title: 'Review Generated',
          body: 'Your mindspace review has been generated successfully!',
          icon: path.join(__dirname, 'assets', 'icon.png'), // If available
        }).show();
      }
    }
    
    // Complete progress
    if (mainWindow) {
      mainWindow.setProgressBar(-1);
    }
    
    return response.data;
  } catch (error) {
    console.error('Error calling API:', error);
    
    // Reset progress on error
    if (mainWindow) {
      mainWindow.setProgressBar(-1);
    }
    
    // Show error notification
    if (Notification.isSupported()) {
      new Notification({
        title: 'Generation Failed',
        body: `Error: ${error.message}`,
      }).show();
    }
    
    return {
      success: false,
      error: error.message,
    };
  }
});

ipcMain.handle('get-project-info', async (event, projectPath) => {
  try {
    const response = await axios.get(`${API_URL}/api/project-info`, {
      params: { project_path: projectPath || null },
    });
    return response.data;
  } catch (error) {
    console.error('Error getting project info:', error);
    return { error: error.message };
  }
});

ipcMain.handle('open-file', async (event, filePath) => {
  try {
    // Resolve absolute path if relative
    const absolutePath = path.isAbsolute(filePath) 
      ? filePath 
      : path.resolve(app.getPath('userData'), filePath);
    
    // Check if file exists
    const fs = require('fs');
    if (!fs.existsSync(absolutePath)) {
      return { success: false, error: 'File does not exist' };
    }
    
    await shell.openPath(absolutePath);
    return { success: true };
  } catch (error) {
    console.error('Error opening file:', error);
    return { success: false, error: error.message };
  }
});

ipcMain.handle('show-open-dialog', async (event, options) => {
  try {
    const { dialog } = require('electron');
    const result = await dialog.showOpenDialog(mainWindow, {
      properties: ['openDirectory'],
      title: 'Select Project Directory',
      ...options,
    });
    
    if (result.canceled) {
      return { canceled: true };
    }
    
    return {
      canceled: false,
      filePaths: result.filePaths,
    };
  } catch (error) {
    console.error('Error showing dialog:', error);
    return { canceled: true, error: error.message };
  }
});

ipcMain.handle('show-error-box', async (event, title, content) => {
  dialog.showErrorBox(title, content);
});

ipcMain.handle('show-message-box', async (event, options) => {
  const result = await dialog.showMessageBox(mainWindow, options);
  return result;
});

ipcMain.handle('check-api-health', async () => {
  try {
    const response = await axios.get(`${API_URL}/api/health`, {
      timeout: 5000, // 5 second timeout
    });
    return { healthy: true, data: response.data };
  } catch (error) {
    return { healthy: false, error: error.message };
  }
});

ipcMain.handle('get-app-version', () => {
  return app.getVersion();
});

ipcMain.handle('get-app-name', () => {
  return app.getName();
});

// DnD Campaign IPC Handlers
ipcMain.handle('start-dnd-campaign', async () => {
  try {
    const response = await axios.post(`${API_URL}/api/dnd-campaign/start`, {}, {
      timeout: 10000,
    });
    
    campaignState = {
      status: 'running',
      message: 'Campaign started...',
      party: [],
      current_scene: 'Initializing...',
      encounters: [],
      log: [],
    };
    
    // Start polling for updates
    startCampaignPolling();
    
    return { success: true, data: response.data };
  } catch (error) {
    console.error('Error starting campaign:', error);
    return { success: false, error: error.message };
  }
});

ipcMain.handle('stop-dnd-campaign', async () => {
  try {
    await axios.post(`${API_URL}/api/dnd-campaign/stop`, {}, {
      timeout: 5000,
    });
    
    stopCampaignPolling();
    campaignState = null;
    
    return { success: true };
  } catch (error) {
    console.error('Error stopping campaign:', error);
    return { success: false, error: error.message };
  }
});

ipcMain.handle('get-campaign-state', async () => {
  try {
    const response = await axios.get(`${API_URL}/api/dnd-campaign/state`, {
      timeout: 5000,
    });
    
    if (response.data && response.data.state) {
      campaignState = response.data.state;
    }
    
    return campaignState;
  } catch (error) {
    console.error('Error getting campaign state:', error);
    return campaignState; // Return cached state on error
  }
});

let campaignPollInterval = null;

function startCampaignPolling() {
  if (campaignPollInterval) {
    clearInterval(campaignPollInterval);
  }
  
  campaignPollInterval = setInterval(async () => {
    try {
      const response = await axios.get(`${API_URL}/api/dnd-campaign/state`, {
        timeout: 5000,
      });
      
      if (response.data && response.data.state) {
        const newState = response.data.state;
        
        // Update cached state
        campaignState = newState;
        
        // Send update to campaign window if it exists, otherwise main window
        const targetWindow = campaignWindow || mainWindow;
        if (targetWindow && !targetWindow.isDestroyed()) {
          targetWindow.webContents.send('campaign-update', newState);
        }
        
        // Check if campaign is complete
        if (newState.status === 'complete' || newState.victory) {
          stopCampaignPolling();
        }
      }
    } catch (error) {
      console.error('Error polling campaign state:', error);
    }
  }, 1000); // Poll every second
}

function stopCampaignPolling() {
  if (campaignPollInterval) {
    clearInterval(campaignPollInterval);
    campaignPollInterval = null;
  }
}
