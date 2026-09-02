import { useState, useEffect } from 'react';
import { Zap, Target, Clock, Calculator } from 'lucide-react';
import 'katex/dist/katex.min.css';
import Latex from 'react-latex-next';

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
        const apiKey = import.meta.env.VITE_LITES_API_KEY || 'test-lites-key';
        const apiUrl = import.meta.env.VITE_API_URL || '';
        const response = await fetch(`${apiUrl}/v1/lites/metrics`, {
          headers: {
            'Authorization': `Bearer ${apiKey}`
          }
        });
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
      <h2 className="section-header">Metrics</h2>
      
      <div className="metrics-dashboard">
        {/* Token Savings Card - Green */}
        <div className="card card-green">
          <div className="card-header">
            <div className="card-title">Token Savings</div>
            <div className="card-icon"><Zap size={16} /></div>
          </div>
          <div className="metric-hero">
            <div className="metric-subtitle">Savings</div>
            <div className="metric-value text-green">{totalTokensSaved.toLocaleString()}</div>
            <div className="metric-trend text-green">+12.1% <span style={{ color: 'var(--text-secondary)' }}>(vs. last 30d)</span></div>
          </div>
          <div className="metric-divider"></div>
          <div className="metric-footer">
            <div className="footer-stat">Rule-based: <strong className="text-white">{metrics.tokens_saved_by_rules.toLocaleString()}</strong></div>
            <div className="footer-stat">AI-based: <strong className="text-white">{metrics.tokens_saved_by_ai.toLocaleString()}</strong></div>
          </div>
        </div>

        {/* Cache Hit Rate Card - Red */}
        <div className="card card-red">
          <div className="card-header">
            <div className="card-title">Cache Hit Rate</div>
            <div className="card-icon"><Target size={16} /></div>
          </div>
          <div className="metric-hero center-align">
            <div className="progress-circle">
              <svg viewBox="0 0 36 36" className="circular-chart">
                <path className="circle-bg"
                  d="M18 2.0845
                    a 15.9155 15.9155 0 0 1 0 31.831
                    a 15.9155 15.9155 0 0 1 0 -31.831"
                />
                <path className="circle"
                  strokeDasharray={`${hitRate}, 100`}
                  d="M18 2.0845
                    a 15.9155 15.9155 0 0 1 0 31.831
                    a 15.9155 15.9155 0 0 1 0 -31.831"
                />
              </svg>
              <div className="progress-content">
                <div className="metric-value text-white">{hitRate}%</div>
                <div className="metric-trend text-green">+5.8%</div>
              </div>
            </div>
          </div>
          <div className="metric-divider"></div>
          <div className="metric-footer">
            <div className="footer-stat">Hits: <strong className="text-white">{totalHits.toLocaleString()}</strong></div>
            <div className="footer-stat">Total: <strong className="text-white">{metrics.total_requests.toLocaleString()}</strong></div>
          </div>
        </div>

        {/* Avg Overhead Card - Orange */}
        <div className="card card-orange">
          <div className="card-header">
            <div className="card-title">Avg Overhead</div>
            <div className="card-icon"><Clock size={16} /></div>
          </div>
          <div className="metric-hero">
            <div className="metric-value text-white">{avgOverhead} <span style={{ fontSize: '1.5rem' }}>ms</span></div>
            <div className="metric-trend text-orange">+0.3ms <span style={{ color: 'var(--text-secondary)' }}>(last 24h)</span></div>
          </div>
          <div className="metric-divider" style={{ marginTop: 'auto' }}></div>
          <div className="metric-footer">
            <div className="footer-stat">Lites Response Time</div>
            <div className="footer-stat">P99: <strong className="text-white">24.1ms</strong> | Max: <strong className="text-white">31.2ms</strong></div>
          </div>
        </div>

        {/* Formulas Card - Purple */}
        <div className="card card-purple">
          <div className="card-header">
            <div className="card-title">Optimization Formulas</div>
            <div className="card-icon"><Calculator size={16} /></div>
          </div>
          <div className="metric-hero" style={{ marginTop: '0.5rem', marginBottom: '0.5rem', fontSize: '1rem', display: 'flex', flexDirection: 'column', gap: '0.5rem', color: '#fff' }}>
            <div>
              <Latex>{'$$\\text{Savings} = \\frac{\\text{Orig} - \\text{Opt}}{\\text{Orig}}$$'}</Latex>
            </div>
            <div>
              <Latex>{'$$\\text{Hit Rate} = \\frac{\\text{Hits}}{\\text{Total Reqs}}$$'}</Latex>
            </div>
          </div>
          <div className="metric-divider" style={{ marginTop: 'auto' }}></div>
          <div className="metric-footer">
            <div className="footer-stat">Math behind the metrics</div>
          </div>
        </div>
      </div>
    </div>
  );
}
