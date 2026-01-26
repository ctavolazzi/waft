/**
 * InteractionSystem - Composable interaction handling
 * 
 * Processes hotspot and NPC interactions based on data definitions.
 * Supports conditional logic, sequences, and callbacks.
 */
class InteractionSystem {
    constructor(scene) {
        this.scene = scene;
        this.roomLoader = null;
        this.cursorMode = 'walk'; // walk, look, use, talk, pickup
        this.selectedItem = null;
    }
    
    // ========================================
    // Setup
    // ========================================
    
    setRoomLoader(roomLoader) {
        this.roomLoader = roomLoader;
    }
    
    setCursorMode(mode) {
        this.cursorMode = mode;
        eventBus.emit('cursor:change', { mode });
    }
    
    setSelectedItem(item) {
        this.selectedItem = item;
        if (item) {
            this.setCursorMode('use');
        }
    }
    
    // ========================================
    // Interaction Processing
    // ========================================
    
    interact(target, mode = null) {
        const actualMode = mode || this.cursorMode;
        
        if (target.hotspotConfig) {
            return this.interactHotspot(target.hotspotConfig, actualMode);
        }
        
        if (target.npcConfig) {
            return this.interactNPC(target.npcConfig, actualMode);
        }
        
        return false;
    }
    
    interactHotspot(config, mode) {
        const interactions = config.interactions || {};
        
        // Find matching interaction
        let interaction = null;
        
        // Check for mode-specific interaction with conditions
        const modeKey = mode;
        const modeLockedKey = `${mode}_locked`;
        const modeRepeatKey = `${mode}_repeat`;
        
        if (interactions[modeKey]) {
            const i = interactions[modeKey];
            if (!i.condition || gameState.checkCondition(i.condition)) {
                interaction = i;
            }
        }
        
        // Check for locked version
        if (!interaction && interactions[modeLockedKey]) {
            const i = interactions[modeLockedKey];
            if (!i.condition || gameState.checkCondition(i.condition)) {
                interaction = i;
            }
        }
        
        // Check for repeat version
        if (!interaction && interactions[modeRepeatKey]) {
            const i = interactions[modeRepeatKey];
            if (!i.condition || gameState.checkCondition(i.condition)) {
                interaction = i;
            }
        }
        
        // Default to examine text
        if (!interaction && mode === 'look' && config.examineText) {
            return this.executeAction({ action: 'dialogue', lines: [config.examineText] });
        }
        
        if (interaction) {
            return this.executeAction(interaction, config);
        }
        
        return false;
    }
    
    interactNPC(config, mode) {
        // Emit NPC interaction event
        eventBus.emit(EventBus.NPC_TALK, { npc: config.id, mode });
        
        if (mode === 'talk' && config.dialogue) {
            // Set flags from onTalk
            if (config.onTalk?.setFlag) {
                Object.entries(config.onTalk.setFlag).forEach(([key, value]) => {
                    gameState.setFlag(key, value);
                });
            }
            
            return this.executeAction({ action: 'dialogue', dialogueId: config.dialogue });
        }
        
        if (mode === 'look' && config.examineText) {
            return this.executeAction({ action: 'dialogue', lines: [config.examineText] });
        }
        
        // Use item on NPC
        if (mode === 'use' && this.selectedItem) {
            return this.useItemOn(this.selectedItem, config);
        }
        
        return false;
    }
    
    // ========================================
    // Action Execution
    // ========================================
    
    executeAction(action, context = {}) {
        if (!action) return false;
        
        switch (action.action) {
            case 'dialogue':
                return this.executeDialogue(action);
                
            case 'addItem':
                return this.executeAddItem(action);
                
            case 'changeRoom':
                return this.executeChangeRoom(action);
                
            case 'setFlag':
                return this.executeSetFlag(action);
                
            case 'sequence':
                return this.executeSequence(action);
                
            case 'conditional':
                return this.executeConditional(action);
                
            case 'craft':
                return this.executeCraft(action);
                
            default:
                console.warn(`Unknown action type: ${action.action}`);
                return false;
        }
    }
    
    executeDialogue(action) {
        if (action.dialogueId) {
            dialogueSystem.show(action.dialogueId, action.onComplete);
        } else if (action.lines) {
            dialogueSystem.showLines(action.speaker || '', action.lines, action.onComplete);
        }
        
        // Set any flags
        if (action.setFlag) {
            this.executeSetFlag(action);
        }
        
        eventBus.emit(EventBus.DIALOGUE_START, { dialogueId: action.dialogueId });
        return true;
    }
    
    executeAddItem(action) {
        const itemData = this.getItemData(action.item);
        if (itemData) {
            gameState.addItem(itemData);
            eventBus.emit(EventBus.ITEM_PICKUP, { item: itemData });
            
            // Show pickup message
            dialogueSystem.showSingle('', `Added ${itemData.name} to inventory.`);
            
            // Handle special item effects
            if (itemData.effects?.onAcquire) {
                const effect = itemData.effects.onAcquire;
                if (effect.action === 'setFlag') {
                    gameState.setFlag(effect.flag, effect.value !== undefined ? effect.value : true);
                    
                    // Special handling for combat drone
                    if (effect.flag === 'hasCombatDrone') {
                        // Activate drone if player exists
                        const scene = this.scene;
                        if (scene?.player) {
                            scene.player.acquireDrone();
                        }
                    }
                }
            }
            
            // Give drone if action specifies
            if (action.giveDrone) {
                const scene = this.scene;
                if (scene?.player) {
                    scene.player.acquireDrone();
                }
            }
            
            // Set flags
            if (action.setFlag) {
                this.executeSetFlag(action);
            }
            
            // Hide hotspot
            if (action.hideHotspot && this.roomLoader) {
                this.roomLoader.hideHotspot(action.item);
            }
        }
        return true;
    }
    
    executeChangeRoom(action) {
        eventBus.emit(EventBus.ROOM_EXIT, { room: gameState.get('currentRoom') });
        
        // Optional dialogue before transition
        if (action.dialogue) {
            dialogueSystem.show(action.dialogue, () => {
                this.doRoomChange(action);
            });
        } else if (action.delay) {
            setTimeout(() => this.doRoomChange(action), action.delay);
        } else {
            this.doRoomChange(action);
        }
        
        return true;
    }
    
    doRoomChange(action) {
        const targetRoom = action.target;
        const position = action.playerPosition || { x: 400, y: 400 };
        
        gameState.enterRoom(targetRoom, position);
        
        // Use centralized transition utility
        if (this.scene) {
            const SceneTransition = window.SceneTransition || (typeof SceneTransition !== 'undefined' ? SceneTransition : null);
            if (SceneTransition) {
                SceneTransition.transition(this.scene, targetRoom, {
                    playerX: position.x,
                    playerY: position.y,
                    onCleanup: () => SceneTransition.cleanupPlayer(this.scene?.player)
                });
            } else {
                // Fallback for compatibility
                this.scene.cameras.main.fadeOut(300, 0, 0, 0);
                this.scene.time.delayedCall(300, () => {
                    const sceneMap = {
                        'lab': 'LabScene',
                        'lobby': 'LobbyScene',
                        'underground': 'UndergroundScene',
                        'void': 'VoidScene'
                    };
                    this.scene.scene.start(sceneMap[targetRoom] || targetRoom, { 
                        playerX: position.x, 
                        playerY: position.y 
                    });
                });
            }
        }
        
        eventBus.emit(EventBus.ROOM_ENTER, { room: targetRoom, position });
    }
    
    executeSetFlag(action) {
        if (action.setFlag) {
            Object.entries(action.setFlag).forEach(([key, value]) => {
                gameState.setFlag(key, value);
            });
        }
        return true;
    }
    
    executeCraft(action) {
        // Open crafting UI
        if (action.craftType === 'drone_upgrade') {
            this._openDroneCraftingUI();
        }
        return true;
    }
    
    _openDroneCraftingUI() {
        // Get player's drone
        const scene = this.scene;
        const player = scene?.player;
        const drone = player?.combatDrone;
        
        // Allow upgrading even if drone not active (will activate it)
        if (!drone) {
            // Try to initialize drone if player has it
            if (player && player.hasDrone) {
                const SystemAccessor = window.SystemAccessor || (typeof SystemAccessor !== 'undefined' ? SystemAccessor : null);
                if (SystemAccessor) {
                    const combatSystem = SystemAccessor.getCombatSystem();
                    const npcSystem = SystemAccessor.getNPCSystem();
                    const statsSystem = SystemAccessor.getStatsSystem();
                    
                    if (combatSystem && npcSystem && statsSystem) {
                        player.initCombatDrone({
                            combatSystem,
                            npcSystem,
                            statsSystem
                        });
                        player.activateDrone();
                    }
                } else if (window.gameManager) {
                    // Fallback to legacy access
                    const combatSystem = window.gameManager.getSystem('combatSystem');
                    const npcSystem = window.gameManager.getSystem('npcSystem');
                    const statsSystem = window.gameManager.getSystem('statsSystem');
                    
                    if (combatSystem && npcSystem && statsSystem) {
                        player.initCombatDrone({
                            combatSystem,
                            npcSystem,
                            statsSystem
                        });
                        player.activateDrone();
                    }
                }
            }
            
            if (!player?.combatDrone) {
                dialogueSystem.showSingle('', 'You need to have a combat drone to upgrade it. Find the drone item first.');
                return;
            }
        }
        
        // Ensure drone is active for upgrades
        if (drone && !drone.isActive) {
            drone.activate();
        }
        
        // Get inventory
        const inventory = gameState.getInventory();
        const droneParts = inventory.filter(item => item.craftingMaterial && item.type === 'drone_part');
        
        // Get available recipes
        const availableRecipes = craftingSystem.getAvailableRecipes(inventory, drone);
        
        // Show crafting UI
        this._showCraftingUI(drone, droneParts, availableRecipes);
    }
    
    _showCraftingUI(drone, parts, recipes) {
        // Create crafting UI overlay
        const overlay = document.createElement('div');
        overlay.id = 'crafting-overlay';
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.85);
            z-index: 10000;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Courier New', monospace;
        `;
        
        const panel = document.createElement('div');
        panel.style.cssText = `
            background: rgba(10, 10, 30, 0.95);
            border: 3px solid #00aaff;
            border-radius: 8px;
            padding: 20px;
            max-width: 600px;
            max-height: 80vh;
            overflow-y: auto;
            color: #00ff88;
        `;
        
        // Title
        const title = document.createElement('h2');
        title.textContent = 'DRONE UPGRADE WORKBENCH';
        title.style.cssText = 'color: #00aaff; margin-bottom: 20px; text-align: center;';
        panel.appendChild(title);
        
        // Drone info
        const droneInfo = craftingSystem.getDroneInfo(drone);
        const infoDiv = document.createElement('div');
        infoDiv.style.cssText = 'margin-bottom: 20px; padding: 10px; background: rgba(0, 100, 150, 0.2); border: 1px solid #00aaff;';
        infoDiv.innerHTML = `
            <strong>Current Drone Level: ${droneInfo.level}</strong><br>
            Damage: ${droneInfo.damage} | Cooldown: ${droneInfo.shotCooldown}ms | Range: ${droneInfo.targetRange}px
        `;
        panel.appendChild(infoDiv);
        
        // Available parts
        const partsDiv = document.createElement('div');
        partsDiv.style.cssText = 'margin-bottom: 20px;';
        partsDiv.innerHTML = '<strong>Available Parts:</strong><br>';
        if (parts.length === 0) {
            partsDiv.innerHTML += '<span style="color: #888;">No parts in inventory</span>';
        } else {
            parts.forEach(part => {
                const partSpan = document.createElement('span');
                partSpan.textContent = `${part.icon} ${part.name} `;
                partSpan.style.cssText = 'display: inline-block; margin: 5px; padding: 5px; background: rgba(0, 170, 255, 0.2); border: 1px solid #00aaff;';
                partsDiv.appendChild(partSpan);
            });
        }
        panel.appendChild(partsDiv);
        
        // Available upgrades
        const upgradesDiv = document.createElement('div');
        upgradesDiv.innerHTML = '<strong>Available Upgrades:</strong><br>';
        
        if (recipes.length === 0) {
            upgradesDiv.innerHTML += '<span style="color: #888;">No upgrades available. Collect more parts!</span>';
        } else {
            recipes.forEach(recipe => {
                const recipeDiv = document.createElement('div');
                recipeDiv.style.cssText = 'margin: 10px 0; padding: 10px; background: rgba(0, 100, 150, 0.2); border: 1px solid #00ff88;';
                
                const recipeTitle = document.createElement('div');
                recipeTitle.textContent = recipe.name;
                recipeTitle.style.cssText = 'font-weight: bold; color: #00ff88; margin-bottom: 5px;';
                recipeDiv.appendChild(recipeTitle);
                
                const recipeDesc = document.createElement('div');
                recipeDesc.textContent = recipe.description;
                recipeDesc.style.cssText = 'font-size: 12px; color: #aaa; margin-bottom: 10px;';
                recipeDiv.appendChild(recipeDesc);
                
                const recipeParts = document.createElement('div');
                recipeParts.textContent = `Required: ${recipe.parts.join(', ')}`;
                recipeParts.style.cssText = 'font-size: 11px; color: #888; margin-bottom: 10px;';
                recipeDiv.appendChild(recipeParts);
                
                const craftBtn = document.createElement('button');
                craftBtn.textContent = 'CRAFT';
                craftBtn.style.cssText = `
                    background: #00aaff;
                    color: #000;
                    border: none;
                    padding: 8px 16px;
                    cursor: pointer;
                    font-family: inherit;
                    font-weight: bold;
                `;
                craftBtn.onclick = () => {
                    this._craftUpgrade(recipe.id, overlay);
                };
                recipeDiv.appendChild(craftBtn);
                
                upgradesDiv.appendChild(recipeDiv);
            });
        }
        panel.appendChild(upgradesDiv);
        
        // Close button
        const closeBtn = document.createElement('button');
        closeBtn.textContent = 'CLOSE';
        closeBtn.style.cssText = `
            margin-top: 20px;
            width: 100%;
            background: #ff4444;
            color: #fff;
            border: none;
            padding: 10px;
            cursor: pointer;
            font-family: inherit;
            font-weight: bold;
        `;
        closeBtn.onclick = () => overlay.remove();
        panel.appendChild(closeBtn);
        
        overlay.appendChild(panel);
        document.body.appendChild(overlay);
        
        // Close on escape
        const closeHandler = (e) => {
            if (e.key === 'Escape') {
                overlay.remove();
                document.removeEventListener('keydown', closeHandler);
            }
        };
        document.addEventListener('keydown', closeHandler);
    }
    
    _craftUpgrade(recipeId, overlay) {
        const scene = this.scene;
        const player = scene?.player;
        const drone = player?.combatDrone;
        const inventory = gameState.getInventory();
        
        if (!drone) {
            dialogueSystem.showSingle('', 'Drone not available.');
            return;
        }
        
        // Attempt craft
        const result = craftingSystem.craft(recipeId, inventory, drone);
        
        if (result.success) {
            // Remove consumed parts from inventory
            result.consumedParts.forEach(partId => {
                gameState.removeItem(partId);
            });
            
            // Show success message with stat changes
            let message = result.message;
            if (result.result.statBonus) {
                const bonuses = [];
                if (result.result.statBonus.damage) bonuses.push(`+${result.result.statBonus.damage} damage`);
                if (result.result.statBonus.shotCooldown) bonuses.push(`${result.result.statBonus.shotCooldown}ms faster shots`);
                if (result.result.statBonus.targetRange) bonuses.push(`+${result.result.statBonus.targetRange}px range`);
                if (bonuses.length > 0) {
                    message += ` (${bonuses.join(', ')})`;
                }
            }
            dialogueSystem.showSingle('', message);
            
            // Update drone stats
            if (result.result.level) {
                drone.level = result.result.level;
            }
            
            // Emit event
            if (window.eventBus) {
                window.eventBus.emit('drone:upgraded', { 
                    level: drone.level,
                    recipe: recipeId,
                    player: 'aziah'
                });
            }
            
            // Close UI and refresh
            overlay.remove();
            setTimeout(() => {
                this._openDroneCraftingUI(); // Reopen to show updated state
            }, 500);
        } else {
            dialogueSystem.showSingle('', result.message);
        }
    }
    
    executeSequence(action) {
        const steps = action.steps || [];
        let index = 0;
        
        const executeNext = () => {
            if (index >= steps.length) return;
            
            const step = steps[index];
            index++;
            
            // Handle delays
            if (step.delay) {
                setTimeout(() => {
                    this.executeAction({ ...step, onComplete: executeNext });
                }, step.delay);
            } else {
                this.executeAction({ ...step, onComplete: executeNext });
            }
        };
        
        executeNext();
        return true;
    }
    
    executeConditional(action) {
        if (gameState.checkCondition(action.condition)) {
            return this.executeAction(action.then);
        } else if (action.else) {
            return this.executeAction(action.else);
        }
        return false;
    }
    
    // ========================================
    // Item Usage
    // ========================================
    
    useItemOn(item, target) {
        // Check if item can be used on target
        if (item.usableOn && item.usableOn.includes(target.id)) {
            if (item.effects && item.effects[`on${this.capitalize(target.id)}`]) {
                return this.executeAction(item.effects[`on${this.capitalize(target.id)}`]);
            }
        }
        
        // Default message
        dialogueSystem.showSingle('', `You can't use ${item.name} on that.`);
        return false;
    }
    
    // ========================================
    // Utility
    // ========================================
    
    getItemData(itemId) {
        // This would normally load from items.json
        // For now, return basic item data
        const items = {
            'artifact': { id: 'artifact', name: 'SWAB Artifact', icon: '◈' },
            'keycard': { id: 'keycard', name: 'Security Keycard', icon: '▭' }
        };
        return items[itemId];
    }
    
    capitalize(str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    }
}
