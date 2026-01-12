import React, { useState, useEffect } from 'react'
import './index.css'

const API_BASE = '/api/being'

function App() {
  const [being, setBeing] = useState(null)
  const [loading, setLoading] = useState(false)
  const [logs, setLogs] = useState([])
  const [decisionResults, setDecisionResults] = useState([])
  const [makingDecisions, setMakingDecisions] = useState(false)

  const addLog = (message, type = 'info') => {
    setLogs(prev => [...prev, { 
      message, 
      type, 
      timestamp: new Date().toLocaleTimeString() 
    }])
  }

  const spawnBeing = async () => {
    setLoading(true)
    addLog('Spawning first Being (will use Empirica)...', 'info')
    
    try {
      const response = await fetch(`${API_BASE}/spawn`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          reality_id: 'test_reality',
          initial_skills: {
            reasoning: 30.0,
            creativity: 25.0,
            analysis: 35.0
          }
        })
      })
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      setBeing(data)
      
      if (data.empirica_enabled) {
        addLog(`✅ Being spawned with Empirica! Session ID: ${data.empirica_session_id}`, 'success')
      } else {
        addLog('⚠️ Being spawned but Empirica not enabled', 'warning')
      }
      
      addLog(`Being ID: ${data.being_id}`, 'info')
      addLog(`Lifetimes: ${data.lifetimes}`, 'info')
      addLog(`Stamina: ${data.stamina.toFixed(1)}`, 'info')
    } catch (error) {
      addLog(`❌ Error spawning Being: ${error.message}`, 'error')
      console.error('Error:', error)
    } finally {
      setLoading(false)
    }
  }

  const makeDecision = async (decisionType = null) => {
    if (!being) {
      addLog('❌ No Being spawned yet!', 'error')
      return
    }
    
    setLoading(true)
    addLog(`Making decision: ${decisionType || 'auto'}...`, 'info')
    
    try {
      const response = await fetch(`${API_BASE}/${being.being_id}/decision`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          decision_type: decisionType,
          stamina_cost: 5.0
        })
      })
      
      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
      }
      
      const result = await response.json()
      
      // Update being state
      setBeing(prev => ({
        ...prev,
        stamina: result.stamina_remaining,
        decision_fatigue: result.decision_fatigue_remaining,
        ...result.being_state
      }))
      
      // Add to decision results
      setDecisionResults(prev => [result, ...prev].slice(0, 10))
      
      // Log result
      const experience = result.experience || {}
      addLog(
        `✅ Decision: ${result.decision_type} | Quality: ${experience.quality || 'unknown'} | Stamina: ${result.stamina_remaining.toFixed(1)}`,
        'success'
      )
      
      if (result.empirica_gate) {
        addLog(`🧠 Empirica Gate: ${result.empirica_gate}`, 'info')
      }
      
      if (experience.stamina_depleted) {
        addLog(`⚠️ Stamina depleted! Mistakes: ${experience.mistakes?.length || 0}`, 'warning')
      }
      
    } catch (error) {
      addLog(`❌ Error making decision: ${error.message}`, 'error')
      console.error('Error:', error)
    } finally {
      setLoading(false)
    }
  }

  const makeMultipleDecisions = async (count = 5) => {
    if (!being) {
      addLog('❌ No Being spawned yet!', 'error')
      return
    }
    
    setMakingDecisions(true)
    addLog(`Making ${count} decisions in sequence...`, 'info')
    
    try {
      const response = await fetch(`${API_BASE}/${being.being_id}/decisions/make-multiple?count=${count}`)
      
      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
      }
      
      const result = await response.json()
      
      // Update being state
      setBeing(prev => ({
        ...prev,
        stamina: result.final_state.stamina,
        decision_fatigue: result.final_state.decision_fatigue,
        will_to_live: result.final_state.will_to_live,
        is_sleeping: result.final_state.is_sleeping
      }))
      
      // Add all results
      setDecisionResults(prev => [...result.results, ...prev].slice(0, 20))
      
      // Log summary
      addLog(`✅ Made ${result.decisions_made} decisions`, 'success')
      addLog(`Final Stamina: ${result.final_state.stamina.toFixed(1)}`, 'info')
      addLog(`Final Fatigue: ${result.final_state.decision_fatigue}`, 'info')
      
      // Log Empirica gates
      const empiricaGates = result.results
        .filter(r => r.empirica_gate)
        .map(r => `${r.decision_type}: ${r.empirica_gate}`)
      
      if (empiricaGates.length > 0) {
        addLog(`🧠 Empirica Gates: ${empiricaGates.join(', ')}`, 'info')
      }
      
    } catch (error) {
      addLog(`❌ Error making decisions: ${error.message}`, 'error')
      console.error('Error:', error)
    } finally {
      setMakingDecisions(false)
    }
  }

  const refreshBeing = async () => {
    if (!being) return
    
    setLoading(true)
    try {
      const response = await fetch(`${API_BASE}/${being.being_id}`)
      if (response.ok) {
        const data = await response.json()
        setBeing(data)
        addLog('✅ Being state refreshed', 'success')
      }
    } catch (error) {
      addLog(`❌ Error refreshing: ${error.message}`, 'error')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <div className="header">
        <h1>🧠 WAFT Being Test</h1>
        <p>Testing Being System with Empirica Integration</p>
      </div>

      <div className="grid">
        <div className="section">
          <h2>Being Control</h2>
          
          {!being ? (
            <div>
              <p style={{ marginBottom: '1rem', color: '#888' }}>
                Spawn a Being to start testing. The first Being will automatically use Empirica for epistemic thinking.
              </p>
              <button 
                className="button" 
                onClick={spawnBeing}
                disabled={loading}
              >
                {loading ? 'Spawning...' : '✨ Spawn First Being'}
              </button>
            </div>
          ) : (
            <div>
              <div style={{ marginBottom: '1rem' }}>
                <h3 style={{ color: '#667eea', marginBottom: '0.5rem' }}>
                  Being: {being.being_id.slice(0, 20)}...
                  {being.empirica_enabled && <span className="empirica-badge">EMPIRICA</span>}
                </h3>
                
                <div className="info-grid">
                  <div className="info-item">
                    <label>Lifetimes</label>
                    <value>{being.lifetimes}</value>
                  </div>
                  <div className="info-item">
                    <label>Stamina</label>
                    <value>{being.stamina?.toFixed(1) || 'N/A'}</value>
                  </div>
                  <div className="info-item">
                    <label>Will to Live</label>
                    <value>{being.will_to_live?.toFixed(1) || 'N/A'}</value>
                  </div>
                  <div className="info-item">
                    <label>Decision Fatigue</label>
                    <value>{being.decision_fatigue || 'N/A'}</value>
                  </div>
                  <div className="info-item">
                    <label>Personality</label>
                    <value>{being.personality_type || 'N/A'}</value>
                  </div>
                  <div className="info-item">
                    <label>Empirica Session</label>
                    <value style={{ fontSize: '0.75rem' }}>
                      {being.empirica_session_id ? being.empirica_session_id.slice(0, 20) + '...' : 'None'}
                    </value>
                  </div>
                </div>
              </div>

              <div style={{ marginTop: '1rem' }}>
                <button className="button secondary" onClick={refreshBeing} disabled={loading}>
                  🔄 Refresh State
                </button>
              </div>
            </div>
          )}
        </div>

        <div className="section">
          <h2>Decision Making</h2>
          
          {being ? (
            <div>
              <div style={{ marginBottom: '1rem' }}>
                <button 
                  className="button" 
                  onClick={() => makeDecision()}
                  disabled={loading || being.is_sleeping}
                >
                  🎲 Make Auto Decision
                </button>
                <button 
                  className="button secondary" 
                  onClick={() => makeMultipleDecisions(5)}
                  disabled={makingDecisions || being.is_sleeping}
                >
                  {makingDecisions ? 'Making Decisions...' : '⚡ Make 5 Decisions'}
                </button>
              </div>

              <div style={{ marginTop: '1rem' }}>
                <p style={{ color: '#888', marginBottom: '0.5rem', fontSize: '0.875rem' }}>
                  Manual Decisions:
                </p>
                <button className="button secondary" onClick={() => makeDecision('learn_skill')} disabled={loading}>
                  📚 Learn Skill
                </button>
                <button className="button secondary" onClick={() => makeDecision('record_memory')} disabled={loading}>
                  💭 Record Memory
                </button>
                <button className="button secondary" onClick={() => makeDecision('explore')} disabled={loading}>
                  🔍 Explore
                </button>
                <button className="button secondary" onClick={() => makeDecision('rest')} disabled={loading}>
                  😴 Rest
                </button>
              </div>

              {being.is_sleeping && (
                <div style={{ marginTop: '1rem', padding: '1rem', background: '#2a2a2a', borderRadius: '6px' }}>
                  <p style={{ color: '#f39c12' }}>😴 Being is sleeping and cannot make decisions</p>
                </div>
              )}
            </div>
          ) : (
            <p style={{ color: '#888' }}>Spawn a Being first to make decisions</p>
          )}
        </div>
      </div>

      {decisionResults.length > 0 && (
        <div className="section">
          <h2>Recent Decisions</h2>
          <div style={{ display: 'grid', gap: '1rem' }}>
            {decisionResults.slice(0, 5).map((result, idx) => (
              <div key={idx} className="decision-result">
                <h3>
                  {result.decision_type || 'Unknown'}
                  {result.empirica_gate && (
                    <span className="empirica-badge" style={{ marginLeft: '0.5rem' }}>
                      Gate: {result.empirica_gate}
                    </span>
                  )}
                </h3>
                {result.experience && (
                  <div style={{ marginTop: '0.5rem', fontSize: '0.875rem' }}>
                    <p>Quality: <strong>{result.experience.quality || 'unknown'}</strong></p>
                    <p>Stamina: {result.stamina_remaining?.toFixed(1) || 'N/A'}</p>
                    {result.experience.stamina_depleted && (
                      <p style={{ color: '#f39c12' }}>⚠️ Stamina Depleted</p>
                    )}
                    {result.experience.mistakes && result.experience.mistakes.length > 0 && (
                      <p style={{ color: '#e74c3c' }}>
                        Mistakes: {result.experience.mistakes.join(', ')}
                      </p>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="section">
        <h2>Activity Log</h2>
        <div className="log">
          {logs.length === 0 ? (
            <p style={{ color: '#888', fontStyle: 'italic' }}>No activity yet...</p>
          ) : (
            logs.slice().reverse().map((log, idx) => (
              <div key={idx} className={`log-entry ${log.type}`}>
                <span style={{ color: '#888' }}>[{log.timestamp}]</span> {log.message}
              </div>
            ))
          )}
        </div>
        <button 
          className="button secondary" 
          onClick={() => setLogs([])}
          style={{ marginTop: '1rem' }}
        >
          Clear Log
        </button>
      </div>
    </div>
  )
}

export default App
