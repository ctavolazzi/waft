/**
 * PlayerController - Character movement and interaction
 * 
 * Supports TWO input modes:
 * 1. Click anywhere → character walks there (point-and-click)
 * 2. Arrow keys / WASD → direct movement (action RPG style)
 */
class PlayerController {
    constructor(scene) {
        this.scene = scene;
        this.sprite = null;
        this.walkSpeed = 150;
        
        // Movement state
        this.isMoving = false;
        this.targetX = 0;
        this.targetY = 0;
        this.pendingInteraction = null;
        
        // Keyboard movement
        this.cursors = null;
        this.wasd = null;
        this.isKeyboardMoving = false;
        
        // Walkable area
        this.walkableArea = null;
        
        // Animation frames
        this.direction = 'south';
        this.animating = false;
        
        // Combat drone
        this.combatDrone = null;
        this.hasDrone = false; // Set to true when drone is acquired
    }
    
    // ========================================
    // Setup
    // ========================================
    
    create(x, y, spriteKey = 'aziah_south') {
        this.sprite = this.scene.add.sprite(x, y, spriteKey);
        this.sprite.setScale(1.5);
        this.sprite.setDepth(y); // Depth sorting
        
        // Store reference on sprite
        this.sprite.controller = this;
        
        return this.sprite;
    }
    
    setWalkableArea(bounds) {
        // bounds: { x, y, width, height }
        this.walkableArea = bounds;
    }
    
    // ========================================
    // Keyboard Input Setup
    // ========================================
    
    setupKeyboardInput() {
        // Arrow keys
        this.cursors = this.scene.input.keyboard.createCursorKeys();
        
        // WASD keys
        this.wasd = {
            up: this.scene.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.W),
            down: this.scene.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.S),
            left: this.scene.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.A),
            right: this.scene.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.D)
        };
        
        // Interaction key (E or Space when using keyboard)
        this.interactKey = this.scene.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.E);
    }
    
    // ========================================
    // Click Handling
    // ========================================
    
    handleClick(worldX, worldY, target = null) {
        // Clamp to walkable area
        const dest = this.clampToWalkable(worldX, worldY);
        
        // If clicking on an interactable, store it for after walking
        if (target && (target.hotspotConfig || target.npcConfig)) {
            this.pendingInteraction = target;
            
            // Walk to a point near the target, not on top of it
            const interactPoint = this.getInteractionPoint(target, dest);
            this.walkTo(interactPoint.x, interactPoint.y);
        } else {
            // Just walk to the point
            this.pendingInteraction = null;
            this.walkTo(dest.x, dest.y);
        }
    }
    
    getInteractionPoint(target, clickPoint) {
        // Get the target's position
        let targetX, targetY;
        
        if (target.hotspotConfig) {
            targetX = target.hotspotConfig.position.x;
            targetY = target.hotspotConfig.position.y + (target.hotspotConfig.size.height / 2);
        } else if (target.npcConfig) {
            targetX = target.npcConfig.position.x;
            targetY = target.npcConfig.position.y + 30;
        } else {
            return clickPoint;
        }
        
        // Stand slightly in front of the target (below it in screen coords)
        const standY = Math.min(targetY + 40, this.walkableArea.y + this.walkableArea.height - 10);
        
        return this.clampToWalkable(targetX, standY);
    }
    
    // ========================================
    // Movement
    // ========================================
    
    walkTo(x, y) {
        this.targetX = x;
        this.targetY = y;
        this.isMoving = true;
        
        // Calculate direction
        this.updateDirection(x, y);
        
        // Start walk animation
        this.playWalkAnimation();
        
        // Emit movement event
        eventBus.emit(EventBus.PLAYER_MOVE, { 
            from: { x: this.sprite.x, y: this.sprite.y },
            to: { x, y }
        });
    }
    
    updateDirection(targetX, targetY) {
        const dx = targetX - this.sprite.x;
        const dy = targetY - this.sprite.y;
        
        // Determine primary direction
        if (Math.abs(dx) > Math.abs(dy)) {
            this.direction = dx > 0 ? 'east' : 'west';
        } else {
            this.direction = dy > 0 ? 'south' : 'north';
        }
        
        // Update sprite texture
        this.updateSprite();
    }
    
    updateSprite() {
        const key = `aziah_${this.direction}`;
        if (this.scene.textures.exists(key)) {
            this.sprite.setTexture(key);
        }
    }
    
    playWalkAnimation() {
        if (this.animating) return;
        this.animating = true;
        
        // Simple bob animation
        this.scene.tweens.add({
            targets: this.sprite,
            scaleY: 1.45,
            duration: 150,
            yoyo: true,
            repeat: -1,
            onStop: () => {
                this.sprite.setScale(1.5);
                this.animating = false;
            }
        });
    }
    
    stopWalkAnimation() {
        this.scene.tweens.killTweensOf(this.sprite);
        this.sprite.setScale(1.5);
        this.animating = false;
    }
    
    // ========================================
    // Update Loop
    // ========================================
    
    update(delta) {
        if (!this.sprite) return;
        
        // Check for keyboard movement first (takes priority)
        const keyboardHandled = this.handleKeyboardMovement(delta);
        
        // If keyboard is being used, cancel any click-to-walk movement
        if (keyboardHandled) {
            if (this.isMoving) {
                this.isMoving = false;
                this.pendingInteraction = null;
                this.stopWalkAnimation();
            }
            this.isKeyboardMoving = true;
            // Update game state position for keyboard movement
            gameState.set('playerPosition', { x: this.sprite.x, y: this.sprite.y });
            return;
        } else {
            // No keyboard input - stop keyboard movement state
            if (this.isKeyboardMoving) {
                this.isKeyboardMoving = false;
                this.stopWalkAnimation();
            }
        }
        
        // Click-to-walk movement
        if (!this.isMoving) return;
        
        const dx = this.targetX - this.sprite.x;
        const dy = this.targetY - this.sprite.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        // Arrived at destination
        if (distance < 5) {
            this.arrive();
            return;
        }
        
        // Move towards target
        const speed = this.walkSpeed * (delta / 1000);
        const moveX = (dx / distance) * speed;
        const moveY = (dy / distance) * speed;
        
        // Clamp movement to prevent overshooting
        if (Math.abs(moveX) > Math.abs(dx)) {
            this.sprite.x = this.targetX;
        } else {
            this.sprite.x += moveX;
        }
        
        if (Math.abs(moveY) > Math.abs(dy)) {
            this.sprite.y = this.targetY;
        } else {
            this.sprite.y += moveY;
        }
        
        // Update depth for sorting
        this.sprite.setDepth(this.sprite.y);
        
        // Update direction periodically (not every frame for performance)
        if (Math.floor(Date.now() / 100) % 3 === 0) {
            this.updateDirection(this.targetX, this.targetY);
        }
        
        // Update game state position
        gameState.set('playerPosition', { x: this.sprite.x, y: this.sprite.y });
    }
    
    // ========================================
    // Keyboard Movement
    // ========================================
    
    handleKeyboardMovement(delta) {
        if (!this.cursors && !this.wasd) return false;
        
        // Don't move during dialogue
        if (dialogueSystem?.isActive) return false;
        
        // Get input direction
        let dx = 0;
        let dy = 0;
        
        // Arrow keys
        if (this.cursors) {
            if (this.cursors.left.isDown) dx -= 1;
            if (this.cursors.right.isDown) dx += 1;
            if (this.cursors.up.isDown) dy -= 1;
            if (this.cursors.down.isDown) dy += 1;
        }
        
        // WASD (additive, so both work)
        if (this.wasd) {
            if (this.wasd.left.isDown) dx -= 1;
            if (this.wasd.right.isDown) dx += 1;
            if (this.wasd.up.isDown) dy -= 1;
            if (this.wasd.down.isDown) dy += 1;
        }
        
        // Clamp to -1, 0, 1
        dx = Math.max(-1, Math.min(1, dx));
        dy = Math.max(-1, Math.min(1, dy));
        
        // No movement
        if (dx === 0 && dy === 0) return false;
        
        // Calculate speed (normalize diagonal movement)
        const speed = this.walkSpeed * (delta / 1000);
        let moveX = dx * speed;
        let moveY = dy * speed;
        
        // Normalize diagonal movement
        if (dx !== 0 && dy !== 0) {
            const factor = 0.707; // 1/sqrt(2)
            moveX *= factor;
            moveY *= factor;
        }
        
        // Calculate new position
        let newX = this.sprite.x + moveX;
        let newY = this.sprite.y + moveY;
        
        // Clamp to walkable area
        const clamped = this.clampToWalkable(newX, newY);
        newX = clamped.x;
        newY = clamped.y;
        
        // Apply movement
        this.sprite.x = newX;
        this.sprite.y = newY;
        this.sprite.setDepth(newY);
        
        // Update direction based on input
        this.updateDirectionFromInput(dx, dy);
        
        // Start animation if not already
        if (!this.animating) {
            this.playWalkAnimation();
        }
        
        // Update game state
        gameState.set('playerPosition', { x: newX, y: newY });
        
        return true;
    }
    
    updateDirectionFromInput(dx, dy) {
        // Prioritize horizontal if moving diagonally
        if (Math.abs(dx) >= Math.abs(dy)) {
            if (dx > 0) this.direction = 'east';
            else if (dx < 0) this.direction = 'west';
        } else {
            if (dy > 0) this.direction = 'south';
            else if (dy < 0) this.direction = 'north';
        }
        
        this.updateSprite();
    }
    
    arrive() {
        this.isMoving = false;
        this.stopWalkAnimation();
        
        // Handle pending interaction
        if (this.pendingInteraction) {
            const target = this.pendingInteraction;
            this.pendingInteraction = null;
            
            // Face the target
            this.faceTarget(target);
            
            // Small delay then interact
            this.scene.time.delayedCall(100, () => {
                this.interact(target);
            });
        }
    }
    
    faceTarget(target) {
        let targetX;
        if (target.hotspotConfig) {
            targetX = target.hotspotConfig.position.x;
        } else if (target.npcConfig) {
            targetX = target.npcConfig.position.x;
        } else {
            return;
        }
        
        // Just face left or right for now
        if (targetX < this.sprite.x) {
            this.direction = 'west';
        } else if (targetX > this.sprite.x) {
            this.direction = 'east';
        } else {
            this.direction = 'north'; // Looking at something directly above
        }
        this.updateSprite();
    }
    
    // ========================================
    // Interaction
    // ========================================
    
    interact(target) {
        if (!target) return;
        
        // Get the interaction system from scene or global
        const interactionSystem = this.scene.interactionSystem || window.interactionSystem;
        
        if (interactionSystem) {
            // Default to 'use' for items that can be picked up
            const config = target.hotspotConfig || target.npcConfig;
            
            if (config) {
                // Check for pickup interaction
                if (config.interactions?.pickup) {
                    interactionSystem.interact(target, 'pickup');
                } 
                // Check for use interaction
                else if (config.interactions?.use) {
                    interactionSystem.interact(target, 'use');
                }
                // NPC - talk
                else if (target.npcConfig) {
                    interactionSystem.interact(target, 'talk');
                }
                // Default - look
                else {
                    interactionSystem.interact(target, 'look');
                }
            }
        }
        
        eventBus.emit(EventBus.PLAYER_INTERACT, { target: config?.id || 'unknown' });
    }
    
    // ========================================
    // Utility
    // ========================================
    
    clampToWalkable(x, y) {
        if (!this.walkableArea) return { x, y };
        
        const area = this.walkableArea;
        return {
            x: Math.max(area.x, Math.min(area.x + area.width, x)),
            y: Math.max(area.y, Math.min(area.y + area.height, y))
        };
    }
    
    setPosition(x, y) {
        if (this.sprite) {
            this.sprite.x = x;
            this.sprite.y = y;
            this.sprite.setDepth(y);
        }
    }
    
    getPosition() {
        return this.sprite ? { x: this.sprite.x, y: this.sprite.y } : { x: 0, y: 0 };
    }
    
    // ========================================
    // Combat Drone
    // ========================================
    
    /**
     * Initialize combat drone
     */
    initCombatDrone(systems) {
        if (!this.hasDrone) return;
        
        if (!this.combatDrone) {
            this.combatDrone = new CombatDrone(this.scene, this);
            this.combatDrone.init(systems);
        }
    }
    
    /**
     * Activate combat drone
     */
    activateDrone() {
        if (!this.hasDrone) return;
        
        if (!this.combatDrone) {
            // Initialize if not already done
            if (window.gameManager) {
                const combatSystem = window.gameManager.getSystem('combatSystem');
                const npcSystem = window.gameManager.getSystem('npcSystem');
                const statsSystem = window.gameManager.getSystem('statsSystem');
                
                if (combatSystem && npcSystem && statsSystem) {
                    this.combatDrone = new CombatDrone(this.scene, this);
                    this.combatDrone.init({
                        combatSystem,
                        npcSystem,
                        statsSystem
                    });
                }
            }
        }
        
        if (this.combatDrone) {
            this.combatDrone.activate();
        }
    }
    
    /**
     * Deactivate combat drone
     */
    deactivateDrone() {
        if (this.combatDrone) {
            this.combatDrone.deactivate();
        }
    }
    
    /**
     * Acquire drone (called when player gets drone item/ability)
     */
    acquireDrone() {
        this.hasDrone = true;
        gameState.setFlag('hasCombatDrone', true);
        
        // Auto-activate if systems are ready
        if (window.gameManager) {
            const combatSystem = window.gameManager.getSystem('combatSystem');
            const npcSystem = window.gameManager.getSystem('npcSystem');
            const statsSystem = window.gameManager.getSystem('statsSystem');
            
            if (combatSystem && npcSystem && statsSystem) {
                this.initCombatDrone({
                    combatSystem,
                    npcSystem,
                    statsSystem
                });
                this.activateDrone();
                
                // Visual feedback
                if (this.scene) {
                    this.scene.cameras.main.flash(300, 0, 255, 0);
                }
            }
        }
        
        // Show notification
        if (window.dialogueSystem) {
            window.dialogueSystem.showLines('SYSTEM', [
                'Combat drone acquired!',
                'Press 1 for Burst Shot, 2 for Shield Mode.'
            ]);
        }
        
        // Update objective system
        if (window.objectiveSystem) {
            window.objectiveSystem.checkObjectives();
        }
    }
    
    // ========================================
    // Teleport (instant move)
    // ========================================
    
    teleportTo(x, y) {
        this.isMoving = false;
        this.pendingInteraction = null;
        this.stopWalkAnimation();
        this.setPosition(x, y);
    }
}
