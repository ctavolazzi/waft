/**
 * D&D Toolkit Hub - Card Export
 * Converts entries to rpg-cards JSON format and manages card queue
 */

// Add card to queue
function addToCardQueue(card) {
    if (!card || !card.title) {
        console.error('Invalid card:', card);
        return;
    }

    AppState.cardQueue.push(card);
    updateCardQueueUI();
}

// Update card queue UI
function updateCardQueueUI() {
    const select = document.getElementById('card-queue-list');
    select.innerHTML = '';

    AppState.cardQueue.forEach((card, index) => {
        const option = document.createElement('option');
        option.value = index;
        option.textContent = card.title;
        select.appendChild(option);
    });

    // Update count
    document.getElementById('card-count').textContent = `(${AppState.cardQueue.length})`;

    // Update preview
    updateCardPreview();
}

// Update card preview
function updateCardPreview() {
    const previewDiv = document.getElementById('card-preview-content');

    if (AppState.cardQueue.length === 0) {
        previewDiv.innerHTML = '<p class="placeholder">Add items to queue to preview</p>';
        return;
    }

    let html = '';
    AppState.cardQueue.forEach((card, index) => {
        html += renderCardPreview(card, index);
    });

    previewDiv.innerHTML = html;
}

// Render a card preview
function renderCardPreview(card, index) {
    // Parse contents for preview
    let contentHtml = '';
    if (card.contents) {
        card.contents.forEach(line => {
            if (typeof line !== 'string') return;

            const parts = line.split('|').map(p => p.trim());
            const type = parts[0];

            switch (type) {
                case 'subtitle':
                    contentHtml += `<div style="font-style:italic;opacity:0.8;">${parts[1] || ''}</div>`;
                    break;
                case 'rule':
                case 'ruler':
                    contentHtml += '<hr style="margin:5px 0;border-color:rgba(255,255,255,0.3);">';
                    break;
                case 'property':
                    contentHtml += `<div><strong>${parts[1] || ''}:</strong> ${parts[2] || ''}</div>`;
                    break;
                case 'text':
                    contentHtml += `<div style="margin:5px 0;">${parts[1] || ''}</div>`;
                    break;
                case 'section':
                    contentHtml += `<div style="font-weight:bold;margin-top:10px;color:#c9a227;">${parts[1] || ''}</div>`;
                    break;
                case 'dndstats':
                    const stats = ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA'];
                    contentHtml += '<div style="display:flex;justify-content:space-between;font-size:0.8em;margin:5px 0;">';
                    for (let i = 0; i < 6; i++) {
                        const val = parts[i + 1] || '10';
                        const mod = Math.floor((parseInt(val) - 10) / 2);
                        const modStr = mod >= 0 ? '+' + mod : mod.toString();
                        contentHtml += `<div style="text-align:center;"><div style="color:#c9a227;">${stats[i]}</div><div>${val} (${modStr})</div></div>`;
                    }
                    contentHtml += '</div>';
                    break;
                case 'fill':
                    // Skip fill elements in preview
                    break;
            }
        });
    }

    return `
        <div class="card-preview-item" style="border-left:4px solid ${card.color_front || '#c9a227'};">
            <h4>${card.title}</h4>
            <div class="card-content">${contentHtml}</div>
        </div>
    `;
}

// Remove selected card from queue
function removeFromQueue() {
    const select = document.getElementById('card-queue-list');
    const index = parseInt(select.value);

    if (isNaN(index) || index < 0 || index >= AppState.cardQueue.length) {
        showNotification('Select a card to remove');
        return;
    }

    AppState.cardQueue.splice(index, 1);
    updateCardQueueUI();
    showNotification('Card removed');
}

// Clear all cards from queue
function clearQueue() {
    if (AppState.cardQueue.length === 0) {
        showNotification('Queue is already empty');
        return;
    }

    AppState.cardQueue = [];
    updateCardQueueUI();
    showNotification('Queue cleared');
}

// Download cards as JSON
function downloadCardsJSON() {
    if (AppState.cardQueue.length === 0) {
        showNotification('Add cards to queue first');
        return;
    }

    const json = JSON.stringify(AppState.cardQueue, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = 'dnd-cards.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    showNotification('Downloaded dnd-cards.json');
}

// Open cards in rpg-cards generator
function openInRPGCards() {
    if (AppState.cardQueue.length === 0) {
        showNotification('Add cards to queue first');
        return;
    }

    // rpg-cards can accept data via URL or localStorage
    // For now, we'll copy to clipboard and open the generator
    const json = JSON.stringify(AppState.cardQueue, null, 2);
    copyTextToClipboard(json);

    // Open rpg-cards in new tab
    window.open('../_external/rpg-cards/generator/index.html', '_blank');

    showNotification('Cards copied! Paste in rpg-cards');
}

// Convert SRD entry to card format
function convertToCard(type, data) {
    switch (type) {
        case 'monster':
            return monsterToCardFromSRD(data);
        case 'spell':
            return spellToCardFromSRD(data);
        case 'item':
            return itemToCardFromSRD(data);
    }
}

// Convert SRD monster to card
function monsterToCardFromSRD(m) {
    const contents = [
        `subtitle | ${capitalizeFirst(m.size || 'medium')} ${capitalizeFirst(m.type || 'creature')}`,
        'rule',
        `property | AC | ${m.ac || '?'}`,
        `property | HP | ${m.hp || '?'}`,
        `property | Speed | ${m.speed || '30 ft.'}`,
        `property | CR | ${formatCR(m.cr)}`,
        'rule'
    ];

    // Add stats if available
    if (m.str) {
        contents.push(`dndstats | ${m.str} | ${m.dex} | ${m.con} | ${m.int} | ${m.wis} | ${m.cha}`);
    }

    // Add traits
    if (m.traits && m.traits.length > 0) {
        contents.push('rule');
        contents.push('section | Traits');
        m.traits.slice(0, 2).forEach(t => { // Limit to 2 for card space
            contents.push(`text | <b>${t.name}</b> ${truncate(t.description, 100)}`);
        });
    }

    // Add actions
    if (m.actions && m.actions.length > 0) {
        contents.push('rule');
        contents.push('section | Actions');
        m.actions.slice(0, 2).forEach(a => { // Limit to 2 for card space
            contents.push(`text | <b>${a.name}</b> ${truncate(a.description, 100)}`);
        });
    }

    // Color based on type
    const typeColors = {
        'aberration': 'Purple',
        'beast': 'SaddleBrown',
        'celestial': 'Gold',
        'construct': 'Gray',
        'dragon': 'Crimson',
        'elemental': 'OrangeRed',
        'fey': 'MediumOrchid',
        'fiend': 'DarkRed',
        'giant': 'DarkOliveGreen',
        'humanoid': 'SteelBlue',
        'monstrosity': 'DarkSlateGray',
        'ooze': 'LimeGreen',
        'plant': 'ForestGreen',
        'undead': 'DimGray'
    };

    return {
        count: 1,
        title: m.name,
        color_front: typeColors[m.type] || 'FireBrick',
        icon_front: 'monster-grasp',
        icon_back: 'monster-grasp',
        contents: contents,
        tags: ['monster', m.type || 'creature']
    };
}

// Convert SRD spell to card
function spellToCardFromSRD(s) {
    const levelText = s.level === 0 ? 'Cantrip' : `${ordinal(s.level)} level`;

    const contents = [
        `subtitle | ${levelText} ${capitalizeFirst(s.school || 'evocation')}`,
        'rule',
        `property | Casting Time | ${s.casting_time || '1 action'}`,
        `property | Range | ${s.range || 'Self'}`,
        `property | Components | ${s.components || 'V, S'}`,
        `property | Duration | ${s.duration || 'Instantaneous'}`,
        'rule',
        'fill | 1',
        `text | ${truncate(s.description || '', 250)}`
    ];

    if (s.at_higher_levels) {
        contents.push('fill | 1');
        contents.push('section | At Higher Levels');
        contents.push(`text | ${truncate(s.at_higher_levels, 100)}`);
    }

    // Color based on school
    const schoolColors = {
        'abjuration': 'RoyalBlue',
        'conjuration': 'Goldenrod',
        'divination': 'Silver',
        'enchantment': 'HotPink',
        'evocation': 'OrangeRed',
        'illusion': 'MediumPurple',
        'necromancy': 'DarkSlateGray',
        'transmutation': 'ForestGreen'
    };

    return {
        count: 1,
        title: s.name,
        color_front: schoolColors[s.school] || 'Maroon',
        icon_front: 'white-book-1',
        icon_back: 'robe',
        contents: contents,
        tags: ['spell', s.school || 'evocation']
    };
}

// Convert SRD item to card
function itemToCardFromSRD(i) {
    const contents = [
        `subtitle | ${i.type_line || capitalizeFirst(i.type || 'wondrous item')}`,
        `subtitle | ${i.rarity_line || capitalizeFirst(i.rarity || 'common')}`,
        'rule'
    ];

    if (i.damage) {
        contents.push(`property | Damage | ${i.damage}`);
    }
    if (i.properties) {
        contents.push(`property | Properties | ${i.properties}`);
    }
    if (i.cost) {
        contents.push(`property | Cost | ${i.cost}`);
    }

    contents.push('rule');
    contents.push('fill | 2');

    if (i.description) {
        contents.push(`text | ${truncate(i.description, 200)}`);
    }

    contents.push('fill | 3');

    // Color based on rarity
    const rarityColors = {
        'common': 'Gray',
        'uncommon': 'ForestGreen',
        'rare': 'RoyalBlue',
        'very-rare': 'MediumPurple',
        'legendary': 'Goldenrod',
        'artifact': 'OrangeRed'
    };

    return {
        count: 1,
        title: i.name,
        color_front: rarityColors[i.rarity] || 'Gray',
        icon_front: 'swap-bag',
        icon_back: 'swap-bag',
        contents: contents,
        tags: ['item', i.rarity || 'common']
    };
}

// Helper: truncate text
function truncate(text, maxLength) {
    if (!text) return '';
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength - 3) + '...';
}
