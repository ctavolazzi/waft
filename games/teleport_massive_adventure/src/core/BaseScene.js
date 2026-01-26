/**
 * BaseScene - Composable scene template
 * 
 * All game scenes extend this. Provides:
 * - Room loading from JSON
 * - Player controller
 * - Interaction handling
 * - Click processing
 * - UI hookup
 */

// Import utilities (using dynamic import for compatibility)
// If ES6 modules not available, these will be loaded via script tags
let SceneTransition;
if (typeof import !== 'undefined') {
    import('./SceneTransition.js').then(m => SceneTransition = m.SceneTransition);
} else if (typeof window !== 'undefined' && window.SceneTransition) {
    SceneTransition = window.SceneTransition;
}

class BaseScene extends Phaser.Scene {
    constructor(key) {
        super(key);
        this.roomId = null;
        this.roomData = null;
        this.player = null;
        this.roomLoader = null;
        this.interactionSystem = null;
        this.minimap = null;
    }
    
    // ========================================
    // Lifecycle
    // ========================================
    
    init(data) {
        // Data passed from previous scene
        this.playerStartX = data?.playerX || null;
        this.playerStartY = data?.playerY || null;
    }
    
    create() {
        // Setup UI references FIRST (before loadRoom which calls updateRoomTitle)
        this.setupUI();
        
        // Initialize systems
        this.roomLoader = new RoomLoader(this);
        this.interactionSystem = new InteractionSystem(this);
        this.interactionSystem.setRoomLoader(this.roomLoader);
        this.player = new PlayerController(this);
        
        // Make interaction system available
        window.interactionSystem = this.interactionSystem;
        
        // Create minimap
        this.minimap = new Minimap(this);
        this.minimap.create();
        
        // Load room data
        if (this.roomId && window.roomsData?.rooms?.[this.roomId]) {
            this.roomData = window.roomsData.rooms[this.roomId];
            this.loadRoom();
        } else {
            // If room data not available, at least set a default title
            this.updateRoomTitle(this.scene.key || 'UNKNOWN');
        }
        
        // Setup input
        this.setupInput();
        
        // Fade in
        this.cameras.main.fadeIn(300, 0, 0, 0);
        
        // Emit room enter event
        eventBus.emit(EventBus.ROOM_ENTER, { 
            room: this.roomId,
            sceneName: this.scene.key 
        });
        
        // Update game state
        gameState.enterRoom(this.roomId);
    }
    
    loadRoom() {
        // Draw room
        this.roomLoader.load(this.roomData);
        
        // Set walkable area
        if (this.roomData.walkable) {
            this.player.setWalkableArea(this.roomData.walkable);
        }
        
        // Create player
        const startPos = this.getPlayerStartPosition();
        this.player.create(startPos.x, startPos.y, 'aziah_south');
        
        // Setup keyboard movement (arrow keys + WASD)
        this.player.setupKeyboardInput();
        
        // Initialize combat drone if player has it
        if (this.player.hasDrone || gameState.getFlag('hasCombatDrone')) {
            this.player.hasDrone = true;
            // Use SystemAccessor for clean system access
            const SystemAccessor = window.SystemAccessor || (typeof SystemAccessor !== 'undefined' ? SystemAccessor : null);
            if (SystemAccessor) {
                const combatSystem = SystemAccessor.getCombatSystem();
                const npcSystem = SystemAccessor.getNPCSystem();
                const statsSystem = SystemAccessor.getStatsSystem();
                
                if (combatSystem && npcSystem && statsSystem) {
                    this.player.initCombatDrone({
                        combatSystem,
                        npcSystem,
                        statsSystem
                    });
                    this.player.activateDrone();
                }
            } else if (window.gameManager) {
                // Fallback to legacy access
                const combatSystem = window.gameManager.getSystem('combatSystem');
                const npcSystem = window.gameManager.getSystem('npcSystem');
                const statsSystem = window.gameManager.getSystem('statsSystem');
                
                if (combatSystem && npcSystem && statsSystem) {
                    this.player.initCombatDrone({
                        combatSystem,
                        npcSystem,
                        statsSystem
                    });
                    this.player.activateDrone();
                }
            }
        }
        
        // Set title
        this.updateRoomTitle(this.roomData.name);
    }
    
    getPlayerStartPosition() {
        // Priority: passed data > room default
        if (this.playerStartX !== null && this.playerStartY !== null) {
            return { x: this.playerStartX, y: this.playerStartY };
        }
        
        if (this.roomData?.playerStart) {
            return this.roomData.playerStart;
        }
        
        return { x: 400, y: 400 };
    }
    
    // ========================================
    // Input Handling
    // ========================================
    
    setupInput() {
        // Click anywhere
        this.input.on('pointerdown', (pointer) => {
            // Don't process if dialogue is active
            if (dialogueSystem.isActive) return;
            
            // Check what was clicked
            const target = this.getTargetAtPoint(pointer.x, pointer.y);
            
            // Walk to click, optionally interact
            this.player.handleClick(pointer.x, pointer.y, target);
        });
        
        // Hover for cursor changes
        this.input.on('pointermove', (pointer) => {
            const target = this.getTargetAtPoint(pointer.x, pointer.y);
            this.updateCursor(target);
        });
        
        // Keyboard shortcuts
        this.input.keyboard.on('keydown-I', () => this.toggleInventory());
        this.input.keyboard.on('keydown-SPACE', () => dialogueSystem.advance());
        this.input.keyboard.on('keydown-ENTER', () => dialogueSystem.advance());
        
        // E key to interact with nearby objects (for keyboard movement)
        this.input.keyboard.on('keydown-E', () => this.interactWithNearby());
    }
    
    interactWithNearby() {
        if (dialogueSystem.isActive) return;
        if (!this.player?.sprite) return;
        
        const playerX = this.player.sprite.x;
        const playerY = this.player.sprite.y;
        const interactRange = 60; // Pixels
        
        // Find nearest interactable within range
        let nearest = null;
        let nearestDist = interactRange;
        
        // Check hotspots
        this.roomLoader?.hotspots?.forEach(hotspot => {
            if (!hotspot.hotspotConfig) return;
            const hx = hotspot.hotspotConfig.position.x;
            const hy = hotspot.hotspotConfig.position.y;
            const dist = Math.sqrt((playerX - hx) ** 2 + (playerY - hy) ** 2);
            
            if (dist < nearestDist) {
                nearestDist = dist;
                nearest = hotspot;
            }
        });
        
        // Check NPCs
        this.roomLoader?.npcs?.forEach(npc => {
            if (!npc.npcConfig) return;
            const nx = npc.npcConfig.position.x;
            const ny = npc.npcConfig.position.y;
            const dist = Math.sqrt((playerX - nx) ** 2 + (playerY - ny) ** 2);
            
            if (dist < nearestDist) {
                nearestDist = dist;
                nearest = npc;
            }
        });
        
        // Interact with nearest
        if (nearest) {
            this.player.faceTarget(nearest);
            this.player.interact(nearest);
        }
    }
    
    getTargetAtPoint(x, y) {
        // Check hotspots first
        const hotspot = this.roomLoader?.getHotspotAt(x, y);
        if (hotspot) return hotspot;
        
        // Check NPCs
        const npc = this.roomLoader?.getNPCAt(x, y);
        if (npc) return npc;
        
        return null;
    }
    
    updateCursor(target) {
        const container = document.getElementById('game-container');
        if (!container) return;
        
        if (target) {
            if (target.npcConfig) {
                container.style.cursor = 'url("data:image/svg+xml,<svg xmlns=\'http://www.w3.org/2000/svg\' width=\'32\' height=\'32\'><text y=\'24\' font-size=\'24\'>💬</text></svg>") 16 16, pointer';
            } else if (target.hotspotConfig?.interactions?.pickup) {
                container.style.cursor = 'url("data:image/svg+xml,<svg xmlns=\'http://www.w3.org/2000/svg\' width=\'32\' height=\'32\'><text y=\'24\' font-size=\'24\'>✋</text></svg>") 16 16, grab';
            } else {
                container.style.cursor = 'url("data:image/svg+xml,<svg xmlns=\'http://www.w3.org/2000/svg\' width=\'32\' height=\'32\'><text y=\'24\' font-size=\'24\'>👁️</text></svg>") 16 16, pointer';
            }
        } else {
            container.style.cursor = 'crosshair';
        }
    }
    
    // ========================================
    // UI
    // ========================================
    
    setupUI() {
        // Reference DOM elements
        this.ui = {
            title: document.getElementById('room-title'),
            inventory: document.getElementById('inventory-panel'),
            inventoryItems: document.getElementById('inventory-items'),
            dialogue: document.getElementById('dialogue-box')
        };
        
        // Initialize dialogue system with DOM
        dialogueSystem.init({
            box: this.ui.dialogue,
            speaker: document.getElementById('speaker-name'),
            text: document.getElementById('dialogue-text')
        });
        
        // Subscribe to inventory changes
        gameState.subscribe('inventory', (items) => this.updateInventoryUI(items));
        
        // Initial inventory render
        this.updateInventoryUI(gameState.getInventory());
    }
    
    updateRoomTitle(title) {
        // Try UI reference first
        if (this.ui?.title) {
            this.ui.title.textContent = title;
        } else {
            // Fallback: direct DOM access
            const titleElement = document.getElementById('room-title');
            if (titleElement) {
                titleElement.textContent = title;
            }
        }
    }
    
    updateInventoryUI(items) {
        if (!this.ui?.inventoryItems) return;
        
        this.ui.inventoryItems.innerHTML = '';
        
        items.forEach(item => {
            const slot = document.createElement('div');
            slot.className = 'inventory-slot';
            
            // Get item data for sprite
            const itemData = window.itemsData?.items?.[item.id] || item;
            const spritePath = itemData.sprite ? `assets/objects/${itemData.sprite}.png` : null;
            
            slot.innerHTML = `
                ${spritePath ? `<img src="${spritePath}" style="width: 100%; height: 100%; object-fit: contain; image-rendering: pixelated;" onerror="this.style.display='none'; this.nextElementSibling.style.display='block';" />` : ''}
                <span class="item-icon" style="${spritePath ? 'display: none;' : ''}">${item.icon || itemData.icon || '?'}</span>
            `;
            slot.title = `${item.name || itemData.name}\n${item.description || itemData.description || 'Click for details'}`;
            
            // Click to show detailed card
            slot.addEventListener('click', (e) => {
                e.stopPropagation();
                if (window.inventoryCardSystem) {
                    window.inventoryCardSystem.showCard(item);
                } else {
                    // Fallback to selection
                    this.selectInventoryItem(item);
                }
            });
            
            // Right-click to select (for using items)
            slot.addEventListener('contextmenu', (e) => {
                e.preventDefault();
                this.selectInventoryItem(item);
            });
            
            this.ui.inventoryItems.appendChild(slot);
        });
    }
    
    selectInventoryItem(item) {
        this.interactionSystem.setSelectedItem(item);
        
        // Visual feedback
        document.querySelectorAll('.inventory-slot').forEach(s => s.classList.remove('selected'));
        event.currentTarget.classList.add('selected');
        
        // Show item name
        dialogueSystem.showSingle('', `Selected: ${item.name}`);
    }
    
    toggleInventory() {
        if (this.ui?.inventory) {
            this.ui.inventory.classList.toggle('expanded');
        }
    }
    
    // ========================================
    // Update Loop
    // ========================================
    
    update(time, delta) {
        // Update player
        if (this.player) {
            this.player.update(delta);
            
            // Update combat drone if active
            if (this.player.combatDrone && this.player.combatDrone.isActive) {
                this.player.combatDrone.update(time, delta);
            }
        }
        
        // Update minimap periodically
        if (this.minimap && time % 500 < delta) {
            this.minimap.update();
        }
        
        // Update game manager (coordinates all systems)
        const SystemAccessor = window.SystemAccessor || (typeof SystemAccessor !== 'undefined' ? SystemAccessor : null);
        const gameManager = SystemAccessor ? SystemAccessor.getGameManager() : (window.gameManager || null);
        if (gameManager) {
            gameManager.setCurrentScene(this);
            gameManager.update(time, delta);
        }
    }
    
    // ========================================
    // Scene Transitions
    // ========================================
    
    goToRoom(roomId, playerX, playerY) {
        // Use centralized transition utility
        SceneTransition.transition(this, roomId, {
            playerX,
            playerY,
            onCleanup: () => SceneTransition.cleanupPlayer(this.player)
        });
    }
}
