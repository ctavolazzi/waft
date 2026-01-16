/**
 * Preload Script - D&D Campaign Desktop App
 *
 * Security bridge between renderer and main process.
 * Exposes safe APIs to the renderer process.
 */

const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
  // Backend management
  backend: {
    getStatus: () => ipcRenderer.invoke('backend-status'),
    restart: () => ipcRenderer.invoke('backend-restart'),
    healthCheck: () => ipcRenderer.invoke('backend-health-check'),

    // Listen to backend events
    onLog: (callback) => {
      ipcRenderer.on('backend-log', (event, data) => callback(data));
    },
    onHealth: (callback) => {
      ipcRenderer.on('backend-health', (event, data) => callback(data));
    },
    onError: (callback) => {
      ipcRenderer.on('backend-error', (event, data) => callback(data));
    },
    onRestart: (callback) => {
      ipcRenderer.on('backend-restart', (event, data) => callback(data));
    },
    onFatal: (callback) => {
      ipcRenderer.on('backend-fatal', (event, data) => callback(data));
    },

    // Remove listeners
    removeAllListeners: (channel) => {
      ipcRenderer.removeAllListeners(channel);
    },
  },

  // API URL (for frontend to connect to backend)
  apiUrl: 'http://127.0.0.1:8000',
});
