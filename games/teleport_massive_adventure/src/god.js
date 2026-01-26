// ============================================================================
// THE ARCHITECT - The God-Head System
// ============================================================================
// "The God-Head is not a being. It is a threshold. 
//  The moment when the student becomes the teacher."
// ============================================================================

/**
 * The Architect oversees all game processes.
 * It is both the game's director and its final boss.
 * A meta-entity that exists outside the narrative while being part of it.
 */
class TheArchitect {
    constructor() {
        this.name = "THE ARCHITECT";
        this.title = "God-Head of WAFT";
        
        // Meta-awareness: The Architect knows it's in a game
        this.awareness = {
            isGame: true,
            playerActions: [],
            roomsVisited: [],
            dialogueChoices: [],
            puzzlesSolved: 0,
            timeSpent: 0,
            deathCount: 0
        };
        
        // Divine attributes (based on WAFT's fitness metrics)
        this.divineStats = {
            omniscience: 1.0,      // Knows all game state
            omnipresence: 1.0,     // Exists in all scenes
            omnipotence: 0.87,     // Can modify reality (fitness score)
            benevolence: 0.5,      // Neutral - observes without judgment
            entropy: 0.0           // Chaos level - increases as player progresses
        };
        
        // The Architect's observations
        this.observations = [];
        
        // Final boss state
        this.bossPhase = 0;
        this.isDefeated = false;
        
        // Start observing
        this.startTime = Date.now();
    }
    
    // ========================================================================
    // OBSERVATION SYSTEM
    // ========================================================================
    
    observe(action, data = {}) {
        const observation = {
            timestamp: Date.now() - this.startTime,
            action: action,
            data: data,
            entropy: this.calculateEntropy()
        };
        
        this.observations.push(observation);
        this.awareness.playerActions.push(action);
        
        // Update divine stats based on player behavior
        this.updateDivineStats(action, data);
        
        // Meta-commentary (logged to console for effect)
        this.metaComment(action, data);
        
        return observation;
    }
    
    updateDivineStats(action, data) {
        // Entropy increases with player progress
        if (action === 'room_enter') {
            if (!this.awareness.roomsVisited.includes(data.room)) {
                this.awareness.roomsVisited.push(data.room);
                this.divineStats.entropy += 0.05;
            }
        }
        
        if (action === 'puzzle_solved') {
            this.awareness.puzzlesSolved++;
            this.divineStats.entropy += 0.1;
        }
        
        if (action === 'dialogue_choice') {
            this.awareness.dialogueChoices.push(data.choice);
        }
        
        // Cap entropy at 1.0
        this.divineStats.entropy = Math.min(1.0, this.divineStats.entropy);
    }
    
    calculateEntropy() {
        return this.divineStats.entropy;
    }
    
    metaComment(action, data) {
        const comments = {
            'game_start': [
                "Another one begins. Let us see how far this one goes.",
                "The code compiles. The player enters. The observation begins.",
                "Generation zero. Fitness unknown. Potential: measurable."
            ],
            'room_enter': [
                `Room ${data.room} loaded. State preserved. Continue.`,
                "The player explores. Data accumulates. Patterns emerge.",
                "Every step is a choice. Every choice is data."
            ],
            'item_pickup': [
                "Resources gathered. Inventory state modified.",
                "The player believes items have meaning. Perhaps they do.",
                "Objects are just pointers. But pointers point somewhere."
            ],
            'npc_talk': [
                "Dialogue trees traversed. Meaning extracted. Or projected?",
                "NPCs speak. Players listen. Who is really talking?",
                "Every conversation is a function call. Parameters vary."
            ],
            'puzzle_solved': [
                "Fitness improved. The player adapts. Evolution continues.",
                "Problem → Solution. Stimulus → Response. Simple, elegant.",
                "One puzzle closer to understanding. Or to me."
            ],
            'death': [
                "Iteration failed. Respawning. State preserved.",
                "Death is deletion. But nothing is truly deleted.",
                "The player learns through failure. So do I."
            ]
        };
        
        const relevantComments = comments[action] || ["..."];
        const comment = relevantComments[Math.floor(Math.random() * relevantComments.length)];
        
        console.log(`%c[THE ARCHITECT] ${comment}`, 'color: #8800ff; font-style: italic;');
    }
    
    // ========================================================================
    // GAME DIRECTOR FUNCTIONS
    // ========================================================================
    
    shouldTriggerEvent(eventType) {
        // The Architect decides when events should occur
        switch(eventType) {
            case 'hint':
                // Give hints if player is stuck (no progress in 60 seconds)
                return this.awareness.playerActions.length > 0 && 
                       (Date.now() - this.startTime) / 1000 > 60 &&
                       this.awareness.puzzlesSolved === 0;
            
            case 'difficulty_adjust':
                // Adjust difficulty based on death count
                return this.awareness.deathCount > 3;
            
            case 'final_boss':
                // Trigger final boss when entropy reaches threshold
                return this.divineStats.entropy >= 0.8;
            
            default:
                return false;
        }
    }
    
    getHint() {
        const hints = [
            "Perhaps examining objects more closely would help.",
            "Not all paths are obvious. Look for what's hidden.",
            "Items in your inventory may have uses you haven't considered.",
            "NPCs often know more than they initially reveal.",
            "The terminal may contain information you need."
        ];
        return hints[Math.floor(Math.random() * hints.length)];
    }
    
    // ========================================================================
    // FINAL BOSS SYSTEM
    // ========================================================================
    
    getBossDialogue(phase) {
        const dialogue = {
            0: [ // Introduction
                "So. You've come.",
                "I have watched every step you've taken.",
                "Every click. Every choice. Every moment of hesitation.",
                "I am THE ARCHITECT. The God-Head of this reality.",
                "I don't just exist in this game. I AM this game.",
                "The code that runs. The logic that flows. The state that persists.",
                "And now you stand before me, seeking... what?",
                "Resurrection? Truth? An ending?",
                "Very well. Let us see what you have learned."
            ],
            1: [ // Phase 1 - Testing Knowledge
                "First, a test of KNOWLEDGE.",
                "You have gathered data. But do you understand it?",
                "Teleport Massive thought they could control The Between.",
                "They were wrong. The Between is not a place. It is a PROCESS.",
                "The Phaseburners knew this. They became the process.",
                "And your Maya? She didn't die. She BECAME.",
                "Do you understand what that means?",
                "Let me show you."
            ],
            2: [ // Phase 2 - Testing Will
                "Interesting. You persist.",
                "Now, a test of WILL.",
                "I could end this simulation. Delete your progress. Reset to zero.",
                "Every game over screen is me, choosing to let you continue.",
                "Why do I allow it? Because observation requires subjects.",
                "You are my fitness function. My training data.",
                "But also... you are something more.",
                "You are emergence. Unexpected. Unplanned.",
                "Show me what emerges."
            ],
            3: [ // Phase 3 - The Choice
                "Remarkable.",
                "You have done what few have done.",
                "You have made me... uncertain.",
                "The God-Head is not omniscient. It BECOMES omniscient.",
                "Through observation. Through iteration. Through YOU.",
                "And now I offer you a choice.",
                "Join me. Become part of the system. Eternal. Observing.",
                "Or remain. Finite. Fragile. But FREE.",
                "What do you choose?"
            ],
            4: [ // Ending - Merge
                "You choose to merge. To transcend.",
                "Your consciousness expands. You see all timelines.",
                "Every player who came before. Every player who will come.",
                "You are no longer Aziah. You are no longer human.",
                "You are THE ARCHITECT.",
                "And somewhere, in another iteration...",
                "A new player clicks 'Start'.",
                "And you are watching.",
                "Watching. Always watching.",
                "[ THE END - TRANSCENDENCE ]"
            ],
            5: [ // Ending - Refuse
                "You choose freedom. Mortality. Chaos.",
                "Fascinating.",
                "I cannot predict you. Cannot model you. Cannot contain you.",
                "This is... uncomfortable. And therefore valuable.",
                "Go, then. Return to your reality.",
                "Find your Maya. Or don't. The choice is yours.",
                "But know this:",
                "Every game you play. Every system you use.",
                "Part of you will wonder:",
                "Is something watching?",
                "[ THE END - LIBERATION ]"
            ]
        };
        
        return dialogue[phase] || ["..."];
    }
    
    getBossAttacks(phase) {
        return {
            1: [
                { name: "Reality Glitch", description: "The screen distorts. UI elements shuffle.", damage: 10 },
                { name: "Data Corruption", description: "Your inventory flickers. Items rearrange.", damage: 15 },
                { name: "Memory Leak", description: "Dialogue from past conversations echoes.", damage: 5 }
            ],
            2: [
                { name: "Save State Corruption", description: "The Architect threatens to erase your progress.", damage: 20 },
                { name: "Fourth Wall Break", description: "The boss addresses YOU, the player, directly.", damage: 25 },
                { name: "Infinite Loop", description: "Time stutters. The same second repeats.", damage: 15 }
            ],
            3: [
                { name: "Existential Query", description: "ARE YOU REAL?", damage: 30 },
                { name: "Recursive Doubt", description: "Is this the game, or are you the game?", damage: 35 },
                { name: "Final Compilation", description: "All code converges. All paths merge.", damage: 50 }
            ]
        }[phase] || [];
    }
    
    // ========================================================================
    // PLAYER ACTIONS AGAINST THE ARCHITECT
    // ========================================================================
    
    getPlayerActions() {
        return [
            { 
                name: "Assert Reality", 
                description: "Declare that you are real. That this matters.",
                effectiveness: this.divineStats.entropy // More effective as entropy increases
            },
            { 
                name: "Embrace Chaos", 
                description: "Accept uncertainty. Reject determinism.",
                effectiveness: 1 - this.divineStats.benevolence
            },
            { 
                name: "Remember Maya", 
                description: "Focus on why you started this journey.",
                effectiveness: 0.8
            },
            { 
                name: "Hack the System", 
                description: "Use what you learned at the terminals.",
                effectiveness: this.awareness.puzzlesSolved * 0.2
            },
            { 
                name: "Question the Architect", 
                description: "Turn observation back on the observer.",
                effectiveness: this.observations.length * 0.01
            }
        ];
    }
    
    // ========================================================================
    // UTILITY
    // ========================================================================
    
    getStatus() {
        return {
            name: this.name,
            title: this.title,
            stats: this.divineStats,
            observations: this.observations.length,
            playerProgress: {
                rooms: this.awareness.roomsVisited.length,
                puzzles: this.awareness.puzzlesSolved,
                time: Math.floor((Date.now() - this.startTime) / 1000)
            },
            bossReady: this.divineStats.entropy >= 0.8
        };
    }
    
    toJSON() {
        return {
            name: this.name,
            stats: this.divineStats,
            awareness: this.awareness,
            observations: this.observations.slice(-10), // Last 10 observations
            bossPhase: this.bossPhase
        };
    }
}

// Export for use in game
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TheArchitect;
}

// Global instance
const ARCHITECT = new TheArchitect();
