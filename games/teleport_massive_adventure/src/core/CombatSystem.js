/**
 * CombatSystem - Combat Mechanics & Damage Resolution
 * 
 * ════════════════════════════════════════════════════════════════════════════
 * Coordinates combat between entities:
 * - Attack/damage resolution
 * - Defense calculations
 * - Critical hits
 * - XP rewards
 * - Combat events
 * ════════════════════════════════════════════════════════════════════════════
 */

// ════════════════════════════════════════════════════════════════════════════
// CONFIGURATION
// ════════════════════════════════════════════════════════════════════════════

const COMBAT_CONFIG = {
    // Base damage variance (+/- percent)
    DAMAGE_VARIANCE: 0.15,
    
    // Critical hit multiplier
    CRIT_MULTIPLIER: 1.5,
    
    // XP rewards by enemy type
    XP_REWARDS: {
        enemy: 25,
        boss: 100,
        miniboss: 50,
        npc: 0  // No XP for killing NPCs
    },
    
    // Combat timing (ms)
    ATTACK_COOLDOWN: 500,      // Minimum time between attacks
    INVINCIBILITY_FRAMES: 500, // After taking damage
    COMBO_WINDOW: 1000,        // Time to continue combo
    
    // Knockback
    KNOCKBACK_FORCE: 150,
    KNOCKBACK_DURATION: 200,
    
    // Combat log
    MAX_LOG_ENTRIES: 50,
    
    // Difficulty scaling (multipliers)
    DIFFICULTY: {
        easy: { damageToPlayer: 0.75, xpMultiplier: 0.8 },
        normal: { damageToPlayer: 1.0, xpMultiplier: 1.0 },
        hard: { damageToPlayer: 1.5, xpMultiplier: 1.25 },
        nightmare: { damageToPlayer: 2.0, xpMultiplier: 1.5 }
    }
};

// ════════════════════════════════════════════════════════════════════════════
// COMBAT SYSTEM CLASS
// ════════════════════════════════════════════════════════════════════════════

class CombatSystem {
    constructor() {
        // References to other systems (set via init)
        this.statsSystem = null;
        this.collisionSystem = null;
        this.eventBus = null;
        this.theDealer = null;
        
        // Combat state tracking
        this.combatants = new Map();  // entityId -> combat state
        this.combatLog = [];
        
        // Current difficulty
        this.difficulty = 'normal';
        
        // Event listeners
        this.listeners = new Map();
        
        this._log('CombatSystem initialized');
    }
    
    /**
     * Initialize with system references
     * @param {object} systems - { statsSystem, collisionSystem, eventBus, theDealer }
     */
    init(systems) {
        this.statsSystem = systems.statsSystem;
        this.collisionSystem = systems.collisionSystem;
        this.eventBus = systems.eventBus;
        this.theDealer = systems.theDealer;
        
        // Subscribe to collision events for combat
        if (this.collisionSystem) {
            this.collisionSystem.on('triggerEnter', (collision) => {
                this._handleCombatCollision(collision);
            });
        }
        
        this._log('CombatSystem connected to other systems');
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // COMBATANT MANAGEMENT
    // ════════════════════════════════════════════════════════════════════════
    
    /**
     * Register an entity for combat
     * @param {string} entityId 
     * @param {object} options 
     */
    registerCombatant(entityId, options = {}) {
        const state = {
            entityId,
            lastAttackTime: 0,
            lastDamageTime: 0,
            comboCount: 0,
            comboLastTime: 0,
            isInvincible: false,
            isAttacking: false,
            knockbackVelocity: { x: 0, y: 0 },
            knockbackEndTime: 0,
            
            // Combat modifiers
            damageMultiplier: options.damageMultiplier || 1.0,
            defenseMultiplier: options.defenseMultiplier || 1.0,
            critBonus: options.critBonus || 0,
            
            // Combat role
            faction: options.faction || 'neutral',  // player, enemy, neutral
            hostileTo: options.hostileTo || []
        };
        
        this.combatants.set(entityId, state);
        
        // Register with stats system if not already
        if (this.statsSystem && !this.statsSystem.getStats(entityId)) {
            this.statsSystem.registerCharacter(entityId, options.stats || {});
        }
        
        this._log(`Registered combatant: ${entityId} (${state.faction})`);
        return state;
    }
    
    /**
     * Get combatant state
     * @param {string} entityId 
     */
    getCombatant(entityId) {
        return this.combatants.get(entityId);
    }
    
    /**
     * Unregister a combatant
     * @param {string} entityId 
     */
    unregisterCombatant(entityId) {
        this.combatants.delete(entityId);
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // ATTACK SYSTEM
    // ════════════════════════════════════════════════════════════════════════
    
    /**
     * Perform an attack
     * @param {string} attackerId 
     * @param {string} targetId 
     * @param {object} options - Attack options
     * @returns {object} Attack result
     */
    attack(attackerId, targetId, options = {}) {
        const attacker = this.combatants.get(attackerId);
        const target = this.combatants.get(targetId);
        
        if (!attacker || !target) {
            return { success: false, reason: 'invalid_combatant' };
        }
        
        // Check attack cooldown
        const now = Date.now();
        if (now - attacker.lastAttackTime < COMBAT_CONFIG.ATTACK_COOLDOWN) {
            return { success: false, reason: 'cooldown' };
        }
        
        // Check if target is invincible
        if (target.isInvincible) {
            return { success: false, reason: 'target_invincible' };
        }
        
        // Get stats
        const attackerStats = this.statsSystem?.getStats(attackerId);
        const targetStats = this.statsSystem?.getStats(targetId);
        
        if (!attackerStats || !targetStats) {
            return { success: false, reason: 'missing_stats' };
        }
        
        // Calculate base damage
        let baseDamage = options.baseDamage || attackerStats.attack;
        
        // Apply attacker's damage multiplier
        baseDamage *= attacker.damageMultiplier;
        
        // Apply variance
        const variance = 1 + (Math.random() * 2 - 1) * COMBAT_CONFIG.DAMAGE_VARIANCE;
        baseDamage = Math.floor(baseDamage * variance);
        
        // Check for critical hit
        const critChance = (attackerStats.critical + attacker.critBonus) / 100;
        const isCritical = Math.random() < critChance;
        
        // Apply difficulty scaling if target is player
        if (targetStats.type === 'player') {
            const diffSettings = COMBAT_CONFIG.DIFFICULTY[this.difficulty];
            baseDamage = Math.floor(baseDamage * diffSettings.damageToPlayer);
        }
        
        // Deal damage
        const damageResult = this.statsSystem.damage(targetId, baseDamage, {
            source: attackerId,
            isCritical,
            ignoreDefense: options.ignoreDefense
        });
        
        // Update combat state
        attacker.lastAttackTime = now;
        attacker.isAttacking = true;
        
        // Update combo
        if (now - attacker.comboLastTime < COMBAT_CONFIG.COMBO_WINDOW) {
            attacker.comboCount++;
        } else {
            attacker.comboCount = 1;
        }
        attacker.comboLastTime = now;
        
        // Apply invincibility frames to target
        this._applyInvincibilityFrames(targetId);
        
        // Apply knockback
        if (options.knockback !== false) {
            this._applyKnockback(attackerId, targetId, options.knockbackDirection);
        }
        
        // Check for kill
        if (damageResult.isDead) {
            this._handleKill(attackerId, targetId);
        }
        
        // Build result
        const result = {
            success: true,
            attacker: attackerId,
            target: targetId,
            damage: damageResult.finalDamage,
            isCritical,
            combo: attacker.comboCount,
            targetHp: damageResult.currentHp,
            targetMaxHp: targetStats.maxHp,
            isDead: damageResult.isDead
        };
        
        // Log to combat log
        this._addToLog(result);
        
        // Emit events
        this._emit('attack', result);
        
        // The Dealer commentary
        this._dealerCombatComment(result);
        
        // Reset attacking state after animation
        setTimeout(() => {
            attacker.isAttacking = false;
        }, 200);
        
        return result;
    }
    
    /**
     * Create and execute an area attack
     * @param {string} attackerId 
     * @param {object} area - { x, y, width, height } or { x, y, radius }
     * @param {object} options 
     * @returns {array} Results for each hit target
     */
    areaAttack(attackerId, area, options = {}) {
        if (!this.collisionSystem) {
            return [];
        }
        
        const attacker = this.combatants.get(attackerId);
        if (!attacker) return [];
        
        // Query for targets in area
        let targets;
        if (area.radius) {
            targets = this.collisionSystem.queryRadius(
                area.x, area.y, area.radius,
                this.collisionSystem.CONFIG.LAYERS.ENEMY | 
                this.collisionSystem.CONFIG.LAYERS.NPC
            );
        } else {
            targets = this.collisionSystem.queryBox(
                area.x, area.y, area.width, area.height,
                this.collisionSystem.CONFIG.LAYERS.ENEMY | 
                this.collisionSystem.CONFIG.LAYERS.NPC
            );
        }
        
        // Attack each valid target
        const results = [];
        targets.forEach(hit => {
            const target = hit.collider || hit;
            const targetId = target.entityId;
            
            // Check if hostile
            if (this._isHostile(attackerId, targetId)) {
                const result = this.attack(attackerId, targetId, options);
                if (result.success) {
                    results.push(result);
                }
            }
        });
        
        return results;
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // COMBAT EFFECTS
    // ════════════════════════════════════════════════════════════════════════
    
    /**
     * Apply invincibility frames after taking damage
     */
    _applyInvincibilityFrames(entityId) {
        const combatant = this.combatants.get(entityId);
        if (!combatant) return;
        
        combatant.isInvincible = true;
        combatant.lastDamageTime = Date.now();
        
        setTimeout(() => {
            combatant.isInvincible = false;
        }, COMBAT_CONFIG.INVINCIBILITY_FRAMES);
    }
    
    /**
     * Apply knockback effect
     */
    _applyKnockback(attackerId, targetId, direction = null) {
        const attacker = this.combatants.get(attackerId);
        const target = this.combatants.get(targetId);
        
        if (!attacker || !target) return;
        
        // Calculate knockback direction
        let kbDir = direction;
        if (!kbDir) {
            // Default: away from attacker
            const attackerStats = this.statsSystem?.getStats(attackerId);
            const targetStats = this.statsSystem?.getStats(targetId);
            
            // This would need position data - simplified for now
            kbDir = { x: 1, y: 0 };
        }
        
        // Normalize and apply force
        const len = Math.sqrt(kbDir.x * kbDir.x + kbDir.y * kbDir.y) || 1;
        target.knockbackVelocity = {
            x: (kbDir.x / len) * COMBAT_CONFIG.KNOCKBACK_FORCE,
            y: (kbDir.y / len) * COMBAT_CONFIG.KNOCKBACK_FORCE
        };
        target.knockbackEndTime = Date.now() + COMBAT_CONFIG.KNOCKBACK_DURATION;
        
        this._emit('knockback', { entityId: targetId, velocity: target.knockbackVelocity });
    }
    
    /**
     * Handle entity being killed
     */
    _handleKill(killerId, victimId) {
        const killer = this.combatants.get(killerId);
        const killerStats = this.statsSystem?.getStats(killerId);
        const victimStats = this.statsSystem?.getStats(victimId);
        
        if (!killerStats || !victimStats) return;
        
        // Award XP
        const baseXp = COMBAT_CONFIG.XP_REWARDS[victimStats.type] || 10;
        const diffSettings = COMBAT_CONFIG.DIFFICULTY[this.difficulty];
        const xpReward = Math.floor(baseXp * diffSettings.xpMultiplier);
        
        if (xpReward > 0) {
            this.statsSystem.grantXp(killerId, xpReward, 'combat');
        }
        
        // Emit kill event
        this._emit('kill', {
            killer: killerId,
            victim: victimId,
            xpAwarded: xpReward
        });
        
        // Log
        this._log(`💀 ${killerId} killed ${victimId} (+${xpReward} XP)`);
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // COLLISION HANDLING
    // ════════════════════════════════════════════════════════════════════════
    
    /**
     * Handle combat-related collisions
     */
    _handleCombatCollision(collision) {
        const { colliderA, colliderB } = collision;
        
        // Check for attack hitbox collision
        if (colliderA.userData?.isAttackHitbox) {
            this._handleAttackHitboxCollision(colliderA, colliderB);
        } else if (colliderB.userData?.isAttackHitbox) {
            this._handleAttackHitboxCollision(colliderB, colliderA);
        }
    }
    
    _handleAttackHitboxCollision(attackHitbox, targetCollider) {
        const attackerId = attackHitbox.userData.attackerId;
        const targetId = targetCollider.entityId;
        
        // Check if this is a valid target
        if (!this._isHostile(attackerId, targetId)) return;
        
        // Execute attack
        this.attack(attackerId, targetId, {
            baseDamage: attackHitbox.userData.damage,
            knockback: attackHitbox.userData.knockback
        });
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // FACTION & HOSTILITY
    // ════════════════════════════════════════════════════════════════════════
    
    /**
     * Check if two entities are hostile to each other
     */
    _isHostile(entityA, entityB) {
        const combatantA = this.combatants.get(entityA);
        const combatantB = this.combatants.get(entityB);
        
        if (!combatantA || !combatantB) return false;
        
        // Check explicit hostility
        if (combatantA.hostileTo.includes(combatantB.faction)) return true;
        if (combatantB.hostileTo.includes(combatantA.faction)) return true;
        
        // Default hostilities
        if (combatantA.faction === 'player' && combatantB.faction === 'enemy') return true;
        if (combatantA.faction === 'enemy' && combatantB.faction === 'player') return true;
        
        return false;
    }
    
    /**
     * Set faction for an entity
     */
    setFaction(entityId, faction, hostileTo = []) {
        const combatant = this.combatants.get(entityId);
        if (combatant) {
            combatant.faction = faction;
            combatant.hostileTo = hostileTo;
        }
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // THE DEALER COMMENTARY
    // ════════════════════════════════════════════════════════════════════════
    
    _dealerCombatComment(result) {
        if (!this.theDealer) return;
        
        // Critical hit
        if (result.isCritical && result.success) {
            this.theDealer.comment(
                'combat_critical',
                `A critical strike! ${result.damage} damage. *marks it in the Ledger*`
            );
        }
        
        // Kill
        if (result.isDead) {
            this.theDealer.comment(
                'combat_kill',
                `And they're out. One less player at the table.`
            );
        }
        
        // Big combo
        if (result.combo >= 5) {
            this.theDealer.comment(
                'combat_combo',
                `Combo x${result.combo}! Now we're playing for real.`
            );
        }
        
        // Low health (player)
        const targetStats = this.statsSystem?.getStats(result.target);
        if (targetStats?.type === 'player') {
            const hpPercent = (result.targetHp / result.targetMaxHp) * 100;
            if (hpPercent <= 25 && hpPercent > 0) {
                this.theDealer.comment(
                    'combat_low_hp',
                    `Getting dangerous now. Only ${Math.floor(hpPercent)}% HP remaining...`
                );
            }
        }
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // COMBAT LOG
    // ════════════════════════════════════════════════════════════════════════
    
    _addToLog(entry) {
        this.combatLog.push({
            ...entry,
            timestamp: Date.now()
        });
        
        // Trim log if needed
        while (this.combatLog.length > COMBAT_CONFIG.MAX_LOG_ENTRIES) {
            this.combatLog.shift();
        }
    }
    
    getLog(count = 10) {
        return this.combatLog.slice(-count);
    }
    
    clearLog() {
        this.combatLog = [];
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // DIFFICULTY
    // ════════════════════════════════════════════════════════════════════════
    
    setDifficulty(difficulty) {
        if (COMBAT_CONFIG.DIFFICULTY[difficulty]) {
            this.difficulty = difficulty;
            this._emit('difficultyChanged', { difficulty });
            this._log(`Difficulty set to: ${difficulty}`);
        }
    }
    
    getDifficulty() {
        return this.difficulty;
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // FRAME UPDATE
    // ════════════════════════════════════════════════════════════════════════
    
    /**
     * Update combat state each frame
     * @param {number} delta - Time since last frame in ms
     */
    update(delta, context = {}) {
        const now = Date.now();
        
        this.combatants.forEach((combatant, entityId) => {
            // Update knockback
            if (combatant.knockbackEndTime > now) {
                // Apply knockback velocity (would integrate with physics/movement)
                this._emit('knockbackUpdate', {
                    entityId,
                    velocity: combatant.knockbackVelocity,
                    remaining: combatant.knockbackEndTime - now
                });
            } else if (combatant.knockbackVelocity.x !== 0 || combatant.knockbackVelocity.y !== 0) {
                combatant.knockbackVelocity = { x: 0, y: 0 };
            }
            
            // Reset combo if window expired
            if (combatant.comboCount > 0 && now - combatant.comboLastTime > COMBAT_CONFIG.COMBO_WINDOW) {
                if (combatant.comboCount > 1) {
                    this._emit('comboEnded', { entityId, finalCombo: combatant.comboCount });
                }
                combatant.comboCount = 0;
            }
        });
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // EVENT SYSTEM
    // ════════════════════════════════════════════════════════════════════════
    
    on(event, callback) {
        if (!this.listeners.has(event)) {
            this.listeners.set(event, new Set());
        }
        this.listeners.get(event).add(callback);
        return () => this.listeners.get(event)?.delete(callback);
    }
    
    _emit(event, data) {
        this.listeners.get(event)?.forEach(cb => cb(data));
        this.listeners.get('*')?.forEach(cb => cb(event, data));
    }
    
    _log(message) {
        console.log(`%c[CombatSystem] ${message}`, 'color: #ff4444');
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // DEBUG
    // ════════════════════════════════════════════════════════════════════════
    
    debug() {
        console.log('[CombatSystem] Combatants:', Object.fromEntries(this.combatants));
        console.log('[CombatSystem] Recent Log:', this.getLog(5));
        return {
            combatants: Object.fromEntries(this.combatants),
            log: this.getLog(5),
            difficulty: this.difficulty
        };
    }
}

// ════════════════════════════════════════════════════════════════════════════
// SINGLETON EXPORT
// ════════════════════════════════════════════════════════════════════════════

const combatSystem = new CombatSystem();

// Export config for external use
combatSystem.CONFIG = COMBAT_CONFIG;
