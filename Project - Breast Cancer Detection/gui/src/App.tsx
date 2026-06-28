/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect } from 'react';
import { Patient } from './types';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import DiagnosisPane from './components/DiagnosisPane';
import PatientSearchPane from './components/PatientSearchPane';
import ClinicalAssistant from './components/ClinicalAssistant';
import NewCaseModal from './components/NewCaseModal';
import { ShieldCheck, Server, ToggleLeft, ToggleRight, Radio, HelpCircle, Plus, RefreshCw, AlertCircle } from 'lucide-react';

type SideTab = 'patient-search' | 'diagnostic-queue' | 'settings';

export default function App() {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [activePatient, setActivePatient] = useState<Patient | null>(null);
  const [currentTab, setCurrentTab] = useState<SideTab>('diagnostic-queue');
  const [searchQuery, setSearchQuery] = useState('');
  const [isNewCaseOpen, setIsNewCaseOpen] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [isLoading, setIsLoading] = useState(true);
  const [apiError, setApiError] = useState<string | null>(null);
  
  // Settings tab variables
  const [strictAiTriage, setStrictAiTriage] = useState(true);
  const [simulateDelayedAntigens, setSimulateDelayedAntigens] = useState(true);

  // Fetch patients from Flask API
  const fetchPatients = async () => {
    setIsLoading(true);
    setApiError(null);
    try {
      const res = await fetch('/api/flask/patients');
      if (!res.ok) throw new Error(`API returned ${res.status}`);
      const records = await res.json();
      const mapped: Patient[] = records.map((r: any) => ({
        dbRecordId: r.id,
        id: r.patient_id || `REC-${r.id}`,
        patientId: r.patient_id,
        name: r.patient_name || 'Unknown Patient',
        age: r.patient_age || 0,
        status: r.is_confirmed === false ? 'SURVEILLANCE' : r.is_confirmed === true ? 'POST-OP' : 'PRE-OP' as const,
        avatar: '',
        lastVisit: r.created_at ? new Date(r.created_at).toLocaleDateString('en-US', { month: 'short', day: '2-digit', year: 'numeric' }) : 'N/A',
        predictedClass: (r.diagnosis === 'Malignant' ? 'Malignant' : r.diagnosis === 'Benign' ? 'Benign' : 'Borderline') as 'Malignant' | 'Benign' | 'Borderline',
        confidence: r.prediction_confidence ?? 0,
        priority: (r.diagnosis === 'Malignant' ? 'High Priority' : r.diagnosis === 'Benign' ? 'Observation' : 'Routine') as 'High Priority' | 'Routine' | 'Observation',
        features: {
          meanRadius: r.radius_mean ?? 0,
          texture: r.texture_mean ?? 0,
          perimeter: r.perimeter_mean ?? 0,
          meanArea: r.area_mean ?? 0,
          smoothness: r.smoothness_mean ?? 0,
          compactness: r.compactness_mean ?? 0,
          concavity: r.concavity_mean ?? 0,
          concavePoints: r.concave_points_mean ?? 0,
          symmetry: r.symmetry_mean ?? 0,
          fractalDimension: r.fractal_dimension_mean ?? 0,
          radiusSE: r.radius_se ?? 0,
          textureSE: r.texture_se ?? 0,
          perimeterSE: r.perimeter_se ?? 0,
          areaSE: r.area_se ?? 0,
          smoothnessSE: r.smoothness_se ?? 0,
          compactnessSE: r.compactness_se ?? 0,
          concavitySE: r.concavity_se ?? 0,
          concavePointsSE: r.concave_points_se ?? 0,
          symmetrySE: r.symmetry_se ?? 0,
          fractalDimSE: r.fractal_dimension_se ?? 0,
          worstRadius: r.radius_worst ?? 0,
          worstTexture: r.texture_worst ?? 0,
          worstPerimeter: r.perimeter_worst ?? 0,
          worstArea: r.area_worst ?? 0,
        },
        history: r.feedbacks?.length ? r.feedbacks.map((f: any) => `Feedback: ${f.feedback_body}`) : [],
        longitudinalData: [],
      }));
      setPatients(mapped);
      if (mapped.length > 0 && !activePatient) {
        setActivePatient(mapped[0]);
      } else if (mapped.length > 0 && activePatient) {
        // Refresh the active patient data if it still exists
        const refreshed = mapped.find(p => p.dbRecordId === activePatient.dbRecordId);
        if (refreshed) setActivePatient(refreshed);
        else setActivePatient(mapped[0]);
      }
    } catch (err: any) {
      setApiError(err.message || 'Failed to connect to Flask API');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => { fetchPatients(); }, []);

  // Update a patient record dynamically in our local collection (e.g. after slider adjustments)
  const handleUpdatePatient = (updatedPatient: Patient) => {
    setPatients(prev => prev.map(p => p.id === updatedPatient.id ? updatedPatient : p));
    if (activePatient && activePatient.id === updatedPatient.id) {
      setActivePatient(updatedPatient);
    }
  };

  // After adding a new patient via the modal, refresh from DB
  const handleAddPatient = (newPatient: Patient) => {
    setIsNewCaseOpen(false);
    setCurrentTab('diagnostic-queue');
    fetchPatients();
  };

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="bg-zinc-50 text-zinc-900 font-sans min-h-screen flex overflow-hidden">
      
      {/* 1. Left Sidebar Navigation rail */}
      <Sidebar 
        currentTab={currentTab} 
        setCurrentTab={(tab) => {
          setCurrentTab(tab);
        }} 
        isOpen={isSidebarOpen}
      />

      {/* 2. Main content container */}
      <div className={`flex-1 flex flex-col h-screen overflow-hidden bg-slate-50/50 transition-all duration-300 ${isSidebarOpen ? 'pl-72' : 'pl-0'}`}>
        
        {/* Top App Bar */}
        <Header 
          currentPatient={activePatient} 
          searchQuery={searchQuery}
          setSearchQuery={(q) => {
            setSearchQuery(q);
            if (currentTab !== 'patient-search') {
              setCurrentTab('patient-search');
            }
          }}
          onPrint={handlePrint}
          onToggleSidebar={() => setIsSidebarOpen(!isSidebarOpen)}
        />

        {/* Action bar with New Case button */}
        <div className="px-6 pt-4 flex justify-between items-center shrink-0">
          <div className="flex items-center gap-3">
            <button
              onClick={() => setIsNewCaseOpen(true)}
              className="flex items-center gap-2 px-4 py-2 bg-zinc-900 text-white rounded-lg text-xs font-bold hover:bg-zinc-800 transition-all cursor-pointer shadow-sm"
            >
              <Plus className="w-3.5 h-3.5" />
              New Patient Case
            </button>
            <button
              onClick={fetchPatients}
              className="flex items-center gap-2 px-3 py-2 border border-zinc-200 rounded-lg text-xs font-bold text-zinc-600 hover:bg-zinc-50 transition-all cursor-pointer"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              Refresh
            </button>
          </div>
          <span className="text-[10px] font-mono text-zinc-400">
            {patients.length} record{patients.length !== 1 ? 's' : ''} in database
          </span>
        </div>

        {/* Scrollable multi-pane workspace layout */}
        <main className="flex-1 overflow-y-auto p-6 space-y-6">

          {/* Loading State */}
          {isLoading && (
            <div className="flex flex-col items-center justify-center py-24 text-center">
              <RefreshCw className="w-8 h-8 text-zinc-400 animate-spin mb-4" />
              <p className="text-sm text-zinc-500 font-semibold">Loading patient records...</p>
              <p className="text-xs text-zinc-400 mt-1">Connecting to Flask API</p>
            </div>
          )}

          {/* Error State */}
          {!isLoading && apiError && (
            <div className="flex flex-col items-center justify-center py-24 text-center">
              <div className="w-16 h-16 bg-rose-50 rounded-full flex items-center justify-center mb-4">
                <AlertCircle className="w-8 h-8 text-rose-500" />
              </div>
              <p className="text-sm text-zinc-800 font-bold">Failed to Connect</p>
              <p className="text-xs text-zinc-500 mt-1 max-w-md">{apiError}</p>
              <p className="text-xs text-zinc-400 mt-1">Make sure the Flask server is running on port 5000</p>
              <button
                onClick={fetchPatients}
                className="mt-4 px-4 py-2 bg-zinc-900 text-white rounded-lg text-xs font-bold hover:bg-zinc-800 transition-all cursor-pointer"
              >
                Retry Connection
              </button>
            </div>
          )}

          {/* Empty State */}
          {!isLoading && !apiError && patients.length === 0 && (
            <div className="flex flex-col items-center justify-center py-24 text-center">
              <div className="w-16 h-16 bg-zinc-100 rounded-full flex items-center justify-center mb-4">
                <Plus className="w-8 h-8 text-zinc-400" />
              </div>
              <p className="text-sm text-zinc-800 font-bold">No Patient Records</p>
              <p className="text-xs text-zinc-500 mt-1">Create a new patient case to get started.</p>
              <button
                onClick={() => setIsNewCaseOpen(true)}
                className="mt-4 px-4 py-2 bg-zinc-900 text-white rounded-lg text-xs font-bold hover:bg-zinc-800 transition-all cursor-pointer"
              >
                Initialize First Case
              </button>
            </div>
          )}

          {/* Main Content */}
          {!isLoading && !apiError && patients.length > 0 && (
            <div className="grid grid-cols-12 gap-6 items-start">
              <div className="col-span-12 space-y-6">
                {currentTab === 'diagnostic-queue' && activePatient && (
                  <DiagnosisPane 
                    patient={activePatient} 
                    onUpdatePatient={handleUpdatePatient}
                  />
                )}

                {currentTab === 'patient-search' && (
                  <PatientSearchPane 
                    patients={patients} 
                    activePatient={activePatient}
                    searchQuery={searchQuery}
                    onSelectPatient={(p) => {
                      setActivePatient(p);
                      setCurrentTab('diagnostic-queue');
                    }}
                  />
                )}

                {currentTab === 'settings' && (
                  <div className="bg-white border border-zinc-200 rounded-xl p-6 shadow-xs space-y-6">
                    <div className="border-b border-zinc-100 pb-4">
                      <h2 className="font-heading font-black text-xl text-zinc-900 tracking-tight">OncoAI Clinical Preferences</h2>
                      <p className="text-zinc-500 text-xs">Configure local prognostic math benchmarks and AI diagnostic sensitivities.</p>
                    </div>

                    <div className="space-y-4">
                      <div className="flex justify-between items-center bg-zinc-50 p-4 border border-zinc-100 rounded-lg">
                        <div className="space-y-1">
                          <span className="text-xs font-bold text-zinc-800 tracking-wide uppercase block">High-Stakes AI Strict Mode</span>
                          <p className="text-[11px] text-zinc-500 leading-normal max-w-lg">
                            Under Strict mode, classification criteria is adjusted conservatively in line with the European Society for Medical Oncology (ESMO) protocols.
                          </p>
                        </div>
                        <button 
                          onClick={() => setStrictAiTriage(!strictAiTriage)}
                          className="text-zinc-800 cursor-pointer"
                        >
                          {strictAiTriage ? <ToggleRight className="w-10 h-10 text-black" /> : <ToggleLeft className="w-10 h-10 text-zinc-300" />}
                        </button>
                      </div>

                      <div className="flex justify-between items-center bg-zinc-50 p-4 border border-zinc-100 rounded-lg">
                        <div className="space-y-1">
                          <span className="text-xs font-bold text-zinc-800 tracking-wide uppercase block">Simulate Delayed CA15-3 Antigens</span>
                          <p className="text-[11px] text-zinc-500 leading-normal max-w-lg">
                            Models antigen decay curves to offset clinical response markers against actual mechanical tumor volume shrinkage rates.
                          </p>
                        </div>
                        <button 
                          onClick={() => setSimulateDelayedAntigens(!simulateDelayedAntigens)}
                          className="text-zinc-800 cursor-pointer"
                        >
                          {simulateDelayedAntigens ? <ToggleRight className="w-10 h-10 text-black" /> : <ToggleLeft className="w-10 h-10 text-zinc-300" />}
                        </button>
                      </div>

                      <div className="bg-zinc-950 text-zinc-100 p-5 rounded-lg space-y-3">
                        <div className="flex items-center gap-2">
                          <Server className="w-4 h-4 text-zinc-400" />
                          <span className="text-xs font-bold uppercase tracking-wider">Diagnostic Firmware State</span>
                        </div>
                        <div className="divide-y divide-zinc-800 text-[11px] font-mono">
                          <div className="py-2 flex justify-between">
                            <span className="text-zinc-400">OncoAI Pipeline Version:</span>
                            <span className="text-zinc-100">v4.2.1-prod</span>
                          </div>
                          <div className="py-2 flex justify-between">
                            <span className="text-zinc-400">Integration Server Ingress Port:</span>
                            <span className="text-zinc-100">3000 (Secured Proxy)</span>
                          </div>
                          <div className="py-2 flex justify-between">
                            <span className="text-zinc-400">Gemini Reasoning SDK Model:</span>
                            <span className="text-zinc-100">gemini-3.5-flash</span>
                          </div>
                          <div className="py-2 flex justify-between">
                            <span className="text-zinc-400">Flask Backend:</span>
                            <span className="text-emerald-400 font-bold">✓ Port 5000 (Proxied)</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

        </main>
      </div>

      {/* 3. Drawer Modal for New Case entries */}
      {isNewCaseOpen && (
        <NewCaseModal 
          onClose={() => setIsNewCaseOpen(false)} 
          onAddPatient={handleAddPatient}
          onRefresh={fetchPatients}
        />
      )}

    </div>
  );
}
