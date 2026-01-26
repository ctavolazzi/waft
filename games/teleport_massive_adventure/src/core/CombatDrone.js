/**
 * CombatDrone - Aziah's Back-Mounted Combat Drone
 * 
 * A small drone that pops off Aziah's back and automatically targets/shoots enemies.
 * 
 * Features:
 * - Follows player position
 * - Auto-targets nearest enemy
 * - Fires projectiles at enemies
 * - Visual effects (drone sprite, projectiles, muzzle flash)
 * - Combat integration
 */

class CombatDrone {
    constructor(scene, player) {
        this.scene = scene;
        this.player = player;
        
        // Drone state
        this.isActive = false;
        this.isDeployed = false;
        this.droneSprite = null;
        this.offsetX = 0;
        this.offsetY = -40; // Above player's back
        
        // Targeting
        this.target = null;
        this.targetRange = 300; // Max distance to target enemies
        this.lastTargetCheck = 0;
        this.targetCheckInterval = 200; // Check for targets every 200ms
        
        // Combat
        this.lastShotTime = 0;
        this.shotCooldown = 1000; // 1 second between shots
        this.damage = 12;
        this.projectiles = [];
        
        // Abilities
        this.abilities = {
            burst: {
                name: 'Burst Shot',
                cooldown: 5000, // 5 seconds
                lastUsed: 0,
                active: false
            },
            shield: {
                name: 'Shield Mode',
                cooldown: 10000, // 10 seconds
                duration: 3000, // 3 seconds active
                lastUsed: 0,
                active: false,
                shieldSprite: null
            }
        };
        
        // Visual effects
        this.muzzleFlash = null;
        this.trailGraphics = null;
        
        // Systems (set via init)
        this.combatSystem = null;
        this.npcSystem = null;
        this.statsSystem = null;
        
        // UI
        this.abilityBar = null;
    }
    
    /**
     * Initialize with system references
     */
    init(systems) {
        this.combatSystem = systems.combatSystem;
        this.npcSystem = systems.npcSystem;
        this.statsSystem = systems.statsSystem;
        
        // Setup ability bar UI
        this._setupAbilityBar();
    }
    
    /**
     * Setup ability bar UI
     */
    _setupAbilityBar() {
        this.abilityBar = document.getElementById('ability-bar');
        if (!this.abilityBar) return;
        
        // Setup ability slots
        const ability1 = document.getElementById('ability-1');
        const ability2 = document.getElementById('ability-2');
        
        if (ability1) {
            ability1.addEventListener('click', () => this.useAbility('burst'));
        }
        if (ability2) {
            ability2.addEventListener('click', () => this.useAbility('shield'));
        }
        
        // Keyboard shortcuts (set up in update loop to avoid timing issues)
        this._keyboardSetup = false;
    }
    
    /**
     * Activate the drone (deploy from player's back)
     */
    activate() {
        if (this.isActive) return;
        
        this.isActive = true;
        this.isDeployed = false;
        
        // Show ability bar
        if (this.abilityBar) {
            this.abilityBar.classList.add('visible');
        }
        
        // Create drone sprite (small, above player)
        if (!this.droneSprite && this.player?.sprite) {
            // Use security_drone sprite if available, otherwise use a simple circle
            const hasDroneSprite = this.scene.textures.exists('security_drone_south');
            
            if (hasDroneSprite) {
                this.droneSprite = this.scene.add.sprite(
                    this.player.sprite.x + this.offsetX,
                    this.player.sprite.y + this.offsetY,
                    'security_drone_south'
                );
            } else if (this.scene.textures.exists('combat_drone_south')) {
                // Try combat_drone_* keys
                this.droneSprite = this.scene.add.sprite(
                    this.player.sprite.x + this.offsetX,
                    this.player.sprite.y + this.offsetY,
                    'combat_drone_south'
                );
            } else {
                // Fallback: create a simple drone graphic
                this.droneSprite = this.scene.add.circle(
                    this.player.sprite.x + this.offsetX,
                    this.player.sprite.y + this.offsetY,
                    8,
                    0x00ff88,
                    1
                );
                // Add a small glow
                const glow = this.scene.add.circle(
                    this.player.sprite.x + this.offsetX,
                    this.player.sprite.y + this.offsetY,
                    12,
                    0x00ff88,
                    0.3
                );
                glow.setDepth(this.droneSprite.depth - 1);
            }
            
            this.droneSprite.setScale(0.6);
            this.droneSprite.setDepth(this.player.sprite.depth + 1);
            
            // Deploy animation (pop off back)
            this._deployAnimation();
        }
        
        // Create trail graphics for projectiles
        this.trailGraphics = this.scene.add.graphics();
        
        // Emit event
        if (window.eventBus) {
            window.eventBus.emit('drone:activated', { player: 'aziah' });
        }
    }
    
    /**
     * Deactivate the drone (retract to back)
     */
    deactivate() {
        if (!this.isActive) return;
        
        this.isActive = false;
        this.isDeployed = false;
        this.target = null;
        
        // Hide ability bar
        if (this.abilityBar) {
            this.abilityBar.classList.remove('visible');
        }
        
        // Deactivate shield if active
        if (this.abilities.shield.active) {
            this._deactivateShield();
        }
        
        // Retract animation
        if (this.droneSprite) {
            this.scene.tweens.add({
                targets: this.droneSprite,
                x: this.player.sprite.x + this.offsetX,
                y: this.player.sprite.y + this.offsetY,
                scale: 0,
                alpha: 0,
                duration: 300,
                ease: 'Back.easeIn',
                onComplete: () => {
                    if (this.droneSprite) {
                        this.droneSprite.destroy();
                        this.droneSprite = null;
                    }
                }
            });
        }
        
        // Clear projectiles
        this.projectiles.forEach(proj => {
            if (proj.sprite) proj.sprite.destroy();
        });
        this.projectiles = [];
        
        // Emit event
        if (window.eventBus) {
            window.eventBus.emit('drone:deactivated', { player: 'aziah' });
        }
    }
    
    /**
     * Deploy animation (drone pops off back)
     */
    _deployAnimation() {
        if (!this.droneSprite) return;
        
        const startX = this.player.sprite.x + this.offsetX;
        const startY = this.player.sprite.y + this.offsetY;
        const deployX = startX + 20; // Pop out to the side
        const deployY = startY - 15; // Pop up
        
        // Start hidden, then pop out
        this.droneSprite.setAlpha(0);
        this.droneSprite.setScale(0);
        
        this.scene.tweens.add({
            targets: this.droneSprite,
            x: deployX,
            y: deployY,
            alpha: 1,
            scale: 0.6,
            duration: 400,
            ease: 'Back.easeOut',
            onComplete: () => {
                this.isDeployed = true;
            }
        });
    }
    
    /**
     * Update drone position and behavior
     */
    update(time, delta) {
        if (!this.isActive || !this.droneSprite || !this.player?.sprite) return;
        
        // Setup keyboard shortcuts once
        if (!this._keyboardSetup && this.scene && this.scene.input && this.scene.input.keyboard) {
            const key1 = this.scene.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.ONE);
            const key2 = this.scene.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.TWO);
            
            key1.on('down', () => this.useAbility('burst'));
            key2.on('down', () => this.useAbility('shield'));
            
            this._keyboardSetup = true;
        }
        
        // Follow player (with slight offset)
        const targetX = this.player.sprite.x + this.offsetX;
        const targetY = this.player.sprite.y + this.offsetY;
        
        // Smooth follow
        const followSpeed = 0.15;
        this.droneSprite.x += (targetX - this.droneSprite.x) * followSpeed;
        this.droneSprite.y += (targetY - this.droneSprite.y) * followSpeed;
        
        // Keep depth sorted
        this.droneSprite.setDepth(this.player.sprite.depth + 1);
        
        // Find and target enemies
        if (time - this.lastTargetCheck > this.targetCheckInterval) {
            this._findTarget();
            this.lastTargetCheck = time;
        }
        
        // Shoot at target if available
        if (this.target && this.isDeployed) {
            if (time - this.lastShotTime > this.shotCooldown) {
                this._shoot();
                this.lastShotTime = time;
            }
        }
        
        // Update projectiles
        this._updateProjectiles(time, delta);
        
        // Update shield if active
        this._updateShield();
    }
    
    /**
     * Find nearest enemy to target
     */
    _findTarget() {
        if (!this.npcSystem || !this.droneSprite) return;
        
        const droneX = this.droneSprite.x;
        const droneY = this.droneSprite.y;
        
        let nearestEnemy = null;
        let nearestDistance = this.targetRange;
        
        // Get all NPCs
        const npcs = this.npcSystem.getAllNPCs();
        
        npcs.forEach(npc => {
            // Only target hostile NPCs
            if (!npc.hostile) return;
            
            // Check if NPC is in same scene
            if (npc.roomId !== this.player.roomId) return;
            
            // Calculate distance
            const dx = npc.x - droneX;
            const dy = npc.y - droneY;
            const distance = Math.sqrt(dx * dx + dy * dy);
            
            if (distance < nearestDistance) {
                nearestDistance = distance;
                nearestEnemy = npc;
            }
        });
        
        this.target = nearestEnemy;
        
        // Rotate drone to face target
        if (this.target && this.droneSprite) {
            const angle = Phaser.Math.Angle.Between(
                this.droneSprite.x,
                this.droneSprite.y,
                this.target.x,
                this.target.y
            );
            this.droneSprite.setRotation(angle + Math.PI / 2); // Adjust for sprite orientation
        }
    }
    
    /**
     * Shoot projectile at target
     */
    _shoot() {
        if (!this.target || !this.droneSprite) return;
        
        // Use helper method
        this._createProjectile(
            this.droneSprite.x,
            this.droneSprite.y,
            this.target.x,
            this.target.y,
            this.target.id,
            this.damage
        );
        
        // Muzzle flash effect
        this._createMuzzleFlash();
        
        // Sound effect (if available)
        // this.scene.sound.play('drone_shot', { volume: 0.3 });
    }
    
    /**
     * Create muzzle flash effect
     */
    _createMuzzleFlash() {
        if (!this.droneSprite) return;
        
        // Create flash sprite
        const flash = this.scene.add.circle(
            this.droneSprite.x,
            this.droneSprite.y,
            6,
            0xffffff,
            1
        );
        flash.setDepth(this.droneSprite.depth + 2);
        
        // Animate flash
        this.scene.tweens.add({
            targets: flash,
            scale: 2,
            alpha: 0,
            duration: 100,
            ease: 'Power2',
            onComplete: () => flash.destroy()
        });
    }
    
    /**
     * Update projectile positions and collisions
     */
    _updateProjectiles(time, delta) {
        for (let i = this.projectiles.length - 1; i >= 0; i--) {
            const proj = this.projectiles[i];
            
            // Check lifetime
            if (time - proj.createdAt > proj.lifetime) {
                this._destroyProjectile(i);
                continue;
            }
            
            // Move projectile toward target
            const dx = proj.targetX - proj.sprite.x;
            const dy = proj.targetY - proj.sprite.y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            
            if (distance < 5) {
                // Hit target
                this._hitTarget(proj);
                this._destroyProjectile(i);
                continue;
            }
            
            // Move projectile
            const moveSpeed = (proj.speed * delta) / 1000;
            const moveX = (dx / distance) * moveSpeed;
            const moveY = (dy / distance) * moveSpeed;
            
            proj.sprite.x += moveX;
            proj.sprite.y += moveY;
            
            // Update trail
            if (proj.trail) {
                proj.trail.x = proj.sprite.x;
                proj.trail.y = proj.sprite.y;
            }
            
            // Check collision with target
            if (this.target && this.target.id === proj.targetId) {
                const targetDx = this.target.x - proj.sprite.x;
                const targetDy = this.target.y - proj.sprite.y;
                const targetDist = Math.sqrt(targetDx * targetDx + targetDy * targetDy);
                
                if (targetDist < 15) { // Hit radius
                    this._hitTarget(proj);
                    this._destroyProjectile(i);
                }
            }
        }
    }
    
    /**
     * Handle projectile hitting target
     */
    _hitTarget(projectile) {
        if (!this.combatSystem || !projectile.targetId) return;
        
        // Deal damage through combat system
        this.combatSystem.attack('aziah_drone', projectile.targetId, {
            baseDamage: projectile.damage,
            source: 'drone'
        });
        
        // Hit effect
        this._createHitEffect(projectile.sprite.x, projectile.sprite.y);
    }
    
    /**
     * Create hit effect (spark/explosion)
     */
    _createHitEffect(x, y) {
        // Create spark particles
        for (let i = 0; i < 5; i++) {
            const spark = this.scene.add.circle(
                x + Phaser.Math.Between(-5, 5),
                y + Phaser.Math.Between(-5, 5),
                2,
                0xffaa00,
                1
            );
            spark.setDepth(this.droneSprite.depth + 2);
            
            const angle = (i / 5) * Math.PI * 2;
            const distance = Phaser.Math.Between(10, 20);
            
            this.scene.tweens.add({
                targets: spark,
                x: x + Math.cos(angle) * distance,
                y: y + Math.sin(angle) * distance,
                alpha: 0,
                scale: 0,
                duration: 300,
                ease: 'Power2',
                onComplete: () => spark.destroy()
            });
        }
    }
    
    /**
     * Destroy projectile
     */
    _destroyProjectile(index) {
        const proj = this.projectiles[index];
        if (proj.sprite) proj.sprite.destroy();
        if (proj.trail) proj.trail.destroy();
        this.projectiles.splice(index, 1);
    }
    
    /**
     * Use an ability
     */
    useAbility(abilityKey) {
        if (!this.isActive || !this.isDeployed) return false;
        
        const ability = this.abilities[abilityKey];
        if (!ability) return false;
        
        const now = this.scene.time.now;
        const timeSinceUse = now - ability.lastUsed;
        
        // Check cooldown
        if (timeSinceUse < ability.cooldown) {
            // Show cooldown feedback
            this._showCooldownFeedback(abilityKey);
            return false;
        }
        
        // Use ability
        ability.lastUsed = now;
        
        switch (abilityKey) {
            case 'burst':
                this._useBurstShot();
                break;
            case 'shield':
                this._useShieldMode();
                break;
        }
        
        // Update UI
        this._updateAbilityUI(abilityKey);
        
        return true;
    }
    
    /**
     * Burst Shot ability - fires multiple projectiles in spread pattern
     */
    _useBurstShot() {
        if (!this.target && !this.droneSprite) return;
        
        const burstCount = 5;
        const spreadAngle = Math.PI / 3; // 60 degree spread
        
        // If no target, shoot forward
        let baseAngle = 0;
        if (this.target) {
            baseAngle = Phaser.Math.Angle.Between(
                this.droneSprite.x,
                this.droneSprite.y,
                this.target.x,
                this.target.y
            );
        }
        
        // Fire multiple projectiles
        for (let i = 0; i < burstCount; i++) {
            const angle = baseAngle + (i - burstCount / 2) * (spreadAngle / burstCount);
            const targetX = this.droneSprite.x + Math.cos(angle) * 200;
            const targetY = this.droneSprite.y + Math.sin(angle) * 200;
            
            this._createProjectile(
                this.droneSprite.x,
                this.droneSprite.y,
                targetX,
                targetY,
                this.target?.id || null,
                this.damage * 0.8 // Slightly less damage per shot
            );
        }
        
        // Enhanced muzzle flash
        this._createMuzzleFlash();
        this._createMuzzleFlash();
        
        // Emit event
        if (window.eventBus) {
            window.eventBus.emit('drone:ability', { ability: 'burst', player: 'aziah' });
        }
    }
    
    /**
     * Shield Mode ability - creates temporary shield
     */
    _useShieldMode() {
        if (this.abilities.shield.active) return; // Already active
        
        this.abilities.shield.active = true;
        
        // Create shield visual
        if (this.player?.sprite) {
            this.abilities.shield.shieldSprite = this.scene.add.circle(
                this.player.sprite.x,
                this.player.sprite.y,
                30,
                0x00ff88,
                0.3
            );
            this.abilities.shield.shieldSprite.setStrokeStyle(3, 0x00ff88, 0.8);
            this.abilities.shield.shieldSprite.setDepth(this.player.sprite.depth + 2);
            
            // Pulsing animation
            this.scene.tweens.add({
                targets: this.abilities.shield.shieldSprite,
                scale: 1.2,
                alpha: 0.5,
                duration: 500,
                yoyo: true,
                repeat: -1,
                ease: 'Sine.easeInOut'
            });
        }
        
        // Auto-deactivate after duration
        this.scene.time.delayedCall(this.abilities.shield.duration, () => {
            this._deactivateShield();
        });
        
        // Emit event
        if (window.eventBus) {
            window.eventBus.emit('drone:ability', { ability: 'shield', player: 'aziah' });
        }
    }
    
    /**
     * Deactivate shield
     */
    _deactivateShield() {
        if (!this.abilities.shield.active) return;
        
        this.abilities.shield.active = false;
        
        if (this.abilities.shield.shieldSprite) {
            // Fade out
            this.scene.tweens.add({
                targets: this.abilities.shield.shieldSprite,
                alpha: 0,
                scale: 0.5,
                duration: 300,
                onComplete: () => {
                    if (this.abilities.shield.shieldSprite) {
                        this.abilities.shield.shieldSprite.destroy();
                        this.abilities.shield.shieldSprite = null;
                    }
                }
            });
        }
    }
    
    /**
     * Create projectile (extracted for reuse)
     */
    _createProjectile(startX, startY, targetX, targetY, targetId, damage) {
        const projectile = {
            sprite: this.scene.add.circle(startX, startY, 3, 0x00ff88, 1),
            startX: startX,
            startY: startY,
            targetX: targetX,
            targetY: targetY,
            speed: 400,
            damage: damage || this.damage,
            targetId: targetId,
            lifetime: 2000,
            createdAt: this.scene.time.now
        };
        
        projectile.sprite.setDepth(this.droneSprite.depth + 1);
        projectile.sprite.setStrokeStyle(1, 0xffffff, 0.8);
        
        // Add glow trail
        const trail = this.scene.add.circle(startX, startY, 5, 0x00ff88, 0.5);
        trail.setDepth(projectile.sprite.depth - 1);
        projectile.trail = trail;
        
        this.projectiles.push(projectile);
    }
    
    /**
     * Update ability UI cooldowns
     */
    _updateAbilityUI(abilityKey) {
        if (!this.abilityBar) return;
        
        const slot = document.getElementById(`ability-${abilityKey === 'burst' ? '1' : '2'}`);
        if (!slot) return;
        
        const ability = this.abilities[abilityKey];
        const now = this.scene.time.now;
        const timeSinceUse = now - ability.lastUsed;
        const remainingCooldown = Math.max(0, ability.cooldown - timeSinceUse);
        
        // Add cooldown class
        slot.classList.add('cooldown');
        
        // Show cooldown timer
        let cooldownDisplay = slot.querySelector('.ability-cooldown');
        if (!cooldownDisplay) {
            cooldownDisplay = document.createElement('div');
            cooldownDisplay.className = 'ability-cooldown';
            slot.appendChild(cooldownDisplay);
        }
        
        // Update cooldown display
        const updateCooldown = () => {
            const currentTime = this.scene.time.now;
            const currentRemaining = Math.max(0, ability.cooldown - (currentTime - ability.lastUsed));
            
            if (currentRemaining > 0) {
                cooldownDisplay.textContent = Math.ceil(currentRemaining / 1000);
                requestAnimationFrame(updateCooldown);
            } else {
                slot.classList.remove('cooldown');
                if (cooldownDisplay.parentNode) {
                    cooldownDisplay.remove();
                }
            }
        };
        
        updateCooldown();
    }
    
    /**
     * Show cooldown feedback
     */
    _showCooldownFeedback(abilityKey) {
        const slot = document.getElementById(`ability-${abilityKey === 'burst' ? '1' : '2'}`);
        if (slot) {
            // Flash effect
            slot.style.borderColor = '#ff4444';
            setTimeout(() => {
                slot.style.borderColor = '';
            }, 200);
        }
    }
    
    /**
     * Update shield position if active
     */
    _updateShield() {
        if (!this.abilities.shield.active || !this.abilities.shield.shieldSprite || !this.player?.sprite) return;
        
        // Follow player
        this.abilities.shield.shieldSprite.x = this.player.sprite.x;
        this.abilities.shield.shieldSprite.y = this.player.sprite.y;
        this.abilities.shield.shieldSprite.setDepth(this.player.sprite.depth + 2);
    }
    
    /**
     * Cleanup (call on scene shutdown)
     */
    destroy() {
        this.deactivate();
        if (this.trailGraphics) {
            this.trailGraphics.destroy();
            this.trailGraphics = null;
        }
        if (this.abilities.shield.shieldSprite) {
            this.abilities.shield.shieldSprite.destroy();
            this.abilities.shield.shieldSprite = null;
        }
    }
}

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CombatDrone;
}
