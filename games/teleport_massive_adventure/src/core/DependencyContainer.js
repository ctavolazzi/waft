/**
 * DependencyContainer - Centralized dependency injection
 * 
 * Reduces global window pollution by providing a single registry
 * for all game systems and utilities.
 */

class DependencyContainer {
    constructor() {
        this.services = new Map();
        this.singletons = new Map();
    }

    /**
     * Register a service (factory function)
     * @param {string} name - Service name
     * @param {function} factory - Factory function
     * @param {boolean} singleton - Whether to cache the instance
     */
    register(name, factory, singleton = true) {
        this.services.set(name, { factory, singleton });
    }

    /**
     * Register an instance directly
     * @param {string} name - Service name
     * @param {*} instance - Service instance
     */
    registerInstance(name, instance) {
        this.singletons.set(name, instance);
    }

    /**
     * Get a service instance
     * @param {string} name - Service name
     * @returns {*} Service instance
     */
    get(name) {
        // Check singletons first
        if (this.singletons.has(name)) {
            return this.singletons.get(name);
        }

        // Check registered services
        const service = this.services.get(name);
        if (!service) {
            console.warn(`[DependencyContainer] Service not found: ${name}`);
            return null;
        }

        // Create instance
        const instance = service.factory();

        // Cache if singleton
        if (service.singleton) {
            this.singletons.set(name, instance);
        }

        return instance;
    }

    /**
     * Check if a service is registered
     * @param {string} name - Service name
     * @returns {boolean}
     */
    has(name) {
        return this.services.has(name) || this.singletons.has(name);
    }

    /**
     * Clear all services (for testing/cleanup)
     */
    clear() {
        this.services.clear();
        this.singletons.clear();
    }
}

// Export singleton instance
const container = new DependencyContainer();

// Make available globally for compatibility
if (typeof window !== 'undefined') {
    window.DependencyContainer = DependencyContainer;
    window.dependencyContainer = container;
}
