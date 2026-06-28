/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { Search, UserCheck, AlertTriangle, ChevronRight, Activity, Calendar, Filter } from 'lucide-react';
import { Patient } from '../types';

interface PatientSearchPaneProps {
  patients: Patient[];
  onSelectPatient: (patient: Patient) => void;
  activePatient: Patient | null;
  searchQuery: string;
}

export default function PatientSearchPane({ patients, onSelectPatient, activePatient, searchQuery }: PatientSearchPaneProps) {
  const [filterClass, setFilterClass] = useState<'All' | 'Malignant' | 'Benign' | 'Borderline'>('All');
  const [filterStatus, setFilterStatus] = useState<'All' | 'PRE-OP' | 'SURVEILLANCE' | 'CHEMO' | 'POST-OP'>('All');

  // Multi-criteria filter execution
  const filteredPatients = patients.filter(patient => {
    // 1. Full-text search on Name and ID range
    const matchesSearch = 
      patient.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      patient.id.toLowerCase().includes(searchQuery.toLowerCase());
    
    // 2. Pathology class filters
    const matchesClass = filterClass === 'All' || patient.predictedClass === filterClass;

    // 3. Cycle status filters
    const matchesStatus = filterStatus === 'All' || patient.status === filterStatus;

    return matchesSearch && matchesClass && matchesStatus;
  });

  return (
    <div className="space-y-6">
      
      {/* Search Filter Tools Bar */}
      <div className="bg-white border border-zinc-200 rounded-xl p-5 shadow-xs flex flex-wrap gap-4 items-center justify-between">
        <div className="flex items-center gap-2">
          <Filter className="w-4 h-4 text-zinc-500" />
          <span className="text-xs font-extrabold text-zinc-400 uppercase tracking-widest leading-none">Diagnostic File Triage Filters</span>
        </div>
        
        <div className="flex flex-wrap gap-3 text-xs font-semibold">
          {/* Class select */}
          <div className="flex items-center gap-1.5">
            <span className="text-zinc-500 font-sans">Diagnosis:</span>
            <select
              value={filterClass}
              onChange={(e) => setFilterClass(e.target.value as any)}
              className="bg-zinc-50 hover:bg-zinc-100 border border-zinc-200 rounded px-2 py-1 focus:ring-1 focus:ring-zinc-950 font-sans"
            >
              <option value="All">All Categories</option>
              <option value="Malignant">Malignant (Class V)</option>
              <option value="Benign">Benign (Class I)</option>
              <option value="Borderline">Borderline (Class III)</option>
            </select>
          </div>

          {/* Status select */}
          <div className="flex items-center gap-1.5">
            <span className="text-zinc-500 font-sans">Active Cycle:</span>
            <select
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value as any)}
              className="bg-zinc-50 hover:bg-zinc-100 border border-zinc-250 rounded px-2 py-1 focus:ring-1 focus:ring-zinc-950 font-sans"
            >
              <option value="All">All Cycles</option>
              <option value="PRE-OP">PRE-OP</option>
              <option value="POST-OP">POST-OP</option>
              <option value="CHEMO">CHEMOTHERAPY</option>
              <option value="SURVEILLANCE">SURVEILLANCE</option>
            </select>
          </div>
        </div>
      </div>

      {/* Patients spreadsheet/list */}
      <div className="bg-white border border-zinc-200 rounded-xl overflow-hidden shadow-xs">
        <div className="hidden sm:grid grid-cols-12 gap-4 px-6 py-4 bg-zinc-50 border-b border-zinc-200 text-xs font-extrabold text-zinc-400 uppercase tracking-widest">
          <div className="col-span-5">Patient Name</div>
          <div className="col-span-4">Diagnosis</div>
          <div className="col-span-3 text-right">Last Visit</div>
        </div>

        <div className="divide-y divide-zinc-150">
          {filteredPatients.map((patient) => {
            const isActive = activePatient ? activePatient.id === patient.id : false;
            const isMalignant = patient.predictedClass === 'Malignant';
            const isBorderline = patient.predictedClass === 'Borderline';

            return (
              <div
                key={patient.id}
                onClick={() => onSelectPatient(patient)}
                className={`grid grid-cols-1 sm:grid-cols-12 gap-2 sm:gap-4 px-6 py-4 items-center hover:bg-zinc-50 transition-all cursor-pointer ${
                  isActive ? 'bg-zinc-50/80 border-l-4 border-black pl-5' : ''
                }`}
              >
                <div className="col-span-5">
                  <h4 className="font-heading font-black text-sm text-zinc-900">{patient.name}</h4>
                </div>

                <div className="col-span-4">
                  <span className={`font-sans font-extrabold text-xs inline-flex items-center px-2.5 py-1 rounded-full ${
                    isMalignant 
                      ? 'text-rose-700 bg-rose-50' 
                      : isBorderline 
                        ? 'text-amber-700 bg-amber-50' 
                        : 'text-emerald-700 bg-emerald-50'
                  }`}>
                    {patient.predictedClass} ({patient.confidence}%)
                  </span>
                </div>

                <div className="col-span-3 text-left sm:text-right text-zinc-500 text-xs font-semibold font-sans">
                  {patient.lastVisit}
                </div>
              </div>
            );
          })}
        </div>

        {filteredPatients.length === 0 && (
          <div className="bg-zinc-50 border-t border-zinc-200 p-10 text-center text-zinc-500 font-sans">
            No patient records matched the selected filters or search parameters.
          </div>
        )}
      </div>

    </div>
  );
}
