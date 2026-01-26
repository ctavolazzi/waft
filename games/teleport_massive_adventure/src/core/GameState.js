/**
 * GameState - Centralized state management
 * 
 * Single source of truth for all game state.
 * Observable pattern for reactive updates.
 */
class GameState {
    constructor() {
        this.state = {
            // Player data
            inventory: [],
            currentRoom: null,
            playerPosition: { x: 0, y: 0 },
            
            // Flags (story progress)
            flags: {},
            
            // Statistics
            stats: {
                roomsVisited: [],
                itemsCollected: [],
                npcsSpokenTo: [],
                puzzlesSolved: 0,
                timeStarted: null,
                timePlayed: 0
            },
            
            // Save/Load
            saveSlot: null
        };
        
        // Observers for reactive updates
        this.observers = new Map();
        
        // Event emitter for flag changes
        this.eventListeners = new Map();
    }
    
    // ========================================
    // Event Emitter (for flag changes)
    // ========================================
    
    on(event, callback) {
        if (!this.eventListeners.has(event)) {
            this.eventListeners.set(event, new Set());
        }
        this.eventListeners.get(event).add(callback);
        return this;
    }
    
    emit(event, data) {
        this.eventListeners.get(event)?.forEach(cb => cb(data));
        return this;
    }
    
    // ========================================
    // State Access
    // ========================================
    
    get(path) {
        return path.split('.').reduce((obj, key) => obj?.[key], this.state);
    }
    
    set(path, value) {
        const keys = path.split('.');
        const last = keys.pop();
        const target = keys.reduce((obj, key) => obj[key] = obj[key] || {}, this.state);
        const oldValue = target[last];
        target[last] = value;
        
        // Notify observers
        this.notify(path, value, oldValue);
        
        // Emit event for flag changes
        if (path.startsWith('flags.')) {
            const flagName = path.replace('flags.', '');
            this.emit('flagChanged', { flag: flagName, value, oldValue });
        }
        
        return this;
    }
    
    // ========================================
    // Flag System
    // ========================================
    
    getFlag(name) {
        return this.state.flags[name] ?? false;
    }
    
    setFlag(name, value = true) {
        const oldValue = this.state.flags[name];
        this.state.flags[name] = value;
        this.notify(`flags.${name}`, value);
        this.emit('flagChanged', { flag: name, value, oldValue });
        return this;
    }
    
    checkCondition(condition) {
        if (!condition) return true;
        
        // Simple flag check
        if (condition.flag) {
            const value = this.getFlag(condition.flag);
            if (condition.equals !== undefined) return value === condition.equals;
            if (condition.notEquals !== undefined) return value !== condition.notEquals;
            return !!value;
        }
        
        // All conditions must be true
        if (condition.all) {
            return condition.all.every(c => this.checkCondition(c));
        }
        
        // Any condition must be true
        if (condition.any) {
            return condition.any.some(c => this.checkCondition(c));
        }
        
        return true;
    }
    
    // ========================================
    // Inventory System
    // ========================================
    
    addItem(item) {
        if (!this.hasItem(item.id)) {
            this.state.inventory.push(item);
            this.state.stats.itemsCollected.push(item.id);
            this.notify('inventory', this.state.inventory);
        }
        return this;
    }
    
    removeItem(itemId) {
        const index = this.state.inventory.findIndex(i => i.id === itemId);
        if (index !== -1) {
            this.state.inventory.splice(index, 1);
            this.notify('inventory', this.state.inventory);
        }
        return this;
    }
    
    hasItem(itemId) {
        return this.state.inventory.some(i => i.id === itemId);
    }
    
    getInventory() {
        return [...this.state.inventory];
    }
    
    // ========================================
    // Room Management
    // ========================================
    
    enterRoom(roomId, position) {
        const previousRoom = this.state.currentRoom;
        this.state.currentRoom = roomId;
        
        if (position) {
            this.state.playerPosition = position;
        }
        
        // Track visited rooms
        if (!this.state.stats.roomsVisited.includes(roomId)) {
            this.state.stats.roomsVisited.push(roomId);
        }
        
        this.notify('currentRoom', roomId, previousRoom);
        return this;
    }
    
    // ========================================
    // Observer Pattern
    // ========================================
    
    subscribe(path, callback) {
        if (!this.observers.has(path)) {
            this.observers.set(path, new Set());
        }
        this.observers.get(path).add(callback);
        
        // Return unsubscribe function
        return () => this.observers.get(path)?.delete(callback);
    }
    
    notify(path, newValue, oldValue) {
        // Notify exact path observers
        this.observers.get(path)?.forEach(cb => cb(newValue, oldValue, path));
        
        // Notify wildcard observers
        this.observers.get('*')?.forEach(cb => cb(newValue, oldValue, path));
    }
    
    // ========================================
    // Save/Load
    // ========================================
    
    save(slot = 0) {
        const saveData = {
            version: 1,
            timestamp: Date.now(),
            state: JSON.parse(JSON.stringify(this.state))
        };
        localStorage.setItem(`tm_save_${slot}`, JSON.stringify(saveData));
        return saveData;
    }
    
    load(slot = 0) {
        const data = localStorage.getItem(`tm_save_${slot}`);
        if (data) {
            const saveData = JSON.parse(data);
            this.state = saveData.state;
            this.notify('*', this.state);
            return true;
        }
        return false;
    }
    
    reset() {
        this.state = {
            inventory: [],
            currentRoom: null,
            playerPosition: { x: 0, y: 0 },
            flags: {},
            stats: {
                roomsVisited: [],
                itemsCollected: [],
                npcsSpokenTo: [],
                puzzlesSolved: 0,
                timeStarted: Date.now(),
                timePlayed: 0
            },
            saveSlot: null
        };
        this.notify('*', this.state);
        return this;
    }
    
    // ========================================
    // Debug
    // ========================================
    
    debug() {
        console.log('GameState:', JSON.stringify(this.state, null, 2));
        return this.state;
    }
}

// Singleton export
const gameState = new GameState();
