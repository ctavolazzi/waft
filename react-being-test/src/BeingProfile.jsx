import React from 'react'

// Avatar generation based on being attributes
function generateAvatar(being) {
  if (!being) return '🧙‍♂️'

  // Avatar options based on personality and stats
  const avatars = {
    analytical: ['🧙‍♂️', '🧝‍♂️', '🧑‍🔬', '🦉'],
    creative: ['🧚‍♀️', '🎨', '🦄', '🌟'],
    warrior: ['⚔️', '🛡️', '🗡️', '🦸‍♂️'],
    explorer: ['🧭', '🗺️', '🏃‍♂️', '🎒'],
    mystical: ['🔮', '✨', '🌙', '⭐'],
    default: ['👤', '🎭', '🧬', '💫']
  }

  // Determine avatar category based on skills
  let category = 'default'
  if (being.skills) {
    const topSkill = Object.entries(being.skills).sort((a, b) => b[1] - a[1])[0]
    if (topSkill) {
      if (topSkill[0].includes('reason') || topSkill[0].includes('analy')) category = 'analytical'
      else if (topSkill[0].includes('creat') || topSkill[0].includes('art')) category = 'creative'
      else if (topSkill[0].includes('combat') || topSkill[0].includes('fight')) category = 'warrior'
      else if (topSkill[0].includes('explor') || topSkill[0].includes('adven')) category = 'explorer'
    }
  }

  // If stamina is low or sleeping, show mystical
  if (being.is_sleeping || (being.stamina && being.stamina < 20)) {
    category = 'mystical'
  }

  const options = avatars[category] || avatars.default
  const hash = being.being_id ? being.being_id.charCodeAt(0) + being.being_id.charCodeAt(1) : 0
  return options[hash % options.length]
}

function BeingProfile({ being }) {
  if (!being) {
    return (
      <div className="profile-empty">
        <div className="profile-empty-content">
          <div className="empty-avatar-showcase">
            <div className="empty-avatar-row">
              <span className="empty-avatar-icon">🧙‍♂️</span>
              <span className="empty-avatar-icon">🧝‍♀️</span>
              <span className="empty-avatar-icon">⚔️</span>
            </div>
            <div className="empty-avatar-row">
              <span className="empty-avatar-icon">🔮</span>
              <span className="empty-avatar-icon">🎨</span>
              <span className="empty-avatar-icon">🦄</span>
            </div>
          </div>
          <h2>🎭 No Avatar Created</h2>
          <p>Spawn a Being to generate your unique avatar and begin your adventure!</p>
          <p className="empty-subtitle">Each avatar is uniquely generated based on their skills and personality</p>
        </div>
      </div>
    )
  }

  const staminaPercent = (being.stamina / being.stamina_max) * 100
  const willPercent = (being.will_to_live / 100) * 100
  const fatiguePercent = (being.decision_fatigue / being.decision_quota_max) * 100

  const getStaminaColor = (percent) => {
    if (percent > 60) return '#10b981'
    if (percent > 30) return '#f59e0b'
    return '#ef4444'
  }

  const getWillColor = (percent) => {
    if (percent > 70) return '#667eea'
    if (percent > 40) return '#764ba2'
    return '#8b5cf6'
  }

  const avatar = generateAvatar(being)

  return (
    <div className="profile-container">
      {/* Hero Section */}
      <div className="profile-hero">
        <div className="profile-avatar">
          <div className={`avatar-circle ${being.is_sleeping ? 'sleeping' : ''}`}>
            {avatar}
          </div>
          {being.empirica_enabled && (
            <div className="empirica-crown">👑</div>
          )}
          <div className="avatar-glow"></div>
        </div>
        <div className="profile-header">
          <h1 className="profile-name">
            Avatar {being.being_id?.slice(0, 8)}
          </h1>
          <div className="profile-subtitle">
            <span className="profile-tag">{being.personality_type || 'Wanderer'}</span>
            <span className="profile-tag">Lifetime {being.lifetimes}</span>
            {being.empirica_enabled && (
              <span className="profile-tag empirica">⚡ Empirica Enhanced</span>
            )}
          </div>
          {being.is_first_being && (
            <div className="first-being-badge">
              ✨ First Being
            </div>
          )}
        </div>
      </div>

      {/* Stats Grid */}
      <div className="stats-grid">
        {/* Stamina */}
        <div className="stat-card">
          <div className="stat-header">
            <span className="stat-icon">⚡</span>
            <span className="stat-label">Stamina</span>
          </div>
          <div className="stat-bar">
            <div
              className="stat-bar-fill"
              style={{
                width: `${staminaPercent}%`,
                backgroundColor: getStaminaColor(staminaPercent)
              }}
            />
          </div>
          <div className="stat-value">
            {being.stamina?.toFixed(1)} / {being.stamina_max}
          </div>
        </div>

        {/* Will to Live */}
        <div className="stat-card">
          <div className="stat-header">
            <span className="stat-icon">💜</span>
            <span className="stat-label">Will to Live</span>
          </div>
          <div className="stat-bar">
            <div
              className="stat-bar-fill"
              style={{
                width: `${willPercent}%`,
                backgroundColor: getWillColor(willPercent)
              }}
            />
          </div>
          <div className="stat-value">
            {being.will_to_live?.toFixed(1)} / 100
          </div>
        </div>

        {/* Decision Fatigue */}
        <div className="stat-card">
          <div className="stat-header">
            <span className="stat-icon">🧠</span>
            <span className="stat-label">Decision Fatigue</span>
          </div>
          <div className="stat-bar">
            <div
              className="stat-bar-fill"
              style={{
                width: `${fatiguePercent}%`,
                backgroundColor: '#f59e0b'
              }}
            />
          </div>
          <div className="stat-value">
            {being.decision_fatigue} / {being.decision_quota_max}
          </div>
        </div>

        {/* Luck */}
        <div className="stat-card">
          <div className="stat-header">
            <span className="stat-icon">🍀</span>
            <span className="stat-label">Luck</span>
          </div>
          <div className="stat-number">
            {being.luck?.toFixed(2) || '0.00'}
          </div>
        </div>

        {/* Pleasure */}
        <div className="stat-card">
          <div className="stat-header">
            <span className="stat-icon">😊</span>
            <span className="stat-label">Pleasure</span>
          </div>
          <div className="stat-number positive">
            +{being.pleasure?.toFixed(1) || '0.0'}
          </div>
        </div>

        {/* Pain */}
        <div className="stat-card">
          <div className="stat-header">
            <span className="stat-icon">😣</span>
            <span className="stat-label">Pain</span>
          </div>
          <div className="stat-number negative">
            -{being.pain?.toFixed(1) || '0.0'}
          </div>
        </div>
      </div>

      {/* Skills Section */}
      <div className="profile-section">
        <h2 className="section-title">
          <span className="section-icon">⚔️</span>
          Skills & Abilities
        </h2>
        {being.skills && Object.keys(being.skills).length > 0 ? (
          <div className="skills-grid">
            {Object.entries(being.skills).map(([skill, level]) => (
              <div key={skill} className="skill-item">
                <div className="skill-name">{skill}</div>
                <div className="skill-level">
                  <div className="skill-level-bar">
                    <div
                      className="skill-level-fill"
                      style={{ width: `${Math.min(level, 100)}%` }}
                    />
                  </div>
                  <span className="skill-level-text">Lv {level.toFixed(0)}</span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <p>No skills learned yet. Embark on adventures to gain abilities!</p>
          </div>
        )}
      </div>

      {/* Memories Section */}
      <div className="profile-section">
        <h2 className="section-title">
          <span className="section-icon">📜</span>
          Memories & Experiences
        </h2>
        {being.memories && being.memories.length > 0 ? (
          <div className="memories-list">
            {being.memories.slice(0, 5).map((memory, idx) => (
              <div key={idx} className="memory-item">
                <div className="memory-icon">💭</div>
                <div className="memory-content">
                  <div className="memory-text">{memory.description || memory}</div>
                  {memory.timestamp && (
                    <div className="memory-time">{new Date(memory.timestamp).toLocaleString()}</div>
                  )}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <p>No memories recorded yet. Your journey has just begun!</p>
          </div>
        )}
      </div>

      {/* Lessons Learned */}
      <div className="profile-section">
        <h2 className="section-title">
          <span className="section-icon">📖</span>
          Lessons Learned
        </h2>
        {being.lessons_learned && being.lessons_learned.length > 0 ? (
          <div className="lessons-list">
            {being.lessons_learned.slice(0, 5).map((lesson, idx) => (
              <div key={idx} className="lesson-item">
                <span className="lesson-bullet">✨</span>
                <span className="lesson-text">{lesson.lesson || lesson}</span>
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <p>No lessons learned yet. Wisdom comes with experience!</p>
          </div>
        )}
      </div>

      {/* Status Info */}
      <div className="profile-footer">
        <div className="footer-info">
          <div className="footer-item">
            <span className="footer-label">State:</span>
            <span className="footer-value">{being.state || 'SPAWNING'}</span>
          </div>
          <div className="footer-item">
            <span className="footer-label">Soul ID:</span>
            <span className="footer-value">{being.soul_id?.slice(0, 12) || 'N/A'}...</span>
          </div>
          {being.empirica_session_id && (
            <div className="footer-item">
              <span className="footer-label">Empirica:</span>
              <span className="footer-value empirica">{being.empirica_session_id.slice(0, 12)}...</span>
            </div>
          )}
        </div>
        {being.is_sleeping && (
          <div className="sleeping-banner">
            😴 Avatar is resting and recovering strength
          </div>
        )}
      </div>
    </div>
  )
}

export default BeingProfile
