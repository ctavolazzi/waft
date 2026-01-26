/**
 * Utils Loader - Makes utilities available globally
 * 
 * Since the codebase uses script tags instead of ES6 modules,
 * this file loads utilities and makes them available on window.
 * 
 * Include this script AFTER all utility files are loaded.
 */

(function() {
    'use strict';

    // Make SceneTransition available globally
    if (typeof SceneTransition !== 'undefined') {
        window.SceneTransition = SceneTransition;
    }

    // Make VisualEffects available globally
    if (typeof VisualEffects !== 'undefined') {
        window.VisualEffects = VisualEffects;
    }

    // Make GameConstants available globally
    if (typeof SCENE_MAP !== 'undefined') {
        window.GameConstants = {
            SCENE_MAP,
            SCENE_TRANSITION,
            PLAYER,
            UI,
            DEPTH,
            CURSOR_MODES,
            ITEM_ICONS,
            ROOM_IDS
        };
    }

    console.log('[UtilsLoader] Utilities loaded and available globally');
})();
