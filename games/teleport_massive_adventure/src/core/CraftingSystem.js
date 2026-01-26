/**
 * CraftingSystem - Drone Upgrade Crafting
 * 
 * Handles crafting and upgrading the combat drone at workbenches.
 * 
 * Features:
 * - Workbench interactions
 * - Part combination recipes
 * - Drone leveling/upgrading
 * - Upgrade stat bonuses
 */

class CraftingSystem {
    constructor() {
        this.recipes = this._initializeRecipes();
        this.upgrades = this._initializeUpgrades();
    }
    
    /**
     * Initialize crafting recipes
     */
    _initializeRecipes() {
        return {
            // Level 1 upgrades (basic parts)
            'drone_level_2': {
                name: 'Drone Level 2',
                description: 'Upgrade drone to level 2. Increases damage and fire rate.',
                parts: ['energy_core'],
                result: { level: 2, statBonus: { damage: 3, shotCooldown: -100 } }
            },
            'drone_level_3': {
                name: 'Drone Level 3',
                description: 'Upgrade drone to level 3. Significant damage boost and extended range.',
                parts: ['energy_core', 'weapon_module'],
                result: { level: 3, statBonus: { damage: 5, shotCooldown: -200, targetRange: 50 } }
            },
            'drone_level_4': {
                name: 'Drone Level 4',
                description: 'Upgrade drone to level 4. Maximum power with enhanced shield capabilities.',
                parts: ['energy_core', 'weapon_module', 'shield_generator'],
                result: { level: 4, statBonus: { damage: 8, shotCooldown: -300, targetRange: 100, shieldDuration: 1000 } }
            },
            
            // Ability upgrades (can be done at any level)
            'burst_upgrade': {
                name: 'Enhanced Burst Shot',
                description: 'Increases burst shot damage by 50% and adds 2 more projectiles.',
                parts: ['weapon_module'],
                result: { abilityUpgrade: 'burst', bonus: { damageMultiplier: 1.5, projectileCount: 2 } }
            },
            'shield_upgrade': {
                name: 'Enhanced Shield Mode',
                description: 'Increases shield duration by 2 seconds and adds 50% damage reduction.',
                parts: ['shield_generator'],
                result: { abilityUpgrade: 'shield', bonus: { duration: 2000, damageReduction: 0.5 } }
            }
        };
    }
    
    /**
     * Initialize upgrade definitions
     */
    _initializeUpgrades() {
        return {
            level: 1, // Current drone level
            upgrades: [], // List of applied upgrades
            stats: {
                baseDamage: 12,
                baseShotCooldown: 1000,
                baseTargetRange: 300,
                baseShieldDuration: 3000
            }
        };
    }
    
    /**
     * Check if player can craft a recipe
     */
    canCraft(recipeId, inventory) {
        const recipe = this.recipes[recipeId];
        if (!recipe) return false;
        
        // Check if all required parts are in inventory
        const inventoryItems = inventory.map(item => item.id);
        return recipe.parts.every(partId => inventoryItems.includes(partId));
    }
    
    /**
     * Craft/upgrade drone
     */
    craft(recipeId, inventory, drone) {
        const recipe = this.recipes[recipeId];
        if (!recipe) {
            return { success: false, message: 'Unknown recipe' };
        }
        
        // Check if can craft
        if (!this.canCraft(recipeId, inventory)) {
            return { success: false, message: 'Missing required parts' };
        }
        
        // Check if already upgraded
        if (recipe.result.level && drone.level >= recipe.result.level) {
            return { success: false, message: 'Drone already at this level or higher' };
        }
        
        // Apply upgrade
        const result = this._applyUpgrade(recipe.result, drone);
        
        // Remove parts from inventory (handled by caller)
        return {
            success: true,
            message: `Upgraded to ${recipe.name}!`,
            consumedParts: recipe.parts,
            result: result
        };
    }
    
    /**
     * Apply upgrade to drone
     */
    _applyUpgrade(upgradeResult, drone) {
        if (upgradeResult.level) {
            // Level upgrade
            drone.level = upgradeResult.level;
            
            // Apply stat bonuses
            if (upgradeResult.statBonus) {
                if (upgradeResult.statBonus.damage) {
                    drone.damage += upgradeResult.statBonus.damage;
                }
                if (upgradeResult.statBonus.shotCooldown) {
                    drone.shotCooldown = Math.max(200, drone.shotCooldown + upgradeResult.statBonus.shotCooldown);
                }
                if (upgradeResult.statBonus.targetRange) {
                    drone.targetRange += upgradeResult.statBonus.targetRange;
                }
                if (upgradeResult.statBonus.shieldDuration) {
                    drone.abilities.shield.duration += upgradeResult.statBonus.shieldDuration;
                }
            }
        }
        
        if (upgradeResult.abilityUpgrade) {
            // Ability upgrade
            const ability = drone.abilities[upgradeResult.abilityUpgrade];
            if (ability && upgradeResult.bonus) {
                // Merge bonuses (for multipliers, multiply; for counts, add)
                Object.entries(upgradeResult.bonus).forEach(([key, value]) => {
                    if (key.includes('Multiplier')) {
                        ability[key] = (ability[key] || 1.0) * value;
                    } else if (key.includes('Count') || key.includes('Count')) {
                        ability[key] = (ability[key] || 0) + value;
                    } else {
                        ability[key] = value;
                    }
                });
            }
        }
        
        return upgradeResult;
    }
    
    /**
     * Get available recipes for current inventory
     */
    getAvailableRecipes(inventory, drone) {
        const available = [];
        
        Object.entries(this.recipes).forEach(([recipeId, recipe]) => {
            // For level upgrades, check if already at that level
            if (recipe.result.level && drone.level >= recipe.result.level) {
                return; // Skip - already at or past this level
            }
            
            // For ability upgrades, check if already upgraded
            if (recipe.result.abilityUpgrade) {
                const ability = drone.abilities[recipe.result.abilityUpgrade];
                // Check if upgrade already applied (has the bonus properties)
                if (recipe.result.bonus) {
                    const hasUpgrade = Object.keys(recipe.result.bonus).every(key => {
                        if (key.includes('Multiplier')) {
                            return ability[key] && ability[key] > 1.0;
                        }
                        return ability[key] !== undefined;
                    });
                    if (hasUpgrade) {
                        return; // Skip - already upgraded
                    }
                }
            }
            
            // Check if can craft
            if (this.canCraft(recipeId, inventory)) {
                available.push({
                    id: recipeId,
                    ...recipe
                });
            }
        });
        
        return available;
    }
    
    /**
     * Get drone upgrade info
     */
    getDroneInfo(drone) {
        return {
            level: drone.level || 1,
            damage: drone.damage,
            shotCooldown: drone.shotCooldown,
            targetRange: drone.targetRange,
            abilities: {
                burst: {
                    cooldown: drone.abilities.burst.cooldown,
                    projectileCount: drone.abilities.burst.projectileCount || 5
                },
                shield: {
                    cooldown: drone.abilities.shield.cooldown,
                    duration: drone.abilities.shield.duration
                }
            }
        };
    }
}

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CraftingSystem;
}

// Global instance
const craftingSystem = new CraftingSystem();
