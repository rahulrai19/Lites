import { useState, useEffect } from 'react';
import { Zap, Target, Clock } from 'lucide-react';

interface Metrics {
  total_requests: number;
  exact_cache_hits: number;
  semantic_cache_hits: number;
  tokens_saved_by_rules: number;
  tokens_saved_by_ai: number;
  total_optimization_overhead_ms: number;
}

export function Dashboard() {
  const [metrics, setMetrics] = useState<Metrics>({
    total_requests: 0,
    exact_cache_hits: 0,
    semantic_cache_hits: 0,
    tokens_saved_by_rules: 0,
    tokens_saved_by_ai: 0,
    total_optimization_overhead_ms: 0
  });

  useEffect(() => {
    // Poll metrics every 2 seconds
    const fetchMetrics = async () => {
      try {
        const response = await fetch('/v1/lites/metrics');
        if (response.ok) {
          const data = await response.json();
          setMetrics(data);
        }
      } catch (error) {
        console.error('Failed to fetch metrics:', error);
      }
    };
    
    fetchMetrics();
    const interval = setInterval(fetchMetrics, 2000);
    return () => clearInterval(interval);
  }, []);

  const totalTokensSaved = metrics.tokens_saved_by_rules + metrics.tokens_saved_by_ai;
  
  // Calculate average overhead, avoid division by zero
  const avgOverhead = metrics.total_requests > 0 
    ? Math.round(metrics.total_optimization_overhead_ms / metrics.total_requests)
    : 0;

  const totalHits = metrics.exact_cache_hits + metrics.semantic_cache_hits;
  const hitRate = metrics.total_requests > 0
    ? ((totalHits / metrics.total_requests) * 100).toFixed(1)
    : '0.0';

  return (
    <div>
      <h2 className="section-header">Dashboard Metrics</h2>
      
      <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
        <div className="card">
          <div className="card-header">
            <div className="card-icon"><Zap size={18} /></div>
            <div className="card-title">Token Savings</div>
          </div>
          <div className="metric-value">{totalTokensSaved.toLocaleString()}</div>
          <div className="metric-label">Total tokens saved across all optimizations</div>
          
          <div style={{ marginTop: '1.5rem', display: 'flex', gap: '2rem' }}>
            <div>
              <div style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                {metrics.tokens_saved_by_rules.toLocaleString()}
              </div>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Rule-based</div>
            </div>
            <div>
              <div style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                {metrics.tokens_saved_by_ai.toLocaleString()}
              </div>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>AI-based</div>
            </div>
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
          <div className="card">
            <div className="card-header">
              <div className="card-icon"><Target size={18} /></div>
              <div className="card-title">Cache Hit Rate</div>
            </div>
            <div className="metric-value">{hitRate}%</div>
            <div className="metric-label">{totalHits} hits / {metrics.total_requests} requests</div>
          </div>

          <div className="card">
            <div className="card-header">
              <div className="card-icon"><Clock size={18} /></div>
              <div className="card-title">Avg Overhead</div>
            </div>
            <div className="metric-value" style={{ color: 'var(--text-primary)' }}>{avgOverhead}ms</div>
            <div className="metric-label">Latency added per request</div>
          </div>
        </div>
      </div>
    </div>
  );
}
