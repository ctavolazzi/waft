/**
 * Deck data structures for Teleport Massive Card Game.
 * 
 * A Deck is a collection of cards with metadata, validation, and statistics.
 */

import { Card, cards, getCardType, parseCMC } from './cards';

// ============================================================================
// Types
// ============================================================================

/**
 * An entry in a deck - a card with a count.
 */
export interface DeckEntry {
  cardId: string;
  count: number;
}

/**
 * Deck statistics.
 */
export interface DeckStats {
  totalCards: number;
  uniqueCards: number;
  creatures: number;
  instants: number;
  sorceries: number;
  enchantments: number;
  artifacts: number;
  lands: number;
  averageCMC: number;
  colorDistribution: Record<string, number>;
  rarityDistribution: Record<string, number>;
  cmcCurve: Record<number, number>;
}

/**
 * A deck in the Teleport Massive Card Game.
 */
export interface Deck {
  id: string;
  name: string;
  description: string;
  author: string;
  entries: DeckEntry[];
  format: 'standard' | 'casual' | 'competitive';
  tags: string[];
  createdAt: string;
  updatedAt: string;
}

/**
 * Deck constraints for validation.
 */
export interface DeckConstraints {
  minSize: number;
  maxSize: number;
  maxCopies: number;
}

export const DEFAULT_CONSTRAINTS: DeckConstraints = {
  minSize: 40,
  maxSize: 60,
  maxCopies: 4,
};

// ============================================================================
// Utilities
// ============================================================================

/**
 * Get the Card object for a deck entry.
 */
export function getCard(cardId: string): Card | undefined {
  return cards.find(c => c.id === cardId);
}

/**
 * Expand deck entries into full card list.
 */
export function expandDeck(deck: Deck): Card[] {
  const result: Card[] = [];
  for (const entry of deck.entries) {
    const card = getCard(entry.cardId);
    if (card) {
      for (let i = 0; i < entry.count; i++) {
        result.push(card);
      }
    }
  }
  return result;
}

/**
 * Calculate deck statistics.
 */
export function calculateStats(deck: Deck): DeckStats {
  const expandedCards = expandDeck(deck);
  
  if (expandedCards.length === 0) {
    return {
      totalCards: 0,
      uniqueCards: 0,
      creatures: 0,
      instants: 0,
      sorceries: 0,
      enchantments: 0,
      artifacts: 0,
      lands: 0,
      averageCMC: 0,
      colorDistribution: {},
      rarityDistribution: {},
      cmcCurve: {},
    };
  }

  // Count by type
  const byType = expandedCards.reduce((acc, card) => {
    const type = getCardType(card.typeLine);
    acc[type] = (acc[type] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  // Color distribution (from mana costs)
  const colorDistribution: Record<string, number> = {};
  for (const card of expandedCards) {
    for (const char of card.manaCost.toUpperCase()) {
      if ('WUBRG'.includes(char)) {
        colorDistribution[char] = (colorDistribution[char] || 0) + 1;
      }
    }
  }

  // Rarity distribution
  const rarityDistribution = expandedCards.reduce((acc, card) => {
    acc[card.rarity] = (acc[card.rarity] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  // CMC curve (excluding lands)
  const nonLands = expandedCards.filter(c => getCardType(c.typeLine) !== 'land');
  const cmcCurve = nonLands.reduce((acc, card) => {
    const cmc = parseCMC(card.manaCost);
    acc[cmc] = (acc[cmc] || 0) + 1;
    return acc;
  }, {} as Record<number, number>);

  // Average CMC
  const totalCMC = nonLands.reduce((sum, card) => sum + parseCMC(card.manaCost), 0);
  const averageCMC = nonLands.length > 0 ? totalCMC / nonLands.length : 0;

  return {
    totalCards: expandedCards.length,
    uniqueCards: deck.entries.length,
    creatures: byType.creature || 0,
    instants: byType.instant || 0,
    sorceries: byType.sorcery || 0,
    enchantments: byType.enchantment || 0,
    artifacts: byType.artifact || 0,
    lands: byType.land || 0,
    averageCMC: Math.round(averageCMC * 100) / 100,
    colorDistribution,
    rarityDistribution,
    cmcCurve,
  };
}

/**
 * Validate a deck against constraints.
 */
export function validateDeck(
  deck: Deck,
  constraints: DeckConstraints = DEFAULT_CONSTRAINTS
): { valid: boolean; errors: string[] } {
  const errors: string[] = [];
  const stats = calculateStats(deck);

  // Check size
  if (stats.totalCards < constraints.minSize) {
    errors.push(`Deck has ${stats.totalCards} cards, minimum is ${constraints.minSize}`);
  }
  if (stats.totalCards > constraints.maxSize) {
    errors.push(`Deck has ${stats.totalCards} cards, maximum is ${constraints.maxSize}`);
  }

  // Check max copies (except basic lands would be exempt, but we have none)
  for (const entry of deck.entries) {
    if (entry.count > constraints.maxCopies) {
      const card = getCard(entry.cardId);
      errors.push(`'${card?.name || entry.cardId}' has ${entry.count} copies, maximum is ${constraints.maxCopies}`);
    }
  }

  return { valid: errors.length === 0, errors };
}

/**
 * Export deck as text decklist.
 */
export function exportDecklist(deck: Deck): string {
  const lines = [
    `// ${deck.name}`,
    deck.description ? `// ${deck.description}` : '',
    `// Author: ${deck.author}`,
    `// Format: ${deck.format}`,
    '',
  ];

  // Group by type
  const byType: Record<string, Array<{ name: string; count: number }>> = {};
  for (const entry of deck.entries) {
    const card = getCard(entry.cardId);
    if (card) {
      const type = getCardType(card.typeLine);
      if (!byType[type]) byType[type] = [];
      byType[type].push({ name: card.name, count: entry.count });
    }
  }

  // Output each type
  const typeOrder = ['creature', 'instant', 'sorcery', 'enchantment', 'artifact', 'land'];
  for (const type of typeOrder) {
    const typeCards = byType[type];
    if (typeCards && typeCards.length > 0) {
      const total = typeCards.reduce((sum, c) => sum + c.count, 0);
      lines.push(`// ${type.charAt(0).toUpperCase() + type.slice(1)}s (${total})`);
      for (const { name, count } of typeCards.sort((a, b) => a.name.localeCompare(b.name))) {
        lines.push(`${count}x ${name}`);
      }
      lines.push('');
    }
  }

  return lines.filter(l => l !== undefined).join('\n');
}

// ============================================================================
// Starter Decks
// ============================================================================

/**
 * "Quantum Control" - The official starter deck.
 * 
 * Theme: Blue-focused control deck centered around Aziah Calderon and
 * the quantum mechanics of Teleport Massive. Uses entanglement, observation,
 * and reality manipulation to control the game.
 * 
 * Strategy: Control the board early with cheap scientists, draw cards,
 * and win with powerful mythic finishers.
 */
export const STARTER_DECK_QUANTUM_CONTROL: Deck = {
  id: 'starter-quantum-control',
  name: 'Quantum Control',
  description: 'The official starter deck. Control the board with quantum mechanics and finish with legendary scientists.',
  author: 'Teleport Massive',
  format: 'standard',
  tags: ['starter', 'control', 'blue', 'official'],
  createdAt: '2026-01-20',
  updatedAt: '2026-01-20',
  entries: [
    // Creatures (16)
    { cardId: 'tm-001', count: 1 },  // Aziah Calderon (mythic legendary)
    { cardId: 'tm-002', count: 1 },  // Fai Wei (rare legendary)
    { cardId: 'tm-012', count: 4 },  // Grieving Scientist
    { cardId: 'tm-013', count: 4 },  // Quantum Observer
    { cardId: 'tm-017', count: 4 },  // Lab Assistant
    { cardId: 'tm-019', count: 2 },  // Corporate Security
    
    // Instants (8)
    { cardId: 'tm-003', count: 2 },  // Quantum Entanglement
    { cardId: 'tm-014', count: 2 },  // Probability Collapse
    { cardId: 'tm-020', count: 4 },  // Dr. Chen's Discovery
    
    // Sorceries (4)
    { cardId: 'tm-005', count: 2 },  // Reality Fracture
    { cardId: 'tm-016', count: 2 },  // Entangled Souls
    
    // Enchantments (6)
    { cardId: 'tm-004', count: 2 },  // Scint Protocol
    { cardId: 'tm-007', count: 2 },  // Chen Stabilization Protocol
    { cardId: 'tm-018', count: 2 },  // Recursive Timeline
    
    // Artifacts (6)
    { cardId: 'tm-008', count: 2 },  // Research & Development
    { cardId: 'tm-009', count: 1 },  // SWAB (mythic legendary)
    { cardId: 'tm-010', count: 1 },  // SWAE (mythic legendary)
    { cardId: 'tm-015', count: 2 },  // Scint Detector
    
    // Lands (4)
    { cardId: 'tm-006', count: 4 },  // Teleport Massive HQ
  ],
};

/**
 * "The Vibration" - An aggressive combo deck.
 * 
 * Theme: Multicolor deck focused on The Vibration mythic and
 * reality-bending effects. Exiles and returns permanents for value.
 */
export const STARTER_DECK_THE_VIBRATION: Deck = {
  id: 'starter-the-vibration',
  name: 'The Vibration',
  description: 'An aggressive deck that bends reality to win. Center your strategy around The Vibration.',
  author: 'Teleport Massive',
  format: 'standard',
  tags: ['starter', 'combo', 'multicolor', 'official'],
  createdAt: '2026-01-20',
  updatedAt: '2026-01-20',
  entries: [
    // Creatures (18)
    { cardId: 'tm-002', count: 2 },  // Fai Wei
    { cardId: 'tm-012', count: 4 },  // Grieving Scientist
    { cardId: 'tm-013', count: 4 },  // Quantum Observer
    { cardId: 'tm-017', count: 4 },  // Lab Assistant
    { cardId: 'tm-019', count: 4 },  // Corporate Security
    
    // The Vibration & Support (8)
    { cardId: 'tm-011', count: 2 },  // The Vibration (mythic)
    { cardId: 'tm-003', count: 4 },  // Quantum Entanglement
    { cardId: 'tm-005', count: 2 },  // Reality Fracture
    
    // Card Advantage (8)
    { cardId: 'tm-008', count: 4 },  // Research & Development
    { cardId: 'tm-020', count: 4 },  // Dr. Chen's Discovery
    
    // Enchantments (4)
    { cardId: 'tm-004', count: 2 },  // Scint Protocol
    { cardId: 'tm-018', count: 2 },  // Recursive Timeline
    
    // Lands (6)
    { cardId: 'tm-006', count: 4 },  // Teleport Massive HQ
    // Note: Would need basic lands, but we don't have them yet
  ],
};

/**
 * All available starter decks.
 */
export const STARTER_DECKS: Deck[] = [
  STARTER_DECK_QUANTUM_CONTROL,
  STARTER_DECK_THE_VIBRATION,
];

/**
 * Get a starter deck by ID.
 */
export function getStarterDeck(id: string): Deck | undefined {
  return STARTER_DECKS.find(d => d.id === id);
}

/**
 * Create a new empty deck.
 */
export function createEmptyDeck(name: string = 'New Deck'): Deck {
  return {
    id: `deck-${Date.now()}`,
    name,
    description: '',
    author: '',
    entries: [],
    format: 'casual',
    tags: [],
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  };
}

/**
 * Clone a deck (for editing starter decks).
 */
export function cloneDeck(deck: Deck, newName?: string): Deck {
  return {
    ...deck,
    id: `deck-${Date.now()}`,
    name: newName || `${deck.name} (Copy)`,
    entries: deck.entries.map(e => ({ ...e })),
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  };
}

// ============================================================================
// LocalStorage Persistence
// ============================================================================

const STORAGE_KEY = 'teleport-massive-saved-decks';

/**
 * Get all saved decks from localStorage.
 */
export function getSavedDecks(): Deck[] {
  if (typeof window === 'undefined') return [];
  try {
    const data = localStorage.getItem(STORAGE_KEY);
    return data ? JSON.parse(data) : [];
  } catch {
    return [];
  }
}

/**
 * Save a deck to localStorage.
 */
export function saveDeck(deck: Deck): void {
  if (typeof window === 'undefined') return;
  const decks = getSavedDecks();
  const existingIndex = decks.findIndex(d => d.id === deck.id);
  
  const updatedDeck = { 
    ...deck, 
    updatedAt: new Date().toISOString() 
  };
  
  if (existingIndex >= 0) {
    decks[existingIndex] = updatedDeck;
  } else {
    decks.push(updatedDeck);
  }
  
  localStorage.setItem(STORAGE_KEY, JSON.stringify(decks));
}

/**
 * Delete a saved deck from localStorage.
 */
export function deleteSavedDeck(deckId: string): void {
  if (typeof window === 'undefined') return;
  const decks = getSavedDecks().filter(d => d.id !== deckId);
  localStorage.setItem(STORAGE_KEY, JSON.stringify(decks));
}

/**
 * Convert DeckCard array to Deck entries.
 */
export function cardsToDeckEntries(deckCards: Array<Card & { count: number }>): DeckEntry[] {
  return deckCards.map(card => ({
    cardId: card.id,
    count: card.count,
  }));
}
