/**
 * D&D Toolkit Hub - Main Application
 * Handles tab switching, data loading, and global state
 */

// Global state
const AppState = {
    monsters: [],
    spells: [],
    items: [],
    cardQueue: [],
    currentTab: 'browser',
    dataLoaded: false
};

// Tab switching
function showTab(tabName) {
    // Hide all tab panels
    document.querySelectorAll('.tab-panel').forEach(panel => {
        panel.classList.remove('active');
    });

    // Remove active state from all buttons
    document.querySelectorAll('.tab-nav .rpgui-button').forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected tab
    const tabPanel = document.getElementById('tab-' + tabName);
    if (tabPanel) {
        tabPanel.classList.add('active');
    }

    // Highlight active button
    const tabBtn = document.getElementById('btn-' + tabName);
    if (tabBtn) {
        tabBtn.classList.add('active');
    }

    AppState.currentTab = tabName;
}

// Load JSON data
async function loadData() {
    try {
        // Load monsters
        const monstersRes = await fetch('data/monsters.json');
        if (monstersRes.ok) {
            AppState.monsters = await monstersRes.json();
            document.getElementById('stat-monsters').textContent = AppState.monsters.length;
        }

        // Load spells
        const spellsRes = await fetch('data/spells.json');
        if (spellsRes.ok) {
            AppState.spells = await spellsRes.json();
            document.getElementById('stat-spells').textContent = AppState.spells.length;
        }

        // Load items
        const itemsRes = await fetch('data/items.json');
        if (itemsRes.ok) {
            AppState.items = await itemsRes.json();
            document.getElementById('stat-items').textContent = AppState.items.length;
        }

        AppState.dataLoaded = true;
        console.log('Data loaded:', {
            monsters: AppState.monsters.length,
            spells: AppState.spells.length,
            items: AppState.items.length
        });

        // Initial search to populate results
        performSearch();

    } catch (error) {
        console.error('Error loading data:', error);
    }
}

// Copy text to clipboard
function copyTextToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showNotification('Copied to clipboard!');
        }).catch(err => {
            console.error('Copy failed:', err);
            fallbackCopy(text);
        });
    } else {
        fallbackCopy(text);
    }
}

function fallbackCopy(text) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();
    try {
        document.execCommand('copy');
        showNotification('Copied to clipboard!');
    } catch (err) {
        showNotification('Copy failed');
    }
    document.body.removeChild(textarea);
}

// Simple notification
function showNotification(message) {
    // Create notification element if doesn't exist
    let notification = document.getElementById('notification');
    if (!notification) {
        notification = document.createElement('div');
        notification.id = 'notification';
        notification.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #c9a227;
            color: #1a1a2e;
            padding: 15px 25px;
            border-radius: 5px;
            font-weight: bold;
            z-index: 1000;
            opacity: 0;
            transition: opacity 0.3s;
        `;
        document.body.appendChild(notification);
    }

    notification.textContent = message;
    notification.style.opacity = '1';

    setTimeout(() => {
        notification.style.opacity = '0';
    }, 2000);
}

// Open external tools
function openTool(tool) {
    const toolPaths = {
        'dungeoneer': '../_external/dungeoneer/README.md',
        'rpg-cards': '../_external/rpg-cards/generator/index.html',
        'donjon': '../_external/donjon-to-homebrewery/README.md',
        'srd': '../_external/dnd5e-srd/README.md'
    };

    const path = toolPaths[tool];
    if (path) {
        window.open(path, '_blank');
    }
}

// Get modifier from ability score
function getModifier(score) {
    if (!score) return '+0';
    const mod = Math.floor((score - 10) / 2);
    return mod >= 0 ? '+' + mod : mod.toString();
}

// Format CR display
function formatCR(cr) {
    if (cr === null || cr === undefined) return 'N/A';
    if (cr === 0.125) return '1/8';
    if (cr === 0.25) return '1/4';
    if (cr === 0.5) return '1/2';
    return cr.toString();
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Set initial active tab
    showTab('browser');

    // Load data
    loadData();

    // Initialize RPGUI elements that were added dynamically
    if (typeof RPGUI !== 'undefined' && RPGUI.on_load) {
        RPGUI.on_load(() => {
            console.log('RPGUI loaded');
        });
    }
});
