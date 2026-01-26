/**
 * VisualEffects - Reusable visual effect utilities
 * 
 * Common effects like damage numbers, screen flashes, etc.
 * Keeps code DRY and consistent across scenes.
 */

export class VisualEffects {
    /**
     * Create a floating damage/heal number
     * @param {Phaser.Scene} scene - Scene to add effect to
     * @param {number} x - X position
     * @param {number} y - Y position
     * @param {number} amount - Damage/heal amount
     * @param {string} type - 'damage' or 'heal'
     * @param {object} options - Additional options
     */
    static floatingNumber(scene, x, y, amount, type = 'damage', options = {}) {
        const color = type === 'damage' ? '#ff4444' : '#44ff44';
        const prefix = type === 'damage' ? '-' : '+';
        
        const text = scene.add.text(x, y, `${prefix}${amount}`, {
            fontSize: options.fontSize || '24px',
            color: color,
            fontFamily: 'monospace',
            fontStyle: 'bold',
            stroke: '#000000',
            strokeThickness: 3
        }).setOrigin(0.5);

        scene.tweens.add({
            targets: text,
            y: y - (options.distance || 50),
            alpha: 0,
            scale: options.scale || 1.5,
            duration: options.duration || 800,
            ease: 'Power2',
            onComplete: () => text.destroy()
        });

        return text;
    }

    /**
     * Screen flash effect
     * @param {Phaser.Scene} scene - Scene to flash
     * @param {number} color - Color value (0xRRGGBB)
     * @param {number} duration - Flash duration in ms
     */
    static screenFlash(scene, color = 0xffffff, duration = 250) {
        scene.cameras.main.flash(duration, 
            (color >> 16) & 0xFF,
            (color >> 8) & 0xFF,
            color & 0xFF
        );
    }

    /**
     * Screen shake effect
     * @param {Phaser.Scene} scene - Scene to shake
     * @param {number} duration - Shake duration in ms
     * @param {number} intensity - Shake intensity (0-1)
     */
    static screenShake(scene, duration = 200, intensity = 0.01) {
        scene.cameras.main.shake(duration, intensity);
    }

    /**
     * Create a pulse effect on a sprite
     * @param {Phaser.Scene} scene - Scene
     * @param {Phaser.GameObjects.GameObject} target - Target to pulse
     * @param {object} options - Pulse options
     */
    static pulse(scene, target, options = {}) {
        const {
            scale = 1.2,
            alpha = 0.8,
            duration = 2000,
            repeat = -1
        } = options;

        scene.tweens.add({
            targets: target,
            scaleX: scale,
            scaleY: scale,
            alpha: alpha,
            duration: duration,
            yoyo: true,
            repeat: repeat,
            ease: 'Sine.easeInOut'
        });
    }

    /**
     * Create a glow effect around a sprite
     * @param {Phaser.Scene} scene - Scene
     * @param {number} x - X position
     * @param {number} y - Y position
     * @param {number} radius - Glow radius
     * @param {number} color - Color value
     * @param {object} options - Glow options
     */
    static glow(scene, x, y, radius, color, options = {}) {
        const {
            alpha = 0.12,
            pulseScale = 1.2,
            pulseDuration = 2000
        } = options;

        const glow = scene.add.circle(x, y, radius, color, alpha);

        scene.tweens.add({
            targets: glow,
            scale: pulseScale,
            alpha: alpha * 0.5,
            duration: pulseDuration,
            yoyo: true,
            repeat: -1,
            ease: 'Sine.easeInOut'
        });

        return glow;
    }
}
