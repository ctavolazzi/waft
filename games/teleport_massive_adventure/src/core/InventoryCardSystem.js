/**
 * InventoryCardSystem - Rich item card display
 * 
 * Creates detailed item cards with assets, stats, descriptions, and hints.
 */
class InventoryCardSystem {
    constructor() {
        this.cardOverlay = null;
        this.currentItem = null;
    }
    
    init() {
        this.createCardOverlay();
    }
    
    createCardOverlay() {
        // Create overlay container
        this.cardOverlay = document.createElement('div');
        this.cardOverlay.id = 'item-card-overlay';
        this.cardOverlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.8);
            z-index: 200;
            display: none;
            align-items: center;
            justify-content: center;
            pointer-events: all;
        `;
        
        // Create card
        const card = document.createElement('div');
        card.id = 'item-card';
        card.style.cssText = `
            background: linear-gradient(135deg, #1a1a2e 0%, #2a2a3e 100%);
            border: 2px solid #00aaff;
            border-radius: 8px;
            padding: 20px;
            max-width: 400px;
            max-height: 80vh;
            overflow-y: auto;
            position: relative;
            box-shadow: 0 0 30px rgba(0, 170, 255, 0.5);
        `;
        
        // Close button
        const closeBtn = document.createElement('button');
        closeBtn.textContent = '✕';
        closeBtn.style.cssText = `
            position: absolute;
            top: 10px;
            right: 10px;
            background: transparent;
            border: 1px solid #00aaff;
            color: #00aaff;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 18px;
            line-height: 1;
        `;
        closeBtn.onclick = () => this.hideCard();
        
        card.appendChild(closeBtn);
        this.cardOverlay.appendChild(card);
        
        // Add to body
        document.body.appendChild(this.cardOverlay);
        
        // Close on overlay click
        this.cardOverlay.onclick = (e) => {
            if (e.target === this.cardOverlay) {
                this.hideCard();
            }
        };
    }
    
    showCard(item) {
        if (!this.cardOverlay) return;
        
        this.currentItem = item;
        const card = this.cardOverlay.querySelector('#item-card');
        
        // Get item data
        const itemData = window.itemsData?.items?.[item.id] || item;
        
        // Build card content
        card.innerHTML = `
            <button style="position: absolute; top: 10px; right: 10px; background: transparent; border: 1px solid #00aaff; color: #00aaff; width: 30px; height: 30px; border-radius: 50%; cursor: pointer; font-size: 18px; line-height: 1;" onclick="window.inventoryCardSystem.hideCard()">✕</button>
            
            <div style="text-align: center; margin-bottom: 20px;">
                ${itemData.sprite ? `<img src="assets/objects/${itemData.sprite}.png" style="width: 80px; height: 80px; image-rendering: pixelated;" onerror="this.style.display='none'" />` : ''}
                <h2 style="color: #00ff88; margin: 10px 0 5px 0; font-size: 24px;">${itemData.name || item.name}</h2>
                <div style="font-size: 48px; margin: 10px 0;">${itemData.icon || item.icon || '?'}</div>
            </div>
            
            <div style="color: #aaccff; margin-bottom: 15px; line-height: 1.6;">
                ${itemData.description || item.description || 'No description available.'}
            </div>
            
            ${this._buildStats(itemData)}
            ${this._buildUsage(itemData)}
            ${this._buildHints(itemData)}
            ${this._buildQuote(itemData)}
        `;
        
        this.cardOverlay.style.display = 'flex';
    }
    
    _buildStats(itemData) {
        const stats = [];
        if (itemData.effects?.heal) stats.push(`Heals: ${itemData.effects.heal} HP`);
        if (itemData.attack) stats.push(`Attack: ${itemData.attack}`);
        if (itemData.defense) stats.push(`Defense: ${itemData.defense}`);
        if (itemData.type) stats.push(`Type: ${itemData.type}`);
        
        if (stats.length === 0) return '';
        
        return `
            <div style="border-top: 1px solid #00aaff; padding-top: 15px; margin-top: 15px;">
                <h3 style="color: #00aaff; font-size: 14px; margin-bottom: 10px;">STATS</h3>
                <div style="color: #88ccff; font-size: 12px; line-height: 1.8;">
                    ${stats.map(s => `<div>• ${s}</div>`).join('')}
                </div>
            </div>
        `;
    }
    
    _buildUsage(itemData) {
        if (!itemData.usableOn && !itemData.effects) return '';
        
        const usage = [];
        if (itemData.usableOn) {
            usage.push(`Can be used on: ${itemData.usableOn.join(', ')}`);
        }
        if (itemData.consumeOnUse === false) {
            usage.push('Reusable item');
        } else if (itemData.consumable) {
            usage.push('Single use item');
        }
        
        if (usage.length === 0) return '';
        
        return `
            <div style="border-top: 1px solid #00aaff; padding-top: 15px; margin-top: 15px;">
                <h3 style="color: #00aaff; font-size: 14px; margin-bottom: 10px;">USAGE</h3>
                <div style="color: #88ccff; font-size: 12px; line-height: 1.8;">
                    ${usage.map(u => `<div>• ${u}</div>`).join('')}
                </div>
            </div>
        `;
    }
    
    _buildHints(itemData) {
        const hints = [];
        
        // Generate hints based on item
        if (itemData.id === 'artifact') {
            hints.push('This artifact resonates with dimensional portals.');
            hints.push('Phaseburner might know something about it.');
        } else if (itemData.id === 'keycard') {
            hints.push('Use this on the maintenance hatch in the lobby.');
            hints.push('It grants access to restricted areas.');
        } else if (itemData.id === 'energy_core') {
            hints.push('Used for drone upgrades at workbenches.');
            hints.push('Find workbenches in the lab or underground.');
        } else if (itemData.id === 'weapon_module') {
            hints.push('Enhances drone combat capabilities.');
            hints.push('Combine with other parts at workbenches.');
        } else if (itemData.id === 'shield_generator') {
            hints.push('Improves drone defensive systems.');
            hints.push('Upgrade your drone at workbenches.');
        }
        
        if (hints.length === 0) return '';
        
        return `
            <div style="border-top: 1px solid #00ff88; padding-top: 15px; margin-top: 15px;">
                <h3 style="color: #00ff88; font-size: 14px; margin-bottom: 10px;">💡 HINTS</h3>
                <div style="color: #88ffaa; font-size: 12px; line-height: 1.8; font-style: italic;">
                    ${hints.map(h => `<div>• ${h}</div>`).join('')}
                </div>
            </div>
        `;
    }
    
    _buildQuote(itemData) {
        const quotes = {
            'artifact': '"The Between calls to those who listen."',
            'keycard': '"Access granted. But to what?"',
            'energy_core': '"Power flows through the core."',
            'weapon_module': '"Offense is the best defense."',
            'shield_generator': '"Protection comes in many forms."'
        };
        
        const quote = quotes[itemData.id];
        if (!quote) return '';
        
        return `
            <div style="border-top: 1px solid #ffaa00; padding-top: 15px; margin-top: 15px; text-align: center;">
                <div style="color: #ffaa00; font-size: 12px; font-style: italic; line-height: 1.6;">
                    "${quote}"
                </div>
            </div>
        `;
    }
    
    hideCard() {
        if (this.cardOverlay) {
            this.cardOverlay.style.display = 'none';
        }
        this.currentItem = null;
    }
}

// Create global instance
const inventoryCardSystem = new InventoryCardSystem();
