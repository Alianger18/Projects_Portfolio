/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

export interface LabFeatures {
  meanRadius: number; // in µm
  perimeter: number;  // in mm
  concavity: number;  // 0 to 1 scale
  symmetry: number;   // 0 to 1 scale
  texture: number;    // scale typical 1 to 30
  meanArea?: number;
  smoothness?: number;
  compactness?: number;
  concavePoints?: number;
  fractalDimension?: number;
  radiusSE?: number;
  textureSE?: number;
  perimeterSE?: number;
  areaSE?: number;
  smoothnessSE?: number;
  compactnessSE?: number;
  concavitySE?: number;
  concavePointsSE?: number;
  symmetrySE?: number;
  fractalDimSE?: number;
  worstRadius?: number;
  worstTexture?: number;
  worstPerimeter?: number;
  worstArea?: number;
  [key: string]: number | undefined;
}

export interface GenomicProfile {
  brca1: 'Mutated (Pathogenic)' | 'Wild Type' | 'VUS (Uncertain Signif.)';
  brca2: 'Mutated (Pathogenic)' | 'Wild Type' | 'VUS (Uncertain Signif.)';
  her2Status: 'HER2+ (Overexpressed)' | 'HER2- (Negative)' | 'HER2-Low';
  estrogenReceptor: 'Positive (95%)' | 'Negative' | 'Weakly Positive';
  progesteroneReceptor: 'Positive (80%)' | 'Negative' | 'Weakly Positive';
  tp53MutationalStatus: 'Mutated (Exon 6)' | 'Stable (Wild Type)';
  ki67Index: string; // e.g. "35% (High Proliferation)"
}

export interface LongitudinalPoint {
  month: string;
  tumorSizeMm: number;    // tumor diameter in mm
  ca15_3Marker: number;  // cancer antigen 15-3 (U/mL)
}

export interface Patient {
  id: string;
  dbRecordId?: number;    // Flask Record.id (integer PK)
  patientId?: string;     // Flask Record.patient_id (custom string ID)
  name: string;
  age: number;
  status?: 'PRE-OP' | 'POST-OP' | 'ADJUVANT' | 'SURVEILLANCE' | 'CHEMO';
  avatar?: string;
  lastVisit?: string;
  predictedClass: 'Malignant' | 'Benign' | 'Borderline';
  confidence: number;
  priority?: 'High Priority' | 'Routine' | 'Observation';
  features: LabFeatures;
  genomicProfile?: GenomicProfile;
  history?: string[];
  longitudinalData?: LongitudinalPoint[];
  oncologistVerification?: {
    status: 'Confirmed' | 'Rejected';
    feedback: string;
    verifiedAt: string;
    oncologistName: string;
  };
}

export interface ChatMessage {
  id: string;
  sender: 'doctor' | 'ai';
  text: string;
  timestamp: string;
}
