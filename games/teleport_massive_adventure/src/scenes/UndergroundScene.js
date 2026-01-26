/**
 * UndergroundScene - Beneath TM Headquarters
 * 
 * Contains:
 * - Phaseburner NPC (glitchy, unstable)
 * - Damaged terminal with secrets
 * - Portal to The Void (appears after conditions met)
 * - Exit hatch back to lobby
 */
class UndergroundScene extends BaseScene {
    constructor() {
        super('UndergroundScene');
        this.roomId = 'underground';
    }
    
    create() {
        super.create();
        
        // Dark, oppressive atmosphere
        this.createUndergroundAmbience();
        
        // Steam particles
        this.createSteam();
        
        // Flickering lights
        this.createFlickeringLights();
        
        // Check if portal should appear
        this.checkPortalConditions();
    }
    
    createUndergroundAmbience() {
        // Darkness overlay at edges
        const darkness = this.add.graphics();
        darkness.fillStyle(0x000000, 0.5);
        darkness.fillRect(0, 0, 100, 500);
        darkness.fillRect(700, 0, 100, 500);
        darkness.fillRect(0, 0, 800, 80);
    }
    
    createSteam() {
        // Steam vents
        const vents = [150, 400, 650];
        
        vents.forEach(x => {
            for (let i = 0; i < 5; i++) {
                const steam = this.add.circle(
                    x + Phaser.Math.Between(-20, 20),
                    200,
                    Phaser.Math.Between(5, 15),
                    0xffffff,
                    0.1
                );
                
                this.tweens.add({
                    targets: steam,
                    y: steam.y - Phaser.Math.Between(50, 100),
                    alpha: 0,
                    scale: 2,
                    duration: Phaser.Math.Between(1500, 3000),
                    repeat: -1,
                    delay: Phaser.Math.Between(0, 2000),
                    onRepeat: () => {
                        steam.y = 200;
                        steam.x = x + Phaser.Math.Between(-20, 20);
                        steam.alpha = 0.1;
                        steam.scale = 1;
                    }
                });
            }
        });
    }
    
    createFlickeringLights() {
        const lights = [
            { x: 150, y: 190 },
            { x: 400, y: 190 },
            { x: 650, y: 190 }
        ];
        
        lights.forEach(pos => {
            const light = this.add.rectangle(pos.x, pos.y, 40, 8, 0xffff88, 0.4);
            const cone = this.add.triangle(
                pos.x, pos.y + 50,
                -30, 0,
                30, 0,
                0, -50,
                0xffff88, 0.05
            );
            
            // Random flicker
            this.time.addEvent({
                delay: Phaser.Math.Between(100, 500),
                callback: () => {
                    const alpha = Math.random() > 0.3 ? 0.4 : 0.1;
                    light.alpha = alpha;
                    cone.alpha = alpha * 0.15;
                },
                loop: true
            });
        });
    }
    
    checkPortalConditions() {
        // Portal appears when player has artifact AND talked to phaseburner
        if (gameState.getFlag('hasArtifact') && gameState.getFlag('talkedToPhaseburner')) {
            this.spawnPortal();
        }
        
        // Subscribe to flag changes
        gameState.subscribe('flags.talkedToPhaseburner', () => {
            if (gameState.getFlag('hasArtifact')) {
                this.spawnPortal();
            }
        });
    }
    
    spawnPortal() {
        if (this.portalSpawned) return;
        this.portalSpawned = true;
        
        // Dramatic reveal
        this.cameras.main.shake(500, 0.01);
        
        // Portal graphics
        const portal = this.add.graphics();
        portal.x = 100;
        portal.y = 340;
        
        // Outer ring
        portal.lineStyle(3, 0x8800ff, 0.8);
        portal.strokeCircle(0, 0, 40);
        
        // Inner swirl
        portal.fillStyle(0x4400aa, 0.6);
        portal.fillCircle(0, 0, 35);
        
        // Rotation animation
        this.tweens.add({
            targets: portal,
            angle: 360,
            duration: 5000,
            repeat: -1
        });
        
        // Pulse
        this.tweens.add({
            targets: portal,
            scale: 1.1,
            duration: 1000,
            yoyo: true,
            repeat: -1
        });
        
        // Make interactive
        const hitArea = this.add.circle(100, 340, 40, 0x000000, 0);
        hitArea.setInteractive();
        hitArea.hotspotConfig = {
            id: 'portal',
            name: 'Shimmering Portal',
            position: { x: 100, y: 340 },
            size: { width: 80, height: 80 },
            interactions: {
                use: {
                    action: 'changeRoom',
                    target: 'void'
                }
            }
        };
        
        this.roomLoader.hotspots.push(hitArea);
        
        // Announcement
        dialogueSystem.showLines('', [
            "*A tear in reality opens before you.*",
            "The portal to THE VOID has appeared.",
            "The Architect awaits."
        ]);
    }
}
