/**
 * WAFT Desktop - Preload Script
 *
 * Provides secure IPC bridge between renderer and main process.
 */

const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process
// to use ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
  backend: {
    // Get backend status
    getStatus: () => ipcRenderer.invoke('backend-get-status'),

    // Restart backend
    restart: () => ipcRenderer.invoke('backend-restart'),

    // Manual health check
    healthCheck: () => ipcRenderer.invoke('backend-health-check'),

    // Listen to backend logs
    onLog: (callback) => {
      ipcRenderer.on('backend-log', (event, data) => callback(data));
    },

    // Listen to backend status changes
    onStatus: (callback) => {
      ipcRenderer.on('backend-status', (event, data) => callback(data));
    },

    // Listen to health updates
    onHealth: (callback) => {
      ipcRenderer.on('backend-health', (event, data) => callback(data));
    },

    // Remove listeners
    removeAllListeners: (channel) => {
      ipcRenderer.removeAllListeners(channel);
    }
  }
});
