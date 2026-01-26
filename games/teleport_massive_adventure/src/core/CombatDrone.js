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
        
        // Visual effects
        this.muzzleFlash = null;
        this.trailGraphics = null;
        
        // Systems (set via init)
        this.combatSystem = null;
        this.npcSystem = null;
        this.statsSystem = null;
    }
    
    /**
     * Initialize with system references
     */
    init(systems) {
        this.combatSystem = systems.combatSystem;
        this.npcSystem = systems.npcSystem;
        this.statsSystem = systems.statsSystem;
    }
    
    /**
     * Activate the drone (deploy from player's back)
     */
    activate() {
        if (this.isActive) return;
        
        this.isActive = true;
        this.isDeployed = false;
        
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
        
        // Create projectile
        const projectile = {
            sprite: this.scene.add.circle(
                this.droneSprite.x,
                this.droneSprite.y,
                3,
                0x00ff88,
                1
            ),
            startX: this.droneSprite.x,
            startY: this.droneSprite.y,
            targetX: this.target.x,
            targetY: this.target.y,
            speed: 400,
            damage: this.damage,
            targetId: this.target.id,
            lifetime: 2000, // 2 seconds max
            createdAt: this.scene.time.now
        };
        
        projectile.sprite.setDepth(this.droneSprite.depth + 1);
        projectile.sprite.setStrokeStyle(1, 0xffffff, 0.8);
        
        // Add glow trail
        const trail = this.scene.add.circle(
            projectile.sprite.x,
            projectile.sprite.y,
            5,
            0x00ff88,
            0.5
        );
        trail.setDepth(projectile.sprite.depth - 1);
        projectile.trail = trail;
        
        this.projectiles.push(projectile);
        
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
     * Cleanup (call on scene shutdown)
     */
    destroy() {
        this.deactivate();
        if (this.trailGraphics) {
            this.trailGraphics.destroy();
            this.trailGraphics = null;
        }
    }
}

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CombatDrone;
}
