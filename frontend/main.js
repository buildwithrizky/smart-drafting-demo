const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const fs = require('fs');
const http = require('http');
const FormData = require('form-data');

// ============================================================
// MAIN PROCESS - Electron
// ============================================================

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1280,
    height: 860,
    minWidth: 1024,
    minHeight: 700,
    title: 'SINSW Smart Drafting Engine - POC Demo',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      enableRemoteModule: false
    },
    icon: path.join(__dirname, 'public', 'icon.png')
  });

  mainWindow.loadFile(path.join(__dirname, 'public', 'index.html'));

  // Open DevTools in development
  // mainWindow.webContents.openDevTools();

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.whenReady().then(createWindow);

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

// ============================================================
// IPC HANDLERS
// ============================================================

// Handle file selection dialog
ipcMain.handle('select-file', async () => {
  const result = await dialog.showOpenDialog(mainWindow, {
    title: 'Pilih Dokumen untuk OCR Extraction',
    filters: [
      { name: 'Documents', extensions: ['pdf', 'png', 'jpg', 'jpeg', 'tiff', 'bmp'] },
      { name: 'PDF Files', extensions: ['pdf'] },
      { name: 'Images', extensions: ['png', 'jpg', 'jpeg', 'tiff', 'bmp'] },
      { name: 'All Files', extensions: ['*'] }
    ],
    properties: ['openFile']
  });

  if (result.canceled || result.filePaths.length === 0) {
    return null;
  }

  const filePath = result.filePaths[0];
  const stats = fs.statSync(filePath);

  return {
    path: filePath,
    name: path.basename(filePath),
    size: stats.size,
    extension: path.extname(filePath).toLowerCase()
  };
});

// Handle OCR extraction via backend API
ipcMain.handle('extract-document', async (event, filePath) => {
  return new Promise((resolve, reject) => {
    const fileBuffer = fs.readFileSync(filePath);
    const fileName = path.basename(filePath);
    const boundary = '----FormBoundary' + Math.random().toString(36).substr(2);

    // Build multipart form data manually
    const header = `------FormBoundary${boundary}\r\nContent-Disposition: form-data; name="file"; filename="${fileName}"\r\nContent-Type: application/octet-stream\r\n\r\n`;
    const footer = `\r\n------FormBoundary${boundary}--\r\n`;

    const headerBuffer = Buffer.from(header);
    const footerBuffer = Buffer.from(footer);
    const bodyBuffer = Buffer.concat([headerBuffer, fileBuffer, footerBuffer]);

    const options = {
      hostname: '127.0.0.1',
      port: 8500,
      path: '/extract',
      method: 'POST',
      family: 4,  // Force IPv4
      headers: {
        'Content-Type': `multipart/form-data; boundary=----FormBoundary${boundary}`,
        'Content-Length': bodyBuffer.length
      }
    };

    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          reject(new Error('Failed to parse response: ' + data));
        }
      });
    });

    // Timeout 120 seconds for large PDF files
    req.setTimeout(120000, () => {
      req.destroy();
      reject(new Error('Request timeout — file too large or backend overloaded'));
    });

    req.on('error', (e) => {
      reject(new Error('Backend not running. Start backend first: python3 backend/app.py\n' + e.message));
    });

    req.write(bodyBuffer);
    req.end();
  });
});

// Handle health check
ipcMain.handle('check-backend', async () => {
  return new Promise((resolve) => {
    const options = {
      hostname: '127.0.0.1',
      port: 8500,
      path: '/health',
      method: 'GET',
      family: 4  // Force IPv4
    };
    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          resolve({ status: 'error', message: 'Invalid response' });
        }
      });
    });
    req.on('error', () => {
      resolve({ status: 'offline', message: 'Backend not running' });
    });
    req.setTimeout(3000, () => {
      req.destroy();
      resolve({ status: 'timeout', message: 'Backend timeout' });
    });
    req.end();
  });
});
