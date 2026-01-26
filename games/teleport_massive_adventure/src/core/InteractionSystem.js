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
        
        // Trigger scene change in Phaser
        if (this.scene) {
            this.scene.cameras.main.fadeOut(300, 0, 0, 0);
            this.scene.time.delayedCall(300, () => {
                // Map room ID to scene key
                const sceneMap = {
                    'lab': 'LabScene',
                    'lobby': 'LobbyScene',
                    'underground': 'UndergroundScene',
                    'void': 'ArchitectScene'
                };
                this.scene.scene.start(sceneMap[targetRoom] || targetRoom, { 
                    playerX: position.x, 
                    playerY: position.y 
                });
            });
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
