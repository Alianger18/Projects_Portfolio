/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { Search, Bell, Share2, Printer, Menu } from 'lucide-react';
import { Patient } from '../types';

interface HeaderProps {
  currentPatient: Patient | null;
  searchQuery: string;
  setSearchQuery: (query: string) => void;
  onPrint: () => void;
  onToggleSidebar: () => void;
}

export default function Header({ currentPatient, searchQuery, setSearchQuery, onPrint, onToggleSidebar }: HeaderProps) {
  const isEmergency = currentPatient ? currentPatient.predictedClass === 'Malignant' && currentPatient.confidence >= 90 : false;

  return (
    <header className="h-20 flex justify-between items-center px-6 border-b border-zinc-200 bg-white shrink-0 z-30 shadow-xs">
      <div className="flex items-center gap-6 flex-1">
        {/* Toggle Button / 3 Lines */}
        <button 
          onClick={onToggleSidebar}
          className="p-2 hover:bg-zinc-100 rounded-lg transition-all text-zinc-900 cursor-pointer focus:outline-none flex items-center justify-center shrink-0 border border-zinc-200"
          title="Toggle Navigation Menu"
        >
          <Menu className="w-5 h-5 text-zinc-900" />
        </button>

        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded bg-black flex items-center justify-center text-white font-black text-lg tracking-wider">
            Ω
          </div>
          <span className="font-sans font-black text-2xl tracking-tighter text-zinc-900">
            OncoAI
          </span>
        </div>
        
        <div className="relative group max-w-md w-full">
          <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 text-zinc-400 w-4 h-4" />
          <input
            className="w-full bg-zinc-50 border border-zinc-200 hover:border-zinc-300 rounded-full pl-10 pr-4 py-2 focus:outline-none focus:ring-1 focus:ring-zinc-900 focus:border-zinc-900 text-sm transition-all"
            placeholder="Global Patient Search (Name, Gender, ID...)"
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
      </div>

      <div className="flex items-center gap-6">
        <div className="flex items-center gap-2.5 text-zinc-600 pl-6">
          <button className="p-2 hover:bg-zinc-100 rounded-full transition-all relative" title="Notifications">
            <Bell className="w-5 h-5 text-zinc-600" />
            {isEmergency && <span className="absolute top-1 right-1 w-2.5 h-2.5 bg-rose-600 border-2 border-white rounded-full"></span>}
          </button>
          <button className="p-2 hover:bg-zinc-100 rounded-full transition-all text-zinc-600" title="Share Case File">
            <Share2 className="w-5 h-5" />
          </button>
          <button 
            onClick={onPrint} 
            className="p-2 hover:bg-zinc-100 rounded-full transition-all text-zinc-600" 
            title="Download PDF/Print Case File"
          >
            <Printer className="w-5 h-5" />
          </button>
        </div>
      </div>
    </header>
  );
}
