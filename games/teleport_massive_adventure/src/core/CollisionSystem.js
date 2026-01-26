/**
 * CollisionSystem - Hit Boxes & Collision Detection
 * 
 * ════════════════════════════════════════════════════════════════════════════
 * Handles all collision detection including:
 * - Axis-Aligned Bounding Boxes (AABB)
 * - Circle colliders
 * - Trigger zones
 * - Layer-based collision filtering
 * ════════════════════════════════════════════════════════════════════════════
 */

// ════════════════════════════════════════════════════════════════════════════
// CONFIGURATION
// ════════════════════════════════════════════════════════════════════════════

const COLLISION_CONFIG = {
    // Collision layers (bitmask for efficient filtering)
    LAYERS: {
        NONE: 0,
        PLAYER: 1 << 0,       // 1
        ENEMY: 1 << 1,        // 2
        NPC: 1 << 2,          // 4
        PROJECTILE: 1 << 3,   // 8
        ITEM: 1 << 4,         // 16
        WALL: 1 << 5,         // 32
        TRIGGER: 1 << 6,      // 64
        HAZARD: 1 << 7,       // 128
        ALL: 0xFF             // 255
    },
    
    // What each layer collides with
    COLLISION_MATRIX: {
        PLAYER: ['ENEMY', 'NPC', 'WALL', 'ITEM', 'TRIGGER', 'HAZARD'],
        ENEMY: ['PLAYER', 'WALL', 'PROJECTILE'],
        NPC: ['PLAYER', 'WALL'],
        PROJECTILE: ['ENEMY', 'WALL'],
        ITEM: ['PLAYER'],
        WALL: ['PLAYER', 'ENEMY', 'NPC', 'PROJECTILE'],
        TRIGGER: ['PLAYER'],
        HAZARD: ['PLAYER']
    },
    
    // Default hitbox sizes by entity type
    DEFAULT_HITBOXES: {
        player: { width: 32, height: 48, offsetX: 0, offsetY: 8 },
        enemy: { width: 40, height: 48, offsetX: 0, offsetY: 8 },
        npc: { width: 32, height: 48, offsetX: 0, offsetY: 8 },
        item: { width: 24, height: 24, offsetX: 0, offsetY: 0 },
        projectile: { width: 8, height: 8, offsetX: 0, offsetY: 0 },
        trigger: { width: 64, height: 64, offsetX: 0, offsetY: 0 }
    },
    
    // Debug visualization
    DEBUG: {
        showHitboxes: false,
        hitboxColor: 0x00ff00,
        hitboxAlpha: 0.3,
        triggerColor: 0x0000ff,
        attackColor: 0xff0000
    }
};

// ════════════════════════════════════════════════════════════════════════════
// COLLIDER TYPES
// ════════════════════════════════════════════════════════════════════════════

/**
 * Base Collider class
 */
class Collider {
    constructor(entityId, type = 'box') {
        this.id = `${entityId}_${Date.now()}`;
        this.entityId = entityId;
        this.type = type;  // 'box', 'circle', 'polygon'
        this.layer = COLLISION_CONFIG.LAYERS.NONE;
        this.collidesWithMask = 0;
        this.enabled = true;
        this.isTrigger = false;  // Triggers don't block movement
        this.isStatic = false;   // Static colliders don't move
        
        // Position (world coordinates)
        this.x = 0;
        this.y = 0;
        
        // Custom data
        this.userData = {};
        
        // Callbacks
        this.onCollisionEnter = null;
        this.onCollisionStay = null;
        this.onCollisionExit = null;
        this.onTriggerEnter = null;
        this.onTriggerStay = null;
        this.onTriggerExit = null;
    }
    
    setLayer(layerName) {
        this.layer = COLLISION_CONFIG.LAYERS[layerName] || COLLISION_CONFIG.LAYERS.NONE;
        
        // Auto-set collision mask from matrix
        const collidesWith = COLLISION_CONFIG.COLLISION_MATRIX[layerName] || [];
        this.collidesWithMask = collidesWith.reduce((mask, layer) => {
            return mask | (COLLISION_CONFIG.LAYERS[layer] || 0);
        }, 0);
        
        return this;
    }
    
    canCollideWith(other) {
        if (!this.enabled || !other.enabled) return false;
        return (this.collidesWithMask & other.layer) !== 0;
    }
}

/**
 * Box Collider (AABB)
 */
class BoxCollider extends Collider {
    constructor(entityId, width, height, offsetX = 0, offsetY = 0) {
        super(entityId, 'box');
        this.width = width;
        this.height = height;
        this.offsetX = offsetX;
        this.offsetY = offsetY;
    }
    
    getBounds() {
        return {
            left: this.x + this.offsetX - this.width / 2,
            right: this.x + this.offsetX + this.width / 2,
            top: this.y + this.offsetY - this.height / 2,
            bottom: this.y + this.offsetY + this.height / 2,
            centerX: this.x + this.offsetX,
            centerY: this.y + this.offsetY,
            width: this.width,
            height: this.height
        };
    }
    
    containsPoint(px, py) {
        const b = this.getBounds();
        return px >= b.left && px <= b.right && py >= b.top && py <= b.bottom;
    }
}

/**
 * Circle Collider
 */
class CircleCollider extends Collider {
    constructor(entityId, radius, offsetX = 0, offsetY = 0) {
        super(entityId, 'circle');
        this.radius = radius;
        this.offsetX = offsetX;
        this.offsetY = offsetY;
    }
    
    getBounds() {
        const cx = this.x + this.offsetX;
        const cy = this.y + this.offsetY;
        return {
            left: cx - this.radius,
            right: cx + this.radius,
            top: cy - this.radius,
            bottom: cy + this.radius,
            centerX: cx,
            centerY: cy,
            radius: this.radius
        };
    }
    
    containsPoint(px, py) {
        const cx = this.x + this.offsetX;
        const cy = this.y + this.offsetY;
        const dx = px - cx;
        const dy = py - cy;
        return (dx * dx + dy * dy) <= (this.radius * this.radius);
    }
}

// ════════════════════════════════════════════════════════════════════════════
// COLLISION SYSTEM
// ════════════════════════════════════════════════════════════════════════════

class CollisionSystem {
    constructor() {
        // All registered colliders
        this.colliders = new Map();
        
        // Collision pairs from last frame (for enter/exit detection)
        this.activeCollisions = new Set();
        
        // Event listeners
        this.listeners = new Map();
        
        // Debug graphics (Phaser)
        this.debugGraphics = null;
        this.debugEnabled = COLLISION_CONFIG.DEBUG.showHitboxes;
        
        this._log('CollisionSystem initialized');
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // COLLIDER MANAGEMENT
    // ════════════════════════════════════════════════════════════════════════
    
    /**
     * Create a box collider
     * @param {string} entityId 
     * @param {object} options 
     * @returns {BoxCollider}
     */
    createBoxCollider(entityId, options = {}) {
        const defaults = COLLISION_CONFIG.DEFAULT_HITBOXES[options.type] || 
                        COLLISION_CONFIG.DEFAULT_HITBOXES.player;
        
        const collider = new BoxCollider(
            entityId,
            options.width || defaults.width,
            options.height || defaults.height,
            options.offsetX ?? defaults.offsetX,
            options.offsetY ?? defaults.offsetY
        );
        
        collider.x = options.x || 0;
        collider.y = options.y || 0;
        collider.isTrigger = options.isTrigger || false;
        collider.isStatic = options.isStatic || false;
        collider.userData = options.userData || {};
        
        if (options.layer) {
            collider.setLayer(options.layer);
        }
        
        this.colliders.set(collider.id, collider);
        this._emit('colliderCreated', { collider });
        this._log(`Created box collider for ${entityId} (${collider.width}x${collider.height})`);
        
        return collider;
    }
    
    /**
     * Create a circle collider
     * @param {string} entityId 
     * @param {object} options 
     * @returns {CircleCollider}
     */
    createCircleCollider(entityId, options = {}) {
        const collider = new CircleCollider(
            entityId,
            options.radius || 16,
            options.offsetX || 0,
            options.offsetY || 0
        );
        
        collider.x = options.x || 0;
        collider.y = options.y || 0;
        collider.isTrigger = options.isTrigger || false;
        collider.isStatic = options.isStatic || false;
        collider.userData = options.userData || {};
        
        if (options.layer) {
            collider.setLayer(options.layer);
        }
        
        this.colliders.set(collider.id, collider);
        this._emit('colliderCreated', { collider });
        this._log(`Created circle collider for ${entityId} (r=${collider.radius})`);
        
        return collider;
    }
    
    /**
     * Create an attack hitbox (temporary damaging area)
     * @param {string} attackerId 
     * @param {object} options 
     * @returns {BoxCollider}
     */
    createAttackHitbox(attackerId, options = {}) {
        const collider = this.createBoxCollider(`${attackerId}_attack`, {
            width: options.width || 48,
            height: options.height || 48,
            x: options.x,
            y: options.y,
            layer: 'PROJECTILE',
            isTrigger: true,
            userData: {
                attackerId,
                damage: options.damage || 10,
                knockback: options.knockback || 0,
                isAttackHitbox: true
            }
        });
        
        // Auto-destroy after duration
        if (options.duration) {
            setTimeout(() => {
                this.removeCollider(collider.id);
            }, options.duration);
        }
        
        return collider;
    }
    
    /**
     * Remove a collider
     * @param {string} colliderId 
     */
    removeCollider(colliderId) {
        if (this.colliders.has(colliderId)) {
            const collider = this.colliders.get(colliderId);
            this.colliders.delete(colliderId);
            
            // Clean up active collisions involving this collider
            this.activeCollisions.forEach(pairKey => {
                if (pairKey.includes(colliderId)) {
                    this.activeCollisions.delete(pairKey);
                }
            });
            
            this._emit('colliderRemoved', { colliderId });
        }
    }
    
    /**
     * Get collider by ID
     * @param {string} colliderId 
     * @returns {Collider}
     */
    getCollider(colliderId) {
        return this.colliders.get(colliderId);
    }
    
    /**
     * Get all colliders for an entity
     * @param {string} entityId 
     * @returns {array}
     */
    getCollidersForEntity(entityId) {
        return Array.from(this.colliders.values())
            .filter(c => c.entityId === entityId);
    }
    
    /**
     * Update collider position
     * @param {string} colliderId 
     * @param {number} x 
     * @param {number} y 
     */
    updatePosition(colliderId, x, y) {
        const collider = this.colliders.get(colliderId);
        if (collider) {
            collider.x = x;
            collider.y = y;
        }
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // COLLISION DETECTION
    // ════════════════════════════════════════════════════════════════════════
    
    /**
     * Check collision between two colliders
     * @param {Collider} a 
     * @param {Collider} b 
     * @returns {object|null} Collision info or null
     */
    checkCollision(a, b) {
        if (!a.canCollideWith(b)) return null;
        
        // Box vs Box
        if (a.type === 'box' && b.type === 'box') {
            return this._boxVsBox(a, b);
        }
        
        // Circle vs Circle
        if (a.type === 'circle' && b.type === 'circle') {
            return this._circleVsCircle(a, b);
        }
        
        // Box vs Circle
        if (a.type === 'box' && b.type === 'circle') {
            return this._boxVsCircle(a, b);
        }
        if (a.type === 'circle' && b.type === 'box') {
            return this._boxVsCircle(b, a);
        }
        
        return null;
    }
    
    /**
     * AABB collision detection
     */
    _boxVsBox(a, b) {
        const boundsA = a.getBounds();
        const boundsB = b.getBounds();
        
        // Check for overlap
        if (boundsA.left < boundsB.right &&
            boundsA.right > boundsB.left &&
            boundsA.top < boundsB.bottom &&
            boundsA.bottom > boundsB.top) {
            
            // Calculate overlap
            const overlapX = Math.min(boundsA.right - boundsB.left, boundsB.right - boundsA.left);
            const overlapY = Math.min(boundsA.bottom - boundsB.top, boundsB.bottom - boundsA.top);
            
            // Determine push direction (smallest overlap)
            let pushX = 0, pushY = 0;
            if (overlapX < overlapY) {
                pushX = boundsA.centerX < boundsB.centerX ? -overlapX : overlapX;
            } else {
                pushY = boundsA.centerY < boundsB.centerY ? -overlapY : overlapY;
            }
            
            return {
                colliderA: a,
                colliderB: b,
                overlapX,
                overlapY,
                pushX,
                pushY,
                contactPoint: {
                    x: (boundsA.centerX + boundsB.centerX) / 2,
                    y: (boundsA.centerY + boundsB.centerY) / 2
                }
            };
        }
        
        return null;
    }
    
    /**
     * Circle vs Circle collision detection
     */
    _circleVsCircle(a, b) {
        const boundsA = a.getBounds();
        const boundsB = b.getBounds();
        
        const dx = boundsB.centerX - boundsA.centerX;
        const dy = boundsB.centerY - boundsA.centerY;
        const distance = Math.sqrt(dx * dx + dy * dy);
        const combinedRadius = boundsA.radius + boundsB.radius;
        
        if (distance < combinedRadius) {
            const overlap = combinedRadius - distance;
            const nx = dx / distance || 0;
            const ny = dy / distance || 0;
            
            return {
                colliderA: a,
                colliderB: b,
                overlap,
                pushX: -nx * overlap,
                pushY: -ny * overlap,
                contactPoint: {
                    x: boundsA.centerX + nx * boundsA.radius,
                    y: boundsA.centerY + ny * boundsA.radius
                }
            };
        }
        
        return null;
    }
    
    /**
     * Box vs Circle collision detection
     */
    _boxVsCircle(box, circle) {
        const boxBounds = box.getBounds();
        const circleBounds = circle.getBounds();
        
        // Find closest point on box to circle center
        const closestX = Math.max(boxBounds.left, Math.min(circleBounds.centerX, boxBounds.right));
        const closestY = Math.max(boxBounds.top, Math.min(circleBounds.centerY, boxBounds.bottom));
        
        // Calculate distance
        const dx = circleBounds.centerX - closestX;
        const dy = circleBounds.centerY - closestY;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        if (distance < circleBounds.radius) {
            const overlap = circleBounds.radius - distance;
            const nx = dx / distance || 0;
            const ny = dy / distance || 0;
            
            return {
                colliderA: box,
                colliderB: circle,
                overlap,
                pushX: nx * overlap,
                pushY: ny * overlap,
                contactPoint: { x: closestX, y: closestY }
            };
        }
        
        return null;
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // FRAME UPDATE
    // ════════════════════════════════════════════════════════════════════════
    
    /**
     * Update collision detection for this frame
     * Call this each frame after positions are updated
     */
    update(delta, context = {}) {
        const currentCollisions = new Set();
        const colliderArray = Array.from(this.colliders.values());
        
        // Check all pairs
        for (let i = 0; i < colliderArray.length; i++) {
            for (let j = i + 1; j < colliderArray.length; j++) {
                const a = colliderArray[i];
                const b = colliderArray[j];
                
                const collision = this.checkCollision(a, b);
                
                if (collision) {
                    const pairKey = this._getPairKey(a.id, b.id);
                    currentCollisions.add(pairKey);
                    
                    // Determine if this is a trigger or solid collision
                    const isTrigger = a.isTrigger || b.isTrigger;
                    
                    // Check if this is a new collision (enter)
                    if (!this.activeCollisions.has(pairKey)) {
                        if (isTrigger) {
                            this._handleTriggerEnter(collision);
                        } else {
                            this._handleCollisionEnter(collision);
                        }
                    } else {
                        // Ongoing collision (stay)
                        if (isTrigger) {
                            this._handleTriggerStay(collision);
                        } else {
                            this._handleCollisionStay(collision);
                        }
                    }
                }
            }
        }
        
        // Check for collision exits
        this.activeCollisions.forEach(pairKey => {
            if (!currentCollisions.has(pairKey)) {
                this._handleCollisionExit(pairKey);
            }
        });
        
        // Update active collisions
        this.activeCollisions = currentCollisions;
        
        // Draw debug
        if (this.debugEnabled && this.debugGraphics) {
            this._drawDebug();
        }
    }
    
    _getPairKey(idA, idB) {
        return idA < idB ? `${idA}|${idB}` : `${idB}|${idA}`;
    }
    
    _handleCollisionEnter(collision) {
        collision.colliderA.onCollisionEnter?.(collision, collision.colliderB);
        collision.colliderB.onCollisionEnter?.(collision, collision.colliderA);
        this._emit('collisionEnter', collision);
    }
    
    _handleCollisionStay(collision) {
        collision.colliderA.onCollisionStay?.(collision, collision.colliderB);
        collision.colliderB.onCollisionStay?.(collision, collision.colliderA);
        this._emit('collisionStay', collision);
    }
    
    _handleCollisionExit(pairKey) {
        const [idA, idB] = pairKey.split('|');
        const colliderA = this.colliders.get(idA);
        const colliderB = this.colliders.get(idB);
        
        if (colliderA) colliderA.onCollisionExit?.(colliderB);
        if (colliderB) colliderB.onCollisionExit?.(colliderA);
        this._emit('collisionExit', { idA, idB, colliderA, colliderB });
    }
    
    _handleTriggerEnter(collision) {
        collision.colliderA.onTriggerEnter?.(collision, collision.colliderB);
        collision.colliderB.onTriggerEnter?.(collision, collision.colliderA);
        this._emit('triggerEnter', collision);
    }
    
    _handleTriggerStay(collision) {
        collision.colliderA.onTriggerStay?.(collision, collision.colliderB);
        collision.colliderB.onTriggerStay?.(collision, collision.colliderA);
        this._emit('triggerStay', collision);
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // QUERIES
    // ════════════════════════════════════════════════════════════════════════
    
    /**
     * Query colliders at a point
     * @param {number} x 
     * @param {number} y 
     * @param {number} layerMask - Optional layer filter
     * @returns {array} Colliders at point
     */
    queryPoint(x, y, layerMask = COLLISION_CONFIG.LAYERS.ALL) {
        const results = [];
        
        this.colliders.forEach(collider => {
            if ((collider.layer & layerMask) && collider.containsPoint(x, y)) {
                results.push(collider);
            }
        });
        
        return results;
    }
    
    /**
     * Query colliders in a radius
     * @param {number} x 
     * @param {number} y 
     * @param {number} radius 
     * @param {number} layerMask 
     * @returns {array}
     */
    queryRadius(x, y, radius, layerMask = COLLISION_CONFIG.LAYERS.ALL) {
        const results = [];
        const radiusSq = radius * radius;
        
        this.colliders.forEach(collider => {
            if (!(collider.layer & layerMask)) return;
            
            const bounds = collider.getBounds();
            const dx = bounds.centerX - x;
            const dy = bounds.centerY - y;
            const distSq = dx * dx + dy * dy;
            
            if (distSq <= radiusSq) {
                results.push({
                    collider,
                    distance: Math.sqrt(distSq)
                });
            }
        });
        
        // Sort by distance
        results.sort((a, b) => a.distance - b.distance);
        return results;
    }
    
    /**
     * Query colliders in a box area
     * @param {number} x 
     * @param {number} y 
     * @param {number} width 
     * @param {number} height 
     * @param {number} layerMask 
     * @returns {array}
     */
    queryBox(x, y, width, height, layerMask = COLLISION_CONFIG.LAYERS.ALL) {
        const results = [];
        const queryBounds = {
            left: x - width / 2,
            right: x + width / 2,
            top: y - height / 2,
            bottom: y + height / 2
        };
        
        this.colliders.forEach(collider => {
            if (!(collider.layer & layerMask)) return;
            
            const bounds = collider.getBounds();
            
            // AABB overlap check
            if (bounds.left < queryBounds.right &&
                bounds.right > queryBounds.left &&
                bounds.top < queryBounds.bottom &&
                bounds.bottom > queryBounds.top) {
                results.push(collider);
            }
        });
        
        return results;
    }
    
    /**
     * Raycast from point in direction
     * @param {number} startX 
     * @param {number} startY 
     * @param {number} dirX 
     * @param {number} dirY 
     * @param {number} maxDistance 
     * @param {number} layerMask 
     * @returns {object|null} First hit or null
     */
    raycast(startX, startY, dirX, dirY, maxDistance = 1000, layerMask = COLLISION_CONFIG.LAYERS.ALL) {
        const results = [];
        
        // Normalize direction
        const len = Math.sqrt(dirX * dirX + dirY * dirY);
        const dx = dirX / len;
        const dy = dirY / len;
        
        this.colliders.forEach(collider => {
            if (!(collider.layer & layerMask)) return;
            
            const bounds = collider.getBounds();
            
            // Simple ray-AABB intersection
            let tmin = 0;
            let tmax = maxDistance;
            
            // X axis
            if (Math.abs(dx) > 0.0001) {
                const tx1 = (bounds.left - startX) / dx;
                const tx2 = (bounds.right - startX) / dx;
                tmin = Math.max(tmin, Math.min(tx1, tx2));
                tmax = Math.min(tmax, Math.max(tx1, tx2));
            }
            
            // Y axis
            if (Math.abs(dy) > 0.0001) {
                const ty1 = (bounds.top - startY) / dy;
                const ty2 = (bounds.bottom - startY) / dy;
                tmin = Math.max(tmin, Math.min(ty1, ty2));
                tmax = Math.min(tmax, Math.max(ty1, ty2));
            }
            
            if (tmin <= tmax && tmin >= 0 && tmin <= maxDistance) {
                results.push({
                    collider,
                    distance: tmin,
                    point: {
                        x: startX + dx * tmin,
                        y: startY + dy * tmin
                    }
                });
            }
        });
        
        // Return closest hit
        results.sort((a, b) => a.distance - b.distance);
        return results[0] || null;
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // DEBUG VISUALIZATION
    // ════════════════════════════════════════════════════════════════════════
    
    /**
     * Enable debug visualization
     * @param {Phaser.GameObjects.Graphics} graphics 
     */
    enableDebug(graphics) {
        this.debugEnabled = true;
        this.debugGraphics = graphics;
    }
    
    disableDebug() {
        this.debugEnabled = false;
        if (this.debugGraphics) {
            this.debugGraphics.clear();
        }
    }
    
    _drawDebug() {
        if (!this.debugGraphics) return;
        
        this.debugGraphics.clear();
        
        this.colliders.forEach(collider => {
            if (!collider.enabled) return;
            
            const bounds = collider.getBounds();
            let color = COLLISION_CONFIG.DEBUG.hitboxColor;
            
            if (collider.isTrigger) {
                color = COLLISION_CONFIG.DEBUG.triggerColor;
            }
            if (collider.userData?.isAttackHitbox) {
                color = COLLISION_CONFIG.DEBUG.attackColor;
            }
            
            this.debugGraphics.lineStyle(1, color, 1);
            this.debugGraphics.fillStyle(color, COLLISION_CONFIG.DEBUG.hitboxAlpha);
            
            if (collider.type === 'box') {
                this.debugGraphics.fillRect(
                    bounds.left, bounds.top,
                    bounds.width, bounds.height
                );
                this.debugGraphics.strokeRect(
                    bounds.left, bounds.top,
                    bounds.width, bounds.height
                );
            } else if (collider.type === 'circle') {
                this.debugGraphics.fillCircle(bounds.centerX, bounds.centerY, bounds.radius);
                this.debugGraphics.strokeCircle(bounds.centerX, bounds.centerY, bounds.radius);
            }
        });
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // EVENT SYSTEM
    // ════════════════════════════════════════════════════════════════════════
    
    on(event, callback) {
        if (!this.listeners.has(event)) {
            this.listeners.set(event, new Set());
        }
        this.listeners.get(event).add(callback);
        return () => this.listeners.get(event)?.delete(callback);
    }
    
    _emit(event, data) {
        this.listeners.get(event)?.forEach(cb => cb(data));
        this.listeners.get('*')?.forEach(cb => cb(event, data));
    }
    
    _log(message) {
        console.log(`%c[CollisionSystem] ${message}`, 'color: #ff8800');
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // CLEANUP
    // ════════════════════════════════════════════════════════════════════════
    
    /**
     * Remove all colliders
     */
    clear() {
        this.colliders.clear();
        this.activeCollisions.clear();
        if (this.debugGraphics) {
            this.debugGraphics.clear();
        }
    }
}

// ════════════════════════════════════════════════════════════════════════════
// SINGLETON EXPORT
// ════════════════════════════════════════════════════════════════════════════

const collisionSystem = new CollisionSystem();

// Export config and classes for external use
collisionSystem.CONFIG = COLLISION_CONFIG;
collisionSystem.BoxCollider = BoxCollider;
collisionSystem.CircleCollider = CircleCollider;
