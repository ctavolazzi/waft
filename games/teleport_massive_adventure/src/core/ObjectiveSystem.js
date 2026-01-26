/**
 * ObjectiveSystem - Tracks game objectives and provides contextual hints
 * 
 * Manages current objectives, completed objectives, and provides
 * contextual thought bubble hints based on game state.
 */
class ObjectiveSystem {
    constructor() {
        this.objectives = [];
        this.currentObjective = null;
        this.completedObjectives = [];
        
        // Objective definitions
        this.objectiveDefinitions = this._initializeObjectives();
        
        // Thought bubble element
        this.thoughtBubble = null;
        this.updateInterval = null;
    }
    
    _initializeObjectives() {
        return {
            'start': {
                id: 'start',
                name: 'Explore the Lab',
                description: 'Look around your lab. Something feels off today.',
                hint: 'Examine the photo on the wall. It might remind you of something important.',
                condition: { flag: 'visitedLab', equals: true },
                nextObjective: 'examine_photo'
            },
            'examine_photo': {
                id: 'examine_photo',
                name: 'Remember Maya',
                description: 'The photo brings back memories...',
                hint: 'You should pick up that artifact. It might be important.',
                condition: { flag: 'examinedPhoto', equals: true },
                nextObjective: 'pickup_artifact'
            },
            'pickup_artifact': {
                id: 'pickup_artifact',
                name: 'Collect the Artifact',
                description: 'That strange artifact from The Between...',
                hint: 'Check the terminal. Your research might have answers.',
                condition: { flag: 'hasArtifact', equals: true },
                nextObjective: 'use_terminal'
            },
            'use_terminal': {
                id: 'use_terminal',
                name: 'Access Research Terminal',
                description: 'Your research data might hold clues.',
                hint: 'The door to the lobby is on the right. Maybe someone there knows something.',
                condition: { flag: 'terminalHacked', equals: true },
                nextObjective: 'go_to_lobby'
            },
            'go_to_lobby': {
                id: 'go_to_lobby',
                name: 'Go to Lobby',
                description: 'The main lobby might have answers.',
                hint: 'Talk to the security guard. They might know what\'s happening.',
                condition: { flag: 'visitedLobby', equals: true },
                nextObjective: 'talk_to_guard'
            },
            'talk_to_guard': {
                id: 'talk_to_guard',
                name: 'Speak with Security',
                description: 'The guard might have information.',
                hint: 'Look around. There might be a keycard somewhere.',
                condition: { flag: 'talkedToGuard', equals: true },
                nextObjective: 'find_keycard'
            },
            'find_keycard': {
                id: 'find_keycard',
                name: 'Find Security Keycard',
                description: 'You need access to restricted areas.',
                hint: 'The keycard should be nearby. Check the floor near the guard.',
                condition: { flag: 'hasKeycard', equals: true },
                nextObjective: 'use_maintenance_hatch'
            },
            'use_maintenance_hatch': {
                id: 'use_maintenance_hatch',
                name: 'Access Maintenance Area',
                description: 'The maintenance hatch leads underground.',
                hint: 'Use the keycard on the maintenance hatch to go underground.',
                condition: { flag: 'visitedUnderground', equals: true },
                nextObjective: 'talk_to_phaseburner'
            },
            'talk_to_phaseburner': {
                id: 'talk_to_phaseburner',
                name: 'Meet Phaseburner',
                description: 'A glitched entity in the underground...',
                hint: 'Phaseburner mentioned a portal. Check the damaged terminal for clues.',
                condition: { flag: 'talkedToPhaseburner', equals: true },
                nextObjective: 'use_damaged_terminal'
            },
            'use_damaged_terminal': {
                id: 'use_damaged_terminal',
                name: 'Access Encrypted Files',
                description: 'The terminal holds encrypted data.',
                hint: 'With the artifact and terminal data, the portal should appear. Look for it.',
                condition: { flag: 'terminalHackedUnderground', equals: true },
                nextObjective: 'enter_portal'
            },
            'enter_portal': {
                id: 'enter_portal',
                name: 'Enter the Portal',
                description: 'The dimensional portal awaits...',
                hint: 'The portal is your way forward. Step through when ready.',
                condition: { flag: 'visitedVoid', equals: true },
                nextObjective: 'face_dealer'
            },
            'use_drone': {
                id: 'use_drone',
                name: 'Use Your Drone',
                description: 'Your combat drone is ready.',
                hint: 'Your drone auto-targets enemies. Press 1 for Burst Shot, 2 for Shield Mode. Find workbenches to upgrade it.',
                condition: { flag: 'hasCombatDrone', equals: true },
                nextObjective: 'enter_portal'
            },
            'face_dealer': {
                id: 'face_dealer',
                name: 'Confront THE DEALER',
                description: 'The final confrontation...',
                hint: 'Use your words wisely. Question, bluff, or invoke Maya\'s memory.',
                condition: { flag: 'defeatedDealer', equals: true },
                nextObjective: 'choose_ending'
            },
            'choose_ending': {
                id: 'choose_ending',
                name: 'Make Your Choice',
                description: 'The final decision...',
                hint: 'Choose your path: Liberation, Unity, or Destruction.',
                condition: { flag: 'endingChosen', equals: true },
                nextObjective: null
            }
        };
    }
    
    init() {
        // Get thought bubble element
        this.thoughtBubble = document.getElementById('god-commentary');
        if (!this.thoughtBubble) {
            console.warn('Thought bubble element not found');
            return;
        }
        
        // Start with first objective
        this.setCurrentObjective('start');
        
        // Update thought bubble periodically
        this.updateInterval = setInterval(() => this.updateThoughtBubble(), 2000);
        
        // Listen to game state changes
        if (window.gameState) {
            gameState.on('flagChanged', () => {
                this.checkObjectives();
            });
        }
        
        // Initial update
        this.updateThoughtBubble();
    }
    
    setCurrentObjective(objectiveId) {
        const objective = this.objectiveDefinitions[objectiveId];
        if (!objective) return;
        
        this.currentObjective = objective;
        this.updateThoughtBubble();
    }
    
    checkObjectives() {
        if (!this.currentObjective) return;
        
        // Check if current objective is complete
        if (gameState.checkCondition(this.currentObjective.condition)) {
            // Mark as complete
            this.completedObjectives.push(this.currentObjective.id);
            
            // Move to next objective
            if (this.currentObjective.nextObjective) {
                this.setCurrentObjective(this.currentObjective.nextObjective);
            } else {
                // No more objectives
                this.currentObjective = null;
                this.updateThoughtBubble();
            }
        }
    }
    
    updateThoughtBubble() {
        if (!this.thoughtBubble) return;
        
        let thought = '';
        
        if (this.currentObjective) {
            thought = this.currentObjective.hint;
        } else {
            // Default thoughts
            const defaultThoughts = [
                "What am I trying to remember?",
                "Something feels incomplete...",
                "I should keep exploring.",
                "The answers are here somewhere."
            ];
            thought = defaultThoughts[Math.floor(Math.random() * defaultThoughts.length)];
        }
        
        // Update with fade animation
        this.thoughtBubble.style.opacity = '0';
        setTimeout(() => {
            this.thoughtBubble.textContent = thought;
            this.thoughtBubble.style.opacity = '0.8';
        }, 200);
    }
    
    getCurrentHint() {
        return this.currentObjective?.hint || 'Keep exploring...';
    }
    
    destroy() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
            this.updateInterval = null;
        }
    }
}

// Create global instance
const objectiveSystem = new ObjectiveSystem();
