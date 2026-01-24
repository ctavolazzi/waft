/**
 * D&D Toolkit Hub - SRD Browser
 * Search and filter functionality for monsters, spells, and items
 */

// Current search results
let searchResults = [];
let selectedEntry = null;

// Perform search based on current filters
function performSearch() {
    const searchTerm = document.getElementById('search-input').value.toLowerCase().trim();
    const filterType = document.getElementById('filter-type').value;
    const filterCR = document.getElementById('filter-cr').value;

    searchResults = [];

    // Search monsters
    if (filterType === 'all' || filterType === 'monster') {
        AppState.monsters.forEach(monster => {
            if (matchesSearch(monster.name, searchTerm) && matchesCR(monster.cr, filterCR)) {
                searchResults.push({
                    type: 'monster',
                    data: monster,
                    display: `[M] ${monster.name} (CR ${formatCR(monster.cr)})`
                });
            }
        });
    }

    // Search spells
    if (filterType === 'all' || filterType === 'spell') {
        AppState.spells.forEach(spell => {
            if (matchesSearch(spell.name, searchTerm) && matchesLevel(spell.level, filterCR)) {
                const levelText = spell.level === 0 ? 'Cantrip' : `Lvl ${spell.level}`;
                searchResults.push({
                    type: 'spell',
                    data: spell,
                    display: `[S] ${spell.name} (${levelText})`
                });
            }
        });
    }

    // Search items
    if (filterType === 'all' || filterType === 'item') {
        AppState.items.forEach(item => {
            if (matchesSearch(item.name, searchTerm) && matchesRarity(item.rarity, filterCR)) {
                const rarityText = item.rarity ? capitalizeFirst(item.rarity) : 'Common';
                searchResults.push({
                    type: 'item',
                    data: item,
                    display: `[I] ${item.name} (${rarityText})`
                });
            }
        });
    }

    // Sort results alphabetically
    searchResults.sort((a, b) => a.data.name.localeCompare(b.data.name));

    // Update results list
    updateResultsList();
}

// Check if name matches search term
function matchesSearch(name, searchTerm) {
    if (!searchTerm) return true;
    return name.toLowerCase().includes(searchTerm);
}

// Check if CR matches filter
function matchesCR(cr, filterValue) {
    if (filterValue === 'all') return true;
    if (filterValue === '10+') return cr >= 10;
    return cr === parseFloat(filterValue);
}

// Check if spell level matches filter
function matchesLevel(level, filterValue) {
    if (filterValue === 'all') return true;
    if (filterValue === '10+') return false; // No spells above 9
    return level === parseInt(filterValue);
}

// Check if rarity matches filter (simplified)
function matchesRarity(rarity, filterValue) {
    if (filterValue === 'all') return true;
    // Map rarity to rough "level" for filtering
    const rarityLevels = {
        'common': 0,
        'uncommon': 1,
        'rare': 2,
        'very-rare': 3,
        'legendary': 4,
        'artifact': 5
    };
    return true; // For now, show all items regardless of CR filter
}

// Update the results select list
function updateResultsList() {
    const select = document.getElementById('results-select');
    select.innerHTML = '';

    searchResults.forEach((result, index) => {
        const option = document.createElement('option');
        option.value = index;
        option.textContent = result.display;
        select.appendChild(option);
    });

    // Update count
    document.getElementById('result-count').textContent = `(${searchResults.length})`;

    // Clear details panel
    selectedEntry = null;
    document.getElementById('details-content').innerHTML = '<p class="placeholder">Select an entry to view details</p>';
}

// Show details for selected entry
function showDetails() {
    const select = document.getElementById('results-select');
    const index = parseInt(select.value);

    if (isNaN(index) || index < 0 || index >= searchResults.length) return;

    selectedEntry = searchResults[index];
    const detailsDiv = document.getElementById('details-content');

    switch (selectedEntry.type) {
        case 'monster':
            detailsDiv.innerHTML = renderMonsterDetails(selectedEntry.data);
            break;
        case 'spell':
            detailsDiv.innerHTML = renderSpellDetails(selectedEntry.data);
            break;
        case 'item':
            detailsDiv.innerHTML = renderItemDetails(selectedEntry.data);
            break;
    }
}

// Render monster statblock
function renderMonsterDetails(monster) {
    const statsHtml = monster.str ? `
        <div class="stats-table">
            <div class="stat-col"><span class="stat-label">STR</span><span class="stat-value">${monster.str} (${getModifier(monster.str)})</span></div>
            <div class="stat-col"><span class="stat-label">DEX</span><span class="stat-value">${monster.dex} (${getModifier(monster.dex)})</span></div>
            <div class="stat-col"><span class="stat-label">CON</span><span class="stat-value">${monster.con} (${getModifier(monster.con)})</span></div>
            <div class="stat-col"><span class="stat-label">INT</span><span class="stat-value">${monster.int} (${getModifier(monster.int)})</span></div>
            <div class="stat-col"><span class="stat-label">WIS</span><span class="stat-value">${monster.wis} (${getModifier(monster.wis)})</span></div>
            <div class="stat-col"><span class="stat-label">CHA</span><span class="stat-value">${monster.cha} (${getModifier(monster.cha)})</span></div>
        </div>
    ` : '';

    const traitsHtml = monster.traits && monster.traits.length > 0 ? `
        <div class="section-title">Traits</div>
        ${monster.traits.map(t => `<div class="trait"><span class="trait-name">${t.name}</span> ${t.description}</div>`).join('')}
    ` : '';

    const actionsHtml = monster.actions && monster.actions.length > 0 ? `
        <div class="section-title">Actions</div>
        ${monster.actions.map(a => `<div class="action"><span class="action-name">${a.name}</span> ${a.description}</div>`).join('')}
    ` : '';

    return `
        <div class="statblock">
            <h4>${monster.name}</h4>
            <div class="type-line">${capitalizeFirst(monster.size || 'medium')} ${monster.type || 'creature'}${monster.subtype ? ` (${monster.subtype})` : ''}</div>

            <div class="stat-line"><strong>Armor Class</strong> ${monster.ac || '?'}</div>
            <div class="stat-line"><strong>Hit Points</strong> ${monster.hp || '?'}</div>
            <div class="stat-line"><strong>Speed</strong> ${monster.speed || '30 ft.'}</div>

            ${statsHtml}

            ${monster.senses ? `<div class="stat-line"><strong>Senses</strong> ${monster.senses}</div>` : ''}
            ${monster.languages ? `<div class="stat-line"><strong>Languages</strong> ${monster.languages}</div>` : ''}
            <div class="stat-line"><strong>Challenge</strong> ${formatCR(monster.cr)}</div>

            ${traitsHtml}
            ${actionsHtml}
        </div>
    `;
}

// Render spell details
function renderSpellDetails(spell) {
    const levelSchool = spell.level === 0
        ? `${capitalizeFirst(spell.school || 'evocation')} cantrip`
        : `${ordinal(spell.level)}-level ${spell.school || 'evocation'}`;

    return `
        <div class="spell-details">
            <div class="spell-header">
                <h4>${spell.name}</h4>
                <div class="spell-level-school">${levelSchool}</div>
            </div>

            <div class="spell-meta">
                <p><strong>Casting Time:</strong> ${spell.casting_time || '1 action'}</p>
                <p><strong>Range:</strong> ${spell.range || 'Self'}</p>
                <p><strong>Components:</strong> ${spell.components || 'V, S'}</p>
                <p><strong>Duration:</strong> ${spell.duration || 'Instantaneous'}</p>
                ${spell.classes && spell.classes.length > 0 ? `<p><strong>Classes:</strong> ${spell.classes.map(c => capitalizeFirst(c)).join(', ')}</p>` : ''}
            </div>

            <div class="spell-description">
                ${spell.description || 'No description available.'}
            </div>

            ${spell.at_higher_levels ? `
                <div class="higher-levels">
                    <strong>At Higher Levels:</strong> ${spell.at_higher_levels}
                </div>
            ` : ''}
        </div>
    `;
}

// Render item details
function renderItemDetails(item) {
    const typeLine = [
        item.type_line || capitalizeFirst(item.type || 'wondrous item'),
        item.rarity_line || capitalizeFirst(item.rarity || 'common')
    ].filter(Boolean).join(', ');

    return `
        <div class="item-details">
            <h4>${item.name}</h4>
            <div class="item-type-line">${typeLine}</div>

            <div class="item-properties">
                ${item.damage ? `<p><strong>Damage:</strong> ${item.damage}</p>` : ''}
                ${item.properties ? `<p><strong>Properties:</strong> ${item.properties}</p>` : ''}
                ${item.cost ? `<p><strong>Cost:</strong> ${item.cost}</p>` : ''}
                ${item.weight ? `<p><strong>Weight:</strong> ${item.weight}</p>` : ''}
            </div>

            ${item.description ? `<div class="item-description">${item.description}</div>` : ''}
        </div>
    `;
}

// Copy current entry to clipboard
function copyToClipboard() {
    if (!selectedEntry) {
        showNotification('Select an entry first');
        return;
    }

    let text = '';
    switch (selectedEntry.type) {
        case 'monster':
            text = formatMonsterText(selectedEntry.data);
            break;
        case 'spell':
            text = formatSpellText(selectedEntry.data);
            break;
        case 'item':
            text = formatItemText(selectedEntry.data);
            break;
    }

    copyTextToClipboard(text);
}

// Format monster as plain text
function formatMonsterText(m) {
    let text = `${m.name}\n`;
    text += `${capitalizeFirst(m.size || 'medium')} ${m.type || 'creature'}\n\n`;
    text += `AC: ${m.ac || '?'}\n`;
    text += `HP: ${m.hp || '?'}\n`;
    text += `Speed: ${m.speed || '30 ft.'}\n`;
    text += `CR: ${formatCR(m.cr)}\n`;

    if (m.str) {
        text += `\nSTR ${m.str} | DEX ${m.dex} | CON ${m.con} | INT ${m.int} | WIS ${m.wis} | CHA ${m.cha}\n`;
    }

    if (m.traits && m.traits.length > 0) {
        text += '\nTraits:\n';
        m.traits.forEach(t => {
            text += `- ${t.name} ${t.description}\n`;
        });
    }

    if (m.actions && m.actions.length > 0) {
        text += '\nActions:\n';
        m.actions.forEach(a => {
            text += `- ${a.name} ${a.description}\n`;
        });
    }

    return text;
}

// Format spell as plain text
function formatSpellText(s) {
    const levelSchool = s.level === 0
        ? `${capitalizeFirst(s.school || 'evocation')} cantrip`
        : `${ordinal(s.level)}-level ${s.school || 'evocation'}`;

    let text = `${s.name}\n${levelSchool}\n\n`;
    text += `Casting Time: ${s.casting_time || '1 action'}\n`;
    text += `Range: ${s.range || 'Self'}\n`;
    text += `Components: ${s.components || 'V, S'}\n`;
    text += `Duration: ${s.duration || 'Instantaneous'}\n\n`;
    text += s.description || '';

    if (s.at_higher_levels) {
        text += `\n\nAt Higher Levels: ${s.at_higher_levels}`;
    }

    return text;
}

// Format item as plain text
function formatItemText(i) {
    let text = `${i.name}\n`;
    text += `${i.type_line || capitalizeFirst(i.type || 'wondrous item')}, ${i.rarity_line || capitalizeFirst(i.rarity || 'common')}\n\n`;

    if (i.damage) text += `Damage: ${i.damage}\n`;
    if (i.properties) text += `Properties: ${i.properties}\n`;
    if (i.cost) text += `Cost: ${i.cost}\n`;
    if (i.weight) text += `Weight: ${i.weight}\n`;

    if (i.description) {
        text += `\n${i.description}`;
    }

    return text;
}

// Export selected entry to card format
function exportToCard() {
    if (!selectedEntry) {
        showNotification('Select an entry first');
        return;
    }

    const card = convertToCard(selectedEntry.type, selectedEntry.data);
    addToCardQueue(card);
    showNotification('Added to card queue!');
}

// Helper functions
function capitalizeFirst(str) {
    if (!str) return '';
    return str.charAt(0).toUpperCase() + str.slice(1);
}

function ordinal(n) {
    const suffixes = ['th', 'st', 'nd', 'rd'];
    const v = n % 100;
    return n + (suffixes[(v - 20) % 10] || suffixes[v] || suffixes[0]);
}
