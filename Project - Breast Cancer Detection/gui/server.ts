/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import express from 'express';
import path from 'path';
import { createServer as createViteServer } from 'vite';

import dotenv from 'dotenv';

// Load environment variables
dotenv.config();



async function startServer() {
  const app = express();
  const PORT = 3000;

  // Use JSON middleware
  app.use(express.json());

  // 1. Health check route
  app.get('/api/health', (req, res) => {
    res.json({ status: 'ok', time: new Date().toISOString() });
  });



  // --- Flask API Proxy Routes (forward to Flask on port 5000) ---
  const FLASK_API = 'http://localhost:5000';

  app.get('/api/flask/patients', async (req, res) => {
    try {
      const response = await fetch(`${FLASK_API}/patients`);
      const data = await response.json();
      res.status(response.status).json(data);
    } catch (error: any) {
      res.status(502).json({ error: 'Flask API unreachable. Ensure the Flask server is running on port 5000.' });
    }
  });

  app.post('/api/flask/predict', async (req, res) => {
    try {
      const response = await fetch(`${FLASK_API}/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(req.body),
      });
      const data = await response.json();
      res.status(response.status).json(data);
    } catch (error: any) {
      res.status(502).json({ error: 'Flask API unreachable.' });
    }
  });

  app.post('/api/flask/reject/:id', async (req, res) => {
    try {
      const response = await fetch(`${FLASK_API}/reject/${req.params.id}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(req.body),
      });
      const data = await response.json();
      res.status(response.status).json(data);
    } catch (error: any) {
      res.status(502).json({ error: 'Flask API unreachable.' });
    }
  });




  // Serve Vite assets in development, serve static bundle in production
  if (process.env.NODE_ENV !== "production") {
    console.log('Initializing Vite Development Server middleware...');
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: 'spa',
    });
    app.use(vite.middlewares);
  } else {
    console.log('Production mode: serving built static assets from dist/');
    const distPath = path.join(process.cwd(), 'dist');
    app.use(express.static(distPath));
    app.get('*', (req, res) => {
      res.sendFile(path.join(distPath, 'index.html'));
    });
  }

  app.listen(PORT, '0.0.0.0', () => {
    console.log(`OncoAI Diagnostic Dashboard listening on http://localhost:${PORT}`);
  });
}

startServer();

