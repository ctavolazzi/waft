/**
 * EventBus - Decoupled event system
 * 
 * Allows game components to communicate without direct dependencies.
 * The God (Architect) observes all events through this bus.
 */
class EventBus {
    constructor() {
        this.listeners = new Map();
        this.history = [];
        this.maxHistory = 100;
    }
    
    // ========================================
    // Core Event System
    // ========================================
    
    on(event, callback, options = {}) {
        if (!this.listeners.has(event)) {
            this.listeners.set(event, new Set());
        }
        
        const listener = { callback, once: options.once || false };
        this.listeners.get(event).add(listener);
        
        // Return unsubscribe function
        return () => this.off(event, callback);
    }
    
    once(event, callback) {
        return this.on(event, callback, { once: true });
    }
    
    off(event, callback) {
        const listeners = this.listeners.get(event);
        if (listeners) {
            listeners.forEach(l => {
                if (l.callback === callback) {
                    listeners.delete(l);
                }
            });
        }
    }
    
    emit(event, data = {}) {
        const timestamp = Date.now();
        const eventRecord = { event, data, timestamp };
        
        // Record history
        this.history.push(eventRecord);
        if (this.history.length > this.maxHistory) {
            this.history.shift();
        }
        
        // Notify listeners
        const listeners = this.listeners.get(event);
        if (listeners) {
            listeners.forEach(listener => {
                listener.callback(data, eventRecord);
                if (listener.once) {
                    listeners.delete(listener);
                }
            });
        }
        
        // Wildcard listeners
        const wildcardListeners = this.listeners.get('*');
        if (wildcardListeners) {
            wildcardListeners.forEach(listener => {
                listener.callback(data, eventRecord);
            });
        }
        
        return eventRecord;
    }
    
    // ========================================
    // Event Categories
    // ========================================
    
    // Game flow events
    static GAME_START = 'game:start';
    static GAME_PAUSE = 'game:pause';
    static GAME_RESUME = 'game:resume';
    static GAME_SAVE = 'game:save';
    static GAME_LOAD = 'game:load';
    
    // Room events
    static ROOM_ENTER = 'room:enter';
    static ROOM_EXIT = 'room:exit';
    static ROOM_LOADED = 'room:loaded';
    
    // Player events
    static PLAYER_MOVE = 'player:move';
    static PLAYER_INTERACT = 'player:interact';
    static PLAYER_EXAMINE = 'player:examine';
    
    // Inventory events
    static ITEM_PICKUP = 'item:pickup';
    static ITEM_USE = 'item:use';
    static ITEM_COMBINE = 'item:combine';
    
    // NPC events
    static NPC_TALK = 'npc:talk';
    static NPC_REACT = 'npc:react';
    
    // Dialogue events
    static DIALOGUE_START = 'dialogue:start';
    static DIALOGUE_ADVANCE = 'dialogue:advance';
    static DIALOGUE_END = 'dialogue:end';
    static DIALOGUE_CHOICE = 'dialogue:choice';
    
    // Puzzle events
    static PUZZLE_ATTEMPT = 'puzzle:attempt';
    static PUZZLE_SOLVE = 'puzzle:solve';
    static PUZZLE_FAIL = 'puzzle:fail';
    
    // Combat events (for boss)
    static COMBAT_START = 'combat:start';
    static COMBAT_ACTION = 'combat:action';
    static COMBAT_DAMAGE = 'combat:damage';
    static COMBAT_END = 'combat:end';
    
    // God events
    static GOD_OBSERVE = 'god:observe';
    static GOD_INTERVENE = 'god:intervene';
    static GOD_COMMENT = 'god:comment';
    
    // ========================================
    // Utility
    // ========================================
    
    getHistory(filter = null) {
        if (!filter) return [...this.history];
        
        return this.history.filter(record => {
            if (typeof filter === 'string') {
                return record.event === filter;
            }
            if (filter instanceof RegExp) {
                return filter.test(record.event);
            }
            return true;
        });
    }
    
    clearHistory() {
        this.history = [];
    }
}

const eventBus = new EventBus();
