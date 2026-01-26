/**
 * GameManager - Central coordinator for all game systems
 * 
 * ════════════════════════════════════════════════════════════════════════════
 * Responsibilities:
 * - System initialization and lifecycle management
 * - Centralized update loop coordination
 * - Dependency injection
 * - Error handling and recovery
 * - System cleanup
 * ════════════════════════════════════════════════════════════════════════════
 */

class GameManager {
    constructor() {
        // System registry
        this.systems = new Map();
        
        // System initialization order (dependencies first)
        this.initOrder = [
            'eventBus',
            'gameState',
            'statsSystem',
            'collisionSystem',
            'combatSystem',
            'npcSystem',
            'dialogueSystem',
            'interactionSystem',
            'theDealer'
        ];
        
        // Update order (systems that need to update each frame)
        this.updateOrder = [
            'collisionSystem',
            'combatSystem',
            'npcSystem'
        ];
        
        // Current scene reference
        this.currentScene = null;
        
        // Update loop state
        this.isUpdating = false;
        this.lastUpdateTime = 0;
        
        // Error handling
        this.errorHandlers = new Map();
        
        this._log('GameManager initialized');
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // SYSTEM REGISTRATION
    // ════════════════════════════════════════════════════════════════════════
    
    /**
     * Register a system with the manager
     * @param {string} name - System identifier
     * @param {object} system - System instance
     * @param {object} options - { initOrder, updateOrder, dependencies }
     */
    registerSystem(name, system, options = {}) {
        if (this.systems.has(name)) {
            console.warn(`[GameManager] System ${name} already registered, replacing...`);
        }
        
        this.systems.set(name, {
            instance: system,
            name: name,
            initialized: false,
            dependencies: options.dependencies || [],
            initOrder: options.initOrder !== undefined ? options.initOrder : this.initOrder.indexOf(name),
            updateOrder: options.updateOrder !== undefined ? options.updateOrder : this.updateOrder.indexOf(name),
            updateEnabled: options.updateEnabled !== false
        });
        
        this._log(`Registered system: ${name}`);
        return this;
    }
    
    /**
     * Get a registered system
     * @param {string} name 
     * @returns {object|null} System instance or null
     */
    getSystem(name) {
        const system = this.systems.get(name);
        return system ? system.instance : null;
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // INITIALIZATION
    // ════════════════════════════════════════════════════════════════════════
    
    /**
     * Initialize all systems in dependency order
     * @param {object} context - Game context (Phaser game instance, etc.)
     */
    async initialize(context = {}) {
        this._log('Initializing all systems...');
        
        // Sort systems by init order
        const sortedSystems = Array.from(this.systems.values())
            .sort((a, b) => {
                // Systems with explicit initOrder come first
                if (a.initOrder !== -1 && b.initOrder === -1) return -1;
                if (a.initOrder === -1 && b.initOrder !== -1) return 1;
                return a.initOrder - b.initOrder;
            });
        
        // Initialize each system
        for (const system of sortedSystems) {
            try {
                await this._initializeSystem(system, context);
            } catch (error) {
                this._handleError(`Failed to initialize ${system.name}`, error);
                // Continue with other systems
            }
        }
        
        this._log('All systems initialized');
        return this;
    }
    
    /**
     * Initialize a single system
     * @private
     */
    async _initializeSystem(system, context) {
        if (system.initialized) {
            this._log(`System ${system.name} already initialized, skipping`);
            return;
        }
        
        // Check dependencies
        for (const dep of system.dependencies) {
            const depSystem = this.systems.get(dep);
            if (!depSystem || !depSystem.initialized) {
                throw new Error(`System ${system.name} depends on ${dep} which is not initialized`);
            }
        }
        
        // Get dependencies for injection
        const dependencies = {};
        for (const dep of system.dependencies) {
            dependencies[dep] = this.getSystem(dep);
        }
        
        // Call init if method exists
        if (typeof system.instance.init === 'function') {
            await system.instance.init({
                ...dependencies,
                ...context,
                gameManager: this
            });
        }
        
        system.initialized = true;
        this._log(`✓ Initialized: ${system.name}`);
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // UPDATE LOOP
    // ════════════════════════════════════════════════════════════════════════
    
    /**
     * Main update loop - called by Phaser scene update()
     * @param {number} time - Current time
     * @param {number} delta - Time since last frame (ms)
     */
    update(time, delta) {
        if (this.isUpdating) {
            // Prevent recursive updates
            return;
        }
        
        this.isUpdating = true;
        this.lastUpdateTime = time;
        
        try {
            // Get player position from current scene
            const playerPos = this._getPlayerPosition();
            
            // Update systems in order
            const sortedSystems = Array.from(this.systems.values())
                .filter(s => s.initialized && s.updateEnabled && s.updateOrder !== -1)
                .sort((a, b) => a.updateOrder - b.updateOrder);
            
            for (const system of sortedSystems) {
                try {
                    if (typeof system.instance.update === 'function') {
                        // Pass delta and context
                        system.instance.update(delta, {
                            time,
                            delta,
                            playerPos,
                            scene: this.currentScene
                        });
                    }
                } catch (error) {
                    this._handleError(`Error updating ${system.name}`, error);
                }
            }
        } finally {
            this.isUpdating = false;
        }
    }
    
    /**
     * Get player position from current scene
     * @private
     */
    _getPlayerPosition() {
        if (!this.currentScene?.player?.sprite) {
            return null;
        }
        
        return {
            x: this.currentScene.player.sprite.x,
            y: this.currentScene.player.sprite.y
        };
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // SCENE MANAGEMENT
    // ════════════════════════════════════════════════════════════════════════
    
    /**
     * Set the current active scene
     * @param {Phaser.Scene} scene 
     */
    setCurrentScene(scene) {
        const previousScene = this.currentScene;
        this.currentScene = scene;
        
        // Notify systems of scene change
        this.systems.forEach((system, name) => {
            if (system.initialized && typeof system.instance.onSceneChange === 'function') {
                try {
                    system.instance.onSceneChange(scene, previousScene);
                } catch (error) {
                    this._handleError(`Error in ${name}.onSceneChange`, error);
                }
            }
        });
        
        this._log(`Scene changed: ${previousScene?.scene?.key || 'none'} → ${scene?.scene?.key || 'none'}`);
    }
    
    /**
     * Cleanup when scene is destroyed
     * @param {Phaser.Scene} scene 
     */
    cleanupScene(scene) {
        this._log(`Cleaning up scene: ${scene?.scene?.key}`);
        
        // Notify systems
        this.systems.forEach((system, name) => {
            if (system.initialized && typeof system.instance.onSceneCleanup === 'function') {
                try {
                    system.instance.onSceneCleanup(scene);
                } catch (error) {
                    this._handleError(`Error in ${name}.onSceneCleanup`, error);
                }
            }
        });
        
        if (this.currentScene === scene) {
            this.currentScene = null;
        }
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // ERROR HANDLING
    // ════════════════════════════════════════════════════════════════════════
    
    /**
     * Register an error handler
     * @param {string} systemName - System to handle errors for (or '*' for all)
     * @param {function} handler - Error handler function
     */
    onError(systemName, handler) {
        if (!this.errorHandlers.has(systemName)) {
            this.errorHandlers.set(systemName, new Set());
        }
        this.errorHandlers.get(systemName).add(handler);
        return this;
    }
    
    /**
     * Handle an error
     * @private
     */
    _handleError(message, error) {
        const errorInfo = {
            message,
            error,
            timestamp: Date.now(),
            systems: Array.from(this.systems.keys())
        };
        
        console.error(`[GameManager] ${message}`, error);
        
        // Call error handlers
        const handlers = [
            ...(this.errorHandlers.get('*') || []),
            ...(this.errorHandlers.get(message.split(' ')[0]) || [])
        ];
        
        handlers.forEach(handler => {
            try {
                handler(errorInfo);
            } catch (e) {
                console.error('[GameManager] Error handler threw exception', e);
            }
        });
        
        // Emit error event if eventBus is available
        const eventBus = this.getSystem('eventBus');
        if (eventBus) {
            eventBus.emit('game:error', errorInfo);
        }
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // UTILITY
    // ════════════════════════════════════════════════════════════════════════
    
    /**
     * Get all system names
     * @returns {string[]}
     */
    getSystemNames() {
        return Array.from(this.systems.keys());
    }
    
    /**
     * Check if a system is initialized
     * @param {string} name 
     * @returns {boolean}
     */
    isSystemInitialized(name) {
        const system = this.systems.get(name);
        return system ? system.initialized : false;
    }
    
    /**
     * Shutdown all systems (cleanup)
     */
    async shutdown() {
        this._log('Shutting down all systems...');
        
        // Shutdown in reverse order
        const sortedSystems = Array.from(this.systems.values())
            .sort((a, b) => b.initOrder - a.initOrder);
        
        for (const system of sortedSystems) {
            if (system.initialized && typeof system.instance.shutdown === 'function') {
                try {
                    await system.instance.shutdown();
                } catch (error) {
                    this._handleError(`Error shutting down ${system.name}`, error);
                }
            }
        }
        
        this.systems.clear();
        this.currentScene = null;
        this._log('All systems shut down');
    }
    
    _log(message) {
        console.log(`%c[GameManager] ${message}`, 'color: #00ff88');
    }
    
    /**
     * Debug: Get system status
     */
    debug() {
        const status = {};
        this.systems.forEach((system, name) => {
            status[name] = {
                initialized: system.initialized,
                updateEnabled: system.updateEnabled,
                dependencies: system.dependencies
            };
        });
        console.log('[GameManager] System Status:', status);
        return status;
    }
}

// Singleton export
const gameManager = new GameManager();
