/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { Patient } from '../types';
import { ShieldCheck, ShieldAlert, Dna, Anchor, Award, Info, Activity } from 'lucide-react';

interface GenomicRecordPaneProps {
  patient: Patient;
}

export default function GenomicRecordPane({ patient }: GenomicRecordPaneProps) {
  const genomics = patient.genomicProfile;

  // Determine hereditary and targeted therapies based on patient metrics
  const therapeuticGuides = [
    {
      marker: 'BRCA1 / BRCA2 Mutation',
      status: genomics.brca1.includes('Mutated') || genomics.brca2.includes('Mutated'),
      desc: 'BRCA mutations undermine homologous recombination DNA repair.',
      therapy: 'Consider PARP Inhibitors (e.g., Olaparib, Talazoparib) or intensive surveillance.',
    },
    {
      marker: 'HER2 Expression',
      status: genomics.her2Status.includes('HER2+'),
      desc: 'Overexpression promotes cell growth signaling via EGFR pathways.',
      therapy: 'Indicated for anti-HER2 targeted monoclonal antibodies (e.g., Trastuzumab, Pertuzumab).',
    },
    {
      marker: 'Hormone Receptors (ER/PR)',
      status: genomics.estrogenReceptor.includes('Positive') || genomics.progesteroneReceptor.includes('Positive'),
      desc: 'Steroid binding triggers transcription of growth promoter genes.',
      therapy: 'Select selective estrogen receptor modulators (SERMs like Tamoxifen) or Aromatase Inhibitors.',
    }
  ];

  return (
    <div className="space-y-6">
      
      {/* Header Info */}
      <div className="bg-white border border-zinc-200 rounded-xl p-6 shadow-xs flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="w-10 h-10 rounded bg-zinc-950 flex items-center justify-center text-white shrink-0">
            <Dna className="w-5 h-5 text-white" />
          </div>
          <div>
            <h2 className="font-heading font-black text-xl text-zinc-900 tracking-tight">Molecular & Genomic Profiling</h2>
            <p className="text-zinc-500 text-xs">High-throughput DNA sequencing and immunohistopathological markers for {patient.name}</p>
          </div>
        </div>
        <div className="font-mono text-[10px] text-zinc-500 bg-zinc-100 border border-zinc-200 px-2.5 py-1 rounded">
          SEQUENCE RUN: NEXTSEQ-550
        </div>
      </div>

      <div className="grid grid-cols-12 gap-6">
        
        {/* Gene Alterations Grid (BRCA, TP53, HER2, receptors) */}
        <div className="col-span-12 lg:col-span-8 space-y-6">
          <div className="grid grid-cols-2 gap-4">
            
            {/* BRCA1 Card */}
            <div className="bg-white border border-zinc-200 p-5 rounded-xl flex items-start gap-4">
              <div className={`p-2 rounded ${genomics.brca1.includes('Mutated') ? 'bg-rose-50 text-rose-700' : 'bg-emerald-50 text-emerald-700'}`}>
                {genomics.brca1.includes('Mutated') ? <ShieldAlert className="w-5 h-5" /> : <ShieldCheck className="w-5 h-5" />}
              </div>
              <div className="space-y-1">
                <span className="text-[10px] uppercase font-bold tracking-widest text-zinc-400">Gene BRCA1</span>
                <h4 className="font-sans font-bold text-zinc-805 text-sm">{genomics.brca1}</h4>
                <p className="text-[11px] text-zinc-505 leading-relaxed">
                  {genomics.brca1.includes('Mutated') 
                    ? 'Pathogenic germline variant. Elevates lifetime breast carcinoma risk significantly.' 
                    : 'Unmutated. Standard wild-type genomic sequence.'
                  }
                </p>
              </div>
            </div>

            {/* BRCA2 Card */}
            <div className="bg-white border border-zinc-200 p-5 rounded-xl flex items-start gap-4">
              <div className={`p-2 rounded ${genomics.brca2.includes('Mutated') ? 'bg-rose-50 text-rose-700' : 'bg-emerald-50 text-emerald-700'}`}>
                {genomics.brca2.includes('Mutated') ? <ShieldAlert className="w-5 h-5" /> : <ShieldCheck className="w-5 h-5" />}
              </div>
              <div className="space-y-1">
                <span className="text-[10px] uppercase font-bold tracking-widest text-zinc-400">Gene BRCA2</span>
                <h4 className="font-sans font-bold text-zinc-805 text-sm">{genomics.brca2}</h4>
                <p className="text-[11px] text-zinc-505 leading-relaxed">
                  {genomics.brca2.includes('Mutated') 
                    ? 'Pathogenic variant present. Requires genetic counselling for family members.' 
                    : 'Unmutated. Standard wild-type genomic sequence.'
                  }
                </p>
              </div>
            </div>

            {/* HER2 Receptor Card */}
            <div className="bg-white border border-zinc-200 p-5 rounded-xl flex items-start gap-4">
              <div className={`p-2 rounded ${genomics.her2Status.includes('Overexpressed') ? 'bg-rose-50 text-rose-700' : 'bg-zinc-100 text-zinc-700'}`}>
                <Activity className="w-5 h-5" />
              </div>
              <div className="space-y-1">
                <span className="text-[10px] uppercase font-bold tracking-widest text-zinc-400">HER2 / neu Receptor</span>
                <h4 className="font-sans font-bold text-zinc-805 text-sm">{genomics.her2Status}</h4>
                <p className="text-[11px] text-zinc-505 leading-relaxed">
                  {genomics.her2Status.includes('Overexpressed') 
                    ? 'Amplified growth receptor drives rapid replication. Strongly matches Trastuzumab protocols.' 
                    : 'Normal receptor density.'
                  }
                </p>
              </div>
            </div>

            {/* TP53 Check Card */}
            <div className="bg-white border border-zinc-200 p-5 rounded-xl flex items-start gap-4">
              <div className={`p-2 rounded ${genomics.tp53MutationalStatus.includes('Mutated') ? 'bg-rose-50 text-rose-700' : 'bg-emerald-50 text-emerald-700'}`}>
                <Anchor className="w-5 h-5" />
              </div>
              <div className="space-y-1">
                <span className="text-[10px] uppercase font-bold tracking-widest text-zinc-400">Tumor Suppressor TP53</span>
                <h4 className="font-sans font-bold text-zinc-850 text-sm">{genomics.tp53MutationalStatus}</h4>
                <p className="text-[11px] text-zinc-505 leading-relaxed">
                  {genomics.tp53MutationalStatus.includes('Mutated') 
                    ? 'Loss of p53 surveillance prevents apoptosis of mutated cells.' 
                    : 'Stable. Active p53 cellular suicide surveillance triggers correctly.'
                  }
                </p>
              </div>
            </div>

          </div>

          {/* Table of Receptors Status (immuno-histochemistry) */}
          <div className="bg-white border border-zinc-200 rounded-xl p-6">
            <h3 className="text-xs font-extrabold text-zinc-400 uppercase tracking-widest mb-4">Receptor Expression Panel</h3>
            <div className="divide-y divide-zinc-100 text-xs">
              <div className="py-2.5 flex justify-between">
                <span className="text-zinc-600 font-medium">Estrogen Receptor (ER) Level</span>
                <span className="font-bold text-zinc-900">{genomics.estrogenReceptor}</span>
              </div>
              <div className="py-2.5 flex justify-between">
                <span className="text-zinc-600 font-medium">Progesterone Receptor (PR) Level</span>
                <span className="font-bold text-zinc-900">{genomics.progesteroneReceptor}</span>
              </div>
              <div className="py-2.5 flex justify-between">
                <span className="text-zinc-600 font-medium">Ki-67 Cellular Proliferation Index</span>
                <span className="font-bold text-rose-600">{genomics.ki67Index}</span>
              </div>
            </div>
          </div>

        </div>

        {/* Right Column: Targeted Molecular Therapy Matching */}
        <div className="col-span-12 lg:col-span-4 bg-zinc-900 text-zinc-100 rounded-xl p-6 flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 mb-6">
              <Award className="w-5 h-5 text-zinc-400" />
              <h3 className="font-sans font-black text-sm tracking-tight">Therapeutic Drug Matching</h3>
            </div>
            
            <p className="text-zinc-400 text-[11px] leading-relaxed mb-6">
              Genetic markers directly suggest highly precise molecular interventions. OncoAI automatically calculates match probabilities against standard clinical pathways.
            </p>

            <div className="space-y-4">
              {therapeuticGuides.map((guide, i) => (
                <div key={i} className="bg-zinc-800 p-4 rounded-lg border border-zinc-700/50 space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-xs font-extrabold text-zinc-350">{guide.marker}</span>
                    <span className={`text-[9px] font-sans font-bold px-1.5 py-0.5 rounded uppercase tracking-wider ${
                      guide.status ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20' : 'bg-zinc-700 text-zinc-400'
                    }`}>
                      {guide.status ? 'Matched' : 'Unmatched'}
                    </span>
                  </div>
                  <p className="text-[10px] text-zinc-400 leading-normal">{guide.desc}</p>
                  {guide.status && (
                    <div className="bg-zinc-950/40 p-2 border border-zinc-700/20 rounded text-[10px] text-zinc-100">
                      <span className="font-bold blocking">Indicated Therapy: </span>
                      {guide.therapy}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>

          <div className="border-t border-zinc-800 pt-4 mt-6 text-center text-zinc-500 text-[10px] flex items-center justify-center gap-1">
            <Info className="w-3.5 h-3.5" />
            AIG-IVD Diagnostic Software. For Oncology Use.
          </div>
        </div>

      </div>
    </div>
  );
}
