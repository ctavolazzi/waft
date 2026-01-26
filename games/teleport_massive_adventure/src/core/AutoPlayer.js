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
            { scene: 'LabScene', action: 'walkTo', x: 200, y: 320 },
            { scene: 'LabScene', action: 'wait', duration: 1000 },
            { scene: 'LabScene', action: 'interact', targetId: 'artifact', mode: 'pickup' },
            { scene: 'LabScene', action: 'wait', duration: 2000 },
            
            // Use terminal
            { scene: 'LabScene', action: 'log', message: '💻 Using research terminal...' },
            { scene: 'LabScene', action: 'walkTo', x: 600, y: 350 },
            { scene: 'LabScene', action: 'interact', targetId: 'terminal', mode: 'use' },
            { scene: 'LabScene', action: 'wait', duration: 3000 },
            
            // Go to lobby
            { scene: 'LabScene', action: 'log', message: '🚪 Heading to lobby...' },
            { scene: 'LabScene', action: 'walkTo', x: 750, y: 350 },
            { scene: 'LabScene', action: 'wait', duration: 1500 },
            { scene: 'LabScene', action: 'interact', targetId: 'door_lobby', mode: 'use' },
            { scene: 'LabScene', action: 'wait', duration: 3000 },
            
            // === LOBBY SCENE ===
            { scene: 'LobbyScene', action: 'wait', duration: 1500 },
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
            { scene: 'LobbyScene', action: 'walkTo', x: 300, y: 450 },
            { scene: 'LobbyScene', action: 'wait', duration: 1000 },
            { scene: 'LobbyScene', action: 'interact', targetId: 'keycard', mode: 'pickup' },
            { scene: 'LobbyScene', action: 'wait', duration: 2000 },
            
            // Use maintenance hatch
            { scene: 'LobbyScene', action: 'log', message: '🕳️ Using keycard on maintenance hatch...' },
            { scene: 'LobbyScene', action: 'walkTo', x: 400, y: 220 },
            { scene: 'LobbyScene', action: 'wait', duration: 1500 },
            { scene: 'LobbyScene', action: 'interact', targetId: 'maintenance_hatch', mode: 'use' },
            { scene: 'LobbyScene', action: 'wait', duration: 3000 },
            
            // === UNDERGROUND SCENE ===
            { scene: 'UndergroundScene', action: 'wait', duration: 1500 },
            { scene: 'UndergroundScene', action: 'log', message: '🔦 Descended to underground...' },
            
            // Talk to Phaseburner
            { scene: 'UndergroundScene', action: 'log', message: '👻 Approaching Phaseburner...' },
            { scene: 'UndergroundScene', action: 'walkTo', x: 200, y: 350 },
            { scene: 'UndergroundScene', action: 'wait', duration: 1500 },
            { scene: 'UndergroundScene', action: 'interact', targetId: 'phaseburner', mode: 'talk' },
            { scene: 'UndergroundScene', action: 'wait', duration: 6000 },
            
            // Use damaged terminal
            { scene: 'UndergroundScene', action: 'log', message: '💻 Accessing damaged terminal...' },
            { scene: 'UndergroundScene', action: 'walkTo', x: 650, y: 320 },
            { scene: 'UndergroundScene', action: 'wait', duration: 1500 },
            { scene: 'UndergroundScene', action: 'interact', targetId: 'damaged_terminal', mode: 'use' },
            { scene: 'UndergroundScene', action: 'wait', duration: 6000 },
            
            // Enter portal (should appear after talking to phaseburner + having artifact)
            { scene: 'UndergroundScene', action: 'log', message: '🌀 Portal has appeared! Entering...' },
            { scene: 'UndergroundScene', action: 'walkTo', x: 100, y: 300 },
            { scene: 'UndergroundScene', action: 'wait', duration: 2000 },
            { scene: 'UndergroundScene', action: 'interact', targetId: 'portal', mode: 'use' },
            { scene: 'UndergroundScene', action: 'wait', duration: 10000 },
            
            // === VOID SCENE (Boss) ===
            { scene: 'VoidScene', action: 'wait', duration: 4000 },
            { scene: 'VoidScene', action: 'log', message: '🎭 Confronting THE DEALER...' },
            
            // Wait for boss encounter to start
            { scene: 'VoidScene', action: 'wait', duration: 4000 },
            
            // Phase 1 - Multiple actions to defeat boss (100 HP, need ~5-6 actions)
            { scene: 'VoidScene', action: 'log', message: '⚔️ Phase 1 - Starting combat' },
            { scene: 'VoidScene', action: 'wait', duration: 3000 },
            { scene: 'VoidScene', action: 'bossAction', actionKey: 'question' }, // 30 damage
            { scene: 'VoidScene', action: 'wait', duration: 6000 },
            
            { scene: 'VoidScene', action: 'bossAction', actionKey: 'bluff' }, // 20 damage
            { scene: 'VoidScene', action: 'wait', duration: 6000 },
            
            { scene: 'VoidScene', action: 'bossAction', actionKey: 'maya' }, // 15 damage
            { scene: 'VoidScene', action: 'wait', duration: 6000 },
            
            { scene: 'VoidScene', action: 'bossAction', actionKey: 'question' }, // 30 damage
            { scene: 'VoidScene', action: 'wait', duration: 6000 },
            
            { scene: 'VoidScene', action: 'bossAction', actionKey: 'bluff' }, // 20 damage (total: 115, phase ends)
            { scene: 'VoidScene', action: 'wait', duration: 6000 },
            
            // Phase 2
            { scene: 'VoidScene', action: 'log', message: '⚔️ Phase 2 - Continuing fight' },
            { scene: 'VoidScene', action: 'wait', duration: 4000 },
            { scene: 'VoidScene', action: 'bossAction', actionKey: 'question' }, // 30 damage
            { scene: 'VoidScene', action: 'wait', duration: 6000 },
            
            { scene: 'VoidScene', action: 'bossAction', actionKey: 'bluff' }, // 20 damage
            { scene: 'VoidScene', action: 'wait', duration: 6000 },
            
            { scene: 'VoidScene', action: 'bossAction', actionKey: 'maya' }, // 15 damage
            { scene: 'VoidScene', action: 'wait', duration: 6000 },
            
            { scene: 'VoidScene', action: 'bossAction', actionKey: 'question' }, // 30 damage (total: 95, phase ends)
            { scene: 'VoidScene', action: 'wait', duration: 6000 },
            
            // Phase 3
            { scene: 'VoidScene', action: 'log', message: '⚔️ Phase 3 - Final push' },
            { scene: 'VoidScene', action: 'wait', duration: 4000 },
            { scene: 'VoidScene', action: 'bossAction', actionKey: 'question' }, // 30 damage
            { scene: 'VoidScene', action: 'wait', duration: 6000 },
            
            { scene: 'VoidScene', action: 'bossAction', actionKey: 'bluff' }, // 20 damage
            { scene: 'VoidScene', action: 'wait', duration: 6000 },
            
            { scene: 'VoidScene', action: 'bossAction', actionKey: 'maya' }, // 15 damage
            { scene: 'VoidScene', action: 'wait', duration: 6000 },
            
            { scene: 'VoidScene', action: 'bossAction', actionKey: 'question' }, // 30 damage (total: 95, victory!)
            { scene: 'VoidScene', action: 'wait', duration: 6000 },
            
            // Wait for victory and final choice (boss should be defeated by now)
            { scene: 'VoidScene', action: 'log', message: '🎭 Waiting for final choice...' },
            { scene: 'VoidScene', action: 'wait', duration: 10000 },
            
            // Final choice - Liberation ending (retry if needed)
            { scene: 'VoidScene', action: 'log', message: '🎭 Choosing LIBERATION ending' },
            { scene: 'VoidScene', action: 'endingChoice', choice: 'free' },
            { scene: 'VoidScene', action: 'wait', duration: 3000 },
            
            // Complete
            { scene: 'VoidScene', action: 'wait', duration: 8000 },
            { scene: null, action: 'log', message: '✅ PLAYTHROUGH COMPLETE!' },
            { scene: null, action: 'wait', duration: 3000 },
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
        this.stateData = {}; // Reset state data
        this.logArea.innerHTML = '';
        this.log('🎬 AutoPlayer started');
        this.updateUI();
        
        // Wait a moment for game to be ready
        setTimeout(() => {
            this.executeNextStep();
        }, 500);
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
            const currentSceneKey = currentScene?.scene?.key || currentScene?.sys?.settings?.key;
            
            if (!currentSceneKey || currentSceneKey !== expectedSceneKey) {
                // Wrong scene, wait and retry (with max retries)
                const retryCount = this.stateData?.sceneRetries || 0;
                if (retryCount < 30) { // Max 15 seconds wait (increased)
                    this.log(`⏳ Waiting for ${expectedSceneKey} (current: ${currentSceneKey || 'none'}, attempt ${retryCount + 1}/30)...`);
                    this.stateData = { ...this.stateData, sceneRetries: retryCount + 1 };
                    this.currentStep--; // Retry this step
                    this.stepTimer = setTimeout(() => this.executeNextStep(), 500);
                } else {
                    this.log(`⚠ Scene transition timeout after 30 attempts, continuing anyway`);
                    this.stateData = { ...this.stateData, sceneRetries: 0 };
                    // Continue anyway - might be scene name mismatch
                }
                return;
            }
            
            // Reset scene retry counter on success
            this.stateData = { ...this.stateData, sceneRetries: 0 };
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
                    // Calculate distance and time
                    const distance = Math.sqrt(
                        Math.pow(step.x - player.sprite.x, 2) + 
                        Math.pow(step.y - player.sprite.y, 2)
                    );
                    const walkTime = (distance / (player.walkSpeed || 150)) * 1000;
                    
                    player.walkTo(step.x, step.y);
                    
                    // Wait for movement with polling to ensure completion
                    let movementChecks = 0;
                    const checkMovement = setInterval(() => {
                        movementChecks++;
                        if (!player.isMoving || movementChecks > 50) {
                            clearInterval(checkMovement);
                            // Additional buffer after movement completes
                            this.scheduleNext(this.walkDelay);
                        }
                    }, 100);
                    
                    // Fallback timeout
                    setTimeout(() => {
                        clearInterval(checkMovement);
                        this.scheduleNext(this.walkDelay);
                    }, walkTime + this.walkDelay + 1000);
                } else {
                    this.log(`⚠ Player not available for walkTo`);
                    this.scheduleNext(100);
                }
                break;
                
            case 'interact':
                this.performInteraction(scene, step.targetId, step.mode);
                // Wait longer for interactions (they may trigger dialogue)
                this.scheduleNext(this.actionDelay + 500);
                break;
                
            case 'bossAction':
                this.performBossAction(scene, step.actionKey);
                // Wait longer for boss action to complete (dialogue, damage, etc.)
                this.scheduleNext(3000);
                break;
                
            case 'endingChoice':
                this.performEndingChoice(scene, step.choice);
                // Wait for ending sequence to complete
                this.scheduleNext(5000);
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
            // Walk to target first if player exists and target has position
            if (scene.player && scene.player.sprite) {
                let targetPos;
                if (target.hotspotConfig?.position) {
                    targetPos = target.hotspotConfig.position;
                } else if (target.npcConfig?.position) {
                    targetPos = target.npcConfig.position;
                } else {
                    // No position, try to interact directly
                    scene.interactionSystem.interact(target, mode);
                    this.log(`→ ${mode}: ${targetId} (direct)`);
                    return;
                }
                
                const interactPoint = scene.player.getInteractionPoint(target, { x: targetPos.x, y: targetPos.y });
                scene.player.walkTo(interactPoint.x, interactPoint.y);
                
                // Wait for movement to complete, then interact
                const checkMovement = setInterval(() => {
                    if (!scene.player.isMoving) {
                        clearInterval(checkMovement);
                        if (scene.interactionSystem) {
                            scene.interactionSystem.interact(target, mode);
                        }
                    }
                }, 100);
                
                // Timeout fallback
                setTimeout(() => {
                    clearInterval(checkMovement);
                    if (scene.interactionSystem) {
                        scene.interactionSystem.interact(target, mode);
                    }
                }, 2000);
            } else {
                scene.interactionSystem.interact(target, mode);
            }
            this.log(`→ ${mode}: ${targetId}`);
        } else {
            this.log(`⚠ Target not found: ${targetId} (hotspots: ${scene.roomLoader.hotspots?.length || 0}, npcs: ${scene.roomLoader.npcs?.length || 0})`);
            // Try to find by name variation
            if (scene.roomLoader.hotspots) {
                const altTarget = scene.roomLoader.hotspots.find(h => 
                    h.hotspotConfig?.id?.toLowerCase().includes(targetId.toLowerCase()) ||
                    h.hotspotConfig?.name?.toLowerCase().includes(targetId.toLowerCase())
                );
                if (altTarget && scene.interactionSystem) {
                    this.log(`→ Found alternative target, trying ${altTarget.hotspotConfig?.id || altTarget.hotspotConfig?.name}`);
                    scene.interactionSystem.interact(altTarget, mode);
                }
            }
        }
    }
    
    performBossAction(scene, actionKey) {
        // Wait for player turn to be available (with retry logic)
        if (!scene?.isPlayerTurn && scene?.combatActive) {
            this.log(`⏳ Waiting for player turn... (combatActive: ${scene.combatActive}, isPlayerTurn: ${scene.isPlayerTurn})`);
            // Retry after a delay (up to 5 times)
            const retryCount = this.stateData?.bossActionRetries || 0;
            if (retryCount < 5) {
                this.stateData = { ...this.stateData, bossActionRetries: retryCount + 1 };
                this.stepTimer = setTimeout(() => {
                    this.currentStep--; // Retry this step
                    this.executeNextStep();
                }, 2000);
            } else {
                this.log(`⚠ Max retries reached for boss action, skipping`);
                this.stateData = { ...this.stateData, bossActionRetries: 0 };
                this.scheduleNext(1000);
            }
            return;
        }
        
        // Reset retry counter on success
        this.stateData = { ...this.stateData, bossActionRetries: 0 };
        
        // Click the boss action button
        if (scene?.playerAction) {
            scene.playerAction(actionKey);
            this.log(`→ Boss action: ${actionKey}`);
        } else if (scene?.actionButtons) {
            // Try to find and click the button directly
            const buttonData = scene.actionButtons.find(b => b.action?.key === actionKey);
            if (buttonData && buttonData.btn) {
                if (buttonData.btn.visible) {
                    // Simulate click
                    buttonData.btn.emit('pointerdown');
                    this.log(`→ Boss action (button click): ${actionKey}`);
                } else {
                    // Button exists but not visible - wait a bit
                    this.log(`⏳ Boss action button not visible yet: ${actionKey}`);
                    this.stepTimer = setTimeout(() => {
                        this.currentStep--; // Retry
                        this.executeNextStep();
                    }, 1000);
                }
            } else {
                this.log(`⚠ Boss action button not found: ${actionKey} (available: ${scene.actionButtons.map(b => b.action?.key).join(', ')})`);
                // Try to use playerAction anyway
                if (scene.playerAction) {
                    scene.playerAction(actionKey);
                }
            }
        } else {
            this.log(`⚠ Boss action not available (scene: ${scene?.scene?.key}, has playerAction: ${!!scene?.playerAction})`);
        }
    }
    
    performEndingChoice(scene, choice) {
        // Wait for final choice UI to appear (with retry logic)
        if (!scene?.finalChoiceShown) {
            const retryCount = this.stateData?.endingRetries || 0;
            if (retryCount < 15) {
                this.log(`⏳ Waiting for final choice UI... (attempt ${retryCount + 1}/15)`);
                this.stateData = { ...this.stateData, endingRetries: retryCount + 1 };
                // Retry after a delay
                this.stepTimer = setTimeout(() => {
                    this.currentStep--; // Retry this step
                    this.executeNextStep();
                }, 2000);
            } else {
                this.log(`⚠ Max retries reached for ending choice, trying to force show`);
                this.stateData = { ...this.stateData, endingRetries: 0 };
                // Try to force show the choice UI
                if (scene && typeof scene._showFinalChoice === 'function') {
                    scene._showFinalChoice();
                    this.stepTimer = setTimeout(() => {
                        this.currentStep--; // Retry after forcing show
                        this.executeNextStep();
                    }, 1000);
                }
            }
            return;
        }
        
        // Reset retry counter
        this.stateData = { ...this.stateData, endingRetries: 0 };
        
        // Map choice keys
        const choiceMap = {
            'free': 'free',
            'join': 'merge',
            'destroy': 'destroy',
            'merge': 'merge'
        };
        
        const mappedChoice = choiceMap[choice] || 'free';
        
        if (scene?.ending) {
            scene.ending(mappedChoice);
            this.log(`→ Chose ending: ${mappedChoice} (from ${choice})`);
        } else if (scene?.endingButtons) {
            // Try to find and click the button directly
            const buttonData = scene.endingButtons.find(b => b.key === mappedChoice);
            if (buttonData && buttonData.btn) {
                buttonData.btn.emit('pointerdown');
                this.log(`→ Chose ending (button click): ${mappedChoice}`);
            } else {
                this.log(`⚠ Ending button not found: ${mappedChoice} (available: ${scene.endingButtons.map(b => b.key).join(', ')})`);
                // Try to find by partial match
                const altButton = scene.endingButtons.find(b => 
                    b.key.includes(mappedChoice) || mappedChoice.includes(b.key)
                );
                if (altButton && altButton.btn) {
                    altButton.btn.emit('pointerdown');
                    this.log(`→ Chose ending (alternative match): ${altButton.key}`);
                }
            }
        } else {
            this.log(`⚠ Ending choice not available (has ending: ${!!scene?.ending}, has buttons: ${!!scene?.endingButtons})`);
        }
    }
    
    getCurrentScene() {
        // Try multiple ways to get the current scene
        if (window.game) {
            // Method 1: Phaser scene manager (get active scenes)
            const activeScenes = window.game.scene.getScenes(true);
            if (activeScenes && activeScenes.length > 0) {
                // Find the one that's actually active
                const active = activeScenes.find(s => s.scene && s.scene.isActive);
                if (active) return active;
                // Otherwise return the first one
                return activeScenes[0];
            }
            
            // Method 2: Direct scene access
            const scenes = window.game.scene.scenes;
            if (scenes && scenes.length > 0) {
                // Return the most recently started scene (last in array)
                return scenes[scenes.length - 1];
            }
            
            // Method 3: Try scene manager directly
            if (window.game.scene.sceneManager) {
                const running = window.game.scene.sceneManager.getScenes(true);
                if (running && running.length > 0) {
                    return running[running.length - 1];
                }
            }
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
            } else if (!dialogueSystem?.isActive && this.isRunning) {
                // Dialogue finished, continue with next step
                // Don't schedule here - let the normal flow continue
            }
        }, this.dialogueSpeed);
    }
    
    /**
     * Get current progress for debugging
     */
    getProgress() {
        return {
            currentStep: this.currentStep,
            totalSteps: this.script.length,
            progress: this.script.length > 0 ? (this.currentStep / this.script.length * 100).toFixed(1) + '%' : '0%',
            isRunning: this.isRunning,
            isPaused: this.isPaused,
            currentScene: this.getCurrentScene()?.scene?.key || 'none'
        };
    }
}

// Create global instance
const autoPlayer = new AutoPlayer();
