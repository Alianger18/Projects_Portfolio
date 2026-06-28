/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import express from 'express';
import path from 'path';
import { createServer as createViteServer } from 'vite';
import { GoogleGenAI, Type } from '@google/genai';
import dotenv from 'dotenv';

// Load environment variables
dotenv.config();

let aiClient: GoogleGenAI | null = null;

function getAI(): GoogleGenAI {
  if (!aiClient) {
    const key = process.env.GEMINI_API_KEY;
    if (!key || key === 'MY_GEMINI_API_KEY' || key.trim() === '') {
      throw new Error('GEMINI_API_KEY environment variable is required but missing or unconfigured.');
    }
    aiClient = new GoogleGenAI({
      apiKey: key,
      httpOptions: {
        headers: {
          'User-Agent': 'aistudio-build',
        }
      }
    });
  }
  return aiClient;
}

async function startServer() {
  const app = express();
  const PORT = 3000;

  // Use JSON middleware
  app.use(express.json());

  // 1. Health check route
  app.get('/api/health', (req, res) => {
    res.json({ status: 'ok', time: new Date().toISOString() });
  });

  // 2. Patient AI re-evaluation route
  app.post('/api/gemini/evaluate', async (req, res) => {
    const { features, patientName, age } = req.body;
    try {
      const ai = getAI();
      const prompt = `
        Analyze the following breast fine-needle aspiration (FNA) diagnostic metrics for patient ${patientName || 'Unknown'}, age ${age || 'N/A'}:
        - Mean Radius: ${features.meanRadius} µm
        - Perimeter: ${features.perimeter} mm
        - Concavity (0-1): ${features.concavity}
        - Symmetry (0-1): ${features.symmetry}
        - Texture: ${features.texture}
        
        Provide an oncology diagnostic recommendation (Malignant, Benign, or Borderline), a confidence level as a percentage, a concise clinical rationale, and a list of structured follow-up recommendations. Because this is for board-certified clinical oncologists, do not explain elementary biology; focus strictly on cell characteristics, nuclear grade implications, and clinical thresholds.
      `;

      const response = await ai.models.generateContent({
        model: 'gemini-3.5-flash',
        contents: prompt,
        config: {
          systemInstruction: 'You are an elite automated diagnostic pathologist classifier specializing in breast oncology and cytopathology.',
          responseMimeType: 'application/json',
          responseSchema: {
            type: Type.OBJECT,
            properties: {
              predictedClass: {
                type: Type.STRING,
                description: "Must be exactly 'Malignant' or 'Benign' or 'Borderline'"
              },
              confidence: {
                type: Type.INTEGER,
                description: "Biopsy prediction confidence score, integer between 1 and 100"
              },
              rationale: {
                type: Type.STRING,
                description: "A professional logical analysis explaining why these radius, perimeter, and concavity stats point to this diagnosis."
              },
              actions: {
                type: Type.ARRAY,
                items: { type: Type.STRING },
                description: "Action plan (clinical next steps like core needle biopsy, MRI, or 6-month surveillance)."
              }
            },
            required: ["predictedClass", "confidence", "rationale", "actions"]
          }
        }
      });

      if (!response.text) {
        throw new Error("No response text from Gemini");
      }

      const results = JSON.parse(response.text.trim());
      res.json(results);
    } catch (error: any) {
      console.error('Core diagnostic evaluation error:', error);
      res.status(500).json({
        error: error.message || 'Biopsy evaluation algorithm encountered an internal failure.',
        predictedClass: 'Borderline',
        confidence: 50,
        rationale: 'AI engine fallback triggered due to local configuration state. Standard clinical guidelines recommend clinical correlation and diagnostic biopsy.',
        actions: ['Recommend urgent tissue histology validation.', 'Schedule diagnostic breast ultrasound.']
      });
    }
  });

  // 3. Detailed oncology report generator
  app.post('/api/gemini/report', async (req, res) => {
    const { patient } = req.body;
    try {
      const ai = getAI();
      const prompt = `
        Synthesize a highly professional, pristine oncology consultation report for the following patient:
        Patient Name: ${patient.name}
        Age: ${patient.age}
        Case ID: ${patient.id}
        Diagnostic Class: ${patient.predictedClass} (With ${patient.confidence}% confidence)
        Lab Features:
        - Mean Radius: ${patient.features.meanRadius} µm
        - Perimeter: ${patient.features.perimeter} mm
        - Concavity: ${patient.features.concavity}
        - Symmetry: ${patient.features.symmetry}
        - Texture: ${patient.features.texture}
        Genomics:
        - BRCA1: ${patient.genomicProfile.brca1}
        - BRCA2: ${patient.genomicProfile.brca2}
        - HER2 Status: ${patient.genomicProfile.her2Status}
        - ER Status: ${patient.genomicProfile.estrogenReceptor}
        - PR Status: ${patient.genomicProfile.progesteroneReceptor}
        - TP53 Status: ${patient.genomicProfile.tp53MutationalStatus}
        - Ki-67 Proliferation Index: ${patient.genomicProfile.ki67Index}

        Requirements for formatting:
        Write a robust markdown document with three main sections:
        1. CLINICAL ASSESSMENT & DIFFERENTIAL DIAGNOSIS (Correlate cell size and concavity with invasiveness, including HER2 and molecular subtype classification)
        2. PATHOLOGICAL CORRELATION & GENOMICS ANALYSIS (Analyze mutational profiles, estrogen/progesterone pathways, cell proliferation risk, BRCA risk score)
        3. SUGGESTED TREATMENT PROTOCOL & NEXT ACTIONS (Suggest a comprehensive pathway, e.g. Neoadjuvant chemo AC-T regimen if Malignant, surgery planning, molecular targeted agents like Trastuzumab if HER2+, or selective estrogen modulators like Tamoxifen)
        Never use conversational preamble or markdown outer wrappers. Jump straight into the title.
      `;

      const response = await ai.models.generateContent({
        model: 'gemini-3.5-flash',
        contents: prompt,
        config: {
          systemInstruction: 'You are the chief of breast oncological pathology at OncoAI clinical headquarters, signing off on molecular and tissue biopsy reports.'
        }
      });

      res.json({ report: response.text });
    } catch (error: any) {
      console.error('Report compilation error:', error);
      res.status(500).json({ error: error.message || 'Unable to compile clinical oncology report.' });
    }
  });

  // 4. Clinical Oncology Assistant Chat Proxy
  app.post('/api/gemini/chat', async (req, res) => {
    const { messages, patient } = req.body;
    try {
      const ai = getAI();
      
      // Map frontend messages key into gemini content structure
      const formattedContents = messages.map((m: any) => ({
        role: m.sender === 'doctor' ? 'user' : 'model',
        parts: [{ text: m.text }]
      }));

      const systemInstruction = `
        You are OncoAI, an elite, double-board certified clinical oncologist and molecular geneticist specializing in breast cancer diagnostics and therapeutics.
        You are assisting Dr. Richardson in evaluating a specific patient case:
        Patient: ${patient.name} (${patient.age} years old)
        ID: ${patient.id}
        Current Biopsy Verdict: ${patient.predictedClass} (AI Confidence: ${patient.confidence}%)
        Diagnostic Lab Cell Biopsy Parameters:
        - Mean Radius: ${patient.features.meanRadius} µm
        - Perimeter: ${patient.features.perimeter} mm
        - Concavity: ${patient.features.concavity}
        - Symmetry: ${patient.features.symmetry}
        - Texture: ${patient.features.texture}
        Current Patient Molecular Profiles (Genomics):
        - BRCA1: ${patient.genomicProfile.brca1}
        - BRCA2: ${patient.genomicProfile.brca2}
        - HER2 Status: ${patient.genomicProfile.her2Status}
        - Ki-67 Index: ${patient.genomicProfile.ki67Index}
        - ER Status: ${patient.genomicProfile.estrogenReceptor}
        - PR Status: ${patient.genomicProfile.progesteroneReceptor}
        - TP53 Status: ${patient.genomicProfile.tp53MutationalStatus}

        Your clinical tone should be authoritative, analytical, and highly structured. Always cite cell biopsy metrics or genomic profiles when relevant to back up your diagnostics or treatment suggestions. Use bullet points or key labels. Answer all clinical inquiries with pure professionalism. If the question is outside medicine, guide them back politely to oncology diagnostics.
      `;

      const response = await ai.models.generateContent({
        model: 'gemini-3.5-flash',
        contents: formattedContents,
        config: {
          systemInstruction
        }
      });

      res.json({ text: response.text });
    } catch (error: any) {
      console.error('Assistant chat error:', error);
      res.status(500).json({ error: error.message || 'Oncology AI conversational proxy was disconnected.' });
    }
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

  app.post('/api/flask/generate', async (req, res) => {
    try {
      const response = await fetch(`${FLASK_API}/generate`, {
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

