/**
 * Minimap - Visual navigation aid
 * 
 * Shows current room layout, player position, and important locations.
 */
class Minimap {
    constructor(scene) {
        this.scene = scene;
        this.container = null;
        this.canvas = null;
        this.ctx = null;
        this.width = 120;
        this.height = 90;
        this.scale = 0.15; // Scale factor for room coordinates
        this.visible = true;
    }
    
    create() {
        // Create minimap container
        this.container = document.createElement('div');
        this.container.id = 'minimap';
        this.container.style.cssText = `
            position: absolute;
            top: 10px;
            left: 10px;
            width: ${this.width}px;
            height: ${this.height}px;
            background: rgba(10, 10, 30, 0.85);
            border: 2px solid #00aaff;
            border-radius: 4px;
            z-index: 100;
            pointer-events: none;
        `;
        
        // Create canvas
        this.canvas = document.createElement('canvas');
        this.canvas.width = this.width;
        this.canvas.height = this.height;
        this.ctx = this.canvas.getContext('2d');
        this.container.appendChild(this.canvas);
        
        // Add to game container
        const gameContainer = document.getElementById('game-container');
        if (gameContainer) {
            gameContainer.appendChild(this.container);
        }
        
        // Initial render
        this.update();
    }
    
    update() {
        if (!this.ctx || !this.visible) return;
        
        const roomData = this.scene.roomData;
        if (!roomData) return;
        
        // Clear canvas
        this.ctx.clearRect(0, 0, this.width, this.height);
        
        // Draw background
        this.ctx.fillStyle = '#1a1a2e';
        this.ctx.fillRect(0, 0, this.width, this.height);
        
        // Draw room bounds (walls)
        if (roomData.bounds) {
            const { width, height } = roomData.bounds;
            this.ctx.strokeStyle = '#446688';
            this.ctx.lineWidth = 2;
            this.ctx.strokeRect(0, 0, width * this.scale, height * this.scale);
        }
        
        // Draw walkable area
        if (roomData.walkable) {
            const { x, y, width, height } = roomData.walkable;
            this.ctx.fillStyle = '#2a2a3e';
            this.ctx.fillRect(
                x * this.scale,
                y * this.scale,
                width * this.scale,
                height * this.scale
            );
            
            // Draw walkable border
            this.ctx.strokeStyle = '#3a3a4e';
            this.ctx.lineWidth = 1;
            this.ctx.strokeRect(
                x * this.scale,
                y * this.scale,
                width * this.scale,
                height * this.scale
            );
        }
        
        // Draw hotspots (doors, items, etc.)
        if (roomData.hotspots) {
            roomData.hotspots.forEach(hotspot => {
                if (hotspot.visible && !gameState.checkCondition(hotspot.visible)) return;
                
                const { x, y } = hotspot.position;
                const color = hotspot.id.includes('door') ? '#00ff88' : 
                             hotspot.id.includes('terminal') ? '#00aaff' : '#ffaa00';
                
                this.ctx.fillStyle = color;
                this.ctx.fillRect(
                    x * this.scale - 2,
                    y * this.scale - 2,
                    4, 4
                );
            });
        }
        
        // Draw player position
        if (this.scene.player && this.scene.player.sprite) {
            const playerX = this.scene.player.sprite.x * this.scale;
            const playerY = this.scene.player.sprite.y * this.scale;
            
            this.ctx.fillStyle = '#00ff88';
            this.ctx.beginPath();
            this.ctx.arc(playerX, playerY, 3, 0, Math.PI * 2);
            this.ctx.fill();
        }
        
        // Draw NPCs
        if (this.scene.roomLoader && this.scene.roomLoader.npcs) {
            this.scene.roomLoader.npcs.forEach(npc => {
                if (npc.npcConfig && npc.npcConfig.position) {
                    const { x, y } = npc.npcConfig.position;
                    this.ctx.fillStyle = '#ff4444';
                    this.ctx.fillRect(
                        x * this.scale - 2,
                        y * this.scale - 2,
                        4, 4
                    );
                }
            });
        }
        
        // Draw room border
        this.ctx.strokeStyle = '#00aaff';
        this.ctx.lineWidth = 1;
        this.ctx.strokeRect(1, 1, this.width - 2, this.height - 2);
    }
    
    toggle() {
        this.visible = !this.visible;
        if (this.container) {
            this.container.style.display = this.visible ? 'block' : 'none';
        }
    }
    
    destroy() {
        if (this.container && this.container.parentNode) {
            this.container.parentNode.removeChild(this.container);
        }
    }
}
