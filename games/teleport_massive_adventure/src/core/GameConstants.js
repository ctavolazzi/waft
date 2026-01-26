/**
 * GameConstants - Centralized configuration and constants
 * 
 * All magic numbers, strings, and configuration values should live here.
 * This makes the game easier to balance, debug, and maintain.
 */

export const SCENE_MAP = {
    'lab': 'LabScene',
    'lobby': 'LobbyScene',
    'underground': 'UndergroundScene',
    'void': 'VoidScene'
};

export const SCENE_TRANSITION = {
    FADE_DURATION: 300,
    FADE_COLOR: 0x000000
};

export const PLAYER = {
    DEFAULT_SPEED: 150,
    DEFAULT_POSITION: { x: 400, y: 400 },
    INTERACTION_RANGE: 60,
    SPRITE_SCALE: 1.5
};

export const UI = {
    INVENTORY_SLOT_SIZE: 40,
    DIALOGUE_BOX_WIDTH: 700,
    DIALOGUE_BOX_PADDING: 15
};

export const DEPTH = {
    BACKGROUND: 0,
    FLOOR: 1,
    OBJECTS: 5,
    CHARACTERS: 10,
    UI: 100
};

export const CURSOR_MODES = {
    WALK: 'walk',
    LOOK: 'look',
    USE: 'use',
    TALK: 'talk',
    PICKUP: 'pickup'
};

export const ITEM_ICONS = {
    ARTIFACT: '◈',
    KEYCARD: '▭',
    DEFAULT: '?'
};

export const ROOM_IDS = {
    LAB: 'lab',
    LOBBY: 'lobby',
    UNDERGROUND: 'underground',
    VOID: 'void'
};
