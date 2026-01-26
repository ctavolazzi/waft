/**
 * LabScene - Aziah's Research Lab
 * 
 * Starting location. Contains:
 * - Research terminal
 * - Strange artifact (pickup)
 * - Photo of Maya
 * - Patrolling Security Guard
 * - Door to lobby
 */
class LabScene extends BaseScene {
    constructor() {
        super('LabScene');
        this.roomId = 'lab';
        this.guard = null;
        this.guardSprite = null;
    }
    
    preload() {
        // Load lab-specific assets if needed
    }
    
    create() {
        super.create();
        
        // Lab-specific ambient effects
        this.createLabAmbience();
        
        // Create patrolling guard
        this.createPatrollingGuard();
        
        // Starting dialogue if first visit
        if (!gameState.getFlag('visitedLab')) {
            gameState.setFlag('visitedLab', true);
            this.time.delayedCall(500, () => {
                dialogueSystem.showLines('AZIAH', [
                    "Another day in the lab.",
                    "The research into The Between continues...",
                    "Maybe today I'll find the answer."
                ]);
            });
        }
    }
    
    createPatrollingGuard() {
        // Create NPC through NPCSystem
        this.guard = npcSystem.createNPC('lab_guard', {
            name: 'Security Guard',
            type: 'guard',
            x: 600,
            y: 350,
            hostile: false,  // Non-hostile in lab (friendly NPC)
            hp: 50,
            attack: 10,
            defense: 5,
            detectionRange: 120
        });
        
        // Set patrol route (walk back and forth in the lab)
        this.guard.setPatrolRoute([
            { x: 600, y: 350 },  // Near terminal
            { x: 400, y: 350 },  // Center
            { x: 200, y: 350 },  // Near artifact
            { x: 400, y: 450 },  // Lower center
            { x: 600, y: 450 },  // Lower right
        ]);
        
        // Start patrolling
        this.guard.setState(npcSystem.State.PATROL);
        
        // Create guard sprite
        this.guardSprite = this.add.sprite(
            this.guard.x, 
            this.guard.y, 
            'guard_south'
        ).setScale(2).setDepth(5);
        
        // Add detection indicator (exclamation mark when alert)
        this.alertIndicator = this.add.text(
            this.guard.x,
            this.guard.y - 40,
            '!',
            { 
                fontSize: '24px', 
                color: '#ff0000',
                fontStyle: 'bold'
            }
        ).setOrigin(0.5).setDepth(10).setVisible(false);
        
        // Subscribe to guard state changes
        npcSystem.on('stateChange', ({ npc, newState }) => {
            if (npc.id === 'lab_guard') {
                this.onGuardStateChange(newState);
            }
        });
        
        // Subscribe to guard detecting player
        npcSystem.on('detectPlayer', ({ npc }) => {
            if (npc.id === 'lab_guard') {
                this.onGuardDetect();
            }
        });
    }
    
    onGuardStateChange(newState) {
        // Show/hide alert indicator
        if (newState === npcSystem.State.ALERT || newState === npcSystem.State.CHASE) {
            this.alertIndicator?.setVisible(true);
            this.tweens.add({
                targets: this.alertIndicator,
                scale: { from: 1.5, to: 1 },
                duration: 200
            });
        } else {
            this.alertIndicator?.setVisible(false);
        }
    }
    
    onGuardDetect() {
        // Guard noticed something - show dialogue
        if (!gameState.getFlag('guard_noticed')) {
            gameState.setFlag('guard_noticed', true);
            dialogueSystem.showLines('GUARD', [
                "Hmm? Oh, it's just you, Aziah.",
                "Working late again?",
                "Don't mind me, just doing my rounds."
            ]);
            // Return to patrol after dialogue
            this.time.delayedCall(3000, () => {
                this.guard?.setState(npcSystem.State.PATROL);
            });
        }
    }
    
    createLabAmbience() {
        // Terminal glow
        const glow = this.add.rectangle(650, 300, 100, 100, 0x00aaff, 0.1);
        this.tweens.add({
            targets: glow,
            alpha: 0.2,
            duration: 1000,
            yoyo: true,
            repeat: -1
        });
        
        // Floating data particles
        for (let i = 0; i < 15; i++) {
            const text = this.add.text(
                Phaser.Math.Between(50, 750),
                Phaser.Math.Between(200, 480),
                Phaser.Math.Between(0, 1) ? '0' : '1',
                { fontSize: '10px', color: '#00aaff' }
            ).setAlpha(0.3);
            
            this.tweens.add({
                targets: text,
                y: text.y - 80,
                alpha: 0,
                duration: Phaser.Math.Between(2000, 4000),
                repeat: -1,
                onRepeat: () => {
                    text.y = Phaser.Math.Between(400, 500);
                    text.x = Phaser.Math.Between(50, 750);
                    text.alpha = 0.3;
                }
            });
        }
    }
    
    update(time, delta) {
        super.update(time, delta);
        
        // Update guard sprite position and animation (NPCSystem handles logic)
        if (this.guard && this.guardSprite) {
            this.guardSprite.x = this.guard.x;
            this.guardSprite.y = this.guard.y;
            
            // Update sprite based on facing
            const textureKey = `guard_${this.guard.facing}`;
            if (this.textures.exists(textureKey)) {
                this.guardSprite.setTexture(textureKey);
            }
            
            // Update alert indicator position
            if (this.alertIndicator) {
                this.alertIndicator.x = this.guard.x;
                this.alertIndicator.y = this.guard.y - 40;
            }
            
            // Depth sorting - characters closer to bottom render on top
            this.guardSprite.setDepth(Math.floor(this.guard.y));
            if (this.player?.sprite) {
                this.player.sprite.setDepth(Math.floor(this.player.sprite.y));
            }
        }
    }
    
    // Cleanup when leaving scene
    shutdown() {
        if (this.guard) {
            npcSystem.removeNPC('lab_guard');
        }
    }
}
