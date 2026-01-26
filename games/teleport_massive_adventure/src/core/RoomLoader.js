/**
 * RoomLoader - Data-driven room creation
 * 
 * Loads room definitions from JSON and creates Phaser scenes dynamically.
 * Supports hotspots, NPCs, ambient effects, and conditional visibility.
 */
class RoomLoader {
    constructor(scene) {
        this.scene = scene;
        this.roomData = null;
        this.hotspots = [];
        this.npcs = [];
        this.sprites = new Map();
    }
    
    // ========================================
    // Room Loading
    // ========================================
    
    load(roomData) {
        this.roomData = roomData;
        this.hotspots = [];
        this.npcs = [];
        
        // Draw background
        this.createBackground(roomData.background);
        
        // Create hotspots
        if (roomData.hotspots) {
            roomData.hotspots.forEach(h => this.createHotspot(h));
        }
        
        // Create NPCs
        if (roomData.npcs) {
            roomData.npcs.forEach(n => this.createNPC(n));
        }
        
        // Create ambient effects
        if (roomData.ambient) {
            this.createAmbient(roomData.ambient);
        }
        
        // Emit room loaded event
        eventBus.emit(EventBus.ROOM_LOADED, { room: roomData.id });
        
        return this;
    }
    
    // ========================================
    // Background Creation
    // ========================================
    
    createBackground(bgConfig) {
        if (!bgConfig) return;
        
        const graphics = this.scene.add.graphics();
        
        switch (bgConfig.type) {
            case 'procedural':
                this.drawProceduralBackground(graphics, bgConfig);
                break;
            case 'image':
                this.scene.add.image(400, 250, bgConfig.key);
                break;
            case 'color':
                graphics.fillStyle(parseInt(bgConfig.color.replace('#', '0x')), 1);
                graphics.fillRect(0, 0, 800, 500);
                break;
        }
    }
    
    drawProceduralBackground(graphics, config) {
        const colors = config.colors || {};
        const style = config.style || 'default';
        
        switch (style) {
            case 'lab':
                this.drawLabStyle(graphics, colors);
                break;
            case 'corporate':
                this.drawCorporateStyle(graphics, colors);
                break;
            case 'underground':
                this.drawUndergroundStyle(graphics, colors);
                break;
            case 'void':
                this.drawVoidStyle(graphics, colors);
                break;
            default:
                this.drawDefaultStyle(graphics, colors);
        }
    }
    
    drawLabStyle(graphics, colors) {
        // Floor
        graphics.fillStyle(parseInt((colors.floor || '#222233').replace('#', '0x')), 1);
        graphics.fillRect(0, 200, 800, 300);
        
        // Floor tiles
        for (let x = 0; x < 800; x += 50) {
            for (let y = 200; y < 500; y += 50) {
                graphics.lineStyle(1, 0x333344, 0.3);
                graphics.strokeRect(x, y, 50, 50);
            }
        }
        
        // Wall
        graphics.fillStyle(parseInt((colors.wall || '#2a2a3e').replace('#', '0x')), 1);
        graphics.fillRect(0, 0, 800, 200);
        
        // Wall panels
        for (let x = 0; x < 800; x += 100) {
            graphics.lineStyle(2, 0x3a3a4e, 0.5);
            graphics.strokeRect(x + 5, 10, 90, 180);
        }
        
        // Accent glow
        const accent = parseInt((colors.accent || '#00aaff').replace('#', '0x'));
        graphics.fillStyle(accent, 0.3);
        graphics.fillRect(300, 50, 200, 10);
    }
    
    drawCorporateStyle(graphics, colors) {
        // Polished floor
        graphics.fillStyle(parseInt((colors.floor || '#1a1a28').replace('#', '0x')), 1);
        graphics.fillRect(0, 200, 800, 300);
        
        // Reflective stripes
        for (let x = 0; x < 800; x += 80) {
            graphics.fillStyle(0x222238, 1);
            graphics.fillRect(x, 200, 40, 300);
        }
        
        // Wall
        graphics.fillStyle(parseInt((colors.wall || '#252535').replace('#', '0x')), 1);
        graphics.fillRect(0, 0, 800, 200);
        
        // Logo area
        graphics.fillStyle(parseInt((colors.accent || '#00aaff').replace('#', '0x')), 0.2);
        graphics.fillRect(325, 60, 150, 80);
    }
    
    drawUndergroundStyle(graphics, colors) {
        // Dark floor
        graphics.fillStyle(parseInt((colors.floor || '#0f0f18').replace('#', '0x')), 1);
        graphics.fillRect(0, 200, 800, 300);
        
        // Puddles
        graphics.fillStyle(0x111122, 0.5);
        graphics.fillEllipse(300, 420, 100, 30);
        graphics.fillEllipse(550, 380, 80, 25);
        
        // Pipes
        graphics.fillStyle(0x333344, 1);
        graphics.fillRect(0, 0, 800, 30);
        graphics.fillRect(100, 0, 20, 200);
        graphics.fillRect(500, 0, 20, 200);
    }
    
    drawVoidStyle(graphics, colors) {
        // Gradient void
        for (let y = 0; y < 500; y += 5) {
            const intensity = Math.sin(y * 0.01) * 0.1;
            const color = Phaser.Display.Color.GetColor(
                Math.floor(10 + intensity * 50),
                Math.floor(5 + intensity * 20),
                Math.floor(30 + intensity * 100)
            );
            graphics.fillStyle(color, 1);
            graphics.fillRect(0, y, 800, 5);
        }
        
        // Floating shapes
        for (let i = 0; i < 20; i++) {
            const x = Math.random() * 800;
            const y = Math.random() * 300;
            const size = 5 + Math.random() * 15;
            graphics.fillStyle(0x8800ff, 0.3);
            
            if (Math.random() > 0.5) {
                graphics.fillCircle(x, y, size);
            } else {
                graphics.fillRect(x - size/2, y - size/2, size, size);
            }
        }
    }
    
    drawDefaultStyle(graphics, colors) {
        graphics.fillStyle(0x1a1a2e, 1);
        graphics.fillRect(0, 0, 800, 500);
    }
    
    // ========================================
    // Hotspot Creation
    // ========================================
    
    createHotspot(config) {
        // Check visibility condition
        if (config.visible && !gameState.checkCondition(config.visible)) {
            return null;
        }
        
        const { x, y } = config.position;
        const { width, height } = config.size;
        
        // Create invisible interaction zone
        const zone = this.scene.add.rectangle(x, y, width, height, 0xffffff, 0)
            .setInteractive();
        
        // Store config on zone
        zone.hotspotConfig = config;
        zone.name = config.name;
        
        // Create sprite if specified
        if (config.sprite) {
            const sprite = this.scene.add.sprite(x, y, config.sprite);
            sprite.setDepth(y);
            zone.sprite = sprite;
            this.sprites.set(config.id, sprite);
        }
        
        this.hotspots.push(zone);
        return zone;
    }
    
    // ========================================
    // NPC Creation
    // ========================================
    
    createNPC(config) {
        const { x, y } = config.position;
        
        const npc = this.scene.add.sprite(x, y, config.sprite);
        npc.setDepth(y);
        npc.setScale(1.5);
        npc.setInteractive();
        
        // Store config
        npc.npcConfig = config;
        npc.name = config.name;
        
        // Apply effects
        if (config.effects) {
            this.applyNPCEffects(npc, config.effects);
        }
        
        this.npcs.push(npc);
        this.sprites.set(config.id, npc);
        return npc;
    }
    
    applyNPCEffects(npc, effects) {
        if (effects.glitch || effects.alpha_pulse) {
            this.scene.tweens.add({
                targets: npc,
                alpha: effects.alpha_pulse?.min || 0.5,
                x: npc.x + (effects.glitch ? 5 : 0),
                duration: effects.alpha_pulse?.duration || 200,
                yoyo: true,
                repeat: -1,
                ease: 'Stepped',
                easeParams: [3]
            });
        }
    }
    
    // ========================================
    // Ambient Effects
    // ========================================
    
    createAmbient(config) {
        if (config.particles === 'data_streams') {
            this.createDataParticles();
        }
        
        if (config.flickerLights) {
            this.createFlickeringLights();
        }
        
        if (config.particles === 'cosmic_data') {
            this.createCosmicParticles();
        }
    }
    
    createDataParticles() {
        for (let i = 0; i < 20; i++) {
            const text = this.scene.add.text(
                Math.random() * 800,
                Math.random() * 500,
                Math.random() > 0.5 ? '0' : '1',
                { fontSize: '10px', color: '#00aaff', alpha: 0.3 }
            );
            
            this.scene.tweens.add({
                targets: text,
                y: text.y - 100,
                alpha: 0,
                duration: 2000 + Math.random() * 2000,
                repeat: -1,
                onRepeat: () => {
                    text.y = 500;
                    text.x = Math.random() * 800;
                    text.alpha = 0.3;
                }
            });
        }
    }
    
    createFlickeringLights() {
        const lights = [
            this.scene.add.rectangle(150, 190, 60, 10, 0xffff88, 0.5),
            this.scene.add.rectangle(450, 190, 60, 10, 0xffff88, 0.5)
        ];
        
        lights.forEach(light => {
            this.scene.tweens.add({
                targets: light,
                alpha: 0.2,
                duration: 100,
                yoyo: true,
                repeat: -1,
                repeatDelay: Math.random() * 2000
            });
        });
    }
    
    createCosmicParticles() {
        for (let i = 0; i < 30; i++) {
            const particle = this.scene.add.text(
                Math.random() * 800,
                Math.random() * 500,
                Math.random() > 0.5 ? '0' : '1',
                { fontSize: '10px', color: '#4400aa' }
            );
            
            this.scene.tweens.add({
                targets: particle,
                y: particle.y - 100 - Math.random() * 200,
                alpha: 0,
                duration: 3000 + Math.random() * 2000,
                repeat: -1,
                onRepeat: () => {
                    particle.y = 500 + Math.random() * 100;
                    particle.x = Math.random() * 800;
                    particle.alpha = 0.5;
                }
            });
        }
    }
    
    // ========================================
    // Interaction Handling
    // ========================================
    
    getHotspotAt(x, y) {
        return this.hotspots.find(h => h.getBounds().contains(x, y));
    }
    
    getNPCAt(x, y) {
        return this.npcs.find(n => n.getBounds().contains(x, y));
    }
    
    hideHotspot(id) {
        const sprite = this.sprites.get(id);
        if (sprite) {
            sprite.destroy();
            this.sprites.delete(id);
        }
        
        const hotspotIndex = this.hotspots.findIndex(h => h.hotspotConfig?.id === id);
        if (hotspotIndex !== -1) {
            this.hotspots[hotspotIndex].destroy();
            this.hotspots.splice(hotspotIndex, 1);
        }
    }
    
    // ========================================
    // Cleanup
    // ========================================
    
    destroy() {
        this.hotspots.forEach(h => h.destroy());
        this.npcs.forEach(n => n.destroy());
        this.sprites.forEach(s => s.destroy());
        this.hotspots = [];
        this.npcs = [];
        this.sprites.clear();
    }
}
