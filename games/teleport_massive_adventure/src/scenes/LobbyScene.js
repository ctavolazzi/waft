/**
 * LobbyScene - TM Corporate Lobby
 * 
 * Contains:
 * - Security guard NPC
 * - Keycard on floor (pickup)
 * - TM holographic display
 * - Maintenance hatch (locked without keycard)
 * - Door back to lab
 */
class LobbyScene extends BaseScene {
    constructor() {
        super('LobbyScene');
        this.roomId = 'lobby';
    }
    
    create() {
        super.create();
        
        // Corporate holographic logo
        this.createTMLogo();
        
        // Reflective floor effect
        this.createReflectiveFloor();
    }
    
    createTMLogo() {
        const logo = this.add.text(400, 100, 'TELEPORT\nMASSIVE', {
            fontSize: '28px',
            fontFamily: 'monospace',
            color: '#00aaff',
            align: 'center'
        }).setOrigin(0.5);
        
        // Hologram flicker
        this.tweens.add({
            targets: logo,
            alpha: 0.7,
            duration: 100,
            yoyo: true,
            repeat: -1,
            repeatDelay: Phaser.Math.Between(1000, 3000)
        });
        
        // Scan line
        const scanLine = this.add.rectangle(400, 60, 200, 2, 0x00aaff, 0.5);
        this.tweens.add({
            targets: scanLine,
            y: 140,
            duration: 2000,
            repeat: -1,
            ease: 'Linear'
        });
    }
    
    createReflectiveFloor() {
        // Subtle floor shine
        for (let x = 0; x < 800; x += 80) {
            const shine = this.add.rectangle(x + 40, 350, 2, 150, 0x4488ff, 0.1);
            this.tweens.add({
                targets: shine,
                alpha: 0.2,
                duration: Phaser.Math.Between(1500, 3000),
                yoyo: true,
                repeat: -1
            });
        }
    }
}
