import { useEffect, useState } from 'react'
import {
  Activity,
  ArrowRight,
  BrainCircuit,
  CheckCircle2,
  Clock3,
  Database,
  FolderOpen,
  History,
  Lightbulb,
  LoaderCircle,
  RotateCw,
  ShieldAlert,
  Sparkles,
  Tag,
  Users,
  Wallet,
  Zap
} from 'lucide-react'

const API = (import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000').replace(/\/+$/, '')

function List({ items }) {
  return <ul>{(items || []).map((item, i) => <li key={i}>{item}</li>)}</ul>
}

function formatDate(isoStr) {
  if (!isoStr) return 'Recently'
  try {
    const d = new Date(isoStr)
    return d.toLocaleDateString(undefined, {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch {
    return 'Recently'
  }
}

export default function App() {
  const [decision, setDecision] = useState('')
  const [category, setCategory] = useState('Education & Academics')
  const [context, setContext] = useState('')
  const [horizon, setHorizon] = useState('6 months')
  const [constraints, setConstraints] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [apiMode, setApiMode] = useState('checking')
  const [dbStatus, setDbStatus] = useState('checking')
  const [dbMessage, setDbMessage] = useState('')
  const [history, setHistory] = useState([])
  const [historyLoading, setHistoryLoading] = useState(false)

  const checkHealth = async () => {
    try {
      const res = await fetch(`${API}/api/health`)
      const d = await res.json()
      setApiMode(d.ai_mode || 'demo')
      setDbStatus(d.db_status || 'disconnected')
      if (d.db_details?.message) {
        setDbMessage(d.db_details.message)
      }
    } catch {
      setApiMode('offline')
      setDbStatus('offline')
    }
  }

  const fetchHistory = async () => {
    setHistoryLoading(true)
    try {
      const res = await fetch(`${API}/api/simulations?limit=20`)
      if (res.ok) {
        const data = await res.json()
        setHistory(data.simulations || [])
      }
    } catch {
      // Backend may be offline or DB not reachable
    } finally {
      setHistoryLoading(false)
    }
  }

  useEffect(() => {
    checkHealth()
    fetchHistory()
  }, [])

  const sample = () => {
    setDecision('What if our college introduces a four-day working week?')
    setCategory('Education & Academics')
    setContext('A college with 2,000 students, 120 faculty members and regular laboratory sessions.')
    setHorizon('6 months')
    setConstraints('Maintain required teaching hours, laboratory access and student support services.')
    setResult(null)
    setError('')
  }

  const simulate = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    setResult(null)
    try {
      const response = await fetch(`${API}/api/simulate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          decision,
          category,
          context,
          time_horizon: horizon,
          constraints
        })
      })
      const data = await response.json()
      if (!response.ok) throw new Error(data.detail || 'Simulation failed')
      setResult(data)
      // Refresh history list so the newly saved simulation appears immediately
      fetchHistory()
      setTimeout(() => {
        document.getElementById('results')?.scrollIntoView({ behavior: 'smooth' })
      }, 100)
    } catch (err) {
      setError(`${err.message}. Make sure the FastAPI backend is running and accessible.`)
    } finally {
      setLoading(false)
    }
  }

  const loadHistoryItem = async (item) => {
    try {
      // If full scenarios are already present in item, load directly
      if (item.scenarios && item.scenarios.length > 0) {
        setResult(item)
      } else {
        const res = await fetch(`${API}/api/simulations/${item.id}`)
        if (!res.ok) throw new Error('Could not load simulation details')
        const fullData = await res.json()
        setResult(fullData)
      }
      setTimeout(() => {
        document.getElementById('results')?.scrollIntoView({ behavior: 'smooth' })
      }, 100)
    } catch (err) {
      setError(`Failed to load historical simulation: ${err.message}`)
    }
  }

  const reopenInForm = (item) => {
    setDecision(item.question || item.decision || '')
    setCategory(item.category || 'General')
    setContext(item.context || '')
    setHorizon(item.time_horizon || '6 months')
    setConstraints(item.constraints || '')
    document.querySelector('.workspace')?.scrollIntoView({ behavior: 'smooth' })
  }

  const agents = [
    { name: 'People Impact', icon: Users, desc: 'Stakeholders, adoption and wellbeing' },
    { name: 'Operations & Cost', icon: Wallet, desc: 'Resources, delivery and constraints' },
    { name: 'Risk & Opportunity', icon: ShieldAlert, desc: 'Uncertainty, risks and upside' }
  ]

  return (
    <div className="app-shell">
      <header className="topbar">
        <a className="brand" href="#">
          <span className="brand-icon"><BrainCircuit size={21} /></span>
          <span>FUTUREMIND<span className="brand-ai"> AI</span></span>
        </a>
        <div className="top-meta">
          <div className="status-badge" title="AI Model Status">
            <span className={`status-dot ${apiMode === 'offline' ? 'offline' : ''}`}></span>
            <span>{apiMode === 'qwen' ? 'Qwen AI connected' : apiMode === 'demo' ? 'Demo mode' : apiMode === 'offline' ? 'Backend offline' : 'Connecting...'}</span>
          </div>
          <div className="status-separator"></div>
          <div className="status-badge" title={dbMessage || `MongoDB Atlas Status: ${dbStatus}`}>
            <Database size={13} className={dbStatus === 'connected' ? 'db-icon-connected' : 'db-icon-warning'} />
            <span className={`status-dot ${dbStatus === 'connected' ? 'connected' : dbStatus === 'disconnected' ? 'warning' : 'offline'}`}></span>
            <span>
              {dbStatus === 'connected'
                ? 'MongoDB Atlas'
                : dbStatus === 'disconnected'
                ? 'MongoDB Disconnected'
                : 'MongoDB Checking'}
            </span>
          </div>
        </div>
      </header>

      <main className="main">
        <section className="hero">
          <div className="eyebrow"><Sparkles size={14} /> DECISION INTELLIGENCE STUDIO</div>
          <h1>Explore tomorrow.<br /><span>Before you decide.</span></h1>
          <p className="hero-copy">Turn uncertain decisions into structured possibilities. Three specialist AI agents examine your decision, then build scenarios and save insights directly to MongoDB Atlas.</p>
          <div className="hero-pills">
            <span><Users size={14} /> Multi-agent analysis</span>
            <span><Activity size={14} /> Scenario planning</span>
            <span><Zap size={14} /> Qwen powered</span>
            <span><Database size={14} /> MongoDB Atlas</span>
          </div>
        </section>

        <section className="workspace">
          <div className="section-heading">
            <div>
              <div className="eyebrow">01 / DEFINE YOUR DECISION</div>
              <h2>What are you thinking about?</h2>
            </div>
            <button className="sample-btn" onClick={sample}>
              Load sample decision <ArrowRight size={14} />
            </button>
          </div>
          <form className="decision-form" onSubmit={simulate}>
            <label>
              YOUR DECISION
              <textarea
                required
                minLength={8}
                maxLength={1200}
                value={decision}
                onChange={e => setDecision(e.target.value)}
                placeholder="Example: What if we introduce a four-day working week?"
              />
            </label>
            <label>
              BACKGROUND CONTEXT
              <textarea
                value={context}
                onChange={e => setContext(e.target.value)}
                placeholder="Who is affected? What is happening now? Add any useful facts..."
                rows="3"
              />
            </label>
            <div className="form-row form-row-3">
              <label>
                CATEGORY
                <select value={category} onChange={e => setCategory(e.target.value)}>
                  <option>Education & Academics</option>
                  <option>Business & Strategy</option>
                  <option>Operations & Process</option>
                  <option>Technology & Product</option>
                  <option>Finance & Investment</option>
                  <option>Workplace & People</option>
                  <option>Personal & Career</option>
                  <option>General</option>
                </select>
              </label>
              <label>
                TIME HORIZON
                <select value={horizon} onChange={e => setHorizon(e.target.value)}>
                  <option>1 month</option>
                  <option>3 months</option>
                  <option>6 months</option>
                  <option>1 year</option>
                  <option>3 years</option>
                </select>
              </label>
              <label>
                CONSTRAINTS
                <input
                  value={constraints}
                  onChange={e => setConstraints(e.target.value)}
                  placeholder="Budget, rules, deadlines..."
                />
              </label>
            </div>
            <button className="primary-btn" disabled={loading || decision.trim().length < 8}>
              {loading ? (
                <><LoaderCircle className="spin" size={18} /> Analyzing possibilities...</>
              ) : (
                <><Sparkles size={17} /> Simulate outcomes <ArrowRight size={17} /></>
              )}
            </button>
            {error && <div className="error">{error}</div>}
          </form>
        </section>

        <section className="agents-section">
          <div className="eyebrow">02 / SPECIALIST AGENTS</div>
          <h2>Three perspectives. One clearer picture.</h2>
          <div className="agent-grid">
            {agents.map((a, i) => (
              <div className="agent-card" key={a.name}>
                <div className={`agent-icon agent-${i}`}><a.icon size={20} /></div>
                <div className="agent-number">AGENT 0{i + 1}</div>
                <h3>{a.name}</h3>
                <p>{a.desc}</p>
                <span className="agent-state"><span className="mini-dot"></span> Ready to analyze</span>
              </div>
            ))}
          </div>
        </section>

        {result && (
          <section className="results" id="results">
            <div className="result-head">
              <div>
                <div className="eyebrow">03 / SIMULATION RESULTS</div>
                <h2>Your possible futures</h2>
                <p className="result-decision">{result.decision || result.question}</p>
              </div>
              <div className="result-tags">
                <span className="mode-tag category-badge"><Tag size={11} /> {result.category || category}</span>
                <span className={`mode-tag ${result.mode}`}>
                  {result.mode === 'qwen' ? '✦ Qwen AI analysis' : 'Demo analysis'}
                </span>
                {result.saved_to_db && (
                  <span className="mode-tag db-saved-badge">
                    <Database size={11} /> Saved to MongoDB
                  </span>
                )}
              </div>
            </div>

            <div className="disclaimer">
              <ShieldAlert size={16} />
              {result.disclaimer}
            </div>

            <div className="scenario-grid">
              {(result.scenarios || []).map((s, i) => (
                <article className={`scenario-card scenario-${i}`} key={s.name}>
                  <div className="scenario-top">
                    <span className="scenario-index">0{i + 1}</span>
                    <span className="scenario-label">{s.likelihood_label}</span>
                  </div>
                  <h3>{s.name}</h3>
                  <p>{s.description}</p>
                  <div className="scenario-block">
                    <h4>Potential impacts</h4>
                    <List items={s.impacts} />
                  </div>
                  <div className="scenario-block">
                    <h4>Risks</h4>
                    <List items={s.risks} />
                  </div>
                  <div className="scenario-block">
                    <h4>Opportunities</h4>
                    <List items={s.opportunities} />
                  </div>
                </article>
              ))}
            </div>

            <div className="insights-grid">
              <div className="panel">
                <div className="panel-title"><Lightbulb size={18} /> Recommended next steps</div>
                <List items={result.recommendations} />
              </div>
              <div className="panel">
                <div className="panel-title"><CheckCircle2 size={18} /> Key assumptions</div>
                <List items={result.key_assumptions} />
                <div className="confidence">
                  <span>Analysis confidence</span>
                  <strong>{result.confidence}</strong>
                </div>
              </div>
            </div>

            <div className="agent-results">
              <div className="panel-title"><BrainCircuit size={18} /> Specialist agent findings</div>
              <div className="agent-result-grid">
                {(result.agent_insights || result.agent_analysis || []).map(a => (
                  <div className="agent-result" key={a.agent}>
                    <h4>{a.agent}</h4>
                    <p>{a.summary}</p>
                    <b>Benefits</b>
                    <List items={a.benefits} />
                    <b>Concerns</b>
                    <List items={a.concerns} />
                    <b>Assumptions</b>
                    <List items={a.assumptions} />
                  </div>
                ))}
              </div>
            </div>
          </section>
        )}

        <section className="history-section" id="history">
          <div className="section-heading">
            <div>
              <div className="eyebrow"><History size={14} /> 04 / SIMULATION HISTORY</div>
              <h2>Saved Simulations</h2>
              <p className="history-subtitle">
                {dbStatus === 'connected'
                  ? 'Access previously synthesized simulations stored securely in your MongoDB Atlas cluster.'
                  : 'Simulations will be preserved in MongoDB Atlas once the connection is active.'}
              </p>
            </div>
            <button className="sample-btn" onClick={fetchHistory} disabled={historyLoading}>
              <RotateCw size={13} className={historyLoading ? 'spin' : ''} />
              Refresh
            </button>
          </div>

          {historyLoading ? (
            <div className="history-status-box">
              <LoaderCircle className="spin" size={24} />
              <span>Loading saved simulations from MongoDB...</span>
            </div>
          ) : history.length === 0 ? (
            <div className="history-status-box">
              <Database size={24} className="history-empty-icon" />
              <p>No saved simulations found yet.</p>
              <span className="history-hint">
                {dbStatus === 'connected'
                  ? 'Simulate your first decision above to persist results to MongoDB Atlas.'
                  : (dbMessage || 'Configure your valid MongoDB password in backend/.env to enable Atlas persistence.')}
              </span>
            </div>
          ) : (
            <div className="history-grid">
              {history.map((item) => (
                <article className="history-card" key={item.id}>
                  <div className="history-top">
                    <span className="history-category"><Tag size={11} /> {item.category || 'General'}</span>
                    <span className="history-date"><Clock3 size={11} /> {formatDate(item.created_at)}</span>
                  </div>
                  <h3 className="history-title">{item.question || item.decision}</h3>
                  {item.final_recommendation && (
                    <p className="history-rec">
                      <strong>Lead recommendation:</strong> {item.final_recommendation}
                    </p>
                  )}
                  <div className="history-meta">
                    <span className={`history-mode-pill ${item.mode}`}>
                      {item.mode === 'qwen' ? 'Qwen AI' : 'Demo'}
                    </span>
                    <span className="history-horizon">{item.time_horizon || '6 months'}</span>
                  </div>
                  <div className="history-actions">
                    <button className="history-btn-reopen" onClick={() => reopenInForm(item)}>
                      <FolderOpen size={13} /> Reopen
                    </button>
                    <button className="history-btn-view" onClick={() => loadHistoryItem(item)}>
                      View Results <ArrowRight size={13} />
                    </button>
                  </div>
                </article>
              ))}
            </div>
          )}
        </section>

        <footer>
          <span>FUTUREMIND AI</span>
          <span><Clock3 size={13} /> Think in scenarios, decide with evidence.</span>
        </footer>
      </main>
    </div>
  )
}
