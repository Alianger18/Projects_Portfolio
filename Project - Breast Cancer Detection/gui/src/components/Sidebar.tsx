/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { Users, Activity, Dna, LineChart, Settings, Plus } from 'lucide-react';

type SideTab = 'patient-search' | 'diagnostic-queue' | 'settings';

interface SidebarProps {
  currentTab: SideTab;
  setCurrentTab: (tab: SideTab) => void;
  isOpen: boolean;
}

export default function Sidebar({ currentTab, setCurrentTab, isOpen }: SidebarProps) {
  const doctorAvatar = "https://lh3.googleusercontent.com/aida-public/AB6AXuD-GGkUD8S6wBAF-qrZzDpsl9_uRDsPkmiB0yOIk1brEG_taiOt_aKiz5glVmfcMJAhN2KeD_ISChDYacjmKu2FS6odOixEA7dPs8K-wbclliEO9Fq--G4EyGqT5hScoZ9hYFdsbORRepQfTSggs9XjftNdJtrf9hlfVjwZoFX6PcAJdV5Wv6gMdPABQ8KJ9eqLTaJhdUwtKwoJu3-H83VKoPxRCLgKaHdb-c3fRpir5Ac6Adma8azy7OiZGi8gBGq5LopCBOLgdBE";

  const navigationItems = [
    {
      id: 'patient-search' as SideTab,
      label: 'Patients',
      icon: Users,
    },
    {
      id: 'diagnostic-queue' as SideTab,
      label: 'Diagnostic Queue',
      icon: Activity,
    },
    {
      id: 'settings' as SideTab,
      label: 'Settings',
      icon: Settings,
    }
  ];

  return (
    <aside className={`fixed top-0 bottom-0 left-0 h-screen w-72 flex flex-col shrink-0 bg-white border-r border-zinc-200 py-6 z-50 transition-transform duration-300 ${isOpen ? 'translate-x-0' : '-translate-x-full'}`}>
      {/* Oncologist Header Block */}
      <div className="px-6 mb-8">
        <div className="text-[10px] font-sans font-black tracking-widest text-zinc-400 uppercase mb-3">
          CURRENT ONCOLOGIST
        </div>
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-full overflow-hidden bg-zinc-100 border border-zinc-200">
            <img 
              referrerPolicy="no-referrer"
              className="w-full h-full object-cover" 
              alt="Dr. Richardson" 
              src={doctorAvatar} 
            />
          </div>
          <div>
            <h3 className="font-sans font-bold text-zinc-900 leading-tight">Dr. Richardson</h3>
            <p className="text-xs text-zinc-500 font-medium font-sans">Oncology Dept.</p>
          </div>
        </div>
      </div>

      {/* Navigation Items */}
      <nav className="flex-1 space-y-1">
        {navigationItems.map((item) => {
          const Icon = item.icon;
          const isActive = currentTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setCurrentTab(item.id)}
              className={`w-full flex items-center gap-4 px-6 py-3.5 transition-all text-left ${
                isActive
                  ? 'text-zinc-950 font-bold border-l-4 border-black bg-zinc-50'
                  : 'text-zinc-500 hover:text-zinc-900 hover:bg-zinc-50'
              }`}
            >
              <Icon className={`w-5 h-5 ${isActive ? 'text-zinc-950' : 'text-zinc-400'}`} />
              <span className="font-sans font-semibold text-sm transition-colors">{item.label}</span>
            </button>
          );
        })}
      </nav>
    </aside>
  );
}
