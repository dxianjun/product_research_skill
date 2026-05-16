export type SourceConfidence = "fact" | "assumption";

export interface Finding {
  statement: string;
  confidence: SourceConfidence;
}

export interface ResearchInput {
  productQuestion: string;
  marketScope: string[];
  userScope: string[];
  competitorScope: string[];
  constraints: string[];
  findings: Finding[];
  options: Array<{
    name: string;
    pros: string[];
    cons: string[];
  }>;
  recommendation: string;
  risks: string[];
  nextExperiments: string[];
}
