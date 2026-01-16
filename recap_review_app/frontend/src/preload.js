/**
 * Preload Script
 * 
 * Exposes safe APIs to the renderer process.
 * 
 * Follows Electron security best practices:
 * - contextIsolation enabled
 * - nodeIntegration disabled
 * - Only exposes necessary APIs
 */

const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  // Recap and Review API
  recapAndReview: (data) => ipcRenderer.invoke('recap-and-review', data),
  getProjectInfo: (projectPath) => ipcRenderer.invoke('get-project-info', projectPath),
  checkApiHealth: () => ipcRenderer.invoke('check-api-health'),
  
  // File operations
  openFile: (filePath) => ipcRenderer.invoke('open-file', filePath),
  showOpenDialog: (options) => ipcRenderer.invoke('show-open-dialog', options),
  
  // Dialogs
  showErrorBox: (title, content) => ipcRenderer.invoke('show-error-box', title, content),
  showMessageBox: (options) => ipcRenderer.invoke('show-message-box', options),
  
  // App info
  getAppVersion: () => ipcRenderer.invoke('get-app-version'),
  getAppName: () => ipcRenderer.invoke('get-app-name'),
  
  // Menu events
  onMenuGenerateReview: (callback) => {
    ipcRenderer.on('menu-generate-review', callback);
    return () => ipcRenderer.removeListener('menu-generate-review', callback);
  },
  
  // Recent documents
  getRecentDocuments: () => ipcRenderer.invoke('get-recent-documents'),
  clearRecentDocuments: () => ipcRenderer.invoke('clear-recent-documents'),
  
  // Theme
  getTheme: () => ipcRenderer.invoke('get-theme'),
  setTheme: (theme) => ipcRenderer.invoke('set-theme', theme),
  onThemeChanged: (callback) => {
    ipcRenderer.on('theme-changed', (event, theme) => callback(theme));
    return () => ipcRenderer.removeListener('theme-changed', callback);
  },
  
  // DnD Campaign API
  startDnDCampaign: () => ipcRenderer.invoke('start-dnd-campaign'),
  stopDnDCampaign: () => ipcRenderer.invoke('stop-dnd-campaign'),
  getCampaignState: () => ipcRenderer.invoke('get-campaign-state'),
  onCampaignUpdate: (callback) => {
    ipcRenderer.on('campaign-update', (event, data) => callback(event, data));
    return () => ipcRenderer.removeListener('campaign-update', callback);
  },
});
