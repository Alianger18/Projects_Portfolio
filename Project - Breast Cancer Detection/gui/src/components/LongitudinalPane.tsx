/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { Patient, LongitudinalPoint } from '../types';
import { TrendingDown, Calendar, Database, Target, TrendingUp, Info } from 'lucide-react';

interface LongitudinalPaneProps {
  patient: Patient;
}

export default function LongitudinalPane({ patient }: LongitudinalPaneProps) {
  const data = patient.longitudinalData;
  const [hoveredPointIndex, setHoveredPointIndex] = useState<number | null>(null);

  if (!data || data.length === 0) {
    return (
      <div className="bg-white border border-zinc-200 rounded-xl p-8 text-center text-zinc-500 font-sans">
        No longitudinal data points registered for this patient mass.
      </div>
    );
  }

  // Calculate coordinates for custom SVG charting
  // Dimension coordinates bounds
  const width = 580;
  const height = 180;
  const paddingLeft = 40;
  const paddingRight = 20;
  const paddingTop = 20;
  const paddingBottom = 40;

  const chartWidth = width - paddingLeft - paddingRight;
  const chartHeight = height - paddingTop - paddingBottom;

  // Find max values for y-scale mapping
  const maxTumorSize = Math.max(...data.map(p => p.tumorSizeMm), 10);
  const maxMarker = Math.max(...data.map(p => p.ca15_3Marker), 20);

  // Map data to x, y coordinates
  const points = data.map((d, index) => {
    // distribute evenly along x-axis
    const x = paddingLeft + (index / (data.length - 1)) * chartWidth;
    // Map tumor size to y
    const yTumor = height - paddingBottom - (d.tumorSizeMm / maxTumorSize) * chartHeight;
    // Map antigen marker to y (scaled differently)
    const yMarker = height - paddingBottom - (d.ca15_3Marker / maxMarker) * chartHeight;

    return { x, yTumor, yMarker, ...d };
  });

  // Build SVG path strings
  const tumorPath = points.length > 0 
    ? `M ${points[0].x} ${points[0].yTumor} ` + points.slice(1).map(p => `L ${p.x} ${p.yTumor}`).join(' ')
    : '';

  const markerPath = points.length > 0 
    ? `M ${points[0].x} ${points[0].yMarker} ` + points.slice(1).map(p => `L ${p.x} ${p.yMarker}`).join(' ')
    : '';

  return (
    <div className="space-y-6">
      
      {/* Intro strip */}
      <div className="bg-white border border-zinc-200 rounded-xl p-6 shadow-xs flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="w-10 h-10 rounded bg-zinc-950 flex items-center justify-center text-white shrink-0">
            <TrendingDown className="w-5 h-5 text-white" />
          </div>
          <div>
            <h2 className="font-heading font-black text-xl text-zinc-900 tracking-tight">Longitudinal Regression Indices</h2>
            <p className="text-zinc-500 text-xs">Tracking tumor shrinkage indices and hematological CA 15-3 antigens against cancer treatment timelines</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Calendar className="w-4 h-4 text-zinc-400" />
          <span className="text-zinc-700 text-xs font-semibold font-sans">Interval: 6-Month Cycle</span>
        </div>
      </div>

      <div className="grid grid-cols-12 gap-6">

        {/* Vector SVG Multi-axis line plot card */}
        <div className="col-span-12 lg:col-span-8 bg-white border border-zinc-200 rounded-xl p-6 shadow-xs flex flex-col justify-between">
          <div>
            <div className="flex justify-between items-center mb-6">
              <h3 className="font-sans font-extrabold text-[11px] uppercase tracking-widest text-zinc-400">Response Trend Analysis</h3>
              
              <div className="flex items-center gap-4 text-xs font-semibold font-sans">
                <div className="flex items-center gap-1.5">
                  <span className="w-3 h-0.5 bg-black inline-block"></span>
                  <span className="text-zinc-700 text-[11px]">Tumor Diameter (mm)</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <span className="w-3 h-0.5 bg-rose-500 inline-block"></span>
                  <span className="text-zinc-700 text-[11px]">CA 15-3 Antigen (U/mL)</span>
                </div>
              </div>
            </div>

            {/* Rendered Graph */}
            <div className="relative w-full overflow-hidden select-none">
              <svg className="w-full h-auto" viewBox={`0 0 ${width} ${height}`}>
                
                {/* Horizontal Baseline Grids */}
                {[0, 0.25, 0.5, 0.75, 1].map((ratio, i) => {
                  const y = paddingTop + ratio * chartHeight;
                  return (
                    <line 
                      key={i} 
                      x1={paddingLeft} 
                      y1={y} 
                      x2={width - paddingRight} 
                      y2={y} 
                      stroke="#f1f5f9" 
                      strokeWidth="1"
                    />
                  );
                })}

                {/* Y-Axis Label (Left) */}
                <text x={paddingLeft - 8} y={paddingTop + 4} textAnchor="end" className="fill-zinc-400 text-[9px] font-sans font-bold">
                  {maxTumorSize}mm
                </text>
                <text x={paddingLeft - 8} y={height - paddingBottom + 4} textAnchor="end" className="fill-zinc-400 text-[9px] font-sans font-bold">
                  0mm
                </text>

                {/* Tumor Diameter Regression Line */}
                <path 
                  d={tumorPath} 
                  fill="none" 
                  stroke="#09090b" 
                  strokeWidth="2.5" 
                  strokeLinecap="round" 
                  strokeLinejoin="round"
                />

                {/* CA15-3 Antigen Line */}
                <path 
                  d={markerPath} 
                  fill="none" 
                  stroke="#e11d48" 
                  strokeWidth="2" 
                  strokeDasharray="4 2"
                  strokeLinecap="round" 
                  strokeLinejoin="round"
                />

                {/* Coordinate Markers & Interactive Hover Rings */}
                {points.map((p, index) => (
                  <g key={index}>
                    {/* Tick line */}
                    <line 
                      x1={p.x} 
                      y1={paddingTop} 
                      x2={p.x} 
                      y2={height - paddingBottom} 
                      stroke={hoveredPointIndex === index ? '#e2e8f0' : '#f8fafc'} 
                      strokeWidth="1"
                    />

                    {/* Tumor Dot */}
                    <circle 
                      cx={p.x} 
                      cy={p.yTumor} 
                      r={hoveredPointIndex === index ? 6 : 4} 
                      fill="#000" 
                      className="cursor-pointer transition-all duration-150"
                      onMouseEnter={() => setHoveredPointIndex(index)}
                      onMouseLeave={() => setHoveredPointIndex(null)}
                    />

                    {/* Antigen Dot */}
                    <circle 
                      cx={p.x} 
                      cy={p.yMarker} 
                      r={hoveredPointIndex === index ? 5 : 3.5} 
                      fill="#e11d48" 
                      className="cursor-pointer transition-all duration-150"
                      onMouseEnter={() => setHoveredPointIndex(index)}
                      onMouseLeave={() => setHoveredPointIndex(null)}
                    />

                    {/* Month Label */}
                    <text 
                      x={p.x} 
                      y={height - paddingBottom + 18} 
                      textAnchor="middle" 
                      className="fill-zinc-500 text-[10px] font-sans font-bold"
                    >
                      {p.month}
                    </text>
                  </g>
                ))}
              </svg>
            </div>
          </div>

          {/* Interactive Legend Floating read-out */}
          <div className="bg-zinc-50 p-4 border border-zinc-100 rounded-lg flex items-center justify-between text-xs mt-4">
            <span className="text-zinc-500 font-sans flex items-center gap-1">
              <Database className="w-3.5 h-3.5" />
              {hoveredPointIndex !== null 
                ? `Readings for ${data[hoveredPointIndex].month}:` 
                : 'Hover points to read exact metrics.'
              }
            </span>
            {hoveredPointIndex !== null ? (
              <div className="flex gap-6 font-mono font-bold text-zinc-900">
                <span className="text-black">Diameter: {data[hoveredPointIndex].tumorSizeMm} mm</span>
                <span className="text-rose-600">CA 15-3: {data[hoveredPointIndex].ca15_3Marker} U/mL</span>
              </div>
            ) : (
              <span className="font-serif italic text-zinc-400 text-xs">Hover data dots</span>
            )}
          </div>
        </div>

        {/* Left Column: Response evaluation details */}
        <div className="col-span-12 lg:col-span-4 bg-white border border-zinc-200 rounded-xl p-6 shadow-xs flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 mb-4">
              <Target className="w-5 h-5 text-zinc-800" />
              <h3 className="font-sans font-extrabold text-[11px] uppercase tracking-widest text-zinc-400">Therapeutic Benchmarks</h3>
            </div>

            <div className="space-y-4">
              
              <div className="border border-zinc-100 p-4 rounded-lg bg-zinc-50 space-y-1.5">
                <div className="flex justify-between items-center">
                  <span className="text-xs font-extrabold text-zinc-900 font-sans">Tumor Mass Regression</span>
                  <TrendingDown className="w-4 h-4 text-emerald-600" />
                </div>
                <div className="text-2xl font-sans font-black text-zinc-900">
                  {points[0].tumorSizeMm > points[points.length - 1].tumorSizeMm 
                    ? `-${Math.round(((points[0].tumorSizeMm - points[points.length - 1].tumorSizeMm) / points[0].tumorSizeMm) * 100)}%` 
                    : `+${Math.round(((points[points.length - 1].tumorSizeMm - points[0].tumorSizeMm) / points[0].tumorSizeMm) * 105)}%`
                  }
                </div>
                <p className="text-[10px] text-zinc-500 leading-normal">Percentage shrink in diameter dimensions from cycle onset.</p>
              </div>

              <div className="border border-zinc-100 p-4 rounded-lg bg-zinc-50 space-y-1.5">
                <div className="flex justify-between items-center">
                  <span className="text-xs font-extrabold text-zinc-900 font-sans">Mitotic Marker Baseline</span>
                  <TrendingUp className="w-4 h-4 text-zinc-400" />
                </div>
                <div className="text-2xl font-sans font-black text-zinc-900">
                  {data[data.length - 1].ca15_3Marker} <span className="text-xs text-zinc-400">U/mL</span>
                </div>
                <p className="text-[10px] text-zinc-500 leading-normal">Most recent cancer antigen index. Antigens typically trail behind tumor mass regressions.</p>
              </div>

            </div>
          </div>

          <div className="border-t border-zinc-150 pt-4 mt-6 text-zinc-400 text-[10px] flex items-center justify-center gap-1">
            <Info className="w-3.5 h-3.5" />
            Recalculated daily against drug administration logs.
          </div>
        </div>

      </div>
    </div>
  );
}
