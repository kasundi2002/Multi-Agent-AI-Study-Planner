import { useMemo, useState } from 'react'
import './App.css'

// ── Difficulty badge helper ───────────────────────────
function DifficultyBadge({ level }) {
  const cls = level?.toLowerCase() ?? 'medium'
  return <span className={`badge ${cls}`}>{level ?? 'Medium'}</span>
}

// ── Section wrapper ───────────────────────────────────
function Panel({ icon, title, children }) {
  return (
    <div className="panel">
      <h2><span className="icon">{icon}</span>{title}</h2>
      {children}
    </div>
  )
}

// ── Main app ──────────────────────────────────────────
function App() {
  const [subject, setSubject] = useState('Machine Learning')
  const [days, setDays] = useState(14)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [result, setResult] = useState(null)

  const sortedScheduleDays = useMemo(() => {
    if (!result?.schedule) return []
    return Object.keys(result.schedule).sort((a, b) => {
      const aNum = Number(a.replace('Day ', ''))
      const bNum = Number(b.replace('Day ', ''))
      return aNum - bNum
    })
  }, [result])

  async function handleSubmit(event) {
    event.preventDefault()
    setLoading(true)
    setError('')
    setResult(null)
    try {
      const response = await fetch('http://127.0.0.1:8000/plan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ subject, days: Number(days) }),
      })
      if (!response.ok) {
        const payload = await response.json()
        throw new Error(payload?.detail || 'Failed to generate study plan')
      }
      setResult(await response.json())
    } catch (err) {
      setError(err.message || 'Could not connect to backend API')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="container">
      {/* ── Hero ── */}
      <header className="hero">
        <h1>Multi-Agent Study Planner</h1>
        <p className="sub">Enter a subject and study window — six AI agents build your plan.</p>
      </header>

      {/* ── Form ── */}
      <form className="panel" onSubmit={handleSubmit}>
        <label>
          Subject
          <input
            id="input-subject"
            value={subject}
            onChange={(e) => setSubject(e.target.value)}
            placeholder="e.g. Machine Learning"
            required
          />
        </label>
        <label>
          Days
          <input
            id="input-days"
            type="number"
            min="1"
            max="365"
            value={days}
            onChange={(e) => setDays(e.target.value)}
            required
          />
        </label>
        <button type="submit" id="btn-generate" disabled={loading}>
          {loading ? <><span className="spinner" />Generating…</> : '✦ Generate Plan'}
        </button>
      </form>

      {error && <div className="error">⚠ {error}</div>}

      {result && (
        <section className="results">

          {/* ── Metadata ── */}
          <Panel icon="🔖" title="Metadata">
            <div className="meta-strip">
              <span><strong>Goal:</strong> {result.goal}</span>
              <span><strong>Days:</strong> {result.days}</span>
              <span><strong>Trace ID:</strong> {result.trace_id}</span>
              <span><strong>Saved:</strong> {result.final_plan_path || '—'}</span>
            </div>
          </Panel>

          {/* ── Topics + Structured (side by side) ── */}
          <div className="results-row">
            <Panel icon="📚" title="Topics">
              <ul className="tag-list">
                {result.topics?.map((t) => (
                  <li key={t} className="tag">{t}</li>
                ))}
              </ul>
            </Panel>

            <Panel icon="🗂️" title="Structured Topics">
              <ol className="ordered-topics">
                {result.structured_topics?.map((t) => (
                  <li key={t}>{t}</li>
                ))}
              </ol>
            </Panel>
          </div>

          {/* ── Difficulty ── */}
          <Panel icon="🎯" title="Difficulty Analysis">
            <div className="difficulty-grid">
              {Object.entries(result.difficulties || {}).map(([topic, level]) => (
                <div key={topic} className="difficulty-row">
                  <span className="topic-name">{topic}</span>
                  <DifficultyBadge level={level} />
                </div>
              ))}
            </div>
          </Panel>

          {/* ── Resources + Schedule (side by side) ── */}
          <div className="results-row">
            <Panel icon="🔗" title="Resources">
              {Object.entries(result.resources || {}).map(([topic, links]) => (
                <div key={topic} className="resource-group">
                  <p className="resource-group-title">{topic}</p>
                  <ul>
                    {links.map((link) => (
                      <li key={link}>
                        <a href={link} target="_blank" rel="noreferrer">↗ {link}</a>
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </Panel>

            <Panel icon="📅" title="Study Schedule">
              <div className="schedule-grid">
                {sortedScheduleDays.map((day) => (
                  <div key={day} className="schedule-day">
                    <p className="schedule-day-title">{day}</p>
                    <ul>
                      {result.schedule[day].map((t) => (
                        <li key={`${day}-${t}`}>{t}</li>
                      ))}
                    </ul>
                  </div>
                ))}
              </div>
            </Panel>
          </div>

          {/* ── Quiz Generator ── */}
          <Panel icon="🧠" title="Quiz Questions">
            {Object.entries(result.quizzes || {}).map(([topic, questions]) => (
              <div key={topic} className="quiz-topic-block">
                <p className="quiz-topic-title">
                  📖 {topic}
                  {result.difficulties?.[topic] && (
                    <DifficultyBadge level={result.difficulties[topic]} />
                  )}
                </p>
                <ul className="quiz-questions">
                  {questions.map((q, i) => (
                    <li key={`${topic}-q${i}`}>{q}</li>
                  ))}
                </ul>
              </div>
            ))}
          </Panel>

        </section>
      )}
    </main>
  )
}

export default App
