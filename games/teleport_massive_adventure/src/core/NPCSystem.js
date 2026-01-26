/**
 * NPCSystem - NPC AI, Patrol, and Behavior
 * 
 * ════════════════════════════════════════════════════════════════════════════
 * Handles all NPC behaviors including:
 * - Patrol routes (waypoint following)
 * - Idle behaviors
 * - Detection and aggro
 * - Combat AI
 * - State machines
 * ════════════════════════════════════════════════════════════════════════════
 */

// ════════════════════════════════════════════════════════════════════════════
// CONFIGURATION
// ════════════════════════════════════════════════════════════════════════════

const NPC_CONFIG = {
    // Movement speeds (pixels per second)
    SPEEDS: {
        patrol: 40,
        chase: 80,
        return: 50,
        wander: 30
    },
    
    // Detection ranges
    DETECTION: {
        sight: 150,       // How far NPCs can see
        hearing: 80,      // Radius for hearing sounds
        peripheral: 60,   // Side vision range
        sightAngle: 90    // Field of view in degrees
    },
    
    // Timing (ms)
    TIMING: {
        idleMin: 2000,
        idleMax: 5000,
        patrolPause: 1000,    // Pause at waypoints
        searchTime: 5000,     // How long to search for player
        forgetTime: 10000,    // Time to forget player
        attackCooldown: 1500  // Time between attacks
    },
    
    // State colors (for debug)
    STATE_COLORS: {
        idle: 0x00ff00,      // Green
        patrol: 0x0000ff,    // Blue
        alert: 0xffff00,     // Yellow
        chase: 0xff0000,     // Red
        attack: 0xff00ff,    // Magenta
        search: 0xff8800,    // Orange
        return: 0x00ffff     // Cyan
    }
};

// ════════════════════════════════════════════════════════════════════════════
// NPC STATES
// ════════════════════════════════════════════════════════════════════════════

const NPCState = {
    IDLE: 'idle',
    PATROL: 'patrol',
    ALERT: 'alert',
    CHASE: 'chase',
    ATTACK: 'attack',
    SEARCH: 'search',
    RETURN: 'return',
    DEAD: 'dead'
};

// ════════════════════════════════════════════════════════════════════════════
// NPC CLASS
// ════════════════════════════════════════════════════════════════════════════

class NPC {
    constructor(id, options = {}) {
        this.id = id;
        this.name = options.name || id;
        this.type = options.type || 'guard';  // guard, patrol, static, boss
        
        // Position & Movement
        this.x = options.x || 0;
        this.y = options.y || 0;
        this.spawnX = this.x;
        this.spawnY = this.y;
        this.velocityX = 0;
        this.velocityY = 0;
        this.facing = options.facing || 'south';  // north, south, east, west
        this.speed = options.speed || NPC_CONFIG.SPEEDS.patrol;
        
        // State Machine
        this.state = NPCState.IDLE;
        this.previousState = null;
        this.stateTime = 0;
        this.stateData = {};
        
        // Patrol
        this.patrolRoute = options.patrolRoute || [];
        this.currentWaypoint = 0;
        this.patrolLoop = options.patrolLoop !== false;  // Loop by default
        this.patrolReverse = false;
        
        // Detection
        this.detectionRange = options.detectionRange || NPC_CONFIG.DETECTION.sight;
        this.canSeePlayer = false;
        this.lastKnownPlayerPos = null;
        this.alertLevel = 0;  // 0-100
        
        // Combat
        this.hostile = options.hostile !== false;
        this.attackRange = options.attackRange || 40;
        this.attackCooldown = 0;
        this.target = null;
        
        // Animation
        this.currentAnimation = 'idle';
        this.animationFrame = 0;
        
        // Callbacks
        this.onStateChange = options.onStateChange || null;
        this.onDetectPlayer = options.onDetectPlayer || null;
        this.onAttack = options.onAttack || null;
        this.onDeath = options.onDeath || null;
        
        // Debug
        this.debugPath = [];
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // STATE MACHINE
    // ════════════════════════════════════════════════════════════════════════
    
    setState(newState, data = {}) {
        if (this.state === newState) return;
        
        this.previousState = this.state;
        this.state = newState;
        this.stateTime = 0;
        this.stateData = data;
        
        // State enter logic
        this._onStateEnter(newState);
        
        // Callback
        this.onStateChange?.(this, newState, this.previousState);
        
        console.log(`%c[NPC:${this.id}] ${this.previousState} → ${newState}`, 
            `color: ${this._getStateColorHex(newState)}`);
    }
    
    _onStateEnter(state) {
        switch (state) {
            case NPCState.IDLE:
                this.stateData.idleTime = this._randomRange(
                    NPC_CONFIG.TIMING.idleMin,
                    NPC_CONFIG.TIMING.idleMax
                );
                this.velocityX = 0;
                this.velocityY = 0;
                break;
                
            case NPCState.PATROL:
                this.speed = NPC_CONFIG.SPEEDS.patrol;
                break;
                
            case NPCState.ALERT:
                this.stateData.alertStart = Date.now();
                this.velocityX = 0;
                this.velocityY = 0;
                break;
                
            case NPCState.CHASE:
                this.speed = NPC_CONFIG.SPEEDS.chase;
                break;
                
            case NPCState.SEARCH:
                this.stateData.searchStart = Date.now();
                this.speed = NPC_CONFIG.SPEEDS.patrol;
                break;
                
            case NPCState.RETURN:
                this.speed = NPC_CONFIG.SPEEDS.return;
                this.stateData.returnTarget = this.patrolRoute.length > 0 
                    ? this.patrolRoute[this.currentWaypoint]
                    : { x: this.spawnX, y: this.spawnY };
                break;
                
            case NPCState.DEAD:
                this.velocityX = 0;
                this.velocityY = 0;
                this.onDeath?.(this);
                break;
        }
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // UPDATE LOOP
    // ════════════════════════════════════════════════════════════════════════
    
    update(delta, playerPos = null) {
        if (this.state === NPCState.DEAD) return;
        
        this.stateTime += delta;
        
        // Update detection
        if (playerPos) {
            this._updateDetection(playerPos);
        }
        
        // Update current state
        switch (this.state) {
            case NPCState.IDLE:
                this._updateIdle(delta);
                break;
            case NPCState.PATROL:
                this._updatePatrol(delta);
                break;
            case NPCState.ALERT:
                this._updateAlert(delta);
                break;
            case NPCState.CHASE:
                this._updateChase(delta, playerPos);
                break;
            case NPCState.ATTACK:
                this._updateAttack(delta, playerPos);
                break;
            case NPCState.SEARCH:
                this._updateSearch(delta);
                break;
            case NPCState.RETURN:
                this._updateReturn(delta);
                break;
        }
        
        // Apply velocity
        this.x += this.velocityX * (delta / 1000);
        this.y += this.velocityY * (delta / 1000);
        
        // Update facing based on velocity
        this._updateFacing();
        
        // Update attack cooldown
        if (this.attackCooldown > 0) {
            this.attackCooldown -= delta;
        }
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // STATE UPDATES
    // ════════════════════════════════════════════════════════════════════════
    
    _updateIdle(delta) {
        // Check for player detection
        if (this.canSeePlayer && this.hostile) {
            this.setState(NPCState.ALERT);
            return;
        }
        
        // After idle time, start patrol
        if (this.stateTime >= this.stateData.idleTime) {
            if (this.patrolRoute.length > 0) {
                this.setState(NPCState.PATROL);
            } else {
                // Reset idle timer for static NPCs
                this.stateData.idleTime = this._randomRange(
                    NPC_CONFIG.TIMING.idleMin,
                    NPC_CONFIG.TIMING.idleMax
                );
                this.stateTime = 0;
            }
        }
    }
    
    _updatePatrol(delta) {
        // Check for player detection
        if (this.canSeePlayer && this.hostile) {
            this.setState(NPCState.ALERT);
            return;
        }
        
        if (this.patrolRoute.length === 0) {
            this.setState(NPCState.IDLE);
            return;
        }
        
        const target = this.patrolRoute[this.currentWaypoint];
        const distance = this._distanceTo(target.x, target.y);
        
        // Reached waypoint?
        if (distance < 5) {
            this.velocityX = 0;
            this.velocityY = 0;
            
            // Pause at waypoint
            if (!this.stateData.pausing) {
                this.stateData.pausing = true;
                this.stateData.pauseEnd = this.stateTime + NPC_CONFIG.TIMING.patrolPause;
            }
            
            if (this.stateTime >= this.stateData.pauseEnd) {
                this.stateData.pausing = false;
                this._advanceWaypoint();
            }
        } else {
            // Move toward waypoint
            this._moveToward(target.x, target.y, this.speed);
        }
    }
    
    _updateAlert(delta) {
        // Look at player
        if (this.lastKnownPlayerPos) {
            this._lookAt(this.lastKnownPlayerPos.x, this.lastKnownPlayerPos.y);
        }
        
        // Alert builds up, then chase
        this.alertLevel = Math.min(100, this.alertLevel + delta * 0.05);
        
        if (this.alertLevel >= 100) {
            if (this.canSeePlayer) {
                this.setState(NPCState.CHASE);
            } else {
                this.setState(NPCState.SEARCH);
            }
        }
        
        // If player leaves detection during alert, go back to patrol
        if (!this.canSeePlayer && this.stateTime > 2000) {
            this.alertLevel = Math.max(0, this.alertLevel - delta * 0.03);
            if (this.alertLevel <= 0) {
                this.setState(NPCState.PATROL);
            }
        }
    }
    
    _updateChase(delta, playerPos) {
        if (!playerPos) {
            this.setState(NPCState.SEARCH);
            return;
        }
        
        // Lost sight of player?
        if (!this.canSeePlayer) {
            this.lastKnownPlayerPos = { ...playerPos };
            this.setState(NPCState.SEARCH);
            return;
        }
        
        const distance = this._distanceTo(playerPos.x, playerPos.y);
        
        // In attack range?
        if (distance <= this.attackRange) {
            this.setState(NPCState.ATTACK, { target: playerPos });
        } else {
            // Chase player
            this._moveToward(playerPos.x, playerPos.y, this.speed);
        }
    }
    
    _updateAttack(delta, playerPos) {
        if (!playerPos) {
            this.setState(NPCState.SEARCH);
            return;
        }
        
        const distance = this._distanceTo(playerPos.x, playerPos.y);
        
        // Player moved out of range?
        if (distance > this.attackRange * 1.5) {
            this.setState(NPCState.CHASE);
            return;
        }
        
        // Stop moving while attacking
        this.velocityX = 0;
        this.velocityY = 0;
        
        // Look at player
        this._lookAt(playerPos.x, playerPos.y);
        
        // Attack when cooldown is ready
        if (this.attackCooldown <= 0) {
            this._performAttack(playerPos);
            this.attackCooldown = NPC_CONFIG.TIMING.attackCooldown;
        }
    }
    
    _updateSearch(delta) {
        const searchElapsed = Date.now() - this.stateData.searchStart;
        
        // Search time expired?
        if (searchElapsed > NPC_CONFIG.TIMING.searchTime) {
            this.setState(NPCState.RETURN);
            return;
        }
        
        // Found player again?
        if (this.canSeePlayer) {
            this.setState(NPCState.CHASE);
            return;
        }
        
        // Move toward last known position
        if (this.lastKnownPlayerPos) {
            const distance = this._distanceTo(
                this.lastKnownPlayerPos.x, 
                this.lastKnownPlayerPos.y
            );
            
            if (distance > 10) {
                this._moveToward(
                    this.lastKnownPlayerPos.x,
                    this.lastKnownPlayerPos.y,
                    this.speed
                );
            } else {
                // Reached last known position, look around
                this.velocityX = 0;
                this.velocityY = 0;
                
                // Rotate periodically
                if (Math.floor(this.stateTime / 1000) % 2 === 0) {
                    const directions = ['north', 'east', 'south', 'west'];
                    const idx = Math.floor(this.stateTime / 1000) % 4;
                    this.facing = directions[idx];
                }
            }
        }
    }
    
    _updateReturn(delta) {
        // Found player while returning?
        if (this.canSeePlayer && this.hostile) {
            this.setState(NPCState.ALERT);
            return;
        }
        
        const target = this.stateData.returnTarget;
        if (!target) {
            this.setState(NPCState.IDLE);
            return;
        }
        
        const distance = this._distanceTo(target.x, target.y);
        
        if (distance < 5) {
            // Reached return point
            this.alertLevel = 0;
            this.lastKnownPlayerPos = null;
            
            if (this.patrolRoute.length > 0) {
                this.setState(NPCState.PATROL);
            } else {
                this.setState(NPCState.IDLE);
            }
        } else {
            this._moveToward(target.x, target.y, this.speed);
        }
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // DETECTION
    // ════════════════════════════════════════════════════════════════════════
    
    _updateDetection(playerPos) {
        const distance = this._distanceTo(playerPos.x, playerPos.y);
        const wasVisible = this.canSeePlayer;
        
        // Simple distance-based detection
        // TODO: Add line-of-sight check with raycasting
        this.canSeePlayer = distance <= this.detectionRange;
        
        // Check if within field of view
        if (this.canSeePlayer) {
            const angle = this._angleTo(playerPos.x, playerPos.y);
            const facingAngle = this._getFacingAngle();
            const angleDiff = Math.abs(this._normalizeAngle(angle - facingAngle));
            
            // Outside field of view?
            if (angleDiff > NPC_CONFIG.DETECTION.sightAngle / 2) {
                // Can still detect if very close (peripheral vision)
                if (distance > NPC_CONFIG.DETECTION.peripheral) {
                    this.canSeePlayer = false;
                }
            }
        }
        
        // Callbacks
        if (this.canSeePlayer && !wasVisible) {
            this.lastKnownPlayerPos = { ...playerPos };
            this.onDetectPlayer?.(this, playerPos);
        }
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // COMBAT
    // ════════════════════════════════════════════════════════════════════════
    
    _performAttack(targetPos) {
        this.currentAnimation = 'attack';
        
        this.onAttack?.(this, {
            x: this.x,
            y: this.y,
            targetX: targetPos.x,
            targetY: targetPos.y,
            facing: this.facing
        });
    }
    
    takeDamage(amount, source = null) {
        // Alert immediately when taking damage
        if (this.state === NPCState.IDLE || this.state === NPCState.PATROL) {
            this.setState(NPCState.ALERT);
            if (source) {
                this.lastKnownPlayerPos = { x: source.x, y: source.y };
            }
        }
    }
    
    die() {
        this.setState(NPCState.DEAD);
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // PATROL MANAGEMENT
    // ════════════════════════════════════════════════════════════════════════
    
    setPatrolRoute(waypoints) {
        this.patrolRoute = waypoints.map(wp => ({
            x: wp.x,
            y: wp.y,
            pauseTime: wp.pauseTime || NPC_CONFIG.TIMING.patrolPause
        }));
        this.currentWaypoint = 0;
    }
    
    addWaypoint(x, y, pauseTime = null) {
        this.patrolRoute.push({
            x,
            y,
            pauseTime: pauseTime || NPC_CONFIG.TIMING.patrolPause
        });
    }
    
    _advanceWaypoint() {
        if (this.patrolLoop) {
            this.currentWaypoint = (this.currentWaypoint + 1) % this.patrolRoute.length;
        } else {
            // Ping-pong patrol
            if (this.patrolReverse) {
                this.currentWaypoint--;
                if (this.currentWaypoint < 0) {
                    this.currentWaypoint = 1;
                    this.patrolReverse = false;
                }
            } else {
                this.currentWaypoint++;
                if (this.currentWaypoint >= this.patrolRoute.length) {
                    this.currentWaypoint = this.patrolRoute.length - 2;
                    this.patrolReverse = true;
                }
            }
        }
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // MOVEMENT HELPERS
    // ════════════════════════════════════════════════════════════════════════
    
    _moveToward(targetX, targetY, speed) {
        const dx = targetX - this.x;
        const dy = targetY - this.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        if (distance > 0) {
            this.velocityX = (dx / distance) * speed;
            this.velocityY = (dy / distance) * speed;
        }
    }
    
    _lookAt(targetX, targetY) {
        const dx = targetX - this.x;
        const dy = targetY - this.y;
        
        // Determine facing based on angle
        if (Math.abs(dx) > Math.abs(dy)) {
            this.facing = dx > 0 ? 'east' : 'west';
        } else {
            this.facing = dy > 0 ? 'south' : 'north';
        }
    }
    
    _updateFacing() {
        if (Math.abs(this.velocityX) < 0.1 && Math.abs(this.velocityY) < 0.1) return;
        
        if (Math.abs(this.velocityX) > Math.abs(this.velocityY)) {
            this.facing = this.velocityX > 0 ? 'east' : 'west';
        } else {
            this.facing = this.velocityY > 0 ? 'south' : 'north';
        }
    }
    
    _distanceTo(x, y) {
        const dx = x - this.x;
        const dy = y - this.y;
        return Math.sqrt(dx * dx + dy * dy);
    }
    
    _angleTo(x, y) {
        return Math.atan2(y - this.y, x - this.x) * (180 / Math.PI);
    }
    
    _getFacingAngle() {
        switch (this.facing) {
            case 'east': return 0;
            case 'south': return 90;
            case 'west': return 180;
            case 'north': return -90;
            default: return 0;
        }
    }
    
    _normalizeAngle(angle) {
        while (angle > 180) angle -= 360;
        while (angle < -180) angle += 360;
        return angle;
    }
    
    _randomRange(min, max) {
        return Math.random() * (max - min) + min;
    }
    
    _getStateColorHex(state) {
        const color = NPC_CONFIG.STATE_COLORS[state] || 0xffffff;
        return `#${color.toString(16).padStart(6, '0')}`;
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // SERIALIZATION
    // ════════════════════════════════════════════════════════════════════════
    
    toJSON() {
        return {
            id: this.id,
            x: this.x,
            y: this.y,
            state: this.state,
            facing: this.facing,
            alertLevel: this.alertLevel,
            currentWaypoint: this.currentWaypoint
        };
    }
}

// ════════════════════════════════════════════════════════════════════════════
// NPC SYSTEM (MANAGER)
// ════════════════════════════════════════════════════════════════════════════

class NPCSystem {
    constructor() {
        this.npcs = new Map();
        this.listeners = new Map();
        
        // References to other systems
        this.statsSystem = null;
        this.combatSystem = null;
        this.collisionSystem = null;
        this.theDealer = null;
        
        this._log('NPCSystem initialized');
    }
    
    /**
     * Initialize with system references
     */
    init(systems) {
        this.statsSystem = systems.statsSystem;
        this.combatSystem = systems.combatSystem;
        this.collisionSystem = systems.collisionSystem;
        this.theDealer = systems.theDealer;
    }
    
    /**
     * Create and register an NPC
     */
    createNPC(id, options = {}) {
        const npc = new NPC(id, options);
        
        // Setup callbacks
        npc.onStateChange = (npc, newState, oldState) => {
            this._emit('stateChange', { npc, newState, oldState });
        };
        
        npc.onDetectPlayer = (npc, playerPos) => {
            this._emit('detectPlayer', { npc, playerPos });
            
            // The Dealer commentary
            if (this.theDealer && npc.hostile) {
                this.theDealer.comment('npc_detect', 
                    `${npc.name} spotted you. *shuffles cards* Things are about to get interesting.`
                );
            }
        };
        
        npc.onAttack = (npc, attackData) => {
            this._emit('attack', { npc, attackData });
            this._handleNPCAttack(npc, attackData);
        };
        
        npc.onDeath = (npc) => {
            this._emit('death', { npc });
        };
        
        // Register with stats if enemy
        if (options.hostile !== false && this.statsSystem) {
            this.statsSystem.registerCharacter(id, {
                name: npc.name,
                type: options.type === 'boss' ? 'boss' : 'enemy',
                hp: options.hp || 40,
                maxHp: options.hp || 40,
                attack: options.attack || 8,
                defense: options.defense || 3
            });
        }
        
        // Register with combat system
        if (this.combatSystem) {
            this.combatSystem.registerCombatant(id, {
                faction: 'enemy',
                hostileTo: ['player']
            });
        }
        
        // Create collision hitbox
        if (this.collisionSystem) {
            const hitbox = this.collisionSystem.createBoxCollider(id, {
                width: options.hitboxWidth || 32,
                height: options.hitboxHeight || 40,
                x: npc.x,
                y: npc.y,
                layer: 'ENEMY',
                userData: { npcId: id }
            });
            npc.colliderId = hitbox.id;
        }
        
        this.npcs.set(id, npc);
        this._log(`Created NPC: ${id} (${npc.type})`);
        
        return npc;
    }
    
    /**
     * Get an NPC by ID
     */
    getNPC(id) {
        return this.npcs.get(id);
    }
    
    /**
     * Remove an NPC
     */
    removeNPC(id) {
        const npc = this.npcs.get(id);
        if (npc) {
            // Cleanup collision
            if (npc.colliderId && this.collisionSystem) {
                this.collisionSystem.removeCollider(npc.colliderId);
            }
            
            // Cleanup stats
            if (this.statsSystem) {
                this.statsSystem.unregisterCharacter(id);
            }
            
            // Cleanup combat
            if (this.combatSystem) {
                this.combatSystem.unregisterCombatant(id);
            }
            
            this.npcs.delete(id);
        }
    }
    
    /**
     * Update all NPCs
     * @param {number} delta - Time since last frame (ms)
     * @param {object} context - Update context { time, delta, playerPos, scene }
     */
    update(delta, context = {}) {
        // Support both old API (delta, playerPos) and new API (delta, context)
        const playerPos = context.playerPos || context;
        
        this.npcs.forEach(npc => {
            npc.update(delta, playerPos);
            
            // Update collider position
            if (npc.colliderId && this.collisionSystem) {
                this.collisionSystem.updatePosition(npc.colliderId, npc.x, npc.y);
            }
        });
    }
    
    /**
     * Handle scene changes
     */
    onSceneChange(newScene, oldScene) {
        // Cleanup NPCs from old scene if needed
        if (oldScene) {
            // Could remove scene-specific NPCs here
        }
    }
    
    /**
     * Handle NPC attack
     */
    _handleNPCAttack(npc, attackData) {
        if (!this.combatSystem) return;
        
        // Get player ID (assumed 'aziah' for now)
        const playerId = 'aziah';
        
        // Get NPC stats for damage
        const npcStats = this.statsSystem?.getStats(npc.id);
        const damage = npcStats?.attack || 8;
        
        // Execute attack through combat system
        this.combatSystem.attack(npc.id, playerId, {
            baseDamage: damage
        });
    }
    
    /**
     * Get all NPCs in a scene/room
     */
    getNPCsInRoom(roomId) {
        return Array.from(this.npcs.values()).filter(npc => npc.roomId === roomId);
    }
    
    /**
     * Notify NPC of damage (from combat system)
     */
    notifyDamage(npcId, amount, source) {
        const npc = this.npcs.get(npcId);
        if (npc) {
            npc.takeDamage(amount, source);
            
            // Check if dead
            const stats = this.statsSystem?.getStats(npcId);
            if (stats && !stats.isAlive) {
                npc.die();
            }
        }
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
    }
    
    _log(message) {
        console.log(`%c[NPCSystem] ${message}`, 'color: #aa44ff');
    }
    
    /**
     * Debug: Get all NPC states
     */
    debug() {
        const states = {};
        this.npcs.forEach((npc, id) => {
            states[id] = {
                state: npc.state,
                position: { x: Math.floor(npc.x), y: Math.floor(npc.y) },
                facing: npc.facing,
                alertLevel: Math.floor(npc.alertLevel),
                canSeePlayer: npc.canSeePlayer
            };
        });
        console.log('[NPCSystem] NPC States:', states);
        return states;
    }
}

// ════════════════════════════════════════════════════════════════════════════
// SINGLETON EXPORT
// ════════════════════════════════════════════════════════════════════════════

const npcSystem = new NPCSystem();

// Export config and classes
npcSystem.CONFIG = NPC_CONFIG;
npcSystem.State = NPCState;
npcSystem.NPC = NPC;
