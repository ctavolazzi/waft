/**
 * Decision Engine API Client
 * 
 * The Bridge between frontend and the Decision Engine API.
 * Works with React, SvelteKit, or any TypeScript/JavaScript frontend.
 */

const API_BASE_URL = process.env.VITE_API_URL || 'http://localhost:8000';
const DECISION_ENDPOINT = `${API_BASE_URL}/api/decision`;

/**
 * Decision Request Interface
 */
export interface DecisionRequest {
  problem: string;
  alternatives: (string | { name: string; description?: string })[];
  criteria: Record<string, number | { weight: number; description?: string }>;
  scores: Record<string, Record<string, number>>;
  methodology?: string;
  show_details?: boolean;
  show_sensitivity?: boolean;
}

/**
 * Decision Response Interface
 */
export interface RankingItem {
  rank: number;
  name: string;
  score: number;
}

export interface DetailedScore {
  criterion_name: string;
  raw_score: number;
  weighted_score: number;
  weight: number;
}

export interface AlternativeAnalysis {
  name: string;
  total_score: number;
  rank: number;
  detailed_scores: DetailedScore[];
}

export interface SensitivityWarning {
  criterion_name: string;
  original_weight: number;
  reduced_weight: number;
  original_winner: string;
  new_winner: string;
  warning: string;
}

export interface DecisionResponse {
  problem: string;
  methodology: string;
  rankings: RankingItem[];
  recommendation: string;
  detailed_analysis: AlternativeAnalysis[];
  sensitivity_warnings: SensitivityWarning[];
  is_robust: boolean;
}

/**
 * Decision Engine API Error
 */
export class DecisionEngineError extends Error {
  constructor(
    message: string,
    public statusCode: number,
    public details?: any
  ) {
    super(message);
    this.name = 'DecisionEngineError';
  }
}

/**
 * Analyze a decision using the Decision Engine API
 * 
 * @param request - Decision request payload
 * @returns Promise resolving to DecisionResponse
 * @throws DecisionEngineError if request fails (400, 422, 500)
 */
export async function analyzeDecision(
  request: DecisionRequest
): Promise<DecisionResponse> {
  try {
    const response = await fetch(`${DECISION_ENDPOINT}/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    const data = await response.json();

    // Handle error responses (400, 422, 500)
    if (!response.ok) {
      const errorMessage = data.detail || data.message || 'Unknown error';
      throw new DecisionEngineError(
        errorMessage,
        response.status,
        data
      );
    }

    return data as DecisionResponse;
  } catch (error) {
    // Re-throw DecisionEngineError as-is
    if (error instanceof DecisionEngineError) {
      throw error;
    }

    // Handle network errors
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new DecisionEngineError(
        'Failed to connect to Decision Engine API. Is the server running?',
        0,
        error
      );
    }

    // Handle unexpected errors
    throw new DecisionEngineError(
      error instanceof Error ? error.message : 'Unknown error occurred',
      0,
      error
    );
  }
}

/**
 * Check Decision Engine API health
 * 
 * @returns Promise resolving to health status
 */
export async function checkHealth(): Promise<{
  status: string;
  version: string;
  core: string;
  engine: string;
}> {
  const response = await fetch(`${DECISION_ENDPOINT}/health`);
  
  if (!response.ok) {
    throw new DecisionEngineError(
      'Health check failed',
      response.status
    );
  }

  return response.json();
}
