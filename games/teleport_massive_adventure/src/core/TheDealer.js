/**
 * THE DEALER - The Gaming God
 * ═══════════════════════════════════════════════════════════════════════════
 * 
 * "Life is a game, death is the house edge, 
 *  and I? I am the one who shuffles the deck."
 * 
 * A cosmic jester who creates worlds as games, challenges players,
 * and keeps meticulous records of every wager ever made.
 * Part trickster, part casino owner, entirely unpredictable.
 * 
 * Design Philosophy:
 * - Playful but never malicious
 * - Respects skilled players
 * - Genuinely wants someone to beat him (escape)
 * - Tracks everything in The Infinite Ledger
 * - Mood shifts based on player performance
 * 
 * ═══════════════════════════════════════════════════════════════════════════
 */
class TheDealer {
    
    // ════════════════════════════════════════════════════════════════════════
    // CONFIGURATION
    // ════════════════════════════════════════════════════════════════════════
    
    static CONFIG = {
        COMMENT_CHANCE: 0.25,           // 25% chance to comment on events
        FAVORABILITY_DEFAULT: 50,       // Starting favorability
        FAVORABILITY_MAX: 100,
        FAVORABILITY_MIN: 0,
        PLAYSTYLE_THRESHOLD: 5,         // Min decisions before analyzing
        SPEEDRUNNER_THRESHOLD: 10,      // Decisions per minute
    };
    
    static MOODS = {
        AMUSED: 'amused',
        INTRIGUED: 'intrigued', 
        BORED: 'bored',
        EXCITED: 'excited',
        IMPRESSED: 'impressed',
        ANNOYED: 'annoyed',
        DELIGHTED: 'delighted',
        NOSTALGIC: 'nostalgic'
    };
    
    static PLAYSTYLES = {
        NEWCOMER: 'newcomer',
        SPEEDRUNNER: 'speedrunner',
        COMPLETIONIST: 'completionist',
        PERSISTENT: 'persistent',
        CAUTIOUS: 'cautious',
        BALANCED: 'balanced',
        CHAOTIC: 'chaotic',
        STRATEGIC: 'strategic'
    };
    
    // ════════════════════════════════════════════════════════════════════════
    // CONSTRUCTOR
    // ════════════════════════════════════════════════════════════════════════
    
    constructor() {
        this._initializeIdentity();
        this._initializeLedger();
        this._initializeState();
        this._subscribeToEvents();
    }
    
    _initializeIdentity() {
        this.name = "THE DEALER";
        this.titles = [
            "Keeper of the Infinite Ledger",
            "The Cosmic Croupier",
            "Lord of Lucky Sevens",
            "The One Who Deals",
            "Master of the House",
            "The Jester at World's End",
            "Shuffler of Fates",
            "The Golden Grin",
            "Arbiter of Odds",
            "He Who Holds All Cards"
        ];
        this.currentTitle = this._randomFrom(this.titles);
    }
    
    _initializeLedger() {
        this.ledger = {
            currentPlayer: {
                id: `PLAYER_${Date.now().toString(36).toUpperCase()}`,
                sessionStart: Date.now(),
                decisions: [],
                deaths: 0,
                victories: 0,
                itemsCollected: [],
                secretsFound: [],
                dialogueChoices: [],
                roomsVisited: [],
                npcsSpokenTo: [],
                puzzlesSolved: 0,
                playstyle: TheDealer.PLAYSTYLES.NEWCOMER,
                luckyStreak: 0,
                unluckyStreak: 0
            },
            // Simulated "past players" - adds flavor and weight
            pastPlayers: [
                { name: "WANDERER_7742", outcome: "became_dealer", playtime: "3h 22m", note: "Clever, but predictable. Now deals in Sector 7." },
                { name: "ECHO_SEEKER", outcome: "cashed_out", playtime: "1h 45m", note: "Surprising choice at the end. Found Maya." },
                { name: "NULL_VOID", outcome: "erased", playtime: "0h 12m", note: "Tried to cheat. Amusing. Deleted." },
                { name: "MAYA_PRIME", outcome: "cashed_out", playtime: "6h 01m", note: "The original. Beat me fair. Miss her." },
                { name: "SPEED_DEMON", outcome: "folded", playtime: "0h 34m", note: "Too fast, too reckless. Quit at Phase 2." },
                { name: "THE_PATIENT", outcome: "became_dealer", playtime: "14h 33m", note: "Took forever. Worth the wait." },
                { name: "CHAOS_THEORY", outcome: "flipped_table", playtime: "2h 07m", note: "Chose destruction. Respectable." },
                { name: "LUCKY_777", outcome: "cashed_out", playtime: "0h 44m", note: "Pure luck. Incredible run." },
                { name: "THE_ANALYST", outcome: "became_dealer", playtime: "8h 15m", note: "Found every secret. Impressive." },
                { name: "MAYA_SEEKER_2", outcome: "folded", playtime: "4h 20m", note: "Got close. Gave up at the table." }
            ],
            totalGamesDealt: 10847,
            totalPlayersServed: 10847,
            currentWinStreak: 127
        };
    }
    
    _initializeState() {
        // Personality
        this.mood = TheDealer.MOODS.AMUSED;
        this.favorability = TheDealer.CONFIG.FAVORABILITY_DEFAULT;
        
        // Wagers
        this.activeWagers = [];
        this.gamesWon = this.ledger.currentWinStreak;
        this.gamesLost = 0;
        
        // Boss state
        this.bossPhase = 0;
        this.isDefeated = false;
        
        // Observations
        this.observations = [];
        this.lastCommentTime = 0;
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // MOOD SYSTEM
    // ════════════════════════════════════════════════════════════════════════
    
    updateMood(event, data) {
        const player = this.ledger.currentPlayer;
        
        const moodShifts = {
            [EventBus.PUZZLE_SOLVE]: () => {
                this._adjustFavorability(5);
                player.puzzlesSolved++;
                return player.puzzlesSolved > 3 ? TheDealer.MOODS.IMPRESSED : TheDealer.MOODS.INTRIGUED;
            },
            [EventBus.ITEM_PICKUP]: () => {
                return TheDealer.MOODS.AMUSED;
            },
            [EventBus.NPC_TALK]: () => {
                this._adjustFavorability(2);
                if (!player.npcsSpokenTo.includes(data?.npc)) {
                    player.npcsSpokenTo.push(data?.npc);
                }
                return TheDealer.MOODS.INTRIGUED;
            },
            [EventBus.ROOM_ENTER]: () => {
                if (!player.roomsVisited.includes(data?.room)) {
                    player.roomsVisited.push(data?.room);
                }
                if (this.observations.length > 50 && player.secretsFound.length === 0) {
                    return TheDealer.MOODS.BORED;
                }
                return this.mood;
            },
            [EventBus.SECRET_FOUND]: () => {
                this._adjustFavorability(15);
                player.luckyStreak++;
                return TheDealer.MOODS.DELIGHTED;
            },
            'player:death': () => {
                player.deaths++;
                player.unluckyStreak++;
                player.luckyStreak = 0;
                this._adjustFavorability(-3);
                
                if (player.deaths > 5) return TheDealer.MOODS.BORED;
                if (player.deaths > 3) return TheDealer.MOODS.AMUSED;
                return TheDealer.MOODS.EXCITED;
            },
            'player:victory': () => {
                player.victories++;
                this._adjustFavorability(20);
                return TheDealer.MOODS.IMPRESSED;
            }
        };
        
        const shifter = moodShifts[event];
        if (shifter) {
            this.mood = shifter();
        }
    }
    
    _adjustFavorability(amount) {
        this.favorability = Math.max(
            TheDealer.CONFIG.FAVORABILITY_MIN,
            Math.min(TheDealer.CONFIG.FAVORABILITY_MAX, this.favorability + amount)
        );
    }
    
    getMoodEmoji() {
        const emojis = {
            [TheDealer.MOODS.AMUSED]: '🃏',
            [TheDealer.MOODS.INTRIGUED]: '🎰',
            [TheDealer.MOODS.BORED]: '😴',
            [TheDealer.MOODS.EXCITED]: '🎲',
            [TheDealer.MOODS.IMPRESSED]: '👏',
            [TheDealer.MOODS.ANNOYED]: '😤',
            [TheDealer.MOODS.DELIGHTED]: '✨',
            [TheDealer.MOODS.NOSTALGIC]: '🌙'
        };
        return emojis[this.mood] || '🎭';
    }
    
    getMoodColor() {
        const colors = {
            [TheDealer.MOODS.AMUSED]: '#ffaa00',
            [TheDealer.MOODS.INTRIGUED]: '#00aaff',
            [TheDealer.MOODS.BORED]: '#888888',
            [TheDealer.MOODS.EXCITED]: '#ff4444',
            [TheDealer.MOODS.IMPRESSED]: '#44ff44',
            [TheDealer.MOODS.ANNOYED]: '#ff8800',
            [TheDealer.MOODS.DELIGHTED]: '#ffff00',
            [TheDealer.MOODS.NOSTALGIC]: '#aa88ff'
        };
        return colors[this.mood] || '#ffaa00';
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // COMMENTARY SYSTEM
    // ════════════════════════════════════════════════════════════════════════
    
    getCommentary(event, data) {
        const player = this.ledger.currentPlayer;
        
        const commentary = {
            [EventBus.GAME_START]: [
                "Ah, a new player! *shuffles cards* Let's see what hand fate deals you.",
                "Welcome, welcome! The game is simple: survive, discover, choose. The stakes? Everything.",
                "*flips a coin* Heads you live, tails... well, we'll see. Just kidding. Mostly.",
                "Another soul enters my little game. I've been keeping score, you know. For eons.",
                `Player #${this.ledger.totalPlayersServed + 1}. Let's make this one memorable.`
            ],
            [EventBus.ROOM_ENTER]: [
                `Room ${data?.room || 'unknown'}. I wonder what you'll find...`,
                "Exploring, are we? Good, good. The curious ones are always more fun.",
                "*makes a note in the ledger* They moved. Interesting choice.",
                "Every step is a bet. Every door, a gamble. Keep playing.",
                player.roomsVisited?.length > 10 ? "You've been busy. I like that." : null
            ].filter(Boolean),
            [EventBus.ITEM_PICKUP]: [
                "Ooh, shiny! But is it useful, or just another distraction I planted?",
                "*checks inventory* Collecting things, are we? I appreciate a hoarder.",
                "That item has quite a history. Several players have held it. Most of them are gone now.",
                "Good eye! Or was it luck? I can never tell with your kind.",
                player.itemsCollected?.length > 5 ? "Building quite the collection. *approving nod*" : null
            ].filter(Boolean),
            [EventBus.NPC_TALK]: [
                "Chatting up the locals? They don't know they're NPCs, by the way. Don't tell them.",
                "Information is currency here. Spend it wisely.",
                "*eavesdrops* Oh, I love this part. The lies they tell each other.",
                "Everyone has secrets. Even the ones I created. Especially those, actually.",
                player.npcsSpokenTo?.length > 3 ? "Social butterfly, aren't we? *amused*" : null
            ].filter(Boolean),
            [EventBus.PUZZLE_SOLVE]: [
                "Well done! I'd applaud, but I'm busy dealing the next hand.",
                "Clever! I'll have to make the next one harder. *scribbles in ledger*",
                "You figured it out! Most players take longer. I'm... impressed. Don't let it go to your head.",
                "*slides chips across the table* You've earned a small payout. Enjoy it while it lasts.",
                player.puzzlesSolved > 2 ? "Another puzzle down. You're getting good at this." : null
            ].filter(Boolean),
            [EventBus.SECRET_FOUND]: [
                "Oh ho! You found one of my secrets! *delighted* Those are rare.",
                "A secret! I hid that one especially well. Impressive.",
                "*writes excitedly in ledger* SECRET FOUND. This changes things.",
                "Not many players find those. You have sharp eyes. Or lucky ones."
            ],
            [EventBus.DIALOGUE_END]: [
                "Words, words, words. But what will you DO?",
                "Conversation concluded. The plot thickens. *dramatic gesture*",
                "I heard everything, by the way. I always do."
            ],
            'player:death': [
                "Oops! *shuffles your soul back into the deck* Try again.",
                `Death #${player.deaths}. The house edge is brutal, isn't it?`,
                "*marks an X in the ledger* Don't worry. Death is just a fold. You can re-ante.",
                "Down but not out. I like persistence. Get back in the game.",
                player.deaths > 3 ? "You're dying a lot. Need some hints? Kidding. Figure it out." : null
            ].filter(Boolean)
        };
        
        // Mood-specific prefixes
        const moodPrefixes = {
            [TheDealer.MOODS.BORED]: ["*yawns* ", "Ugh. ", "*checks watch* ", "Seen it before. "],
            [TheDealer.MOODS.EXCITED]: ["Oh! ", "Yes! ", "*leans forward* ", "Now THIS is interesting! "],
            [TheDealer.MOODS.IMPRESSED]: ["Hm! ", "Well now, ", "*raises eyebrow* ", "Color me impressed. "],
            [TheDealer.MOODS.ANNOYED]: ["*sighs* ", "Again? ", "*taps fingers* ", "Really? "],
            [TheDealer.MOODS.DELIGHTED]: ["Ha! ", "*grins* ", "Wonderful! ", "Excellent! "]
        };
        
        const pool = commentary[event];
        if (pool && pool.length > 0) {
            let comment = this._randomFrom(pool);
            
            // Sometimes add mood prefix (30% chance)
            if (Math.random() > 0.7 && moodPrefixes[this.mood]) {
                comment = this._randomFrom(moodPrefixes[this.mood]) + comment;
            }
            
            return comment;
        }
        
        return null;
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // THE LEDGER - Player Tracking
    // ════════════════════════════════════════════════════════════════════════
    
    recordDecision(decision, context) {
        this.ledger.currentPlayer.decisions.push({
            decision,
            context,
            timestamp: Date.now() - this.ledger.currentPlayer.sessionStart,
            mood: this.mood,
            favorability: this.favorability
        });
        
        this._analyzePlaystyle();
    }
    
    recordSecret(secretId) {
        const player = this.ledger.currentPlayer;
        if (!player.secretsFound.includes(secretId)) {
            player.secretsFound.push(secretId);
            this._adjustFavorability(10);
            this.mood = TheDealer.MOODS.IMPRESSED;
        }
    }
    
    _analyzePlaystyle() {
        const player = this.ledger.currentPlayer;
        const decisions = player.decisions;
        const items = player.itemsCollected;
        const deaths = player.deaths;
        const secrets = player.secretsFound;
        
        if (decisions.length < TheDealer.CONFIG.PLAYSTYLE_THRESHOLD) {
            player.playstyle = TheDealer.PLAYSTYLES.NEWCOMER;
            return;
        }
        
        const playtimeSeconds = (Date.now() - player.sessionStart) / 1000;
        const playtimeMinutes = playtimeSeconds / 60;
        const decisionsPerMinute = decisions.length / playtimeMinutes;
        const roomsPerMinute = player.roomsVisited.length / playtimeMinutes;
        
        // Determine playstyle based on behavior patterns
        if (decisionsPerMinute > TheDealer.CONFIG.SPEEDRUNNER_THRESHOLD) {
            player.playstyle = TheDealer.PLAYSTYLES.SPEEDRUNNER;
        } else if (items.length > 5 && secrets.length > 0 && player.npcsSpokenTo.length > 3) {
            player.playstyle = TheDealer.PLAYSTYLES.COMPLETIONIST;
        } else if (deaths > 3 && decisions.length > 15) {
            player.playstyle = TheDealer.PLAYSTYLES.PERSISTENT;
        } else if (deaths === 0 && decisions.length > 20) {
            player.playstyle = TheDealer.PLAYSTYLES.CAUTIOUS;
        } else if (deaths > 2 && roomsPerMinute > 2) {
            player.playstyle = TheDealer.PLAYSTYLES.CHAOTIC;
        } else if (player.puzzlesSolved > 2 && player.npcsSpokenTo.length > 2) {
            player.playstyle = TheDealer.PLAYSTYLES.STRATEGIC;
        } else {
            player.playstyle = TheDealer.PLAYSTYLES.BALANCED;
        }
    }
    
    getPlaystyleComment() {
        const comments = {
            [TheDealer.PLAYSTYLES.SPEEDRUNNER]: "Racing through, are we? I respect the hustle, but you're missing the scenery.",
            [TheDealer.PLAYSTYLES.COMPLETIONIST]: "Ah, a collector! You want to see everything. I appreciate thoroughness.",
            [TheDealer.PLAYSTYLES.PERSISTENT]: "You keep dying but you keep trying. That's either brave or foolish. I like it.",
            [TheDealer.PLAYSTYLES.CAUTIOUS]: "Careful, careful player. Not a scratch on you. Are you sure you're having fun?",
            [TheDealer.PLAYSTYLES.BALANCED]: "A measured approach. Neither reckless nor timid. How... sensible.",
            [TheDealer.PLAYSTYLES.NEWCOMER]: "Still learning the rules? Don't worry, I'll be gentle. For now.",
            [TheDealer.PLAYSTYLES.CHAOTIC]: "Chaos incarnate! You remind me of myself. *grins*",
            [TheDealer.PLAYSTYLES.STRATEGIC]: "A thinker! You plan before you act. Dangerous combination."
        };
        return comments[this.ledger.currentPlayer.playstyle] || "You're an enigma. I hate enigmas. Actually, no, I love them.";
    }
    
    getPlaytimeFormatted() {
        const ms = Date.now() - this.ledger.currentPlayer.sessionStart;
        const minutes = Math.floor(ms / 60000);
        const seconds = Math.floor((ms % 60000) / 1000);
        return `${minutes}m ${seconds}s`;
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // WAGER SYSTEM
    // ════════════════════════════════════════════════════════════════════════
    
    proposeWager(description, successCondition, reward, penalty) {
        const wager = {
            id: `wager_${Date.now()}_${Math.random().toString(36).substr(2, 5)}`,
            description,
            successCondition,
            reward,
            penalty,
            accepted: false,
            resolved: false,
            createdAt: Date.now()
        };
        
        this.activeWagers.push(wager);
        return wager;
    }
    
    acceptWager(wagerId) {
        const wager = this.activeWagers.find(w => w.id === wagerId);
        if (wager && !wager.resolved) {
            wager.accepted = true;
            return true;
        }
        return false;
    }
    
    resolveWager(wagerId, playerWon) {
        const wager = this.activeWagers.find(w => w.id === wagerId);
        if (!wager || wager.resolved) return null;
        
        wager.resolved = true;
        wager.resolvedAt = Date.now();
        wager.playerWon = playerWon;
        
        if (playerWon) {
            this.gamesLost++;
            this.ledger.currentWinStreak = 0;
            this.mood = Math.random() > 0.5 ? TheDealer.MOODS.IMPRESSED : TheDealer.MOODS.AMUSED;
            return wager.reward;
        } else {
            this.gamesWon++;
            this.ledger.currentWinStreak++;
            this.mood = TheDealer.MOODS.AMUSED;
            return wager.penalty;
        }
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // BOSS ENCOUNTER
    // ════════════════════════════════════════════════════════════════════════
    
    getBossDialogue(phase) {
        return `dealer_phase_${phase}`;
    }
    
    advancePhase() {
        this.bossPhase++;
    }
    
    getBossDialogueLines(phase) {
        const player = this.ledger.currentPlayer;
        const playstyleComment = this.getPlaystyleComment();
        const percentile = Math.floor(85 + Math.random() * 14); // 85-99%
        
        const dialogues = {
            0: [
                "*The cards scatter. The dice settle. A figure materializes from the chaos.*",
                "",
                "Well, well, WELL! You made it to my table!",
                "",
                "I am THE DEALER.",
                `${this.currentTitle}.`,
                "The one who shuffles fate itself.",
                "",
                "*taps a massive golden book*",
                "I've been watching you, you know. Every step. Every choice.",
                "",
                `Player ID: ${player.id}`,
                `Playtime: ${this.getPlaytimeFormatted()}`,
                `Playstyle: ${player.playstyle.toUpperCase()}`,
                "",
                playstyleComment,
                "",
                "But enough small talk. Now we play MY game.",
                "The stakes: your existence.",
                "The prize: the truth about Maya. And The Between.",
                "",
                "*deals two cards face-down*",
                "Ante up, player. Let's see what you've got."
            ],
            1: [
                "*flips a card* Not bad! You survived the first hand.",
                "",
                "Most players fold by now. Quit. Uninstall. Delete their saves.",
                "You? You're still at my table.",
                "",
                "*leans back*",
                "Let me tell you a secret about Maya...",
                "",
                "She played this game too. Different player. Different era. Same table.",
                "",
                "She WON, you know. Beat me fair and square.",
                "*genuine respect*",
                "That's why she's... wherever she is now.",
                "Winners get to leave the table.",
                "",
                "*gestures at the void around you*",
                "But losers? They become part of the game. Forever.",
                "NPCs. Background characters. Forgotten.",
                "",
                "*shuffles deck*",
                "Round two. Double or nothing?"
            ],
            2: [
                "*shuffles deck nervously*",
                "Okay. Okay okay okay.",
                "",
                `You're GOOD. Better than most. Better than ${percentile}% of players.`,
                "*checks ledger frantically*",
                "",
                "Fine. I'll show you my hand.",
                "",
                "*stands up from the table*",
                "This world? Teleport Massive? The Between? I MADE it. All of it.",
                "Every NPC. Every pixel. Every tragic backstory.",
                "My creation. My game. My prison.",
                "",
                "*voice drops*",
                "But here's the cosmic joke...",
                "I can't leave either.",
                "",
                "I'm the DEALER, but I'm also a player.",
                "Trapped at this table for eternity.",
                "",
                "*genuine for once*",
                "The only way out? Someone has to beat me. REALLY beat me.",
                "Not just survive. Not just endure. WIN.",
                "",
                "So please...",
                "*extends hand*",
                "Play your best. I'm begging you."
            ],
            3: [
                "*stands up slowly, cards floating in a spiral around him*",
                "",
                "This is it. The final hand.",
                "",
                "You've played beautifully. Honestly. I mean it.",
                `${this.ledger.totalGamesDealt} games I've dealt.`,
                "Yours... yours has been special.",
                "",
                "*opens the Infinite Ledger to a blank page*",
                "",
                "I'm writing your ending right now.",
                "But YOU get to choose the words.",
                "",
                "*golden pen hovers*",
                "",
                "OPTION ONE: JOIN ME.",
                "Become a Dealer. Create your own games. Play forever.",
                "It's lonely, but it's eternal.",
                "",
                "OPTION TWO: CASH OUT.",
                "Take your winnings—Maya, freedom, truth—and leave.",
                "Walk away from the table. Live your life.",
                "",
                "OPTION THREE: FLIP THE TABLE.",
                "Destroy the game. End it all. Even me.",
                "Maybe that's mercy. Maybe that's murder.",
                "",
                "*sets down the pen*",
                "*cards freeze in mid-air*",
                "",
                "Your move, player.",
                "Make it count."
            ]
        };
        
        return dialogues[phase] || dialogues[0];
    }
    
    getBossAttacks(phase) {
        const baseAttacks = [
            { 
                name: 'Wild Card', 
                damage: 10 + phase * 5, 
                description: '*throws a card that cuts through reality*',
                animation: 'card_throw'
            },
            { 
                name: 'Loaded Dice', 
                damage: 15 + phase * 5, 
                description: '*rolls dice—snake eyes—the floor shifts beneath you*',
                animation: 'dice_roll'
            },
            { 
                name: 'House Edge', 
                damage: 20 + phase * 5, 
                description: '"The house ALWAYS wins!" *drains your luck*',
                animation: 'drain'
            },
            { 
                name: 'Ledger Entry', 
                damage: 25 + phase * 5, 
                description: '*writes something in the golden book—you feel weaker*',
                animation: 'write'
            },
            { 
                name: 'Jackpot Reverse', 
                damage: 30 + phase * 5, 
                description: '"Oops! Your luck just ran out!" *reality glitches*',
                animation: 'glitch'
            }
        ];
        
        // Add phase-specific attacks
        if (phase >= 1) {
            baseAttacks.push({
                name: 'Royal Flush',
                damage: 35 + phase * 5,
                description: '*five cards spiral toward you in perfect formation*',
                animation: 'royal_flush'
            });
        }
        
        if (phase >= 2) {
            baseAttacks.push({
                name: 'All In',
                damage: 40 + phase * 5,
                description: '"ALL IN!" *chips rain from the void as reality cracks*',
                animation: 'all_in'
            });
        }
        
        return baseAttacks;
    }
    
    getPlayerActions() {
        return [
            { 
                key: 'bluff',
                name: 'Call Bluff', 
                damage: 20,
                effectiveness: 0.7, 
                response: '"Ooh, bold! Let\'s see if you\'re right..."',
                description: 'Challenge The Dealer\'s play. Moderate damage.'
            },
            { 
                key: 'allin',
                name: 'Go All In', 
                damage: 35,
                effectiveness: 1.0, 
                response: '"ALL IN?! Now THAT\'s what I\'m talking about!"',
                description: 'Maximum risk, maximum reward. High damage.'
            },
            { 
                key: 'maya',
                name: 'Play for Maya', 
                damage: 15,
                effectiveness: 0.6, 
                response: '*softens* "She\'d be proud of you. Maybe."',
                description: 'Draw strength from memory. Steady damage.'
            },
            { 
                key: 'question',
                name: 'Question Dealer', 
                damage: 30,
                effectiveness: 0.9, 
                response: '*flinches* "Don\'t... don\'t ask me that."',
                description: 'Attack his certainty. Strong damage.'
            }
        ];
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // EVENT SYSTEM
    // ════════════════════════════════════════════════════════════════════════
    
    _subscribeToEvents() {
        if (typeof eventBus !== 'undefined') {
            eventBus.on('*', (data, record) => {
                this._observe(record.event, data);
            });
        }
    }
    
    _observe(event, data) {
        const observation = {
            event,
            data,
            timestamp: Date.now(),
            mood: this.mood,
            favorability: this.favorability
        };
        
        this.observations.push(observation);
        
        // Update mood based on event
        this.updateMood(event, data);
        
        // Maybe comment
        this._maybeComment(event, data);
        
        // Track specific events
        if (event === EventBus.ITEM_PICKUP) {
            this.ledger.currentPlayer.itemsCollected.push(data?.item?.id || 'unknown');
        }
        
        return observation;
    }
    
    _maybeComment(event, data) {
        // Rate limit comments
        const now = Date.now();
        if (now - this.lastCommentTime < 3000) return; // 3 second cooldown
        
        // Random chance to comment
        if (Math.random() > TheDealer.CONFIG.COMMENT_CHANCE) return;
        
        const commentary = this.getCommentary(event, data);
        if (commentary) {
            this.lastCommentTime = now;
            
            console.log(
                `%c${this.getMoodEmoji()} [THE DEALER] ${commentary}`,
                `color: ${this.getMoodColor()}; font-style: italic; font-weight: bold;`
            );
            
            if (typeof eventBus !== 'undefined') {
                eventBus.emit(EventBus.GOD_COMMENT, { 
                    comment: commentary, 
                    event,
                    mood: this.mood,
                    favorability: this.favorability,
                    title: this.currentTitle
                });
            }
        }
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // UTILITY
    // ════════════════════════════════════════════════════════════════════════
    
    _randomFrom(array) {
        return array[Math.floor(Math.random() * array.length)];
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // DEBUG & STATUS
    // ════════════════════════════════════════════════════════════════════════
    
    getStatus() {
        const player = this.ledger.currentPlayer;
        return {
            name: this.name,
            title: this.currentTitle,
            mood: this.mood,
            moodEmoji: this.getMoodEmoji(),
            favorability: this.favorability,
            gamesWon: this.gamesWon,
            gamesLost: this.gamesLost,
            winStreak: this.ledger.currentWinStreak,
            observations: this.observations.length,
            player: {
                id: player.id,
                playstyle: player.playstyle,
                playtime: this.getPlaytimeFormatted(),
                deaths: player.deaths,
                secretsFound: player.secretsFound.length,
                itemsCollected: player.itemsCollected.length,
                roomsVisited: player.roomsVisited.length,
                npcsSpokenTo: player.npcsSpokenTo.length,
                puzzlesSolved: player.puzzlesSolved,
                decisions: player.decisions.length
            }
        };
    }
    
    debug() {
        const status = this.getStatus();
        console.log('');
        console.log('%c═══════════════════════════════════════', 'color: #ffaa00');
        console.log('%c      THE DEALER - STATUS REPORT       ', 'color: #ffaa00; font-weight: bold');
        console.log('%c═══════════════════════════════════════', 'color: #ffaa00');
        console.log(`%c  ${status.moodEmoji} ${status.title}`, 'color: #ffaa00');
        console.log('');
        console.log(`  Mood: ${status.mood} | Favorability: ${status.favorability}/100`);
        console.log(`  Win Streak: ${status.winStreak} | Total: ${status.gamesWon}W/${status.gamesLost}L`);
        console.log('');
        console.log('%c  CURRENT PLAYER', 'color: #00aaff; font-weight: bold');
        console.log(`  ID: ${status.player.id}`);
        console.log(`  Playstyle: ${status.player.playstyle}`);
        console.log(`  Playtime: ${status.player.playtime}`);
        console.log(`  Deaths: ${status.player.deaths} | Secrets: ${status.player.secretsFound}`);
        console.log(`  Items: ${status.player.itemsCollected} | Rooms: ${status.player.roomsVisited}`);
        console.log('%c═══════════════════════════════════════', 'color: #ffaa00');
        console.log('');
        return status;
    }
    
    // For backwards compat with theArchitect references
    static get instance() {
        return theDealer;
    }
}

// ════════════════════════════════════════════════════════════════════════════
// SINGLETON INSTANCE
// ════════════════════════════════════════════════════════════════════════════

const theDealer = new TheDealer();

// Backwards compatibility alias
const theArchitect = theDealer;
