/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export type DiagnosisLabel = 'Malignant' | 'Benign';
export type SeverityLevel = 'High Risk' | 'Low Risk';

export interface DiagnosisResultCardProps {
  /** The predicted class – "Malignant" or "Benign". */
  diagnosis: DiagnosisLabel;
  /** Clinical context text displayed below the diagnosis. */
  description: string;
  /** Model confidence for this prediction (0–100). */
  confidenceScore: number;
  /** Risk severity tag shown in the footer. */
  severity: SeverityLevel;
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/**
 * Half-circle arc geometry.
 * r = 54, half-circumference = π × r ≈ 169.646
 */
const HALF_R = 54;
const HALF_CIRCUMFERENCE = Math.PI * HALF_R; // ≈ 169.646

/** Compute the SVG dash offset for a half-circle gauge (0–100 maps to full arc). */
function computeHalfDashOffset(score: number): number {
  const clamped = Math.min(100, Math.max(0, score));
  return HALF_CIRCUMFERENCE - (HALF_CIRCUMFERENCE * (clamped / 100));
}

/**
 * Pick the colour palette based on diagnosis + confidence score.
 *   • Borderline confidence (35–65%) → amber/orange
 *   • Malignant / High Risk          → rose
 *   • Benign / Low Risk              → emerald
 */
function getColorTokens(diagnosis: DiagnosisLabel, confidence: number) {
  const isBorderline = confidence >= 35 && confidence <= 65;

  if (isBorderline) {
    return {
      primary: 'text-amber-500',
      stroke: 'text-amber-500',
      severityText: 'text-amber-600',
    };
  }

  const isPositive = diagnosis === 'Malignant';
  return {
    primary: isPositive ? 'text-rose-600' : 'text-emerald-600',
    stroke: isPositive ? 'text-rose-600' : 'text-emerald-600',
    severityText: isPositive ? 'text-rose-600' : 'text-emerald-600',
  };
}

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

const DiagnosisResultCard: React.FC<DiagnosisResultCardProps> = ({
  diagnosis,
  description,
  confidenceScore,
  severity,
}) => {
  const colors = getColorTokens(diagnosis, confidenceScore);
  const halfDashOffset = computeHalfDashOffset(confidenceScore);

  // SVG viewBox is 120 wide × 70 tall (half-circle sits in top portion)
  const svgWidth = 120;
  const svgHeight = 70;
  const cx = svgWidth / 2;  // 60
  const cy = 62;             // push centre down so arc opens upward

  return (
    <div className="w-full h-full bg-white border border-zinc-200 rounded-2xl shadow-sm p-6 font-sans flex flex-col justify-between">

      {/* ── Top: Header + Diagnosis ──────────────────────────────────── */}
      <div>
        {/* Minimal header */}
        <h3 className="font-extrabold text-[10px] uppercase tracking-widest text-zinc-400 mb-4">
          AI Diagnosis
        </h3>

        {/* Diagnosis label */}
        <div
          className={`${colors.primary} font-black text-4xl tracking-tighter leading-none`}
        >
          {diagnosis}
        </div>

        {/* Clinical context */}
        <p className="text-zinc-500 text-[11px] leading-relaxed font-medium mt-2">
          {description}
        </p>
      </div>

      {/* ── Middle: Half-circle confidence gauge ─────────────────────── */}
      <div className="flex flex-col items-center justify-center mt-6">
        <div className="relative" style={{ width: svgWidth, height: svgHeight }}>
          <svg
            width={svgWidth}
            height={svgHeight}
            viewBox={`0 0 ${svgWidth} ${svgHeight}`}
            className="overflow-visible"
          >
            {/* Background half-arc (180° from left to right) */}
            <path
              d={`M ${cx - HALF_R} ${cy} A ${HALF_R} ${HALF_R} 0 0 1 ${cx + HALF_R} ${cy}`}
              fill="none"
              stroke="currentColor"
              strokeWidth="7"
              strokeLinecap="round"
              className="text-zinc-100"
            />
            {/* Foreground half-arc – driven by confidenceScore */}
            <path
              d={`M ${cx - HALF_R} ${cy} A ${HALF_R} ${HALF_R} 0 0 1 ${cx + HALF_R} ${cy}`}
              fill="none"
              stroke="currentColor"
              strokeWidth="7"
              strokeLinecap="round"
              strokeDasharray={HALF_CIRCUMFERENCE}
              strokeDashoffset={halfDashOffset}
              className={`${colors.stroke} transition-all duration-700`}
            />
          </svg>
        </div>

        {/* Confidence score underneath the arc */}
        <div className="flex flex-col items-center -mt-4">
          <span className="font-black text-3xl text-zinc-900 leading-none">
            {confidenceScore.toFixed(2)}%
          </span>
          <span className="text-[8px] font-extrabold text-zinc-400 uppercase tracking-widest mt-1">
            Confidence
          </span>
        </div>
      </div>

      {/* ── Footer: Severity only ────────────────────────────────────── */}
      <div className="pt-4 mt-6 border-t border-zinc-100 text-[10px] text-zinc-400 font-medium flex items-center justify-between">
        <span>Severity:</span>
        <strong className={`${colors.severityText} uppercase`}>
          {severity}
        </strong>
      </div>
    </div>
  );
};

export default DiagnosisResultCard;
