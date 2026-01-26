/**
 * SystemAccessor - Unified system access interface
 * 
 * Provides a clean way to access game systems that works with both
 * DependencyContainer (new) and window globals (legacy).
 * 
 * This allows gradual migration without breaking existing code.
 */

class SystemAccessor {
    /**
     * Get a system by name
     * @param {string} systemName - System identifier
     * @returns {*} System instance or null
     */
    static getSystem(systemName) {
        // Try DependencyContainer first (preferred)
        if (typeof window !== 'undefined' && window.dependencyContainer) {
            const system = window.dependencyContainer.get(systemName);
            if (system) return system;
        }

        // Fallback to GameManager
        if (typeof window !== 'undefined' && window.gameManager) {
            const system = window.gameManager.getSystem(systemName);
            if (system) return system;
        }

        // Fallback to direct window access (legacy)
        if (typeof window !== 'undefined' && window[systemName]) {
            return window[systemName];
        }

        return null;
    }

    /**
     * Get GameManager instance
     * @returns {GameManager|null}
     */
    static getGameManager() {
        return this.getSystem('gameManager') || 
               (typeof window !== 'undefined' ? window.gameManager : null);
    }

    /**
     * Get EventBus instance
     * @returns {EventBus|null}
     */
    static getEventBus() {
        return this.getSystem('eventBus') || 
               (typeof window !== 'undefined' ? window.eventBus : null);
    }

    /**
     * Get GameState instance
     * @returns {GameState|null}
     */
    static getGameState() {
        return this.getSystem('gameState') || 
               (typeof window !== 'undefined' ? window.gameState : null);
    }

    /**
     * Get DialogueSystem instance
     * @returns {DialogueSystem|null}
     */
    static getDialogueSystem() {
        return this.getSystem('dialogueSystem') || 
               (typeof window !== 'undefined' ? window.dialogueSystem : null);
    }

    /**
     * Get StatsSystem instance
     * @returns {StatsSystem|null}
     */
    static getStatsSystem() {
        return this.getSystem('statsSystem');
    }

    /**
     * Get CombatSystem instance
     * @returns {CombatSystem|null}
     */
    static getCombatSystem() {
        return this.getSystem('combatSystem');
    }

    /**
     * Get NPCSystem instance
     * @returns {NPCSystem|null}
     */
    static getNPCSystem() {
        return this.getSystem('npcSystem');
    }

    /**
     * Get TheDealer instance
     * @returns {TheDealer|null}
     */
    static getTheDealer() {
        return this.getSystem('theDealer') || 
               (typeof window !== 'undefined' ? window.theDealer : null);
    }
}

// Make available globally
if (typeof window !== 'undefined') {
    window.SystemAccessor = SystemAccessor;
    // Also create a shorthand
    window.getSystem = SystemAccessor.getSystem.bind(SystemAccessor);
}
