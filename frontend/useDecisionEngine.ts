/**
 * React Hook for Decision Engine
 * 
 * Provides state management and methods for decision analysis.
 * 
 * Usage:
 * ```tsx
 * const { data, loading, error, analyze } = useDecisionEngine();
 * 
 * await analyze({
 *   problem: "Choose a car",
 *   alternatives: ["Ferrari", "Toyota"],
 *   criteria: { Cost: 0.6, Speed: 0.4 },
 *   scores: {
 *     Ferrari: { Cost: 1, Speed: 10 },
 *     Toyota: { Cost: 10, Speed: 5 }
 *   }
 * });
 * ```
 */

import { useState, useCallback } from 'react';
import {
  analyzeDecision,
  DecisionRequest,
  DecisionResponse,
  DecisionEngineError,
} from './api_client';

interface UseDecisionEngineReturn {
  /** Analysis result data */
  data: DecisionResponse | null;
  /** Loading state */
  loading: boolean;
  /** Error message (if any) */
  error: string | null;
  /** Analyze a decision */
  analyze: (request: DecisionRequest) => Promise<void>;
  /** Clear current data and error */
  reset: () => void;
}

/**
 * React Hook for Decision Engine
 */
export function useDecisionEngine(): UseDecisionEngineReturn {
  const [data, setData] = useState<DecisionResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const analyze = useCallback(async (request: DecisionRequest) => {
    setLoading(true);
    setError(null);
    setData(null);

    try {
      const result = await analyzeDecision(request);
      setData(result);
      setError(null);
    } catch (err) {
      if (err instanceof DecisionEngineError) {
        // Extract user-friendly error message from API
        const errorMessage = err.message || 'Decision analysis failed';
        setError(errorMessage);
      } else {
        setError('An unexpected error occurred');
      }
      setData(null);
    } finally {
      setLoading(false);
    }
  }, []);

  const reset = useCallback(() => {
    setData(null);
    setError(null);
    setLoading(false);
  }, []);

  return {
    data,
    loading,
    error,
    analyze,
    reset,
  };
}
