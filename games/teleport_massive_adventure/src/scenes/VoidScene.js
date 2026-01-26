/**
 * VoidScene - The Final Confrontation
 * ═══════════════════════════════════════════════════════════════════════════
 * 
 * Boss encounter with THE DEALER at his Infinite Table.
 * Multi-phase card game battle with three possible endings.
 * 
 * Visual Theme: Cosmic Casino
 * - Deep green void (casino felt)
 * - Floating cards, dice, and gold sparkles
 * - The Infinite Table and Ledger
 * - Gold and green color palette
 * 
 * ═══════════════════════════════════════════════════════════════════════════
 */
class VoidScene extends BaseScene {
    
    // ════════════════════════════════════════════════════════════════════════
    // CONFIGURATION
    // ════════════════════════════════════════════════════════════════════════
    
    static CONFIG = {
        COLORS: {
            FELT_DARK: 0x051005,
            FELT_LIGHT: 0x0a4a0a,
            GOLD: 0xffaa00,
            GOLD_DARK: 0xdaa520,
            PLAYER_HP: 0x00ff88,
            DANGER: 0xff4444,
            BUTTON_BG: 0x1a3a1a,
            BUTTON_HOVER: 0x2a5a2a,
            BUTTON_BORDER: 0xffaa00
        },
        BOSS: {
            MAX_HP: 100,
            PHASES: 3
        },
        PLAYER: {
            MAX_HP: 100,
            HEAL_BETWEEN_PHASES: 30
        }
    };
    
    // ════════════════════════════════════════════════════════════════════════
    // LIFECYCLE
    // ════════════════════════════════════════════════════════════════════════
    
    constructor() {
        super('VoidScene');
        this.roomId = 'void';
        this.bossPhase = 0;
        this.playerHP = VoidScene.CONFIG.PLAYER.MAX_HP;
        this.bossHP = VoidScene.CONFIG.BOSS.MAX_HP;
        this.isPlayerTurn = false;
        this.combatActive = false;
    }
    
    create() {
        // Don't call super.create() - custom setup for boss room
        // BUT we need to setup UI and update title
        this.setupUI();
        
        // Load room data for title
        if (this.roomId && window.roomsData?.rooms?.[this.roomId]) {
            this.roomData = window.roomsData.rooms[this.roomId];
            this.updateRoomTitle(this.roomData.name);
        } else {
            this.updateRoomTitle('THE DEALER\'S TABLE');
        }
        
        this.cameras.main.fadeIn(1000, 0, 0, 0);
        
        // Create environment
        this._createVoidBackground();
        this._createTable();
        this._createDealer();
        this._createAmbientEffects();
        
        // Create player
        this.player = new PlayerController(this);
        this.player.create(400, 420, 'aziah_north');
        this.player.setWalkableArea({ x: 100, y: 350, width: 600, height: 130 });
        this.player.setupKeyboardInput();
        
        // Setup UI
        this._createBossUI();
        this._createActionButtons();
        
        // Setup dialogue
        dialogueSystem.init({
            box: document.getElementById('dialogue-box'),
            speaker: document.getElementById('speaker-name'),
            text: document.getElementById('dialogue-text')
        });
        
        // Start boss encounter after dramatic pause
        this.time.delayedCall(1500, () => this._startBossEncounter());
        
        // Emit event
        eventBus.emit(EventBus.COMBAT_START, { boss: 'dealer', room: 'void' });
        
        // Update game state
        gameState.enterRoom(this.roomId);
    }
    
    update(time, delta) {
        if (this.player) {
            this.player.update(delta);
        }
        
        // Animate floating cards
        this._animateFloatingCards(time);
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // ENVIRONMENT CREATION
    // ════════════════════════════════════════════════════════════════════════
    
    _createVoidBackground() {
        const { FELT_DARK, FELT_LIGHT } = VoidScene.CONFIG.COLORS;
        const graphics = this.add.graphics();
        
        // Deep casino gradient
        for (let y = 0; y < 500; y += 2) {
            const intensity = Math.sin(y * 0.008) * 0.15;
            const r = Math.floor(5 + intensity * 10);
            const g = Math.floor(15 + intensity * 30);
            const b = Math.floor(10 + intensity * 20);
            
            graphics.fillStyle(Phaser.Display.Color.GetColor(r, g, b), 1);
            graphics.fillRect(0, y, 800, 2);
        }
    }
    
    _createTable() {
        const { FELT_LIGHT, GOLD_DARK } = VoidScene.CONFIG.COLORS;
        
        // The Infinite Table
        const table = this.add.graphics();
        
        // Main felt surface
        table.fillStyle(FELT_LIGHT, 1);
        table.fillEllipse(400, 200, 300, 130);
        
        // Gold trim (outer)
        table.lineStyle(5, GOLD_DARK, 1);
        table.strokeEllipse(400, 200, 300, 130);
        
        // Inner decorative ring
        table.lineStyle(1, 0x0a6a0a, 0.6);
        table.strokeEllipse(400, 200, 260, 110);
        
        // Betting spots (decorative)
        const spots = [
            { x: 320, y: 230 },
            { x: 400, y: 240 },
            { x: 480, y: 230 }
        ];
        
        spots.forEach(spot => {
            table.lineStyle(2, GOLD_DARK, 0.4);
            table.strokeCircle(spot.x, spot.y, 25);
        });
        
        // Chip stacks on table
        this._createChipStacks();
    }
    
    _createChipStacks() {
        const chipPositions = [
            { x: 280, y: 210, colors: [0xff4444, 0xff4444, 0xffaa00] },
            { x: 520, y: 210, colors: [0x4444ff, 0x44ff44, 0xffffff] }
        ];
        
        chipPositions.forEach(stack => {
            stack.colors.forEach((color, i) => {
                const chip = this.add.circle(stack.x, stack.y - i * 4, 12, color, 1);
                chip.setStrokeStyle(1, 0x000000, 0.5);
            });
        });
    }
    
    _createDealer() {
        const { GOLD } = VoidScene.CONFIG.COLORS;
        
        // The Dealer sprite
        this.dealer = this.add.sprite(400, 160, 'architect_south');
        this.dealer.setScale(2.5);
        this.dealer.setTint(GOLD);
        
        // Divine glow
        this.dealerGlow = this.add.circle(400, 160, 85, GOLD, 0.12);
        this.tweens.add({
            targets: this.dealerGlow,
            scale: 1.2,
            alpha: 0.06,
            duration: 2000,
            yoyo: true,
            repeat: -1,
            ease: 'Sine.easeInOut'
        });
        
        // The Infinite Ledger (floating book)
        this.ledger = this.add.text(485, 95, '📖', { fontSize: '36px' });
        this.tweens.add({
            targets: this.ledger,
            y: 85,
            duration: 2500,
            yoyo: true,
            repeat: -1,
            ease: 'Sine.easeInOut'
        });
        
        // Dealer's title
        this.dealerTitle = this.add.text(400, 80, theDealer.currentTitle, {
            fontSize: '9px',
            color: '#ffaa00',
            fontStyle: 'italic'
        }).setOrigin(0.5).setAlpha(0.7);
        
        // Backwards compat
        this.architect = this.dealer;
    }
    
    _createAmbientEffects() {
        // Floating card symbols
        this.ambientCards = [];
        const cardSymbols = ['♠', '♥', '♦', '♣', '🎲', '🃏'];
        const colors = ['#ff4444', '#ffffff', '#ffaa00', '#44ff44', '#ff4444', '#ffaa00'];
        
        for (let i = 0; i < 25; i++) {
            const symbolIdx = Phaser.Math.Between(0, cardSymbols.length - 1);
            const particle = this.add.text(
                Phaser.Math.Between(0, 800),
                Phaser.Math.Between(0, 500),
                cardSymbols[symbolIdx],
                { 
                    fontSize: Phaser.Math.Between(12, 22) + 'px', 
                    color: colors[symbolIdx]
                }
            ).setAlpha(0.25);
            
            this.tweens.add({
                targets: particle,
                y: particle.y - Phaser.Math.Between(150, 350),
                x: particle.x + Phaser.Math.Between(-60, 60),
                rotation: Phaser.Math.Between(-3, 3),
                alpha: 0,
                duration: Phaser.Math.Between(5000, 10000),
                repeat: -1,
                onRepeat: () => {
                    particle.y = 550;
                    particle.x = Phaser.Math.Between(0, 800);
                    particle.alpha = 0.25;
                }
            });
            
            this.ambientCards.push(particle);
        }
        
        // Gold sparkles
        for (let i = 0; i < 12; i++) {
            const sparkle = this.add.circle(
                Phaser.Math.Between(0, 800),
                Phaser.Math.Between(0, 280),
                Phaser.Math.Between(2, 4),
                0xffaa00,
                0.6
            );
            
            this.tweens.add({
                targets: sparkle,
                alpha: 0,
                scale: 2.5,
                duration: Phaser.Math.Between(1500, 3500),
                repeat: -1,
                onRepeat: () => {
                    sparkle.x = Phaser.Math.Between(0, 800);
                    sparkle.y = Phaser.Math.Between(0, 280);
                    sparkle.alpha = 0.6;
                    sparkle.scale = 1;
                }
            });
        }
        
        // Floating cards around dealer
        this.floatingCards = [];
        const orbitalSymbols = ['♠', '♥', '♦', '♣', '🃏', '♠', '♥', '♦'];
        
        for (let i = 0; i < 8; i++) {
            const angle = (i / 8) * Math.PI * 2;
            const card = this.add.text(
                400 + Math.cos(angle) * 95,
                160 + Math.sin(angle) * 50,
                orbitalSymbols[i],
                { fontSize: '22px', color: '#ffffff' }
            ).setOrigin(0.5);
            
            this.floatingCards.push({ card, baseAngle: angle });
        }
    }
    
    _animateFloatingCards(time) {
        if (!this.floatingCards) return;
        
        const t = time * 0.0005;
        this.floatingCards.forEach(({ card, baseAngle }, i) => {
            const angle = baseAngle + t;
            const radius = 95 + Math.sin(t * 2 + i) * 8;
            card.x = 400 + Math.cos(angle) * radius;
            card.y = 160 + Math.sin(angle) * (radius * 0.55);
            card.rotation = Math.sin(t + i) * 0.15;
            card.setAlpha(0.7 + Math.sin(t * 3 + i) * 0.3);
        });
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // UI CREATION
    // ════════════════════════════════════════════════════════════════════════
    
    _createBossUI() {
        const { GOLD, PLAYER_HP } = VoidScene.CONFIG.COLORS;
        
        // Boss HP bar background
        this.add.rectangle(400, 28, 320, 24, 0x000000, 0.85)
            .setStrokeStyle(2, GOLD, 0.5);
        
        // Boss HP bar fill
        this.bossHPBar = this.add.rectangle(400, 28, 310, 18, GOLD, 1);
        
        // Boss name
        this.add.text(400, 28, '🃏 THE DEALER 🃏', {
            fontSize: '11px',
            color: '#ffffff',
            fontFamily: 'monospace'
        }).setOrigin(0.5);
        
        // Phase indicator
        this.phaseText = this.add.text(400, 50, 'PHASE 1 / 3', {
            fontSize: '9px',
            color: '#ffaa00',
            fontFamily: 'monospace'
        }).setOrigin(0.5).setAlpha(0.8);
        
        // Player HP bar background
        this.add.rectangle(400, 455, 220, 18, 0x000000, 0.85)
            .setStrokeStyle(1, PLAYER_HP, 0.5);
        
        // Player HP bar fill
        this.playerHPBar = this.add.rectangle(400, 455, 214, 14, PLAYER_HP, 1);
        
        // Player name
        this.add.text(400, 455, 'AZIAH', {
            fontSize: '10px',
            color: '#ffffff',
            fontFamily: 'monospace'
        }).setOrigin(0.5);
        
        // Turn indicator
        this.turnIndicator = this.add.text(400, 435, '', {
            fontSize: '10px',
            color: '#ffaa00',
            fontFamily: 'monospace'
        }).setOrigin(0.5);
    }
    
    _createActionButtons() {
        const { BUTTON_BG, BUTTON_HOVER, BUTTON_BORDER } = VoidScene.CONFIG.COLORS;
        const actions = theDealer.getPlayerActions();
        
        this.actionButtons = [];
        const startX = 115;
        const spacing = 145;
        
        actions.forEach((action, i) => {
            // Button background
            const btn = this.add.rectangle(
                startX + i * spacing,
                490,
                135, 32,
                BUTTON_BG, 0.95
            ).setInteractive({ useHandCursor: true });
            
            btn.setStrokeStyle(2, BUTTON_BORDER);
            btn.setVisible(false);
            
            // Button text
            const text = this.add.text(
                startX + i * spacing,
                490,
                action.name,
                { 
                    fontSize: '11px', 
                    color: '#ffaa00',
                    fontFamily: 'monospace',
                    fontStyle: 'bold'
                }
            ).setOrigin(0.5).setVisible(false);
            
            // Damage indicator
            const dmg = this.add.text(
                startX + i * spacing,
                502,
                `DMG: ${action.damage}`,
                { 
                    fontSize: '8px', 
                    color: '#888888',
                    fontFamily: 'monospace'
                }
            ).setOrigin(0.5).setVisible(false);
            
            // Hover effects
            btn.on('pointerover', () => {
                btn.setFillStyle(BUTTON_HOVER);
                btn.setScale(1.05);
                text.setColor('#ffffff');
            });
            
            btn.on('pointerout', () => {
                btn.setFillStyle(BUTTON_BG);
                btn.setScale(1);
                text.setColor('#ffaa00');
            });
            
            btn.on('pointerdown', () => this._playerAction(action));
            
            this.actionButtons.push({ btn, text, dmg, action });
        });
    }
    
    _showActionButtons() {
        this.isPlayerTurn = true;
        this.turnIndicator.setText('YOUR TURN - Choose your move');
        
        this.actionButtons.forEach(({ btn, text, dmg }, i) => {
            // Stagger animation
            this.time.delayedCall(i * 80, () => {
                btn.setVisible(true).setAlpha(0).setScale(0.8);
                text.setVisible(true).setAlpha(0);
                dmg.setVisible(true).setAlpha(0);
                
                this.tweens.add({
                    targets: [btn, text, dmg],
                    alpha: 1,
                    duration: 200
                });
                
                this.tweens.add({
                    targets: btn,
                    scale: 1,
                    duration: 200,
                    ease: 'Back.easeOut'
                });
            });
        });
    }
    
    _hideActionButtons() {
        this.isPlayerTurn = false;
        this.turnIndicator.setText('');
        
        this.actionButtons.forEach(({ btn, text, dmg }) => {
            btn.setVisible(false);
            text.setVisible(false);
            dmg.setVisible(false);
        });
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // BOSS ENCOUNTER FLOW
    // ════════════════════════════════════════════════════════════════════════
    
    _startBossEncounter() {
        this.combatActive = true;
        dialogueSystem.show(theDealer.getBossDialogue(0), () => {
            this._beginPhase(0);
        });
    }
    
    _beginPhase(phase) {
        this.bossPhase = phase;
        this.bossHP = VoidScene.CONFIG.BOSS.MAX_HP;
        this._updateBossHP();
        this._updatePhaseIndicator();
        
        // Show action buttons
        this._showActionButtons();
        
        // Boss takes first action after delay
        this.time.delayedCall(2000, () => this._bossAction());
    }
    
    _updatePhaseIndicator() {
        this.phaseText.setText(`PHASE ${this.bossPhase + 1} / ${VoidScene.CONFIG.BOSS.PHASES}`);
        
        // Flash effect
        this.tweens.add({
            targets: this.phaseText,
            alpha: 0.2,
            duration: 200,
            yoyo: true,
            repeat: 2
        });
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // COMBAT ACTIONS
    // ════════════════════════════════════════════════════════════════════════
    
    _playerAction(action) {
        if (dialogueSystem.isActive || !this.isPlayerTurn) return;
        
        this._hideActionButtons();
        
        // Record the decision
        theDealer.recordDecision(action.key, { phase: this.bossPhase, bossHP: this.bossHP });
        
        // Show action text with dealer's response
        const lines = [
            action.description || `You use ${action.name}!`,
            action.response
        ];
        
        dialogueSystem.showLines('AZIAH', [lines[0]], () => {
            // Deal damage to boss
            this._damageBoss(action.damage);
            
            // Show dealer's reaction
            this.time.delayedCall(800, () => {
                dialogueSystem.showSingle('THE DEALER', action.response);
            });
        });
    }
    
    // Public method for AutoPlayer
    playerAction(actionKey) {
        if (!this.combatActive || !this.isPlayerTurn) {
            console.warn(`[VoidScene] Cannot execute action ${actionKey} - not player turn or combat inactive`);
            return;
        }
        
        // Find action by key
        const actions = theDealer.getPlayerActions();
        const action = actions.find(a => a.key === actionKey);
        
        if (action) {
            this._playerAction(action);
        } else {
            console.warn(`[VoidScene] Action not found: ${actionKey}`);
        }
    }
    
    _bossAction() {
        if (this.bossHP <= 0 || !this.combatActive) return;
        
        this.turnIndicator.setText("THE DEALER'S TURN");
        
        const attacks = theDealer.getBossAttacks(this.bossPhase);
        const attack = attacks[Phaser.Math.Between(0, attacks.length - 1)];
        
        // Visual effects
        this._bossAttackEffect(attack);
        
        // Show attack
        dialogueSystem.showLines('THE DEALER', [attack.description], () => {
            this._damagePlayer(attack.damage);
            
            // Player's turn
            this.time.delayedCall(1200, () => {
                if (this.playerHP > 0 && this.combatActive) {
                    this._showActionButtons();
                }
            });
        });
    }
    
    _bossAttackEffect(attack) {
        // Screen shake
        this.cameras.main.shake(350, 0.012);
        
        // Dealer glow pulse
        this.tweens.add({
            targets: this.dealerGlow,
            scale: 1.8,
            alpha: 0.4,
            duration: 200,
            yoyo: true
        });
        
        // Card burst effect
        if (attack.animation === 'card_throw' || attack.animation === 'royal_flush') {
            this._createCardBurst();
        }
    }
    
    _createCardBurst() {
        for (let i = 0; i < 5; i++) {
            const symbols = ['♠', '♥', '♦', '♣'];
            const card = this.add.text(
                400,
                160,
                symbols[i % 4],
                { fontSize: '28px', color: '#ffffff' }
            ).setOrigin(0.5);
            
            const angle = (i / 5) * Math.PI * 2 - Math.PI / 2;
            
            this.tweens.add({
                targets: card,
                x: 400 + Math.cos(angle) * 200,
                y: 400,
                alpha: 0,
                rotation: Phaser.Math.Between(-4, 4),
                scale: 0.5,
                duration: 600,
                ease: 'Power2',
                onComplete: () => card.destroy()
            });
        }
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // DAMAGE & HP
    // ════════════════════════════════════════════════════════════════════════
    
    _damageBoss(amount) {
        this.bossHP = Math.max(0, this.bossHP - amount);
        this._updateBossHP();
        
        // Flash effect on dealer
        this.dealer.setTint(0xff0000);
        this.time.delayedCall(200, () => this.dealer.setTint(VoidScene.CONFIG.COLORS.GOLD));
        
        // Damage number popup
        this._showDamageNumber(400, 160, amount, '#ff4444');
        
        // Check phase transition
        if (this.bossHP <= 0) {
            this._endPhase();
        } else {
            // Boss retaliates
            this.time.delayedCall(1500, () => this._bossAction());
        }
    }
    
    _damagePlayer(amount) {
        this.playerHP = Math.max(0, this.playerHP - amount);
        this._updatePlayerHP();
        
        // Screen flash
        this.cameras.main.flash(250, 255, 50, 50);
        
        // Damage number popup
        this._showDamageNumber(400, 420, amount, '#ff4444');
        
        if (this.playerHP <= 0) {
            this._playerDefeated();
        }
    }
    
    _showDamageNumber(x, y, amount, color) {
        // Use centralized visual effects utility
        const VisualEffects = window.VisualEffects || (typeof VisualEffects !== 'undefined' ? VisualEffects : null);
        if (VisualEffects) {
            VisualEffects.floatingNumber(this, x, y, amount, 'damage', { color });
        } else {
            // Fallback for compatibility
            const dmgText = this.add.text(x, y, `-${amount}`, {
                fontSize: '24px',
                color: color,
                fontFamily: 'monospace',
                fontStyle: 'bold',
                stroke: '#000000',
                strokeThickness: 3
            }).setOrigin(0.5);
            
            this.tweens.add({
                targets: dmgText,
                y: y - 50,
                alpha: 0,
                scale: 1.5,
                duration: 800,
                ease: 'Power2',
                onComplete: () => dmgText.destroy()
            });
        }
    }
    
    _updateBossHP() {
        const width = (this.bossHP / VoidScene.CONFIG.BOSS.MAX_HP) * 310;
        this.tweens.add({
            targets: this.bossHPBar,
            displayWidth: Math.max(0, width),
            duration: 300,
            ease: 'Power2'
        });
        
        // Color shift at low HP
        if (this.bossHP < 30) {
            this.bossHPBar.setFillStyle(0xff6600);
        }
    }
    
    _updatePlayerHP() {
        const width = (this.playerHP / VoidScene.CONFIG.PLAYER.MAX_HP) * 214;
        this.tweens.add({
            targets: this.playerHPBar,
            displayWidth: Math.max(0, width),
            duration: 300,
            ease: 'Power2'
        });
        
        // Color shift at low HP
        if (this.playerHP < 30) {
            this.playerHPBar.setFillStyle(VoidScene.CONFIG.COLORS.DANGER);
        } else {
            this.playerHPBar.setFillStyle(VoidScene.CONFIG.COLORS.PLAYER_HP);
        }
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // PHASE TRANSITIONS
    // ════════════════════════════════════════════════════════════════════════
    
    _endPhase() {
        this._hideActionButtons();
        this.turnIndicator.setText('');
        
        if (this.bossPhase < VoidScene.CONFIG.BOSS.PHASES - 1) {
            // Next phase
            theDealer.advancePhase();
            
            dialogueSystem.show(theDealer.getBossDialogue(this.bossPhase + 1), () => {
                // Heal player between phases
                this.playerHP = Math.min(
                    VoidScene.CONFIG.PLAYER.MAX_HP,
                    this.playerHP + VoidScene.CONFIG.PLAYER.HEAL_BETWEEN_PHASES
                );
                this._updatePlayerHP();
                
                // Show heal effect
                this._showHealEffect();
                
                this._beginPhase(this.bossPhase + 1);
            });
        } else {
            // Final phase complete - victory!
            this._victory();
        }
    }
    
    _showHealEffect() {
        const healText = this.add.text(400, 420, `+${VoidScene.CONFIG.PLAYER.HEAL_BETWEEN_PHASES}`, {
            fontSize: '20px',
            color: '#44ff44',
            fontFamily: 'monospace',
            fontStyle: 'bold'
        }).setOrigin(0.5);
        
        this.tweens.add({
            targets: healText,
            y: 380,
            alpha: 0,
            duration: 1000,
            ease: 'Power2',
            onComplete: () => healText.destroy()
        });
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // ENDINGS
    // ════════════════════════════════════════════════════════════════════════
    
    _victory() {
        this.combatActive = false;
        this._hideActionButtons();
        
        // Victory fanfare
        this.cameras.main.flash(500, 255, 215, 0);
        
        // Show final dialogue and choice
        dialogueSystem.show(theDealer.getBossDialogue(3), () => {
            this._showFinalChoice();
        });
    }
    
    _showFinalChoice() {
        this.finalChoiceShown = true;
        const { GOLD } = VoidScene.CONFIG.COLORS;
        
        // Darken background
        const overlay = this.add.rectangle(400, 250, 800, 500, 0x000000, 0.7);
        
        // Choice container
        const choiceBox = this.add.rectangle(400, 300, 500, 200, 0x0a200a, 0.95);
        choiceBox.setStrokeStyle(3, GOLD);
        
        // Title
        this.add.text(400, 220, 'CHOOSE YOUR ENDING', {
            fontSize: '16px',
            color: '#ffaa00',
            fontFamily: 'monospace',
            fontStyle: 'bold'
        }).setOrigin(0.5);
        
        // Three ending buttons
        const endings = [
            { 
                key: 'merge', 
                label: '🃏 BECOME DEALER', 
                desc: 'Join the eternal game',
                color: 0x440088,
                x: 250
            },
            { 
                key: 'free', 
                label: '💰 CASH OUT', 
                desc: 'Take Maya and leave',
                color: 0x004488,
                x: 400
            },
            { 
                key: 'destroy', 
                label: '🔥 FLIP TABLE', 
                desc: 'End everything',
                color: 0x880044,
                x: 550
            }
        ];
        
        this.endingButtons = [];
        endings.forEach(ending => {
            const btn = this.add.rectangle(ending.x, 300, 140, 60, ending.color, 1)
                .setInteractive({ useHandCursor: true });
            btn.setStrokeStyle(2, GOLD);
            
            this.add.text(ending.x, 290, ending.label, {
                fontSize: '11px',
                color: '#ffffff',
                fontFamily: 'monospace',
                fontStyle: 'bold'
            }).setOrigin(0.5);
            
            this.add.text(ending.x, 310, ending.desc, {
                fontSize: '9px',
                color: '#aaaaaa',
                fontFamily: 'monospace'
            }).setOrigin(0.5);
            
            btn.on('pointerover', () => btn.setScale(1.1));
            btn.on('pointerout', () => btn.setScale(1));
            btn.on('pointerdown', () => this._ending(ending.key));
            
            // Store for AutoPlayer access
            this.endingButtons.push({ btn, key: ending.key });
        });
    }
    
    _ending(choice) {
        const endingDialogues = {
            'merge': 'ending_merge',
            'free': 'ending_free',
            'destroy': 'ending_destroy'
        };
        
        // Record the ending choice
        theDealer.recordDecision(`ending_${choice}`, { finalChoice: true });
        
        const dialogueId = endingDialogues[choice] || 'ending_free';
        
        dialogueSystem.show(dialogueId, () => {
            // Ending-specific visual
            if (choice === 'destroy') {
                this.cameras.main.shake(2000, 0.05);
                this.cameras.main.fadeOut(4000, 255, 100, 0);
            } else {
                this.cameras.main.fadeOut(3000, 0, 0, 0);
            }
            
            this.time.delayedCall(4000, () => {
                gameState.setFlag('gameCompleted', true);
                gameState.setFlag('endingChoice', choice);
                gameState.reset();
                // Use centralized transition
                const SceneTransition = window.SceneTransition || (typeof SceneTransition !== 'undefined' ? SceneTransition : null);
                if (SceneTransition) {
                    SceneTransition.transition(this, 'lab', {
                        playerX: 400,
                        playerY: 400,
                        onCleanup: () => SceneTransition.cleanupPlayer(this.player)
                    });
                } else {
                    this.scene.start('LabScene');
                }
            });
        });
    }
    
    // Public method for AutoPlayer
    ending(choice) {
        // Map AutoPlayer choice keys to VoidScene keys
        const choiceMap = {
            'free': 'free',
            'join': 'merge',
            'destroy': 'destroy',
            'merge': 'merge'
        };
        
        const mappedChoice = choiceMap[choice] || 'free';
        
        // Check if final choice UI is showing
        if (this.finalChoiceShown) {
            this._ending(mappedChoice);
        } else {
            // If not showing yet, wait for it
            console.warn(`[VoidScene] Final choice UI not ready, waiting...`);
            this.time.delayedCall(1000, () => {
                if (this.finalChoiceShown) {
                    this._ending(mappedChoice);
                } else {
                    // Force show if needed
                    this._showFinalChoice();
                    this.time.delayedCall(500, () => this._ending(mappedChoice));
                }
            });
        }
    }
    
    _playerDefeated() {
        this.combatActive = false;
        this._hideActionButtons();
        
        // Record death
        eventBus.emit('player:death', { boss: 'dealer', phase: this.bossPhase });
        
        dialogueSystem.showLines('THE DEALER', [
            "*catches your falling cards*",
            "Ah. You've gone bust.",
            "",
            "*flips through the Ledger*",
            "Don't worry. In my casino, death is just... a fold.",
            "You can re-ante. Try again.",
            "",
            "*winks*",
            "I'll be waiting at the table."
        ], () => {
            this.cameras.main.fadeOut(1500, 0, 0, 0);
            this.time.delayedCall(1500, () => {
                gameState.setFlag('lostToDealer', true);
                // Use centralized transition
                const SceneTransition = window.SceneTransition || (typeof SceneTransition !== 'undefined' ? SceneTransition : null);
                if (SceneTransition) {
                    SceneTransition.transition(this, 'underground', {
                        playerX: 400,
                        playerY: 400,
                        onCleanup: () => SceneTransition.cleanupPlayer(this.player)
                    });
                } else {
                    this.scene.start('UndergroundScene');
                }
            });
        });
    }
}
