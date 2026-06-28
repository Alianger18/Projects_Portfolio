/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { Patient } from '../types';
import { UserPlus, Wand2, User, Activity, Loader2, Check, AlertCircle } from 'lucide-react';

interface NewCaseModalProps {
  onClose: () => void;
  onAddPatient: (patient: Patient) => void;
  onRefresh: () => void;
}

// The 30 feature keys exactly as the Flask model expects them (note: spaces in "concave points")
const FEATURE_KEYS = [
  "radius_mean", "texture_mean", "perimeter_mean", "area_mean", "smoothness_mean", "compactness_mean",
  "concavity_mean", "concave points_mean", "symmetry_mean", "fractal_dimension_mean", "radius_se",
  "texture_se", "perimeter_se", "area_se", "smoothness_se", "compactness_se", "concavity_se",
  "concave points_se", "symmetry_se", "fractal_dimension_se", "radius_worst",
  "texture_worst", "perimeter_worst", "area_worst", "smoothness_worst",
  "compactness_worst", "concavity_worst", "concave points_worst",
  "symmetry_worst", "fractal_dimension_worst"
];

const formatFeatureLabel = (key: string): string => {
  return key.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
};

export default function NewCaseModal({ onClose, onAddPatient, onRefresh }: NewCaseModalProps) {
  const [name, setName] = useState('');
  const [age, setAge] = useState<number>(45);
  const [targetConfidence, setTargetConfidence] = useState<number>(75);

  // Generated features state
  const [generatedFeatures, setGeneratedFeatures] = useState<Record<string, number> | null>(null);
  const [generatedDiagnosis, setGeneratedDiagnosis] = useState<string | null>(null);
  const [generatedConfidence, setGeneratedConfidence] = useState<number | null>(null);

  // Loading & error states
  const [isGenerating, setIsGenerating] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Generate features using the Flask /generate endpoint
  const handleGenerate = async () => {
    setIsGenerating(true);
    setError(null);
    try {
      const res = await fetch('/api/flask/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ target_confidence: targetConfidence }),
      });
      if (!res.ok) throw new Error(`Generation failed (${res.status})`);
      const data = await res.json();
      setGeneratedFeatures(data.features);
      setGeneratedDiagnosis(data.diagnosis);
      setGeneratedConfidence(data.confidence);
    } catch (err: any) {
      setError(err.message || 'Failed to generate features. Is Flask running?');
    } finally {
      setIsGenerating(false);
    }
  };

  // Save the patient to the Flask DB via /predict
  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim() || !generatedFeatures) return;

    setIsSaving(true);
    setError(null);
    try {
      const payload: Record<string, any> = {
        ...generatedFeatures,
        patient_name: name.trim(),
        patient_age: age,
      };

      const res = await fetch('/api/flask/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.description || `Save failed (${res.status})`);
      }
      const result = await res.json();

      // Create the patient object for the GUI
      const newPatient: Patient = {
        dbRecordId: result.record_id,
        id: result.patient_id || `REC-${result.record_id}`,
        patientId: result.patient_id,
        name: name.trim(),
        age,
        predictedClass: result.diagnosis === 'Malignant' ? 'Malignant' : result.diagnosis === 'Benign' ? 'Benign' : 'Borderline',
        confidence: result.confidence,
        features: {
          meanRadius: generatedFeatures['radius_mean'] ?? 0,
          texture: generatedFeatures['texture_mean'] ?? 0,
          perimeter: generatedFeatures['perimeter_mean'] ?? 0,
          concavity: generatedFeatures['concavity_mean'] ?? 0,
          symmetry: generatedFeatures['symmetry_mean'] ?? 0,
        },
      };

      onAddPatient(newPatient);
      onRefresh();
      onClose();
    } catch (err: any) {
      setError(err.message || 'Failed to save patient.');
    } finally {
      setIsSaving(false);
    }
  };

  // Confidence slider color based on value
  const getConfidenceColor = () => {
    if (targetConfidence >= 90) return 'text-rose-600';
    if (targetConfidence >= 75) return 'text-amber-600';
    return 'text-emerald-600';
  };

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-xs z-[100] flex items-center justify-center p-4">
      <div className="bg-white w-full max-w-2xl rounded-xl shadow-2xl flex flex-col max-h-[90vh] overflow-hidden">
        
        <div className="p-6 border-b border-zinc-100 flex justify-between items-center bg-zinc-50 shrink-0">
          <div className="flex items-center gap-2">
            <UserPlus className="w-5 h-5 text-zinc-900" />
            <h3 className="font-sans font-black text-xl text-zinc-900">Initialize New Patient File</h3>
          </div>
          <button 
            onClick={onClose}
            className="p-1.5 hover:bg-zinc-200 rounded-full font-bold font-mono transition-all text-zinc-400 hover:text-zinc-600 cursor-pointer"
          >
            ✕
          </button>
        </div>

        <form onSubmit={handleSave} className="flex-1 overflow-y-auto p-6 space-y-6">

          {/* Error Banner */}
          {error && (
            <div className="p-3 bg-rose-50 border border-rose-200 rounded-lg flex items-start gap-2">
              <AlertCircle className="w-4 h-4 text-rose-500 mt-0.5 shrink-0" />
              <p className="text-xs text-rose-700 font-medium">{error}</p>
            </div>
          )}

          {/* Patient Demographics */}
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1">
              <label className="text-xs font-extrabold text-zinc-400 uppercase tracking-widest block">Full Name</label>
              <div className="relative">
                <User className="w-4 h-4 text-zinc-400 absolute left-3 top-3" />
                <input
                  type="text"
                  required
                  placeholder="e.g. Catherine Dupont"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="w-full bg-zinc-50 border border-zinc-200 rounded pl-9 pr-3 py-2 text-xs focus:ring-1 focus:ring-zinc-950 focus:border-zinc-950 focus:bg-white"
                />
              </div>
            </div>

            <div className="space-y-1">
              <label className="text-xs font-extrabold text-zinc-400 uppercase tracking-widest block">Age</label>
              <input
                type="number"
                min="18"
                max="100"
                value={age}
                onChange={(e) => setAge(parseInt(e.target.value))}
                className="w-full bg-zinc-50 border border-zinc-200 rounded px-3 py-2 text-xs focus:ring-1 focus:ring-zinc-950 focus:border-zinc-950 focus:bg-white"
              />
            </div>
          </div>

          {/* Confidence Target Slider + Generate Button */}
          <div className="border border-zinc-200 p-4 rounded-xl space-y-4 bg-zinc-50/50">
            <div className="flex justify-between items-center">
              <h4 className="text-xs font-extrabold text-zinc-900 flex items-center gap-1.5 uppercase tracking-wide">
                <Wand2 className="w-4 h-4 text-zinc-600" />
                Feature Generation Control
              </h4>
              <span className="text-[10px] text-zinc-400 font-medium">Powered by centroid interpolation</span>
            </div>

            <div className="space-y-3">
              <div className="flex justify-between items-baseline">
                <label className="text-[10px] font-bold text-zinc-500 uppercase tracking-wider">
                  Target Malignancy Confidence
                </label>
                <span className={`text-lg font-black font-mono ${getConfidenceColor()}`}>
                  {targetConfidence}%
                </span>
              </div>
              
              <input
                type="range"
                min="50"
                max="99"
                value={targetConfidence}
                onChange={(e) => setTargetConfidence(parseInt(e.target.value))}
                className="w-full h-2 bg-zinc-200 rounded-lg appearance-none cursor-pointer accent-zinc-900"
              />
              
              <div className="flex justify-between text-[9px] font-bold text-zinc-400 uppercase tracking-wider">
                <span>50% (Borderline)</span>
                <span>75% (Moderate)</span>
                <span>99% (High)</span>
              </div>
            </div>

            <button
              type="button"
              onClick={handleGenerate}
              disabled={isGenerating}
              className="w-full flex items-center justify-center gap-2 px-4 py-2.5 bg-zinc-900 text-white rounded-lg text-xs font-bold hover:bg-zinc-800 transition-all cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isGenerating ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  Generating Features...
                </>
              ) : (
                <>
                  <Activity className="w-4 h-4" />
                  Generate 30-Feature Profile
                </>
              )}
            </button>
          </div>

          {/* Generated Features Display */}
          {generatedFeatures && (
            <div className="border border-zinc-200 p-4 rounded-xl space-y-4 bg-white">
              {/* Prediction Result */}
              <div className={`p-4 rounded-lg border flex items-center justify-between ${
                generatedDiagnosis === 'Malignant' 
                  ? 'bg-rose-50 border-rose-200' 
                  : 'bg-emerald-50 border-emerald-200'
              }`}>
                <div className="flex items-center gap-2">
                  <Check className={`w-5 h-5 ${
                    generatedDiagnosis === 'Malignant' ? 'text-rose-600' : 'text-emerald-600'
                  }`} />
                  <div>
                    <span className="text-[10px] font-extrabold uppercase tracking-widest text-zinc-400 block">Model Prediction</span>
                    <span className={`text-lg font-black ${
                      generatedDiagnosis === 'Malignant' ? 'text-rose-700' : 'text-emerald-700'
                    }`}>
                      {generatedDiagnosis}
                    </span>
                  </div>
                </div>
                <div className="text-right">
                  <span className="text-[10px] font-extrabold uppercase tracking-widest text-zinc-400 block">Confidence</span>
                  <span className="text-2xl font-black font-mono text-zinc-900">{generatedConfidence}%</span>
                </div>
              </div>

              {/* Feature Grid */}
              <div>
                <h4 className="text-[10px] font-extrabold text-zinc-400 uppercase tracking-widest mb-3">
                  Generated Feature Values (30 Features)
                </h4>
                <div className="grid grid-cols-2 gap-x-6 gap-y-1.5 max-h-48 overflow-y-auto">
                  {FEATURE_KEYS.map(key => (
                    <div key={key} className="flex justify-between items-baseline py-1 border-b border-zinc-50">
                      <span className="text-[10px] text-zinc-600 font-medium truncate mr-2">
                        {formatFeatureLabel(key)}
                      </span>
                      <span className="text-[10px] font-mono font-bold text-zinc-900 shrink-0">
                        {(generatedFeatures[key] ?? 0).toFixed(4)}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

        </form>

        <div className="p-4 border-t border-zinc-100 flex justify-end gap-2 bg-zinc-50 shrink-0">
          <button 
            type="button" 
            onClick={onClose}
            className="border border-zinc-200 hover:border-zinc-300 hover:bg-zinc-100 text-zinc-650 px-5 py-2 rounded text-xs font-bold transition-all cursor-pointer"
          >
            Cancel
          </button>
          <button 
            type="button" 
            onClick={handleSave}
            disabled={!name.trim() || !generatedFeatures || isSaving}
            className={`px-5 py-2 rounded text-xs font-bold transition-all flex items-center gap-1 cursor-pointer ${
              name.trim() && generatedFeatures && !isSaving
                ? 'bg-black hover:bg-zinc-850 text-white'
                : 'bg-zinc-200 text-zinc-400 cursor-not-allowed'
            }`}
          >
            {isSaving ? (
              <>
                <Loader2 className="w-3.5 h-3.5 animate-spin" />
                Saving...
              </>
            ) : (
              'Save Patient File'
            )}
          </button>
        </div>

      </div>
    </div>
  );
}
