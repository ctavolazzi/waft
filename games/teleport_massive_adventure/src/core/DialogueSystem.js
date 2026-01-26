/**
 * DialogueSystem - Composable dialogue management
 * 
 * Handles all dialogue display, queuing, and callbacks.
 * Supports branching, conditions, and dynamic text.
 */
class DialogueSystem {
    constructor() {
        this.dialogueData = {};
        this.queue = [];
        this.isActive = false;
        this.currentDialogue = null;
        this.onComplete = null;
        
        // DOM elements (set after DOM ready)
        this.elements = {};
    }
    
    // ========================================
    // Setup
    // ========================================
    
    init(elements) {
        this.elements = {
            box: elements.box || document.getElementById('dialogue-box'),
            speaker: elements.speaker || document.getElementById('speaker-name'),
            text: elements.text || document.getElementById('dialogue-text'),
            continueIndicator: elements.continueIndicator || document.getElementById('dialogue-continue')
        };
        
        // Click to advance
        this.elements.box?.addEventListener('click', () => this.advance());
        document.addEventListener('keydown', (e) => {
            if ((e.key === ' ' || e.key === 'Enter') && this.isActive) {
                this.advance();
            }
        });
    }
    
    loadData(dialogueData) {
        this.dialogueData = dialogueData;
    }
    
    // ========================================
    // Core Dialogue Functions
    // ========================================
    
    show(dialogueId, onComplete = null) {
        const dialogue = this.dialogueData[dialogueId];
        if (!dialogue) {
            console.warn(`Dialogue not found: ${dialogueId}`);
            return;
        }
        
        return this.showLines(dialogue.speaker, dialogue.lines, onComplete);
    }
    
    showLines(speaker, lines, onComplete = null) {
        this.queue = [...lines];
        this.currentDialogue = { speaker, lines };
        this.onComplete = onComplete;
        this.isActive = true;
        
        this.displayNext();
        return this;
    }
    
    showSingle(speaker, text) {
        return this.showLines(speaker, [text]);
    }
    
    // ========================================
    // Display Logic
    // ========================================
    
    displayNext() {
        if (this.queue.length === 0) {
            this.hide();
            return;
        }
        
        const line = this.queue.shift();
        const processedLine = this.processLine(line);
        
        if (this.elements.speaker) {
            this.elements.speaker.textContent = this.currentDialogue.speaker || 'OBSERVATION';
        }
        
        if (this.elements.text) {
            this.elements.text.textContent = processedLine;
        }
        
        if (this.elements.box) {
            this.elements.box.classList.add('active');
        }
    }
    
    advance() {
        if (!this.isActive) return;
        
        if (this.queue.length > 0) {
            this.displayNext();
        } else {
            this.hide();
        }
    }
    
    hide() {
        this.isActive = false;
        
        if (this.elements.box) {
            this.elements.box.classList.remove('active');
        }
        
        // Trigger completion callback
        if (this.onComplete) {
            const callback = this.onComplete;
            this.onComplete = null;
            callback();
        }
    }
    
    // ========================================
    // Text Processing
    // ========================================
    
    processLine(line) {
        // Variable substitution: ${varName}
        return line.replace(/\$\{(\w+)\}/g, (match, varName) => {
            return gameState?.get(varName) ?? match;
        });
    }
    
    // ========================================
    // Branching Dialogue
    // ========================================
    
    showChoice(prompt, choices, onChoice) {
        // choices: [{ text: "Option 1", value: "opt1" }, ...]
        this.showSingle('', prompt);
        
        // Create choice buttons (implementation depends on UI)
        // This is a simplified version
        this.pendingChoice = { choices, onChoice };
    }
    
    selectChoice(index) {
        if (!this.pendingChoice) return;
        
        const { choices, onChoice } = this.pendingChoice;
        const selected = choices[index];
        this.pendingChoice = null;
        
        if (onChoice) {
            onChoice(selected.value, selected);
        }
    }
    
    // ========================================
    // Typewriter Effect (Optional)
    // ========================================
    
    typewrite(text, element, speed = 30) {
        return new Promise(resolve => {
            let index = 0;
            element.textContent = '';
            
            const type = () => {
                if (index < text.length) {
                    element.textContent += text[index];
                    index++;
                    setTimeout(type, speed);
                } else {
                    resolve();
                }
            };
            
            type();
        });
    }
}

const dialogueSystem = new DialogueSystem();
