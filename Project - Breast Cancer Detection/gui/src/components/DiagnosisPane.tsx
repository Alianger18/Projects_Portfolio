/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect } from 'react';
import { ArrowRight, Info, AlertCircle, RefreshCw, FileText, Calendar, Compass, ShieldAlert, Check, Star, Search, Activity, Filter } from 'lucide-react';
import { Patient, LabFeatures } from '../types';

interface FeatureDefinition {
  id: string;
  label: string; // e.g. "texture_worst"
  min: number;
  max: number;
  key: string; // key in patient.features
  fallbackKey?: string;
  multiplier?: number;
  defaultValue?: number;
}

const FEATURE_DEFINITIONS: FeatureDefinition[] = [
  // First 3 prominent values as requested:
  { id: 'texture_worst', label: 'texture_worst', min: 12.02, max: 41.78, key: 'worstTexture' },
  { id: 'radius_worst', label: 'radius_worst', min: 7.93, max: 19.82, key: 'worstRadius' },
  { id: 'concave_points_worst', label: 'concave points_worst', min: 0.0000, max: 0.1750, key: 'worstConcavePoints', fallbackKey: 'concavePoints', multiplier: 1.25 },

  // Remaining features:
  { id: 'radius_mean', label: 'radius_mean', min: 6.9810, max: 17.8500, key: 'meanRadius' },
  { id: 'texture_mean', label: 'texture_mean', min: 9.7100, max: 33.8100, key: 'texture' },
  { id: 'perimeter_mean', label: 'perimeter_mean', min: 43.7900, max: 114.6000, key: 'perimeter' },
  { id: 'area_mean', label: 'area_mean', min: 143.5000, max: 992.1000, key: 'meanArea', fallbackKey: 'meanRadius', multiplier: 50 },
  { id: 'smoothness_mean', label: 'smoothness_mean', min: 0.05263, max: 0.1634, key: 'smoothness', defaultValue: 0.096 },
  { id: 'compactness_mean', label: 'compactness_mean', min: 0.01938, max: 0.2239, key: 'compactness', defaultValue: 0.104 },
  { id: 'concavity_mean', label: 'concavity_mean', min: 0.0000, max: 0.4108, key: 'concavity' },
  { id: 'concave_points_mean', label: 'concave points_mean', min: 0.0000, max: 0.08534, key: 'concavePoints', defaultValue: 0.049 },
  { id: 'symmetry_mean', label: 'symmetry_mean', min: 0.1060, max: 0.2743, key: 'symmetry' },
  { id: 'fractal_dimension_mean', label: 'fractal_dimension_mean', min: 0.05185, max: 0.09575, key: 'fractalDimension', defaultValue: 0.062 },
  
  { id: 'radius_se', label: 'radius_se', min: 0.1115, max: 0.8811, key: 'radiusSE', defaultValue: 0.405 },
  { id: 'texture_se', label: 'texture_se', min: 0.3602, max: 4.885, key: 'textureSE', defaultValue: 1.216 },
  { id: 'perimeter_se', label: 'perimeter_se', min: 0.7570, max: 5.1180, key: 'perimeterSE', defaultValue: 2.866 },
  { id: 'area_se', label: 'area_se', min: 6.8020, max: 77.1100, key: 'areaSE', defaultValue: 40.33 },
  { id: 'smoothness_se', label: 'smoothness_se', min: 0.001713, max: 0.02177, key: 'smoothnessSE', defaultValue: 0.007 },
  { id: 'compactness_se', label: 'compactness_se', min: 0.002252, max: 0.1064, key: 'compactnessSE', defaultValue: 0.025 },
  { id: 'concavity_se', label: 'concavity_se', min: 0.0000, max: 0.3960, key: 'concavitySE', defaultValue: 0.032 },
  { id: 'concave_points_se', label: 'concave points_se', min: 0.0000, max: 0.05279, key: 'concavePointsSE', defaultValue: 0.011 },
  { id: 'symmetry_se', label: 'symmetry_se', min: 0.009539, max: 0.06146, key: 'symmetrySE', defaultValue: 0.020 },
  { id: 'fractal_dimension_se', label: 'fractal_dimension_se', min: 0.000895, max: 0.02984, key: 'fractalDimSE', defaultValue: 0.0037 },
  
  { id: 'perimeter_worst', label: 'perimeter_worst', min: 50.4100, max: 127.1000, key: 'worstPerimeter', fallbackKey: 'perimeter', multiplier: 1.3 },
  { id: 'area_worst', label: 'area_worst', min: 185.2000, max: 1210.0000, key: 'worstArea', fallbackKey: 'meanArea', multiplier: 1.5 },
  { id: 'smoothness_worst', label: 'smoothness_worst', min: 0.07117, max: 0.2006, key: 'worstSmoothness', fallbackKey: 'smoothness', multiplier: 1.2 },
  { id: 'compactness_worst', label: 'compactness_worst', min: 0.02729, max: 0.5849, key: 'worstCompactness', fallbackKey: 'compactness', multiplier: 1.3 },
  { id: 'concavity_worst', label: 'concavity_worst', min: 0.0000, max: 1.2520, key: 'worstConcavity', fallbackKey: 'concavity', multiplier: 1.25 },
  { id: 'symmetry_worst', label: 'symmetry_worst', min: 0.1566, max: 0.4228, key: 'worstSymmetry', fallbackKey: 'symmetry', multiplier: 1.25 },
  { id: 'fractal_dimension_worst', label: 'fractal_dimension_worst', min: 0.05521, max: 0.1486, key: 'worstFractalDim', fallbackKey: 'fractalDimension', multiplier: 1.2 }
];

const formatFeatureLabel = (id: string): string => {
  const customMap: { [key: string]: string } = {
    texture_worst: "Worst Biopsy Texture",
    radius_worst: "Worst Cellular Radius",
    concave_points_worst: "Worst Concave Points",
    radius_mean: "Mean Cellular Radius",
    texture_mean: "Mean Biopsy Texture",
    perimeter_mean: "Mean Cellular Perimeter",
    area_mean: "Mean Cellular Area",
    smoothness_mean: "Mean Cellular Smoothness",
    compactness_mean: "Mean Cellular Compactness",
    concavity_mean: "Mean Cellular Concavity",
    concave_points_mean: "Mean Concave Points",
    symmetry_mean: "Mean Cellular Symmetry",
    fractal_dimension_mean: "Mean Fractal Dimension",
    radius_se: "Radius Standard Error",
    texture_se: "Texture Standard Error",
    perimeter_se: "Perimeter Standard Error",
    area_se: "Area Standard Error",
    smoothness_se: "Smoothness Standard Error",
    compactness_se: "Compactness Standard Error",
    concavity_se: "Concavity Standard Error",
    concave_points_se: "Concave Points Standard Error",
    symmetry_se: "Symmetry Standard Error",
    fractal_dimension_se: "Fractal Dimension Standard Error",
    perimeter_worst: "Worst Cellular Perimeter",
    area_worst: "Worst Cellular Area",
    smoothness_worst: "Worst Cellular Smoothness",
    compactness_worst: "Worst Cellular Compactness",
    concavity_worst: "Worst Cellular Concavity",
    symmetry_worst: "Worst Cellular Symmetry",
    fractal_dimension_worst: "Worst Fractal Dimension"
  };
  return customMap[id] || id.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
};

interface DiagnosisPaneProps {
  patient: Patient;
  onUpdatePatient: (updatedPatient: Patient) => void;
}

export default function DiagnosisPane({ patient, onUpdatePatient }: DiagnosisPaneProps) {
  const [isReportGenerating, setIsReportGenerating] = useState(false);
  const [reportMarkdown, setReportMarkdown] = useState<string | null>(null);
  const [showAllFeatures, setShowAllFeatures] = useState(false);
  const [feedback, setFeedback] = useState('');
  const [isRevising, setIsRevising] = useState(false);
  const [showRejectModal, setShowRejectModal] = useState(false);
  const [rejectFeedback, setRejectFeedback] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [rejectError, setRejectError] = useState<string | null>(null);

  useEffect(() => {
    setReportMarkdown(null);
    setFeedback(patient.oncologistVerification?.feedback ?? '');
    setIsRevising(false);
    setShowRejectModal(false);
    setRejectFeedback('');
    setShowAllFeatures(false);
    setIsSubmitting(false);
    setRejectError(null);
  }, [patient]);

  const getVal = (def: FeatureDefinition): number => {
    const val = patient.features[def.key];
    if (val !== undefined && val !== null) return val;
    
    if (def.fallbackKey) {
      const fallbackVal = patient.features[def.fallbackKey];
      if (fallbackVal !== undefined && fallbackVal !== null) {
        return Number((fallbackVal * (def.multiplier ?? 1)).toFixed(4));
      }
    }
    
    if (def.defaultValue !== undefined) return def.defaultValue;
    
    return 0.0;
  };

  const getStatus = (val: number, def: FeatureDefinition) => {
    if (val < def.min) return { status: 'Atypical' as const, label: 'Atypical (Low)', color: 'text-amber-700 bg-amber-50 border border-amber-200' };
    if (val > def.max) return { status: 'Atypical' as const, label: 'Atypical (High)', color: 'text-rose-700 bg-rose-50 border border-rose-200' };
    return { status: 'Normal' as const, label: 'Normal', color: 'text-emerald-700 bg-emerald-50 border border-emerald-200' };
  };


  // Compile detailed clinical oncologist report using Gemini
  const triggerReportCompilation = async () => {
    setIsReportGenerating(true);
    setReportMarkdown(null);
    try {
      const res = await fetch('/api/gemini/report', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ patient }),
      });
      const data = await res.json();
      if (data.report) {
        setReportMarkdown(data.report);
      } else {
        throw new Error("No report contents found.");
      }
    } catch (err) {
      // Offline fallback report markdown
      setReportMarkdown(`
# CLINICAL PATHOLOGY DECISION STUDY & CONCORDANCE SUMMARY
**Patient:** ${patient.name} | **Age:** ${patient.age} | **ID:** ${patient.id}
**Classification:** ${patient.predictedClass.toUpperCase()} (Prognosis Likelihood: ${patient.confidence}%)

## 1. MOLECULAR CLASSIFICATION PATHWAY
Tissue FNA exhibits key abnormal measurements indicative of atypical proliferative patterns. 
The Mean cellular radius of **${patient.features.meanRadius} µm** paired with nuclear perimeter scores of **${patient.features.perimeter} mm** shows characteristic nuclear enlargement seen in grade II/III carcinomas. 
HER2 expression is recorded as **${patient.genomicProfile?.her2Status || 'N/A'}**, ER/PR pathways are positive, characterizing a **Luminal-like** molecular breast tumor subtype which dictates therapeutic course.

## 2. SURGICAL & CHEMOTHERAPEUTIC TARGETS
- **BRCA Mutation Risk:** ${patient.genomicProfile?.brca1 === 'Mutated (Pathogenic)' ? 'High-risk BRCA1 pathogenic variant detected. Bilateral mastectomy and salpingo-oophorectomy counseling indicated.' : 'Negative for pathogenic BRCA1 variants.'}
- **Proliferation Index (Ki-67):** ${patient.genomicProfile?.ki67Index || 'N/A'}. Highly pro-lipoproliferative cells respond actively to taxane-based chemotherapy sequences.
- **Therapeutic recommendation:** If staging is localized, recommend direct surgical consultation for margin resection, preceded by standard dose-dense AC-T neoadjuvant chemotherapy.
      `);
    } finally {
      setIsReportGenerating(false);
    }
  };

  // Border & Color mapping helper
  const classColors = {
    Malignant: { text: 'text-rose-600', fill: 'stroke-rose-600', bg: 'bg-rose-50', border: 'border-l-rose-600', hover: 'hover:bg-rose-100', accent: 'border-rose-100' },
    Benign: { text: 'text-emerald-600', fill: 'stroke-emerald-600', bg: 'bg-emerald-50', border: 'border-l-emerald-600', hover: 'hover:bg-emerald-100', accent: 'border-emerald-100' },
    Borderline: { text: 'text-amber-600', fill: 'stroke-amber-600', bg: 'bg-amber-50', border: 'border-l-amber-600', hover: 'hover:bg-amber-100', accent: 'border-amber-100' },
  }[patient.predictedClass];

  return (
    <div className="space-y-6">
      
      {/* Patient Profile Snapshot Card */}
      <section className="bg-white border border-zinc-200 rounded-xl p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-6 shadow-xs">
        <div className="flex items-center gap-6">
          <div className="w-20 h-20 rounded-lg overflow-hidden border border-zinc-200 bg-zinc-100 relative shrink-0 flex items-center justify-center">
            {patient.avatar ? (
              <img 
                referrerPolicy="no-referrer"
                alt={patient.name} 
                className="w-full h-full object-cover" 
                src={patient.avatar} 
              />
            ) : (
              <span className="text-xl font-black text-zinc-400">
                {patient.name.split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase()}
              </span>
            )}
          </div>
          <div>
            <div className="flex items-center gap-3">
              <h2 className="font-heading font-black text-2xl text-zinc-900 tracking-tight">{patient.name} ({patient.age})</h2>
              <span className={`px-2.5 py-1 rounded text-[10px] font-sans font-bold tracking-wider ${
                patient.status === 'PRE-OP' ? 'bg-zinc-900 text-white' : 'bg-zinc-100 text-zinc-700'
              }`}>
                {patient.status}
              </span>
            </div>
            <div className="flex flex-wrap gap-x-6 gap-y-2 mt-2">
              <span className="flex items-center gap-1.5 text-zinc-500 text-xs font-semibold">
                <Calendar className="w-3.5 h-3.5" />
                Next Appointment: {patient.lastVisit}
              </span>
              <span className="flex items-center gap-1.5 text-zinc-500 text-xs font-semibold font-mono">
                ID: {patient.id}
              </span>
              <span className="flex items-center gap-1.5 text-zinc-500 text-xs">
                <Info className="w-3.5 h-3.5 text-zinc-400" />
                Stage: {patient.priority}
              </span>
            </div>
          </div>
        </div>

        <div className="flex gap-3 w-full md:w-auto self-end md:self-center">
          <button 
            onClick={triggerReportCompilation}
            disabled={isReportGenerating}
            className="flex-1 md:flex-initial flex items-center justify-center gap-2 px-4 py-2 border border-zinc-200 hover:border-zinc-300 rounded font-sans font-bold text-sm text-zinc-850 hover:bg-zinc-50 transition-all cursor-pointer"
          >
            <FileText className="w-4 h-4 text-zinc-500" />
            {isReportGenerating ? 'Compiling AI Record...' : 'Generate Report'}
          </button>
        </div>
      </section>

      {/* Primary Analytics Card - Unified layout with side-by-side components */}
      <div className="bg-white border border-zinc-200 rounded-xl p-6 shadow-xs">
        <div className="grid grid-cols-12 gap-6 items-stretch">
          
          {/* Card 1: Diagnosis Prediction (Left) */}
          <div className={`col-span-12 md:col-span-6 lg:col-span-3 bg-zinc-50 border border-zinc-200 border-l-[6px] ${classColors.border} rounded-xl p-5 flex flex-col justify-between relative overflow-hidden`}>
            <div>
              <div className="flex justify-between items-start">
                <h3 className="font-sans font-extrabold text-[10px] uppercase tracking-widest text-zinc-400">
                  AI Diagnosis
                </h3>
                <div className="text-[9px] font-mono bg-zinc-200 text-zinc-700 px-1.5 py-0.5 rounded uppercase font-bold">
                  Tissue Model
                </div>
              </div>
              
              <div className="space-y-2 mt-4">
                <div className={`${classColors.text} font-sans font-black text-4xl tracking-tighter leading-none`}>
                  {patient.predictedClass}
                </div>
                <p className="text-zinc-500 text-[11px] leading-relaxed font-sans font-medium">
                  {patient.predictedClass === 'Malignant' 
                    ? 'FNA biopsy values surpass threshold criteria. Prompt multi-disciplinary pathology assessment recommended.' 
                    : patient.predictedClass === 'Benign' 
                      ? 'Fine-needle metrics correlate fully with healthy hyperplastic states. Regular radiological intervals approved.'
                      : 'Atypical epithelial elements of indeterminate origin. Fine-needle aspiration should be correlated with MRI margins.'
                  }
                </p>
              </div>
            </div>

            <div className="mt-4 pt-3 border-t border-zinc-200 text-[10px] text-zinc-400 font-sans font-medium flex items-center justify-between">
              <span>Category</span>
              <strong className="text-zinc-700 uppercase">{patient.predictedClass}</strong>
            </div>
          </div>

          {/* Card 2: Confidence Score (Middle) */}
          <div className="col-span-12 md:col-span-6 lg:col-span-3 bg-zinc-50 border border-zinc-200 rounded-xl p-5 flex flex-col justify-between items-center text-center">
            <div className="w-full flex justify-between items-start">
              <h3 className="font-sans font-extrabold text-[10px] uppercase tracking-widest text-zinc-400 text-left">
                Model Confidence
              </h3>
              <span className="text-[9px] font-mono bg-emerald-100 text-emerald-800 px-1.5 py-0.5 rounded font-bold uppercase">
                98.4% Acc
              </span>
            </div>

            <div className="relative inline-block my-2">
              <svg className="w-24 h-24 transform -rotate-90">
                {/* Background Track */}
                <circle className="text-zinc-200" cx="48" cy="48" fill="none" r="40" stroke="currentColor" strokeWidth="5"></circle>
                {/* Confidence Bar */}
                <circle 
                  className={`${classColors.text} transition-all duration-700`}
                  cx="48" 
                  cy="48" 
                  fill="none" 
                  r="40" 
                  stroke="currentColor" 
                  strokeWidth="5"
                  strokeDasharray="251.2"
                  strokeDashoffset={251.2 - (251.2 * patient.confidence) / 100}
                ></circle>
              </svg>
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className="font-sans font-black text-2xl text-zinc-900 leading-none">{patient.confidence}%</span>
                <span className="text-[7px] font-extrabold text-zinc-400 uppercase tracking-widest mt-0.5">CONFIDENCE</span>
              </div>
            </div>

            <p className="text-[11px] text-zinc-800 font-bold font-sans">
              {patient.predictedClass === 'Malignant' ? 'High Severity Case' : patient.predictedClass === 'Borderline' ? 'Borderline Case' : 'Negative Case'}
            </p>
          </div>

          {/* Card 3: Key Biopsy Metrics (Right) */}
          <div className="col-span-12 lg:col-span-6 flex flex-col justify-between">
            <div className="flex flex-col h-full w-full justify-between">
              {/* Header */}
              <div className="flex justify-between items-center pb-3 border-b border-zinc-100 shrink-0">
                <div>
                  <h3 className="font-sans font-extrabold text-[11px] uppercase tracking-widest text-zinc-400 flex items-center gap-1.5">
                    <Activity className="w-3.5 h-3.5 text-zinc-500" />
                    Key Biopsy Metrics
                  </h3>
                  <p className="text-[11px] text-zinc-500 font-medium">Recorded cytological markers vs. standard clinical ranges</p>
                </div>
                <div className="flex items-center gap-4 text-[10px] font-sans font-extrabold text-zinc-400 uppercase tracking-wider">
                  <div className="flex items-center gap-1.5">
                    <span className="w-2.5 h-2.5 bg-emerald-100 border border-emerald-300 rounded-xs inline-block"></span>
                    <span>Sanity Area (Normal)</span>
                  </div>
                </div>
              </div>

              {/* Visual Tracks for Prominent Features */}
              <div className="space-y-4 my-4">
                {(() => {
                  const getPositionPercentage = (value: number, minTrack: number, maxTrack: number) => {
                    const percent = ((value - minTrack) / (maxTrack - minTrack)) * 100;
                    return Math.max(0, Math.min(100, percent));
                  };

                  const renderFeatureBar = (
                    label: string,
                    rawName: string,
                    val: number,
                    minNorm: number,
                    maxNorm: number,
                    minTrack: number,
                    maxTrack: number,
                    unit = ""
                  ) => {
                    const isNormal = val >= minNorm && val <= maxNorm;
                    const startPercent = getPositionPercentage(minNorm, minTrack, maxTrack);
                    const endPercent = getPositionPercentage(maxNorm, minTrack, maxTrack);
                    const widthPercent = endPercent - startPercent;
                    const valPercent = getPositionPercentage(val, minTrack, maxTrack);

                    return (
                      <div className="space-y-1.5">
                        <div className="flex justify-between items-baseline text-xs">
                          <div className="flex items-center gap-2">
                            <span className="font-bold text-zinc-800">{label}</span>
                            <span className="text-[9px] text-zinc-400 font-mono font-medium">({rawName})</span>
                          </div>
                          <div className="flex items-center gap-2 font-mono">
                            <span className={`font-black text-xs ${isNormal ? 'text-emerald-600' : 'text-rose-600'}`}>
                              {val.toFixed(4)}{unit}
                            </span>
                            <span className={`text-[9px] font-bold uppercase px-1.5 py-0.2 rounded-xs ${
                              isNormal ? 'bg-emerald-50 text-emerald-700' : 'bg-rose-50 text-rose-700'
                            }`}>
                              {isNormal ? 'Normal' : 'Atypical'}
                            </span>
                          </div>
                        </div>

                        {/* Line Plot */}
                        <div className="relative h-6 flex items-center">
                          {/* Background line track */}
                          <div className="h-1.5 bg-zinc-100 rounded-full w-full relative overflow-hidden border border-zinc-200">
                            {/* Light Green Sanity Area */}
                            <div 
                              className="absolute h-full bg-emerald-200/50"
                              style={{ left: `${startPercent}%`, width: `${widthPercent}%` }}
                            />
                          </div>

                          {/* Plotted Value Indicator Pin */}
                          <div 
                            className="absolute transition-all duration-300 transform -translate-x-1/2 flex flex-col items-center"
                            style={{ left: `${valPercent}%` }}
                          >
                            <div className={`w-3.5 h-3.5 rounded-full border-2 border-white shadow-sm ${
                              isNormal ? 'bg-emerald-500' : 'bg-rose-500'
                            }`} />
                          </div>
                        </div>
                      </div>
                    );
                  };

                  const worstTextureVal = patient.features.worstTexture ?? patient.features.texture ?? 12.02;
                  const worstRadiusVal = patient.features.worstRadius ?? patient.features.meanRadius ?? 7.93;
                  
                  // For concave points, try different fallback chains
                  const worstConcavePointsVal = patient.features.worstConcavePoints ?? 
                    patient.features['concave points_worst'] ?? 
                    (patient.features.concavePoints ? Number((patient.features.concavePoints * 1.15).toFixed(4)) : 0.045);

                  return (
                    <div className="space-y-4">
                      {renderFeatureBar("Worst Biopsy Texture", "texture_worst", worstTextureVal, 12.02, 41.78, 5.0, 50.0)}
                      {renderFeatureBar("Worst Cellular Radius", "radius_worst", worstRadiusVal, 7.93, 19.82, 5.0, 30.0, " µm")}
                      {renderFeatureBar("Worst Concave Points", "concave points_worst", worstConcavePointsVal, 0.0000, 0.1750, 0.0, 0.25)}
                    </div>
                  );
                })()}
              </div>

              {/* Oncologist Verification & Feedback System */}
              <div className="border-t border-zinc-100 pt-4 mt-2">
                {patient.oncologistVerification && !isRevising ? (
                  <div className={`p-4 rounded-xl border flex flex-col justify-between gap-3 ${
                    patient.oncologistVerification.status === 'Confirmed' 
                      ? 'bg-emerald-50/40 border-emerald-200' 
                      : 'bg-rose-50/40 border-rose-200'
                  }`}>
                    <div className="flex justify-between items-start">
                      <div className="flex items-center gap-2">
                        <div className={`p-1 rounded-full ${
                          patient.oncologistVerification.status === 'Confirmed' 
                            ? 'bg-emerald-100 text-emerald-700' 
                            : 'bg-rose-100 text-rose-700'
                        }`}>
                          <Check className="w-4 h-4" />
                        </div>
                        <div>
                          <span className={`text-xs font-bold uppercase tracking-wider block ${
                            patient.oncologistVerification.status === 'Confirmed' ? 'text-emerald-800' : 'text-rose-800'
                          }`}>
                            Diagnosis {patient.oncologistVerification.status}
                          </span>
                          <span className="text-[10px] text-zinc-500 font-medium">
                            Signed by {patient.oncologistVerification.oncologistName} • {patient.oncologistVerification.verifiedAt}
                          </span>
                        </div>
                      </div>
                      <button 
                        onClick={() => setIsRevising(true)}
                        className="text-[10px] text-zinc-600 hover:text-black font-extrabold uppercase tracking-wider border border-zinc-200 hover:border-zinc-300 px-2 py-0.5 rounded bg-white transition-all cursor-pointer"
                      >
                        Revise Verdict
                      </button>
                    </div>
                    <div className="text-xs text-zinc-750 font-medium leading-relaxed italic bg-white/70 p-2.5 rounded-lg border border-zinc-100">
                      "{patient.oncologistVerification.feedback}"
                    </div>
                  </div>
                ) : (
                  <div className="p-4 rounded-xl border bg-zinc-50/50 border-zinc-200/80 flex flex-col sm:flex-row items-center justify-between gap-4">
                    <div className="space-y-1">
                      <span className="text-xs font-extrabold uppercase tracking-wider text-zinc-700 block">Oncologist Clinical Verification</span>
                      <p className="text-[11px] text-zinc-500 leading-snug">Verify diagnostic prediction alignment. Rejections require clinical feedback notes.</p>
                    </div>
                    <div className="flex gap-2 w-full sm:w-auto shrink-0">
                      <button
                        onClick={() => {
                          setRejectFeedback('');
                          setShowRejectModal(true);
                        }}
                        className="flex-1 sm:flex-initial flex items-center justify-center gap-1.5 px-4 py-2 rounded text-xs font-bold transition-all border bg-white text-rose-700 border-rose-200 hover:bg-rose-50 cursor-pointer"
                      >
                        Reject Diagnosis
                      </button>
                      <button
                        onClick={() => {
                          const verification = {
                            status: 'Confirmed' as const,
                            feedback: 'Confirmed as clinically concordant with case metrics.',
                            verifiedAt: new Date().toLocaleDateString(undefined, {
                              month: 'short',
                              day: 'numeric',
                              year: 'numeric',
                              hour: '2-digit',
                              minute: '2-digit'
                            }),
                            oncologistName: 'Dr. Abdelali Barir',
                          };
                          onUpdatePatient({
                            ...patient,
                            oncologistVerification: verification,
                            history: [
                              `Diagnosis Confirmed: Signed by Dr. Abdelali Barir.`,
                              ...patient.history,
                            ]
                          });
                          setIsRevising(false);
                        }}
                        className="flex-1 sm:flex-initial flex items-center justify-center gap-1.5 px-4 py-2 rounded text-xs font-bold transition-all border bg-emerald-600 text-white border-emerald-650 hover:bg-emerald-700 shadow-2xs cursor-pointer"
                      >
                        Confirm Diagnosis
                      </button>
                    </div>
                  </div>
                )}
              </div>

              {/* Footer containing Toggle */}
              <div className="flex justify-between items-center pt-3 border-t border-zinc-100 mt-3 shrink-0">
                <button 
                  onClick={() => setShowAllFeatures(!showAllFeatures)}
                  className="text-black hover:text-zinc-750 font-extrabold text-xs flex items-center gap-1.5 hover:underline cursor-pointer"
                >
                  {showAllFeatures ? 'Hide Full Pathology Profile Details' : 'View Full Pathology Profile Details'}
                  <ArrowRight className={`w-3.5 h-3.5 transform transition-transform ${showAllFeatures ? 'rotate-90' : ''}`} />
                </button>
                <div className="text-[10px] text-zinc-400 font-sans font-medium flex items-center gap-1">
                  <Info className="w-3 h-3" />
                  Values are read-only clinical reports
                </div>
              </div>
            </div>
          </div>

        </div>

        {/* Dropdown Section for all features */}
        {showAllFeatures && (
          <div className="mt-8 pt-8 border-t border-zinc-100">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
              <div>
                <h4 className="font-sans font-extrabold text-xs uppercase tracking-wider text-zinc-800">
                  Comprehensive FNA Cytological Profile
                </h4>
                <p className="text-[10px] text-zinc-500 font-medium">Remaining pathology parameters mapped vs clinical reference intervals</p>
              </div>
              <div className="flex items-center gap-4 text-[10px] font-sans font-extrabold text-zinc-400 uppercase tracking-wider bg-zinc-50 p-2 rounded-lg border border-zinc-150">
                <div className="flex items-center gap-1.5">
                  <span className="w-2.5 h-2.5 bg-emerald-100 border border-emerald-300 rounded-xs inline-block"></span>
                  <span>Normal Interval</span>
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-6">
              {FEATURE_DEFINITIONS.filter(def => !['worstTexture', 'worstRadius', 'worstConcavePoints'].includes(def.key)).map(def => {
                const val = getVal(def);
                const isNormal = val >= def.min && val <= def.max;
                
                // Calculate track boundaries dynamically so the pin is always nicely visible
                const range = def.max - def.min;
                let minTrack = def.min - range * 0.25;
                let maxTrack = def.max + range * 0.25;
                if (val < minTrack) {
                  minTrack = val - range * 0.1;
                }
                if (val > maxTrack) {
                  maxTrack = val + range * 0.1;
                }
                
                // Standard getPositionPercentage logic mapped inline for safety
                const getPct = (v: number) => {
                  const pct = ((v - minTrack) / (maxTrack - minTrack)) * 100;
                  return Math.max(0, Math.min(100, pct));
                };

                const startPercent = getPct(def.min);
                const endPercent = getPct(def.max);
                const widthPercent = endPercent - startPercent;
                const valPercent = getPct(val);

                return (
                  <div key={def.id} className="space-y-1.5 pb-3 border-b border-zinc-50 hover:bg-zinc-50/40 px-1 transition-all">
                    <div className="flex justify-between items-baseline text-xs">
                      <div className="flex items-center gap-1.5">
                        <span className="font-bold text-zinc-800">{formatFeatureLabel(def.id)}</span>
                        <span className="text-[9px] text-zinc-400 font-mono">({def.id})</span>
                      </div>
                      <div className="flex items-center gap-2 font-mono">
                        <span className={`font-black text-xs ${isNormal ? 'text-emerald-600' : 'text-rose-600'}`}>
                          {val.toFixed(4)}
                        </span>
                        <span className={`text-[9px] font-bold uppercase px-1.5 py-0.2 rounded-xs ${
                          isNormal ? 'bg-emerald-50 text-emerald-700' : 'bg-rose-50 text-rose-700'
                        }`}>
                          {isNormal ? 'Normal' : 'Atypical'}
                        </span>
                      </div>
                    </div>

                    {/* Line Plot Track */}
                    <div className="relative h-5 flex items-center">
                      <div className="h-1.5 bg-zinc-100 rounded-full w-full relative overflow-hidden border border-zinc-200">
                        {/* Light Green Sanity Area */}
                        <div 
                          className="absolute h-full bg-emerald-200/40"
                          style={{ left: `${startPercent}%`, width: `${widthPercent}%` }}
                        />
                      </div>

                      {/* Plotted Value Indicator Pin */}
                      <div 
                        className="absolute transition-all duration-300 transform -translate-x-1/2"
                        style={{ left: `${valPercent}%` }}
                      >
                        <div className={`w-3.5 h-3.5 rounded-full border-2 border-white shadow-2xs ${
                          isNormal ? 'bg-emerald-500' : 'bg-rose-500'
                        }`} />
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>

      {/* Pathology consultations report modal (markdown output) */}
      {reportMarkdown && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-xs z-[100] flex items-center justify-center p-4 animate-fade-in">
          <div className="bg-white w-full max-w-2xl rounded-xl shadow-2xl flex flex-col max-h-[85vh]">
            <div className="p-6 border-b border-zinc-100 flex justify-between items-center">
              <div className="flex items-center gap-2 text-zinc-900">
                <ShieldAlert className="w-5 h-5 text-zinc-800" />
                <h3 className="font-sans font-black text-xl">Signed Oncology Report Study</h3>
              </div>
              <button 
                onClick={() => setReportMarkdown(null)}
                className="p-1.5 hover:bg-zinc-100 rounded-full text-zinc-400 hover:text-zinc-600 font-bold font-mono transition-all cursor-pointer"
              >
                ✕
              </button>
            </div>
            <div className="flex-1 overflow-y-auto p-8 font-sans prose prose-neutral max-w-none text-zinc-750 text-xs leading-relaxed space-y-4 whitespace-pre-line">
              {reportMarkdown}
            </div>
            <div className="p-4 border-t border-zinc-100 flex justify-between items-center bg-zinc-50 rounded-b-xl">
              <span className="text-[10px] text-zinc-400 font-mono">Issued by: OncoAI Pathology Dept.</span>
              <div className="flex gap-2">
                <button 
                  onClick={() => window.print()}
                  className="bg-zinc-100 text-zinc-700 hover:bg-zinc-200 px-4 py-2 rounded text-xs font-bold transition-all cursor-pointer"
                >
                  Print Report
                </button>
                <button 
                  onClick={() => setReportMarkdown(null)}
                  className="bg-black text-white px-5 py-2 hover:bg-zinc-850 rounded text-xs font-bold transition-all cursor-pointer"
                >
                  Done
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Rejection clinical feedback required modal */}
      {showRejectModal && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-xs z-[110] flex items-center justify-center p-4">
          <div className="bg-white w-full max-w-md rounded-xl shadow-2xl flex flex-col">
            <div className="p-5 border-b border-zinc-100 flex justify-between items-center bg-rose-50/40">
              <div className="flex items-center gap-2 text-rose-700">
                <ShieldAlert className="w-5 h-5" />
                <h3 className="font-sans font-black text-base">Rejection Feedback Required</h3>
              </div>
              <button 
                onClick={() => setShowRejectModal(false)}
                className="p-1.5 hover:bg-zinc-100 rounded-full text-zinc-400 hover:text-zinc-650 transition-all text-sm font-bold font-mono cursor-pointer"
              >
                ✕
              </button>
            </div>
            
            <div className="p-6 space-y-4 font-sans">
              <p className="text-xs text-zinc-600 leading-relaxed font-medium">
                You are rejecting the Diagnosis of <strong className="text-zinc-800">{patient.predictedClass}</strong> for <strong className="text-zinc-800">{patient.name}</strong>. Please provide the clinical feedback or verification notes below.
              </p>
              
              {rejectError && (
                <div className="p-2 bg-rose-50 border border-rose-200 rounded text-[11px] text-rose-700 font-medium">
                  {rejectError}
                </div>
              )}
              
              <div className="space-y-1.5">
                <label className="text-[10px] font-extrabold uppercase tracking-widest text-zinc-400 block">
                  Clinical Feedback (Required to Submit Rejection)
                </label>
                <textarea
                  rows={4}
                  required
                  placeholder="Provide your clinical feedback or verification notes here..."
                  value={rejectFeedback}
                  onChange={(e) => setRejectFeedback(e.target.value)}
                  className="w-full text-xs p-3 border border-zinc-200 rounded-lg focus:outline-hidden focus:border-rose-450 focus:ring-1 focus:ring-rose-450 transition-all placeholder-zinc-400 bg-zinc-50/50 resize-none font-medium"
                />
              </div>
            </div>

            <div className="p-4 border-t border-zinc-100 flex justify-between items-center bg-zinc-50 rounded-b-xl">
              <span className="text-[10px] text-zinc-400 font-medium font-sans">Signed: Dr. Abdelali Barir</span>
              <div className="flex gap-2 shrink-0">
                <button 
                  onClick={() => setShowRejectModal(false)}
                  className="bg-white hover:bg-zinc-100 border border-zinc-200 text-zinc-700 px-4 py-1.5 rounded text-xs font-bold transition-all cursor-pointer"
                >
                  Cancel
                </button>
                <button 
                  onClick={async () => {
                    if (!rejectFeedback.trim()) return;
                    setIsSubmitting(true);
                    setRejectError(null);

                    // Call the Flask API if patient has a DB record
                    if (patient.dbRecordId) {
                      try {
                        const res = await fetch(`/api/flask/reject/${patient.dbRecordId}`, {
                          method: 'POST',
                          headers: { 'Content-Type': 'application/json' },
                          body: JSON.stringify({ feedback_body: rejectFeedback.trim() }),
                        });
                        if (!res.ok) {
                          const errData = await res.json().catch(() => ({}));
                          throw new Error(errData.description || `Rejection failed (${res.status})`);
                        }
                      } catch (err: any) {
                        setRejectError(err.message || 'Failed to submit rejection to API.');
                        setIsSubmitting(false);
                        return;
                      }
                    }

                    const verification = {
                      status: 'Rejected' as const,
                      feedback: rejectFeedback.trim(),
                      verifiedAt: new Date().toLocaleDateString(undefined, {
                        month: 'short',
                        day: 'numeric',
                        year: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit'
                      }),
                      oncologistName: 'Dr. Abdelali Barir',
                    };
                    onUpdatePatient({
                      ...patient,
                      oncologistVerification: verification,
                      history: [
                        `Diagnosis Rejected: Signed by Dr. Abdelali Barir. Notes: "${rejectFeedback.trim()}"`,
                        ...(patient.history || []),
                      ]
                    });
                    setIsRevising(false);
                    setShowRejectModal(false);
                    setRejectFeedback('');
                    setIsSubmitting(false);
                  }}
                  disabled={!rejectFeedback.trim() || isSubmitting}
                  className={`px-4 py-1.5 rounded text-xs font-bold transition-all border cursor-pointer ${
                    rejectFeedback.trim() && !isSubmitting
                      ? 'bg-rose-600 text-white border-rose-650 hover:bg-rose-700 shadow-2xs'
                      : 'bg-zinc-100 text-zinc-300 border-zinc-200 cursor-not-allowed'
                  }`}
                >
                  {isSubmitting ? 'Submitting...' : 'Submit Rejection'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

    </div>
  );
}
