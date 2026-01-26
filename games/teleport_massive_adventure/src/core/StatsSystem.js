/**
 * StatsSystem - Character Stats, HP, XP, Leveling
 * 
 * ════════════════════════════════════════════════════════════════════════════
 * Manages all character statistics including:
 * - HP (Health Points) - Current and maximum health
 * - XP (Experience Points) - Accumulated experience
 * - Level - Character progression level
 * - Combat Stats - Attack, Defense, Speed, etc.
 * ════════════════════════════════════════════════════════════════════════════
 */

// ════════════════════════════════════════════════════════════════════════════
// CONFIGURATION
// ════════════════════════════════════════════════════════════════════════════

const STATS_CONFIG = {
    // Base stats for level 1
    BASE_STATS: {
        hp: 100,
        maxHp: 100,
        attack: 10,
        defense: 5,
        speed: 10,
        luck: 5,
        critical: 5  // Critical hit chance %
    },
    
    // XP required per level (level -> XP needed)
    XP_TABLE: [
        0,      // Level 0 (unused)
        0,      // Level 1 (starting)
        100,    // Level 2
        250,    // Level 3
        500,    // Level 4
        850,    // Level 5
        1300,   // Level 6
        1900,   // Level 7
        2600,   // Level 8
        3500,   // Level 9
        5000    // Level 10 (max)
    ],
    
    // Stat gains per level
    LEVEL_UP_GAINS: {
        maxHp: 15,
        attack: 3,
        defense: 2,
        speed: 1,
        luck: 1,
        critical: 1
    },
    
    // Max level
    MAX_LEVEL: 10,
    
    // HP regeneration rate (per second, out of combat)
    HP_REGEN_RATE: 1,
    HP_REGEN_DELAY: 5000,  // Delay after taking damage
    
    // Status effect durations (ms)
    STATUS_DURATIONS: {
        poison: 10000,
        burn: 8000,
        freeze: 5000,
        stun: 2000,
        buff: 15000,
        debuff: 10000
    }
};

// ════════════════════════════════════════════════════════════════════════════
// STATS SYSTEM CLASS
// ════════════════════════════════════════════════════════════════════════════

class StatsSystem {
    constructor() {
        // Character stats registry (characterId -> stats)
        this.characters = new Map();
        
        // Event listeners
        this.listeners = new Map();
        
        // Status effects tracking
        this.statusEffects = new Map();
        
        // HP regen timers
        this.regenTimers = new Map();
        
        this._log('StatsSystem initialized');
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // CHARACTER REGISTRATION
    // ════════════════════════════════════════════════════════════════════════
    
    /**
     * Register a new character with stats
     * @param {string} characterId - Unique character identifier
     * @param {object} options - Initial stats override
     * @returns {object} Character stats object
     */
    registerCharacter(characterId, options = {}) {
        if (this.characters.has(characterId)) {
            this._log(`Character ${characterId} already registered, returning existing`);
            return this.characters.get(characterId);
        }
        
        const stats = {
            id: characterId,
            name: options.name || characterId,
            type: options.type || 'player',  // player, npc, enemy, boss
            
            // Level & XP
            level: options.level || 1,
            xp: options.xp || 0,
            xpToNextLevel: STATS_CONFIG.XP_TABLE[2] || 100,
            
            // Health
            hp: options.hp || STATS_CONFIG.BASE_STATS.hp,
            maxHp: options.maxHp || STATS_CONFIG.BASE_STATS.maxHp,
            
            // Combat stats
            attack: options.attack || STATS_CONFIG.BASE_STATS.attack,
            defense: options.defense || STATS_CONFIG.BASE_STATS.defense,
            speed: options.speed || STATS_CONFIG.BASE_STATS.speed,
            luck: options.luck || STATS_CONFIG.BASE_STATS.luck,
            critical: options.critical || STATS_CONFIG.BASE_STATS.critical,
            
            // Combat state
            isAlive: true,
            inCombat: false,
            lastDamageTime: 0,
            
            // Status effects
            statusEffects: [],
            
            // Modifiers (buffs/debuffs)
            modifiers: {
                attack: 0,
                defense: 0,
                speed: 0,
                luck: 0,
                critical: 0
            }
        };
        
        // Apply level scaling if starting above level 1
        if (stats.level > 1) {
            this._applyLevelScaling(stats, stats.level);
        }
        
        this.characters.set(characterId, stats);
        this._emit('characterRegistered', { characterId, stats });
        this._log(`Registered character: ${characterId} (Level ${stats.level})`);
        
        return stats;
    }
    
    /**
     * Get character stats
     * @param {string} characterId 
     * @returns {object|null}
     */
    getStats(characterId) {
        return this.characters.get(characterId) || null;
    }
    
    /**
     * Remove a character from the system
     * @param {string} characterId 
     */
    unregisterCharacter(characterId) {
        if (this.characters.has(characterId)) {
            this.characters.delete(characterId);
            this.statusEffects.delete(characterId);
            this._clearRegenTimer(characterId);
            this._emit('characterUnregistered', { characterId });
            this._log(`Unregistered character: ${characterId}`);
        }
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // HP MANAGEMENT
    // ════════════════════════════════════════════════════════════════════════
    
    /**
     * Deal damage to a character
     * @param {string} characterId - Target character
     * @param {number} amount - Raw damage amount
     * @param {object} options - Damage options
     * @returns {object} Damage result
     */
    damage(characterId, amount, options = {}) {
        const stats = this.getStats(characterId);
        if (!stats || !stats.isAlive) {
            return { success: false, reason: 'invalid_target' };
        }
        
        // Calculate effective defense
        const effectiveDefense = Math.max(0, stats.defense + stats.modifiers.defense);
        
        // Calculate damage reduction (diminishing returns formula)
        let reduction = effectiveDefense / (effectiveDefense + 50);
        
        // Bypass defense if specified
        if (options.ignoreDefense) {
            reduction = 0;
        }
        
        // Apply reduction
        let finalDamage = Math.max(1, Math.floor(amount * (1 - reduction)));
        
        // Critical hit from attacker?
        if (options.isCritical) {
            finalDamage = Math.floor(finalDamage * 1.5);
        }
        
        // Check for drone shield (if player is taking damage)
        if (characterId === 'aziah') {
            const player = window.game?.scene?.scenes?.find(s => s.player)?.player;
            const drone = player?.combatDrone;
            if (drone && drone.abilities.shield.active && drone.abilities.shield.damageReduction) {
                const shieldReduction = drone.abilities.shield.damageReduction;
                finalDamage = Math.max(1, Math.floor(finalDamage * (1 - shieldReduction)));
                this._log(`🛡️ Shield absorbed ${Math.floor(shieldReduction * 100)}% damage`);
            }
        }
        
        // Apply damage
        const previousHp = stats.hp;
        stats.hp = Math.max(0, stats.hp - finalDamage);
        stats.lastDamageTime = Date.now();
        stats.inCombat = true;
        
        // Stop HP regen
        this._clearRegenTimer(characterId);
        
        // Check for death
        if (stats.hp <= 0) {
            stats.isAlive = false;
            this._emit('characterDied', { 
                characterId, 
                stats, 
                killedBy: options.source || 'unknown' 
            });
            this._log(`💀 ${characterId} has died!`);
        }
        
        const result = {
            success: true,
            target: characterId,
            rawDamage: amount,
            finalDamage,
            reduction: Math.floor(reduction * 100),
            previousHp,
            currentHp: stats.hp,
            isCritical: options.isCritical || false,
            isDead: !stats.isAlive
        };
        
        this._emit('damageTaken', result);
        this._log(`⚔️ ${characterId} took ${finalDamage} damage (${previousHp} → ${stats.hp})`);
        
        return result;
    }
    
    /**
     * Heal a character
     * @param {string} characterId 
     * @param {number} amount 
     * @param {object} options 
     * @returns {object} Heal result
     */
    heal(characterId, amount, options = {}) {
        const stats = this.getStats(characterId);
        if (!stats) {
            return { success: false, reason: 'invalid_target' };
        }
        
        // Can't heal dead characters (unless reviving)
        if (!stats.isAlive && !options.revive) {
            return { success: false, reason: 'target_dead' };
        }
        
        // Revive if needed
        if (!stats.isAlive && options.revive) {
            stats.isAlive = true;
            this._emit('characterRevived', { characterId });
            this._log(`✨ ${characterId} has been revived!`);
        }
        
        const previousHp = stats.hp;
        stats.hp = Math.min(stats.maxHp, stats.hp + amount);
        const actualHeal = stats.hp - previousHp;
        
        const result = {
            success: true,
            target: characterId,
            requestedHeal: amount,
            actualHeal,
            previousHp,
            currentHp: stats.hp,
            maxHp: stats.maxHp
        };
        
        this._emit('healReceived', result);
        this._log(`💚 ${characterId} healed for ${actualHeal} (${previousHp} → ${stats.hp})`);
        
        return result;
    }
    
    /**
     * Set HP directly (for initialization or special effects)
     * @param {string} characterId 
     * @param {number} hp 
     */
    setHp(characterId, hp) {
        const stats = this.getStats(characterId);
        if (!stats) return;
        
        stats.hp = Math.max(0, Math.min(stats.maxHp, hp));
        if (stats.hp <= 0) {
            stats.isAlive = false;
        } else {
            stats.isAlive = true;
        }
        
        this._emit('hpChanged', { characterId, hp: stats.hp, maxHp: stats.maxHp });
    }
    
    /**
     * Start HP regeneration for a character
     * @param {string} characterId 
     */
    startHpRegen(characterId) {
        const stats = this.getStats(characterId);
        if (!stats || !stats.isAlive || stats.hp >= stats.maxHp) return;
        
        // Clear existing timer
        this._clearRegenTimer(characterId);
        
        // Start regen after delay
        const timerId = setTimeout(() => {
            this._regenTick(characterId);
        }, STATS_CONFIG.HP_REGEN_DELAY);
        
        this.regenTimers.set(characterId, timerId);
    }
    
    _regenTick(characterId) {
        const stats = this.getStats(characterId);
        if (!stats || !stats.isAlive || stats.inCombat) {
            this._clearRegenTimer(characterId);
            return;
        }
        
        // Check if enough time since last damage
        const timeSinceDamage = Date.now() - stats.lastDamageTime;
        if (timeSinceDamage < STATS_CONFIG.HP_REGEN_DELAY) {
            // Reschedule
            const delay = STATS_CONFIG.HP_REGEN_DELAY - timeSinceDamage;
            const timerId = setTimeout(() => this._regenTick(characterId), delay);
            this.regenTimers.set(characterId, timerId);
            return;
        }
        
        // Apply regen
        if (stats.hp < stats.maxHp) {
            this.heal(characterId, STATS_CONFIG.HP_REGEN_RATE, { source: 'regen' });
            
            // Continue regen
            const timerId = setTimeout(() => this._regenTick(characterId), 1000);
            this.regenTimers.set(characterId, timerId);
        } else {
            this._clearRegenTimer(characterId);
        }
    }
    
    _clearRegenTimer(characterId) {
        const timerId = this.regenTimers.get(characterId);
        if (timerId) {
            clearTimeout(timerId);
            this.regenTimers.delete(characterId);
        }
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // XP & LEVELING
    // ════════════════════════════════════════════════════════════════════════
    
    /**
     * Award XP to a character
     * @param {string} characterId 
     * @param {number} amount 
     * @param {string} source - Source of XP (combat, quest, discovery)
     * @returns {object} XP result with level up info
     */
    grantXp(characterId, amount, source = 'unknown') {
        const stats = this.getStats(characterId);
        if (!stats) {
            return { success: false, reason: 'invalid_target' };
        }
        
        // Can't gain XP if at max level
        if (stats.level >= STATS_CONFIG.MAX_LEVEL) {
            return { 
                success: true, 
                xpGained: 0, 
                reason: 'max_level',
                level: stats.level 
            };
        }
        
        const previousXp = stats.xp;
        const previousLevel = stats.level;
        
        stats.xp += amount;
        
        // Check for level ups
        const levelUps = [];
        while (
            stats.level < STATS_CONFIG.MAX_LEVEL && 
            stats.xp >= STATS_CONFIG.XP_TABLE[stats.level + 1]
        ) {
            stats.level++;
            const gains = this._applyLevelUp(stats);
            levelUps.push({
                newLevel: stats.level,
                gains
            });
            
            this._emit('levelUp', { 
                characterId, 
                level: stats.level, 
                gains 
            });
            
            this._log(`🎉 ${characterId} leveled up to ${stats.level}!`);
        }
        
        // Update XP to next level
        if (stats.level < STATS_CONFIG.MAX_LEVEL) {
            stats.xpToNextLevel = STATS_CONFIG.XP_TABLE[stats.level + 1];
        } else {
            stats.xpToNextLevel = null;  // Max level
        }
        
        const result = {
            success: true,
            target: characterId,
            xpGained: amount,
            source,
            previousXp,
            currentXp: stats.xp,
            previousLevel,
            currentLevel: stats.level,
            xpToNextLevel: stats.xpToNextLevel,
            levelUps
        };
        
        this._emit('xpGained', result);
        this._log(`⭐ ${characterId} gained ${amount} XP (${source})`);
        
        return result;
    }
    
    /**
     * Apply stat gains for leveling up
     * @private
     */
    _applyLevelUp(stats) {
        const gains = { ...STATS_CONFIG.LEVEL_UP_GAINS };
        
        // Apply gains
        stats.maxHp += gains.maxHp;
        stats.hp = stats.maxHp;  // Full heal on level up
        stats.attack += gains.attack;
        stats.defense += gains.defense;
        stats.speed += gains.speed;
        stats.luck += gains.luck;
        stats.critical += gains.critical;
        
        return gains;
    }
    
    /**
     * Apply level scaling for characters starting above level 1
     * @private
     */
    _applyLevelScaling(stats, targetLevel) {
        for (let i = 1; i < targetLevel; i++) {
            this._applyLevelUp(stats);
        }
    }
    
    /**
     * Get XP progress percentage to next level
     * @param {string} characterId 
     * @returns {number} Percentage (0-100)
     */
    getXpProgress(characterId) {
        const stats = this.getStats(characterId);
        if (!stats || stats.level >= STATS_CONFIG.MAX_LEVEL) return 100;
        
        const currentLevelXp = STATS_CONFIG.XP_TABLE[stats.level];
        const nextLevelXp = STATS_CONFIG.XP_TABLE[stats.level + 1];
        const xpIntoLevel = stats.xp - currentLevelXp;
        const xpNeeded = nextLevelXp - currentLevelXp;
        
        return Math.floor((xpIntoLevel / xpNeeded) * 100);
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // STAT MODIFIERS
    // ════════════════════════════════════════════════════════════════════════
    
    /**
     * Apply a temporary modifier (buff/debuff)
     * @param {string} characterId 
     * @param {string} stat - Stat to modify
     * @param {number} amount - Modifier amount (positive = buff, negative = debuff)
     * @param {number} duration - Duration in ms (0 = permanent until removed)
     * @param {string} source - Source of modifier
     * @returns {string} Modifier ID for removal
     */
    applyModifier(characterId, stat, amount, duration = 0, source = 'unknown') {
        const stats = this.getStats(characterId);
        if (!stats || !stats.modifiers.hasOwnProperty(stat)) {
            return null;
        }
        
        const modifierId = `${stat}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        
        // Apply modifier
        stats.modifiers[stat] += amount;
        
        // Track for removal
        const modifierData = {
            id: modifierId,
            stat,
            amount,
            source,
            appliedAt: Date.now(),
            expiresAt: duration > 0 ? Date.now() + duration : null
        };
        
        if (!this.statusEffects.has(characterId)) {
            this.statusEffects.set(characterId, []);
        }
        this.statusEffects.get(characterId).push(modifierData);
        
        // Set expiration timer
        if (duration > 0) {
            setTimeout(() => {
                this.removeModifier(characterId, modifierId);
            }, duration);
        }
        
        const type = amount > 0 ? 'buff' : 'debuff';
        this._emit('modifierApplied', { characterId, stat, amount, type, source, modifierId });
        this._log(`${amount > 0 ? '⬆️' : '⬇️'} ${characterId} ${stat} ${amount > 0 ? '+' : ''}${amount} (${source})`);
        
        return modifierId;
    }
    
    /**
     * Remove a specific modifier
     * @param {string} characterId 
     * @param {string} modifierId 
     */
    removeModifier(characterId, modifierId) {
        const stats = this.getStats(characterId);
        const effects = this.statusEffects.get(characterId);
        
        if (!stats || !effects) return;
        
        const index = effects.findIndex(e => e.id === modifierId);
        if (index !== -1) {
            const modifier = effects[index];
            stats.modifiers[modifier.stat] -= modifier.amount;
            effects.splice(index, 1);
            
            this._emit('modifierRemoved', { characterId, modifierId, stat: modifier.stat });
            this._log(`❌ ${characterId} modifier removed: ${modifier.stat} ${modifier.amount}`);
        }
    }
    
    /**
     * Clear all modifiers for a character
     * @param {string} characterId 
     */
    clearAllModifiers(characterId) {
        const stats = this.getStats(characterId);
        if (!stats) return;
        
        // Reset all modifiers to 0
        Object.keys(stats.modifiers).forEach(stat => {
            stats.modifiers[stat] = 0;
        });
        
        this.statusEffects.set(characterId, []);
        this._emit('modifiersCleared', { characterId });
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // COMBAT STATE
    // ════════════════════════════════════════════════════════════════════════
    
    /**
     * Enter combat state
     * @param {string} characterId 
     */
    enterCombat(characterId) {
        const stats = this.getStats(characterId);
        if (!stats) return;
        
        stats.inCombat = true;
        this._clearRegenTimer(characterId);
        this._emit('combatEntered', { characterId });
    }
    
    /**
     * Exit combat state
     * @param {string} characterId 
     */
    exitCombat(characterId) {
        const stats = this.getStats(characterId);
        if (!stats) return;
        
        stats.inCombat = false;
        this.startHpRegen(characterId);
        this._emit('combatExited', { characterId });
    }
    
    /**
     * Get effective stat value (base + modifiers)
     * @param {string} characterId 
     * @param {string} stat 
     * @returns {number}
     */
    getEffectiveStat(characterId, stat) {
        const stats = this.getStats(characterId);
        if (!stats) return 0;
        
        const base = stats[stat] || 0;
        const modifier = stats.modifiers[stat] || 0;
        return Math.max(0, base + modifier);
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // EVENT SYSTEM
    // ════════════════════════════════════════════════════════════════════════
    
    /**
     * Subscribe to stats events
     * @param {string} event 
     * @param {function} callback 
     * @returns {function} Unsubscribe function
     */
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
    
    // ════════════════════════════════════════════════════════════════════════
    // UTILITIES
    // ════════════════════════════════════════════════════════════════════════
    
    /**
     * Check if character is alive
     * @param {string} characterId 
     * @returns {boolean}
     */
    isAlive(characterId) {
        const stats = this.getStats(characterId);
        return stats?.isAlive ?? false;
    }
    
    /**
     * Get HP percentage
     * @param {string} characterId 
     * @returns {number} 0-100
     */
    getHpPercent(characterId) {
        const stats = this.getStats(characterId);
        if (!stats) return 0;
        return Math.floor((stats.hp / stats.maxHp) * 100);
    }
    
    /**
     * Get all characters of a type
     * @param {string} type 
     * @returns {array}
     */
    getCharactersByType(type) {
        return Array.from(this.characters.values()).filter(c => c.type === type);
    }
    
    /**
     * Debug output
     */
    debug(characterId = null) {
        if (characterId) {
            const stats = this.getStats(characterId);
            console.log(`[StatsSystem] ${characterId}:`, stats);
            return stats;
        } else {
            const all = Object.fromEntries(this.characters);
            console.log('[StatsSystem] All characters:', all);
            return all;
        }
    }
    
    _log(message) {
        console.log(`%c[StatsSystem] ${message}`, 'color: #00ff88');
    }
}

// ════════════════════════════════════════════════════════════════════════════
// SINGLETON EXPORT
// ════════════════════════════════════════════════════════════════════════════

const statsSystem = new StatsSystem();

// Export config for external use
statsSystem.CONFIG = STATS_CONFIG;
