/**
 * D&D Toolkit Hub - Homebrew Creator
 * Form handling and export functionality
 */

// Switch between creator forms
function switchCreatorForm() {
    const formType = document.getElementById('creator-type').value;

    // Hide all forms
    document.querySelectorAll('.creator-form').forEach(form => {
        form.classList.remove('active');
    });

    // Show selected form
    const selectedForm = document.getElementById('form-' + formType);
    if (selectedForm) {
        selectedForm.classList.add('active');
    }

    // Hide export output
    document.getElementById('export-output').style.display = 'none';
}

// Get form data based on type
function getFormData() {
    const formType = document.getElementById('creator-type').value;

    switch (formType) {
        case 'monster':
            return getMonsterFormData();
        case 'spell':
            return getSpellFormData();
        case 'item':
            return getItemFormData();
    }
}

// Get monster form data
function getMonsterFormData() {
    // Parse actions from textarea
    const actionsText = document.getElementById('monster-actions').value;
    const actions = actionsText.split('\n')
        .filter(line => line.trim())
        .map(line => {
            const match = line.match(/^([^.]+)\.\s*(.*)$/);
            if (match) {
                return { name: match[1].trim(), description: match[2].trim() };
            }
            return { name: 'Action', description: line.trim() };
        });

    return {
        type: 'monster',
        name: document.getElementById('monster-name').value || 'Unnamed Creature',
        size: document.getElementById('monster-size').value,
        monsterType: document.getElementById('monster-type').value,
        ac: parseInt(document.getElementById('monster-ac').value) || 10,
        hp: parseInt(document.getElementById('monster-hp').value) || 10,
        cr: document.getElementById('monster-cr').value,
        speed: document.getElementById('monster-speed').value || '30 ft.',
        str: parseInt(document.getElementById('monster-str').value) || 10,
        dex: parseInt(document.getElementById('monster-dex').value) || 10,
        con: parseInt(document.getElementById('monster-con').value) || 10,
        int: parseInt(document.getElementById('monster-int').value) || 10,
        wis: parseInt(document.getElementById('monster-wis').value) || 10,
        cha: parseInt(document.getElementById('monster-cha').value) || 10,
        actions: actions
    };
}

// Get spell form data
function getSpellFormData() {
    return {
        type: 'spell',
        name: document.getElementById('spell-name').value || 'Unnamed Spell',
        level: parseInt(document.getElementById('spell-level').value),
        school: document.getElementById('spell-school').value,
        castingTime: document.getElementById('spell-casting-time').value || '1 action',
        range: document.getElementById('spell-range').value || 'Self',
        components: document.getElementById('spell-components').value || 'V, S',
        duration: document.getElementById('spell-duration').value || 'Instantaneous',
        description: document.getElementById('spell-description').value || '',
        atHigherLevels: document.getElementById('spell-higher').value || ''
    };
}

// Get item form data
function getItemFormData() {
    return {
        type: 'item',
        name: document.getElementById('item-name').value || 'Unnamed Item',
        itemType: document.getElementById('item-type').value,
        rarity: document.getElementById('item-rarity').value,
        attunement: document.getElementById('item-attunement').checked,
        description: document.getElementById('item-description').value || ''
    };
}

// Export homebrew content
function exportHomebrew(format) {
    const data = getFormData();
    let output = '';

    switch (format) {
        case 'json':
            output = exportToJSON(data);
            break;
        case 'markdown':
            output = exportToMarkdown(data);
            break;
        case 'card':
            const card = homebrewToCard(data);
            addToCardQueue(card);
            showNotification('Added to card queue!');
            showTab('cards');
            return;
    }

    // Show export output
    document.getElementById('export-output').style.display = 'block';
    document.getElementById('export-textarea').value = output;
}

// Export to JSON
function exportToJSON(data) {
    const jsonData = convertToExportJSON(data);
    return JSON.stringify(jsonData, null, 2);
}

// Convert form data to export JSON format
function convertToExportJSON(data) {
    switch (data.type) {
        case 'monster':
            return {
                name: data.name,
                size: data.size,
                type: data.monsterType,
                ac: data.ac,
                hp: data.hp,
                speed: data.speed,
                str: data.str,
                dex: data.dex,
                con: data.con,
                int: data.int,
                wis: data.wis,
                cha: data.cha,
                cr: parseFloat(data.cr),
                cr_display: formatCRDisplay(data.cr),
                actions: data.actions,
                traits: [],
                source: 'homebrew'
            };

        case 'spell':
            return {
                name: data.name,
                level: data.level,
                school: data.school,
                casting_time: data.castingTime,
                range: data.range,
                components: data.components,
                duration: data.duration,
                description: data.description,
                at_higher_levels: data.atHigherLevels || null,
                classes: [],
                source: 'homebrew'
            };

        case 'item':
            return {
                name: data.name,
                type: data.itemType,
                rarity: data.rarity,
                attunement: data.attunement,
                description: data.description,
                source: 'homebrew'
            };
    }
}

// Export to Markdown
function exportToMarkdown(data) {
    switch (data.type) {
        case 'monster':
            return monsterToMarkdown(data);
        case 'spell':
            return spellToMarkdown(data);
        case 'item':
            return itemToMarkdown(data);
    }
}

// Monster to Markdown
function monsterToMarkdown(data) {
    const sizeCap = capitalizeFirst(data.size);
    const typeCap = capitalizeFirst(data.monsterType);

    let md = `# ${data.name}\n\n`;
    md += `*${sizeCap} ${typeCap}*\n\n`;
    md += `---\n\n`;
    md += `**Armor Class** ${data.ac}\n\n`;
    md += `**Hit Points** ${data.hp}\n\n`;
    md += `**Speed** ${data.speed}\n\n`;
    md += `---\n\n`;
    md += `| STR | DEX | CON | INT | WIS | CHA |\n`;
    md += `|:---:|:---:|:---:|:---:|:---:|:---:|\n`;
    md += `| ${data.str} (${getModifier(data.str)}) | ${data.dex} (${getModifier(data.dex)}) | ${data.con} (${getModifier(data.con)}) | ${data.int} (${getModifier(data.int)}) | ${data.wis} (${getModifier(data.wis)}) | ${data.cha} (${getModifier(data.cha)}) |\n\n`;
    md += `---\n\n`;
    md += `**Challenge** ${formatCRDisplay(data.cr)}\n\n`;

    if (data.actions && data.actions.length > 0) {
        md += `## Actions\n\n`;
        data.actions.forEach(action => {
            md += `***${action.name}.*** ${action.description}\n\n`;
        });
    }

    return md;
}

// Spell to Markdown
function spellToMarkdown(data) {
    const levelSchool = data.level === 0
        ? `*${capitalizeFirst(data.school)} cantrip*`
        : `*${ordinal(data.level)}-level ${data.school}*`;

    let md = `# ${data.name}\n\n`;
    md += `${levelSchool}\n\n`;
    md += `---\n\n`;
    md += `**Casting Time:** ${data.castingTime}\n\n`;
    md += `**Range:** ${data.range}\n\n`;
    md += `**Components:** ${data.components}\n\n`;
    md += `**Duration:** ${data.duration}\n\n`;
    md += `---\n\n`;
    md += `${data.description}\n\n`;

    if (data.atHigherLevels) {
        md += `**At Higher Levels.** ${data.atHigherLevels}\n\n`;
    }

    return md;
}

// Item to Markdown
function itemToMarkdown(data) {
    const typeCap = capitalizeFirst(data.itemType);
    const rarityCap = capitalizeFirst(data.rarity.replace('-', ' '));
    const attunement = data.attunement ? ' (requires attunement)' : '';

    let md = `# ${data.name}\n\n`;
    md += `*${typeCap}, ${rarityCap}${attunement}*\n\n`;
    md += `---\n\n`;
    md += `${data.description}\n\n`;

    return md;
}

// Convert homebrew to card format
function homebrewToCard(data) {
    switch (data.type) {
        case 'monster':
            return monsterToCard(data);
        case 'spell':
            return spellToCard(data);
        case 'item':
            return itemToCard(data);
    }
}

// Monster to card
function monsterToCard(data) {
    const contents = [
        `subtitle | ${capitalizeFirst(data.size)} ${capitalizeFirst(data.monsterType)}`,
        'rule',
        `property | AC | ${data.ac}`,
        `property | HP | ${data.hp}`,
        `property | Speed | ${data.speed}`,
        `property | CR | ${formatCRDisplay(data.cr)}`,
        'rule',
        `dndstats | ${data.str} | ${data.dex} | ${data.con} | ${data.int} | ${data.wis} | ${data.cha}`
    ];

    if (data.actions && data.actions.length > 0) {
        contents.push('rule');
        contents.push('section | Actions');
        data.actions.forEach(action => {
            contents.push(`text | <b>${action.name}.</b> ${action.description}`);
        });
    }

    return {
        count: 1,
        title: data.name,
        color_front: 'FireBrick',
        icon_front: 'monster-grasp',
        icon_back: 'monster-grasp',
        contents: contents,
        tags: ['monster', 'homebrew']
    };
}

// Spell to card
function spellToCard(data) {
    const levelText = data.level === 0 ? 'Cantrip' : `${ordinal(data.level)} level`;

    const contents = [
        `subtitle | ${levelText} ${capitalizeFirst(data.school)}`,
        'rule',
        `property | Casting Time | ${data.castingTime}`,
        `property | Range | ${data.range}`,
        `property | Components | ${data.components}`,
        `property | Duration | ${data.duration}`,
        'rule',
        'fill | 1',
        `text | ${data.description}`
    ];

    if (data.atHigherLevels) {
        contents.push('fill | 1');
        contents.push('section | At Higher Levels');
        contents.push(`text | ${data.atHigherLevels}`);
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
        title: data.name,
        color_front: schoolColors[data.school] || 'Maroon',
        icon_front: 'white-book-1',
        icon_back: 'robe',
        contents: contents,
        tags: ['spell', 'homebrew', data.school]
    };
}

// Item to card
function itemToCard(data) {
    const attunementText = data.attunement ? ' (requires attunement)' : '';

    const contents = [
        `subtitle | ${capitalizeFirst(data.itemType)}, ${capitalizeFirst(data.rarity.replace('-', ' '))}${attunementText}`,
        'rule',
        'fill | 2',
        `text | ${data.description}`,
        'fill | 3'
    ];

    // Color based on rarity
    const rarityColors = {
        'common': 'Gray',
        'uncommon': 'ForestGreen',
        'rare': 'RoyalBlue',
        'very-rare': 'MediumPurple',
        'legendary': 'Goldenrod',
        'artifact': 'OrangeRed'
    };

    // Icon based on type
    const typeIcons = {
        'weapon': 'mixed-swords',
        'armor': 'breastplate',
        'wondrous': 'crystal-ball',
        'potion': 'drink-me',
        'ring': 'ring',
        'rod': 'crystal-wand',
        'scroll': 'scroll-unfurled',
        'staff': 'wizard-staff',
        'wand': 'fairy-wand'
    };

    return {
        count: 1,
        title: data.name,
        color_front: rarityColors[data.rarity] || 'Gray',
        icon_front: typeIcons[data.itemType] || 'swap-bag',
        icon_back: 'swap-bag',
        contents: contents,
        tags: ['item', 'homebrew', data.rarity]
    };
}

// Copy export text to clipboard
function copyExport() {
    const textarea = document.getElementById('export-textarea');
    copyTextToClipboard(textarea.value);
}

// Helper: format CR display
function formatCRDisplay(cr) {
    const crNum = parseFloat(cr);
    if (crNum === 0.125) return '1/8';
    if (crNum === 0.25) return '1/4';
    if (crNum === 0.5) return '1/2';
    return cr.toString();
}
