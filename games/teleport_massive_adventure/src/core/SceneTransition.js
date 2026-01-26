/**
 * SceneTransition - Centralized scene transition logic
 * 
 * Handles all scene changes with consistent fade effects and cleanup.
 * Eliminates duplication across BaseScene, InteractionSystem, etc.
 */

import { SCENE_MAP, SCENE_TRANSITION } from './GameConstants.js';

export class SceneTransition {
    /**
     * Transition to a new room/scene
     * @param {Phaser.Scene} currentScene - Current scene instance
     * @param {string} roomId - Room identifier (e.g., 'lab', 'void')
     * @param {object} options - Transition options
     * @param {number} options.playerX - Player X position in new scene
     * @param {number} options.playerY - Player Y position in new scene
     * @param {function} options.onCleanup - Callback before transition
     * @param {function} options.onComplete - Callback after transition
     */
    static transition(currentScene, roomId, options = {}) {
        const {
            playerX = 400,
            playerY = 400,
            onCleanup = null,
            onComplete = null
        } = options;

        // Get scene key from map
        const sceneKey = SCENE_MAP[roomId] || roomId;

        // Run cleanup callback if provided
        if (onCleanup) {
            onCleanup();
        }

        // Fade out
        currentScene.cameras.main.fadeOut(
            SCENE_TRANSITION.FADE_DURATION,
            SCENE_TRANSITION.FADE_COLOR,
            SCENE_TRANSITION.FADE_COLOR,
            SCENE_TRANSITION.FADE_COLOR
        );

        // Start new scene after fade
        currentScene.time.delayedCall(SCENE_TRANSITION.FADE_DURATION, () => {
            currentScene.scene.start(sceneKey, {
                playerX,
                playerY
            });

            if (onComplete) {
                onComplete();
            }
        });
    }

    /**
     * Cleanup player resources before transition
     * @param {object} player - PlayerController instance
     */
    static cleanupPlayer(player) {
        if (player?.combatDrone) {
            player.combatDrone.destroy();
            player.combatDrone = null;
        }
    }
}
