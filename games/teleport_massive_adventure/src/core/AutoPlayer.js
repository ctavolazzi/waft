/**
 * AutoPlayer - Automated Testing/Debug Playthrough
 * 
 * Executes a scripted walkthrough of the entire game.
 * Toggle on/off with button. Shows what the "correct" path is.
 */
class AutoPlayer {
    constructor() {
        this.isRunning = false;
        this.isPaused = false;
        this.currentStep = 0;
        this.currentScene = null;
        this.stepTimer = null;
        this.dialogueTimer = null;
        
        // Speed settings
        this.walkDelay = 800;      // Time to wait after walking
        this.actionDelay = 500;    // Time between actions
        this.dialogueSpeed = 100;  // Auto-advance dialogue (ms per line)
        
        // The complete walkthrough script
        this.script = this.buildScript();
        
        // UI
        this.button = null;
        this.statusText = null;
        this.createUI();
        
        // Subscribe to events for auto-dialogue advance
        eventBus.on(EventBus.DIALOGUE_START, () => this.onDialogueStart());
    }
    
    // ========================================
    // Walkthrough Script
    // ========================================
    
    buildScript() {
        return [
            // === LAB SCENE ===
            { scene: 'LabScene', action: 'log', message: '🎬 Starting automated playthrough...' },
            { scene: 'LabScene', action: 'wait', duration: 1000 },
            
            // Examine photo
            { scene: 'LabScene', action: 'log', message: '📷 Examining photo of Maya...' },
            { scene: 'LabScene', action: 'walkTo', x: 100, y: 350 },
            { scene: 'LabScene', action: 'interact', targetId: 'photo', mode: 'look' },
            { scene: 'LabScene', action: 'wait', duration: 2000 },
            
            // Pick up artifact
            { scene: 'LabScene', action: 'log', message: '✨ Picking up the strange artifact...' },
            { scene: 'LabScene', action: 'walkTo', x: 200, y: 380 },
            { scene: 'LabScene', action: 'interact', targetId: 'artifact', mode: 'pickup' },
            { scene: 'LabScene', action: 'wait', duration: 1500 },
            
            // Use terminal
            { scene: 'LabScene', action: 'log', message: '💻 Using research terminal...' },
            { scene: 'LabScene', action: 'walkTo', x: 600, y: 350 },
            { scene: 'LabScene', action: 'interact', targetId: 'terminal', mode: 'use' },
            { scene: 'LabScene', action: 'wait', duration: 3000 },
            
            // Go to lobby
            { scene: 'LabScene', action: 'log', message: '🚪 Heading to lobby...' },
            { scene: 'LabScene', action: 'walkTo', x: 720, y: 380 },
            { scene: 'LabScene', action: 'interact', targetId: 'door_lobby', mode: 'use' },
            { scene: 'LabScene', action: 'wait', duration: 1000 },
            
            // === LOBBY SCENE ===
            { scene: 'LobbyScene', action: 'wait', duration: 500 },
            { scene: 'LobbyScene', action: 'log', message: '🏢 Arrived in TM Lobby' },
            
            // Look at display
            { scene: 'LobbyScene', action: 'log', message: '📺 Examining TM display...' },
            { scene: 'LobbyScene', action: 'walkTo', x: 400, y: 300 },
            { scene: 'LobbyScene', action: 'interact', targetId: 'tm_display', mode: 'look' },
            { scene: 'LobbyScene', action: 'wait', duration: 2000 },
            
            // Talk to guard
            { scene: 'LobbyScene', action: 'log', message: '👮 Talking to security guard...' },
            { scene: 'LobbyScene', action: 'walkTo', x: 550, y: 380 },
            { scene: 'LobbyScene', action: 'interact', targetId: 'guard', mode: 'talk' },
            { scene: 'LobbyScene', action: 'wait', duration: 3000 },
            
            // Pick up keycard
            { scene: 'LobbyScene', action: 'log', message: '🔑 Found keycard on floor...' },
            { scene: 'LobbyScene', action: 'walkTo', x: 300, y: 420 },
            { scene: 'LobbyScene', action: 'interact', targetId: 'keycard', mode: 'pickup' },
            { scene: 'LobbyScene', action: 'wait', duration: 1500 },
            
            // Use maintenance hatch
            { scene: 'LobbyScene', action: 'log', message: '🕳️ Using keycard on maintenance hatch...' },
            { scene: 'LobbyScene', action: 'walkTo', x: 400, y: 280 },
            { scene: 'LobbyScene', action: 'interact', targetId: 'maintenance_hatch', mode: 'use' },
            { scene: 'LobbyScene', action: 'wait', duration: 1000 },
            
            // === UNDERGROUND SCENE ===
            { scene: 'UndergroundScene', action: 'wait', duration: 500 },
            { scene: 'UndergroundScene', action: 'log', message: '🔦 Descended to underground...' },
            
            // Talk to Phaseburner
            { scene: 'UndergroundScene', action: 'log', message: '👻 Approaching Phaseburner...' },
            { scene: 'UndergroundScene', action: 'walkTo', x: 200, y: 380 },
            { scene: 'UndergroundScene', action: 'interact', targetId: 'phaseburner', mode: 'talk' },
            { scene: 'UndergroundScene', action: 'wait', duration: 4000 },
            
            // Use damaged terminal
            { scene: 'UndergroundScene', action: 'log', message: '💻 Accessing damaged terminal...' },
            { scene: 'UndergroundScene', action: 'walkTo', x: 620, y: 360 },
            { scene: 'UndergroundScene', action: 'interact', targetId: 'damaged_terminal', mode: 'use' },
            { scene: 'UndergroundScene', action: 'wait', duration: 4000 },
            
            // Enter portal (should appear after talking to phaseburner + having artifact)
            { scene: 'UndergroundScene', action: 'log', message: '🌀 Portal has appeared! Entering...' },
            { scene: 'UndergroundScene', action: 'walkTo', x: 100, y: 350 },
            { scene: 'UndergroundScene', action: 'wait', duration: 2000 },
            { scene: 'UndergroundScene', action: 'interact', targetId: 'portal', mode: 'use' },
            { scene: 'UndergroundScene', action: 'wait', duration: 8000 },
            
            // === VOID SCENE (Boss) ===
            { scene: 'VoidScene', action: 'wait', duration: 2000 },
            { scene: 'VoidScene', action: 'log', message: '🎭 Confronting THE ARCHITECT...' },
            
            // Boss fight is handled by dialogue/combat system
            // Auto-select actions
            { scene: 'VoidScene', action: 'wait', duration: 5000 },
            { scene: 'VoidScene', action: 'log', message: '⚔️ Phase 1 - Assert Reality' },
            { scene: 'VoidScene', action: 'bossAction', actionKey: 'assert' },
            { scene: 'VoidScene', action: 'wait', duration: 4000 },
            
            { scene: 'VoidScene', action: 'log', message: '⚔️ Using Remember Maya' },
            { scene: 'VoidScene', action: 'bossAction', actionKey: 'maya' },
            { scene: 'VoidScene', action: 'wait', duration: 4000 },
            
            { scene: 'VoidScene', action: 'log', message: '⚔️ Using Question Observer' },
            { scene: 'VoidScene', action: 'bossAction', actionKey: 'question' },
            { scene: 'VoidScene', action: 'wait', duration: 4000 },
            
            { scene: 'VoidScene', action: 'log', message: '⚔️ Phase 2 - Embrace Chaos' },
            { scene: 'VoidScene', action: 'bossAction', actionKey: 'chaos' },
            { scene: 'VoidScene', action: 'wait', duration: 4000 },
            
            { scene: 'VoidScene', action: 'bossAction', actionKey: 'question' },
            { scene: 'VoidScene', action: 'wait', duration: 4000 },
            
            { scene: 'VoidScene', action: 'bossAction', actionKey: 'assert' },
            { scene: 'VoidScene', action: 'wait', duration: 4000 },
            
            { scene: 'VoidScene', action: 'log', message: '⚔️ Phase 3 - Final push' },
            { scene: 'VoidScene', action: 'bossAction', actionKey: 'maya' },
            { scene: 'VoidScene', action: 'wait', duration: 4000 },
            
            { scene: 'VoidScene', action: 'bossAction', actionKey: 'question' },
            { scene: 'VoidScene', action: 'wait', duration: 4000 },
            
            // Final choice - Liberation ending
            { scene: 'VoidScene', action: 'log', message: '🎭 Final choice - Choosing LIBERATION' },
            { scene: 'VoidScene', action: 'wait', duration: 5000 },
            { scene: 'VoidScene', action: 'endingChoice', choice: 'free' },
            
            // Complete
            { scene: 'VoidScene', action: 'wait', duration: 3000 },
            { scene: null, action: 'log', message: '✅ PLAYTHROUGH COMPLETE!' },
            { scene: null, action: 'stop' }
        ];
    }
    
    // ========================================
    // UI
    // ========================================
    
    createUI() {
        // Create button container
        const container = document.createElement('div');
        container.id = 'auto-player-ui';
        container.style.cssText = `
            position: fixed;
            top: 10px;
            left: 10px;
            z-index: 9999;
            font-family: 'Courier New', monospace;
        `;
        
        // Toggle button
        this.button = document.createElement('button');
        this.button.id = 'auto-player-btn';
        this.button.textContent = '▶ AUTO';
        this.button.style.cssText = `
            background: #1a1a2e;
            color: #00ff88;
            border: 2px solid #00ff88;
            padding: 8px 16px;
            font-family: inherit;
            font-size: 12px;
            cursor: pointer;
            margin-right: 10px;
        `;
        this.button.onclick = () => this.toggle();
        
        // Status text
        this.statusText = document.createElement('span');
        this.statusText.id = 'auto-player-status';
        this.statusText.style.cssText = `
            color: #666;
            font-size: 11px;
        `;
        this.statusText.textContent = 'Ready';
        
        // Log area
        this.logArea = document.createElement('div');
        this.logArea.id = 'auto-player-log';
        this.logArea.style.cssText = `
            margin-top: 8px;
            padding: 8px;
            background: rgba(0, 0, 0, 0.8);
            border: 1px solid #333;
            max-height: 150px;
            overflow-y: auto;
            font-size: 10px;
            color: #888;
            display: none;
            width: 280px;
        `;
        
        container.appendChild(this.button);
        container.appendChild(this.statusText);
        container.appendChild(this.logArea);
        document.body.appendChild(container);
    }
    
    updateUI() {
        if (this.isRunning) {
            if (this.isPaused) {
                this.button.textContent = '▶ RESUME';
                this.button.style.borderColor = '#ffaa00';
                this.button.style.color = '#ffaa00';
                this.statusText.textContent = `Paused at step ${this.currentStep}/${this.script.length}`;
            } else {
                this.button.textContent = '⏸ PAUSE';
                this.button.style.borderColor = '#ff4444';
                this.button.style.color = '#ff4444';
                this.statusText.textContent = `Running... ${this.currentStep}/${this.script.length}`;
            }
            this.logArea.style.display = 'block';
        } else {
            this.button.textContent = '▶ AUTO';
            this.button.style.borderColor = '#00ff88';
            this.button.style.color = '#00ff88';
            this.statusText.textContent = 'Ready';
        }
    }
    
    log(message) {
        const line = document.createElement('div');
        line.textContent = `[${this.currentStep}] ${message}`;
        line.style.marginBottom = '2px';
        this.logArea.appendChild(line);
        this.logArea.scrollTop = this.logArea.scrollHeight;
        
        console.log(`%c[AutoPlayer] ${message}`, 'color: #00ff88');
    }
    
    // ========================================
    // Control
    // ========================================
    
    toggle() {
        if (!this.isRunning) {
            this.start();
        } else if (this.isPaused) {
            this.resume();
        } else {
            this.pause();
        }
    }
    
    start() {
        this.isRunning = true;
        this.isPaused = false;
        this.currentStep = 0;
        this.logArea.innerHTML = '';
        this.log('🎬 AutoPlayer started');
        this.updateUI();
        this.executeNextStep();
    }
    
    pause() {
        this.isPaused = true;
        if (this.stepTimer) {
            clearTimeout(this.stepTimer);
            this.stepTimer = null;
        }
        this.log('⏸ Paused');
        this.updateUI();
    }
    
    resume() {
        this.isPaused = false;
        this.log('▶ Resumed');
        this.updateUI();
        this.executeNextStep();
    }
    
    stop() {
        this.isRunning = false;
        this.isPaused = false;
        if (this.stepTimer) {
            clearTimeout(this.stepTimer);
            this.stepTimer = null;
        }
        if (this.dialogueTimer) {
            clearTimeout(this.dialogueTimer);
            this.dialogueTimer = null;
        }
        this.log('⏹ Stopped');
        this.updateUI();
    }
    
    // ========================================
    // Execution
    // ========================================
    
    executeNextStep() {
        if (!this.isRunning || this.isPaused) return;
        if (this.currentStep >= this.script.length) {
            this.stop();
            return;
        }
        
        const step = this.script[this.currentStep];
        this.currentStep++;
        this.updateUI();
        
        // Check if we're in the right scene
        const currentScene = this.getCurrentScene();
        if (step.scene && step.scene !== null) {
            const expectedSceneKey = step.scene;
            const currentSceneKey = currentScene?.scene?.key;
            
            if (!currentSceneKey || currentSceneKey !== expectedSceneKey) {
                // Wrong scene, wait and retry
                this.log(`⏳ Waiting for ${expectedSceneKey} (current: ${currentSceneKey || 'none'})...`);
                this.currentStep--; // Retry this step
                this.stepTimer = setTimeout(() => this.executeNextStep(), 500);
                return;
            }
        }
        
        // Execute the action
        this.executeAction(step);
    }
    
    executeAction(step) {
        const scene = this.getCurrentScene();
        const player = scene?.player;
        
        switch (step.action) {
            case 'log':
                this.log(step.message);
                this.scheduleNext(100);
                break;
                
            case 'wait':
                this.scheduleNext(step.duration);
                break;
                
            case 'walkTo':
                if (player && player.sprite) {
                    // Wait for player to finish moving
                    const distance = Math.sqrt(
                        Math.pow(step.x - player.sprite.x, 2) + 
                        Math.pow(step.y - player.sprite.y, 2)
                    );
                    const walkTime = (distance / player.walkSpeed) * 1000;
                    
                    player.walkTo(step.x, step.y);
                    
                    // Wait for movement to complete + buffer
                    this.scheduleNext(walkTime + this.walkDelay);
                } else {
                    this.log(`⚠ Player not available for walkTo`);
                    this.scheduleNext(100);
                }
                break;
                
            case 'interact':
                this.performInteraction(scene, step.targetId, step.mode);
                this.scheduleNext(this.actionDelay);
                break;
                
            case 'bossAction':
                this.performBossAction(scene, step.actionKey);
                this.scheduleNext(500);
                break;
                
            case 'endingChoice':
                this.performEndingChoice(scene, step.choice);
                this.scheduleNext(1000);
                break;
                
            case 'stop':
                this.stop();
                break;
                
            default:
                this.scheduleNext(100);
        }
    }
    
    scheduleNext(delay) {
        this.stepTimer = setTimeout(() => this.executeNextStep(), delay);
    }
    
    calculateWalkTime(player, targetX, targetY) {
        if (!player?.sprite) return 1000;
        const dx = targetX - player.sprite.x;
        const dy = targetY - player.sprite.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        const time = (distance / player.walkSpeed) * 1000;
        // Add buffer for pathfinding/obstacles
        return Math.max(time, 500) + 300;
    }
    
    // ========================================
    // Actions
    // ========================================
    
    performInteraction(scene, targetId, mode) {
        if (!scene?.roomLoader) {
            this.log(`⚠ Scene or roomLoader not available`);
            return;
        }
        
        // Find hotspot or NPC by ID
        let target = null;
        
        // Check hotspots
        if (scene.roomLoader.hotspots) {
            target = scene.roomLoader.hotspots.find(h => 
                h.hotspotConfig?.id === targetId || 
                h.hotspotConfig?.name === targetId
            );
        }
        
        // Check NPCs
        if (!target && scene.roomLoader.npcs) {
            target = scene.roomLoader.npcs.find(n => 
                n.npcConfig?.id === targetId || 
                n.npcConfig?.name === targetId
            );
        }
        
        if (target && scene.interactionSystem) {
            // Walk to target first if player exists
            if (scene.player && scene.player.sprite && target.hotspotConfig) {
                const targetPos = target.hotspotConfig.position;
                const interactPoint = scene.player.getInteractionPoint(target, { x: targetPos.x, y: targetPos.y });
                scene.player.walkTo(interactPoint.x, interactPoint.y);
                
                // Wait a bit for movement, then interact
                setTimeout(() => {
                    if (scene.interactionSystem) {
                        scene.interactionSystem.interact(target, mode);
                    }
                }, 500);
            } else {
                scene.interactionSystem.interact(target, mode);
            }
            this.log(`→ ${mode}: ${targetId}`);
        } else {
            this.log(`⚠ Target not found: ${targetId} (hotspots: ${scene.roomLoader.hotspots?.length || 0}, npcs: ${scene.roomLoader.npcs?.length || 0})`);
        }
    }
    
    performBossAction(scene, actionKey) {
        // Click the boss action button
        if (scene?.playerAction) {
            scene.playerAction(actionKey);
            this.log(`→ Boss action: ${actionKey}`);
        } else {
            this.log(`⚠ Boss action not available`);
        }
    }
    
    performEndingChoice(scene, choice) {
        if (scene?.ending) {
            scene.ending(choice);
            this.log(`→ Chose ending: ${choice}`);
        }
    }
    
    getCurrentScene() {
        // Try multiple ways to get the current scene
        if (window.game) {
            // Method 1: Phaser scene manager
            const activeScene = window.game.scene.getScenes(true).find(s => s.scene.isActive);
            if (activeScene) return activeScene;
            
            // Method 2: Direct scene access
            const scenes = window.game.scene.scenes;
            if (scenes && scenes.length > 0) {
                // Return the most recently started scene
                return scenes[scenes.length - 1];
            }
        }
        
        // Fallback: Try to get from Phaser registry
        if (window.Phaser && window.Phaser.Scenes && window.Phaser.Scenes.SceneManager) {
            // This is a last resort
            return null;
        }
        
        return null;
    }
    
    // ========================================
    // Auto Dialogue
    // ========================================
    
    onDialogueStart() {
        if (!this.isRunning || this.isPaused) return;
        
        // Auto-advance dialogue
        this.autoAdvanceDialogue();
    }
    
    autoAdvanceDialogue() {
        if (!this.isRunning || this.isPaused) return;
        if (!dialogueSystem?.isActive) return;
        
        // Clear any existing dialogue timer
        if (this.dialogueTimer) {
            clearTimeout(this.dialogueTimer);
        }
        
        this.dialogueTimer = setTimeout(() => {
            if (dialogueSystem?.isActive && this.isRunning && !this.isPaused) {
                dialogueSystem.advance();
                // Continue until dialogue is done
                this.autoAdvanceDialogue();
            }
        }, this.dialogueSpeed);
    }
}

// Create global instance
const autoPlayer = new AutoPlayer();
