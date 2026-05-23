const { contextBridge, ipcRenderer } = require('electron');

// Expose protected APIs to renderer process
contextBridge.exposeInMainWorld('smartDrafting', {
  // Select file via native dialog
  selectFile: () => ipcRenderer.invoke('select-file'),

  // Send file to backend for OCR extraction
  extractDocument: (filePath) => ipcRenderer.invoke('extract-document', filePath),

  // Check if backend is running
  checkBackend: () => ipcRenderer.invoke('check-backend'),
});
