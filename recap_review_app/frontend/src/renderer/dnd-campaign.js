/**
 * DnD Campaign Renderer
 * 
 * Handles the UI for the self-playing DnD campaign in Electron.
 */

const { electronAPI } = window;

// DOM Elements
const startBtn = document.getElementById('start-btn');
const stopBtn = document.getElementById('stop-btn');
const statusText = document.getElementById('status-text');
const partyGrid = document.getElementById('party-grid');
const currentScene = document.getElementById('current-scene');
const encountersList = document.getElementById('encounters-list');
const campaignLog = document.getElementById('campaign-log');
const victoryScreen = document.getElementById('victory-screen');

let campaignRunning = false;
let updateInterval = null;

// Event Listeners
startBtn.addEventListener('click', startCampaign);
stopBtn.addEventListener('stop', stopCampaign);

// Listen for campaign updates from main process
if (window.electronAPI && window.electronAPI.onCampaignUpdate) {
    const unsubscribe = window.electronAPI.onCampaignUpdate((event, data) => {
        updateUI(data);
    });
    
    // Cleanup on page unload
    window.addEventListener('beforeunload', () => {
        if (unsubscribe) unsubscribe();
    });
}

/**
 * Start the campaign
 */
async function startCampaign() {
    try {
        startBtn.disabled = true;
        stopBtn.disabled = false;
        campaignRunning = true;
        statusText.textContent = '🎲 Starting campaign...';
        
        // Clear previous state
        partyGrid.innerHTML = '';
        encountersList.innerHTML = '';
        campaignLog.innerHTML = '';
        victoryScreen.style.display = 'none';
        
        // Start campaign via IPC
        const result = await window.electronAPI.startDnDCampaign();
        
        if (result.success) {
            statusText.textContent = '🎲 Campaign running...';
            
            // Start polling for updates
            startUpdatePolling();
        } else {
            throw new Error(result.error || 'Failed to start campaign');
        }
    } catch (error) {
        console.error('Error starting campaign:', error);
        statusText.textContent = `❌ Error: ${error.message}`;
        startBtn.disabled = false;
        stopBtn.disabled = true;
        campaignRunning = false;
        
        await electronAPI.showErrorBox('Campaign Error', error.message);
    }
}

/**
 * Stop the campaign
 */
async function stopCampaign() {
    try {
        campaignRunning = false;
        stopUpdatePolling();
        
        await window.electronAPI.stopDnDCampaign();
        
        statusText.textContent = '⏹️ Campaign stopped';
        startBtn.disabled = false;
        stopBtn.disabled = true;
    } catch (error) {
        console.error('Error stopping campaign:', error);
        await electronAPI.showErrorBox('Stop Error', error.message);
    }
}

/**
 * Start polling for campaign updates
 */
function startUpdatePolling() {
    updateInterval = setInterval(async () => {
        if (!campaignRunning) {
            stopUpdatePolling();
            return;
        }
        
        try {
            const state = await window.electronAPI.getCampaignState();
            if (state) {
                updateUI(state);
                
                // Check if campaign is complete
                if (state.status === 'complete' || state.victory) {
                    stopUpdatePolling();
                    campaignRunning = false;
                    startBtn.disabled = false;
                    stopBtn.disabled = true;
                    statusText.textContent = '🎉 Campaign complete!';
                    victoryScreen.style.display = 'block';
                }
            }
        } catch (error) {
            console.error('Error polling campaign state:', error);
        }
    }, 1000); // Poll every second
}

/**
 * Stop polling for updates
 */
function stopUpdatePolling() {
    if (updateInterval) {
        clearInterval(updateInterval);
        updateInterval = null;
    }
}

/**
 * Update the UI with campaign state
 */
function updateUI(state) {
    // Update status
    if (state.message) {
        statusText.textContent = state.message;
    }
    
    // Update party
    if (state.party && state.party.length > 0) {
        updateParty(state.party);
    }
    
    // Update current scene
    if (state.current_scene) {
        currentScene.innerHTML = `<p>${state.current_scene}</p>`;
    }
    
    // Update encounters
    if (state.encounters && state.encounters.length > 0) {
        updateEncounters(state.encounters);
    }
    
    // Update log
    if (state.log && state.log.length > 0) {
        updateLog(state.log);
    }
    
    // Show victory screen
    if (state.victory) {
        victoryScreen.style.display = 'block';
    }
}

/**
 * Update party display
 */
function updateParty(party) {
    partyGrid.innerHTML = party.map(member => {
        const hpPercent = (member.hp / member.max_hp) * 100;
        return `
            <div class="party-member">
                <h3>${member.name}</h3>
                <p class="class-race">${member.race} ${member.class} - Level ${member.level}</p>
                <div class="hp-bar">
                    <div class="hp-fill" style="width: ${hpPercent}%"></div>
                    <span class="hp-text">${member.hp}/${member.max_hp} HP</span>
                </div>
                <p style="margin-top: 8px; font-size: 0.9em;">XP: ${member.experience}</p>
            </div>
        `;
    }).join('');
}

/**
 * Update encounters display
 */
function updateEncounters(encounters) {
    encountersList.innerHTML = encounters.map(encounter => {
        return `
            <div class="encounter">
                <h4>⚔️ ${encounter.name}</h4>
                <p>${encounter.description}</p>
                <p class="encounter-meta">Rounds: ${encounter.rounds || 1} | XP: +${encounter.xp || 0}</p>
            </div>
        `;
    }).join('');
    
    // Scroll to bottom
    encountersList.scrollTop = encountersList.scrollHeight;
}

/**
 * Update log display
 */
function updateLog(log) {
    // Show last 20 entries
    const recentLog = log.slice(-20);
    
    campaignLog.innerHTML = recentLog.map(entry => {
        return `<div class="log-entry">${entry}</div>`;
    }).join('');
    
    // Scroll to bottom
    campaignLog.scrollTop = campaignLog.scrollHeight;
}
