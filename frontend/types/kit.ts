/**
 * TypeScript interfaces for DevLift onboarding kit data structures.
 */

export interface KeyComponent {
  name: string;
  path: string;
  description: string;
}

export interface ComplexityHotspot {
  name: string;
  path: string;
  reason: string;
  tip: string;
}

export interface FirstTask {
  title: string;
  description: string;
  difficulty: 'easy' | 'medium' | 'hard';
}

export interface CommonPattern {
  pattern: string;
  description: string;
  example: string;
}

export interface SetupSummary {
  prerequisites: string[];
  install_steps: string[];
  run_command: string;
  test_command: string;
  notes: string;
}

export interface OnboardingKit {
  architecture_overview: string;
  key_components: KeyComponent[];
  complexity_hotspots: ComplexityHotspot[];
  suggested_first_tasks: FirstTask[];
  common_patterns: CommonPattern[];
  setup_summary: SetupSummary;
}

export interface ReadinessBreakdown {
  label: string;
  score: number;
  max: number;
  note: string;
}

export interface ReadinessScore {
  score: number;
  grade: string;
  verdict: string;
  color: 'green' | 'blue' | 'yellow' | 'red';
  breakdown: ReadinessBreakdown[];
}

export interface AnalyzeResponse {
  owner: string;
  repo: string;
  description: string;
  language: string;
  stars: number;
  forks: number;
  topics: string[];
  files_analyzed: number;
  kit: OnboardingKit;
  readiness: ReadinessScore;
}

export interface RepoSuggestion {
  owner: string;
  repo: string;
  full_name: string;
  description: string;
  stars: number;
  forks: number;
  language: string;
  url: string;
  why: string;
}

export interface RecommendResponse {
  suggestions: RepoSuggestion[];
}

// Made with Bob
