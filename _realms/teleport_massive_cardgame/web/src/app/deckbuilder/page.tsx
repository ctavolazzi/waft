'use client';

import { useState, useMemo, useEffect } from 'react';
import CardComponent from '@/components/CardComponent';
import { cards, Card, getCardType, parseCMC } from '@/data/cards';
import { 
  STARTER_DECKS, 
  Deck, 
  DeckEntry,
  calculateStats, 
  getCard, 
  exportDecklist,
  getSavedDecks,
  saveDeck,
  deleteSavedDeck,
  cardsToDeckEntries,
  createEmptyDeck
} from '@/data/decks';

interface DeckCard extends Card {
  count: number;
}

export default function DeckBuilderPage() {
  const [deck, setDeck] = useState<DeckCard[]>([]);
  const [search, setSearch] = useState('');
  const [deckName, setDeckName] = useState('New Deck');
  const [deckId, setDeckId] = useState<string>(`deck-${Date.now()}`);
  const [showStarterDecks, setShowStarterDecks] = useState(false);
  const [showSavedDecks, setShowSavedDecks] = useState(false);
  const [savedDecks, setSavedDecks] = useState<Deck[]>([]);

  // Load saved decks on mount
  useEffect(() => {
    setSavedDecks(getSavedDecks());
  }, []);

  const filteredCards = useMemo(() => {
    if (!search) return cards;
    return cards.filter(card =>
      card.name.toLowerCase().includes(search.toLowerCase()) ||
      card.abilities.toLowerCase().includes(search.toLowerCase())
    );
  }, [search]);

  const addToDeck = (card: Card) => {
    setDeck(prev => {
      const existing = prev.find(c => c.id === card.id);
      if (existing) {
        if (existing.count >= 4) return prev; // Max 4 copies
        return prev.map(c => c.id === card.id ? { ...c, count: c.count + 1 } : c);
      }
      return [...prev, { ...card, count: 1 }];
    });
  };

  const removeFromDeck = (cardId: string) => {
    setDeck(prev => {
      const existing = prev.find(c => c.id === cardId);
      if (!existing) return prev;
      if (existing.count <= 1) {
        return prev.filter(c => c.id !== cardId);
      }
      return prev.map(c => c.id === cardId ? { ...c, count: c.count - 1 } : c);
    });
  };

  const clearDeck = () => setDeck([]);

  const loadDeckFromEntries = (entries: DeckEntry[], name: string, id?: string) => {
    const newDeck: DeckCard[] = [];
    for (const entry of entries) {
      const card = getCard(entry.cardId);
      if (card) {
        newDeck.push({ ...card, count: entry.count });
      }
    }
    setDeck(newDeck);
    setDeckName(name);
    setDeckId(id || `deck-${Date.now()}`);
  };

  const loadStarterDeck = (starterDeck: Deck) => {
    loadDeckFromEntries(starterDeck.entries, starterDeck.name);
    setShowStarterDecks(false);
  };

  const loadSavedDeck = (savedDeck: Deck) => {
    loadDeckFromEntries(savedDeck.entries, savedDeck.name, savedDeck.id);
    setShowSavedDecks(false);
  };

  const handleSaveDeck = () => {
    const deckToSave: Deck = {
      id: deckId,
      name: deckName,
      description: '',
      author: '',
      entries: cardsToDeckEntries(deck),
      format: 'casual',
      tags: [],
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };
    saveDeck(deckToSave);
    setSavedDecks(getSavedDecks());
    alert(`Deck "${deckName}" saved!`);
  };

  const handleDeleteSavedDeck = (id: string) => {
    if (confirm('Delete this saved deck?')) {
      deleteSavedDeck(id);
      setSavedDecks(getSavedDecks());
    }
  };

  const deckSize = deck.reduce((sum, c) => sum + c.count, 0);
  const avgCMC = deck.length > 0
    ? (deck.reduce((sum, c) => sum + parseCMC(c.manaCost) * c.count, 0) / deckSize).toFixed(1)
    : '0.0';

  const deckByType = useMemo(() => {
    const grouped: Record<string, DeckCard[]> = {};
    deck.forEach(card => {
      const type = getCardType(card.typeLine);
      if (!grouped[type]) grouped[type] = [];
      grouped[type].push(card);
    });
    return grouped;
  }, [deck]);

  const exportDeck = () => {
    let text = `// ${deckName}\n// ${deckSize} cards\n\n`;
    Object.entries(deckByType).forEach(([type, cards]) => {
      text += `// ${type.charAt(0).toUpperCase() + type.slice(1)}s (${cards.reduce((s, c) => s + c.count, 0)})\n`;
      cards.forEach(c => {
        text += `${c.count}x ${c.name}\n`;
      });
      text += '\n';
    });
    
    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${deckName.replace(/\s+/g, '_').toLowerCase()}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold mb-3">Deck Builder</h1>
        <p className="text-white/60">Create your ultimate Teleport Massive deck</p>
        <div className="flex justify-center gap-3 mt-4">
          <button
            onClick={() => setShowStarterDecks(true)}
            className="px-6 py-2 bg-[#C9A227]/20 hover:bg-[#C9A227]/30 text-[#C9A227] border border-[#C9A227]/30 rounded-lg transition-colors"
          >
            📦 Starter Decks
          </button>
          <button
            onClick={() => { setSavedDecks(getSavedDecks()); setShowSavedDecks(true); }}
            className="px-6 py-2 bg-[#0A6FA3]/20 hover:bg-[#0A6FA3]/30 text-[#0A6FA3] border border-[#0A6FA3]/30 rounded-lg transition-colors"
          >
            💾 My Decks {savedDecks.length > 0 && `(${savedDecks.length})`}
          </button>
        </div>
      </div>

      {/* Starter Decks Modal */}
      {showStarterDecks && (
        <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4" onClick={() => setShowStarterDecks(false)}>
          <div className="bg-[#1a1a24] rounded-2xl p-6 max-w-4xl w-full max-h-[90vh] overflow-y-auto border border-white/10" onClick={e => e.stopPropagation()}>
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold">Starter Decks</h2>
              <button onClick={() => setShowStarterDecks(false)} className="text-white/40 hover:text-white text-2xl">×</button>
            </div>
            
            <p className="text-white/60 mb-6">
              Choose a pre-built deck to start with. You can customize it after loading.
            </p>
            
            <div className="grid gap-4">
              {STARTER_DECKS.map(starterDeck => {
                const stats = calculateStats(starterDeck);
                return (
                  <div key={starterDeck.id} className="p-4 rounded-xl bg-white/5 border border-white/10 hover:border-[#0A6FA3]/50 transition-colors">
                    <div className="flex justify-between items-start mb-3">
                      <div>
                        <h3 className="text-xl font-bold text-white">{starterDeck.name}</h3>
                        <p className="text-white/60 text-sm mt-1">{starterDeck.description}</p>
                      </div>
                      <button
                        onClick={() => loadStarterDeck(starterDeck)}
                        className="px-4 py-2 bg-[#0A6FA3] hover:bg-[#0A6FA3]/80 text-white rounded-lg transition-colors flex-shrink-0"
                      >
                        Load Deck
                      </button>
                    </div>
                    
                    <div className="flex flex-wrap gap-2 mt-3">
                      <span className="px-2 py-1 bg-white/10 rounded text-xs text-white/60">
                        {stats.totalCards} cards
                      </span>
                      <span className="px-2 py-1 bg-blue-500/20 rounded text-xs text-blue-400">
                        {stats.creatures} creatures
                      </span>
                      <span className="px-2 py-1 bg-purple-500/20 rounded text-xs text-purple-400">
                        {stats.instants + stats.sorceries} spells
                      </span>
                      <span className="px-2 py-1 bg-[#C9A227]/20 rounded text-xs text-[#C9A227]">
                        Avg CMC: {stats.averageCMC}
                      </span>
                      {starterDeck.tags.map(tag => (
                        <span key={tag} className="px-2 py-1 bg-white/5 rounded text-xs text-white/40">
                          #{tag}
                        </span>
                      ))}
                    </div>
                  </div>
                );
              })}
            </div>
            
            <div className="mt-6 pt-4 border-t border-white/10 text-center">
              <p className="text-white/40 text-sm">
                Tip: Starter decks are great for learning the game. Customize them to fit your playstyle!
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Saved Decks Modal */}
      {showSavedDecks && (
        <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4" onClick={() => setShowSavedDecks(false)}>
          <div className="bg-[#1a1a24] rounded-2xl p-6 max-w-4xl w-full max-h-[90vh] overflow-y-auto border border-white/10" onClick={e => e.stopPropagation()}>
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold">My Saved Decks</h2>
              <button onClick={() => setShowSavedDecks(false)} className="text-white/40 hover:text-white text-2xl">×</button>
            </div>
            
            {savedDecks.length === 0 ? (
              <div className="text-center py-12 text-white/40">
                <div className="text-4xl mb-4">📭</div>
                <p>No saved decks yet</p>
                <p className="text-sm mt-2">Build a deck and click Save to store it here</p>
              </div>
            ) : (
              <div className="grid gap-4">
                {savedDecks.map(savedDeck => {
                  const stats = calculateStats(savedDeck);
                  return (
                    <div key={savedDeck.id} className="p-4 rounded-xl bg-white/5 border border-white/10 hover:border-[#0A6FA3]/50 transition-colors">
                      <div className="flex justify-between items-start">
                        <div className="flex-1">
                          <h3 className="text-xl font-bold text-white">{savedDeck.name}</h3>
                          <p className="text-white/40 text-xs mt-1">
                            Last updated: {new Date(savedDeck.updatedAt).toLocaleDateString()}
                          </p>
                        </div>
                        <div className="flex gap-2">
                          <button
                            onClick={() => loadSavedDeck(savedDeck)}
                            className="px-4 py-2 bg-[#0A6FA3] hover:bg-[#0A6FA3]/80 text-white rounded-lg transition-colors"
                          >
                            Load
                          </button>
                          <button
                            onClick={() => handleDeleteSavedDeck(savedDeck.id)}
                            className="px-3 py-2 bg-red-500/20 hover:bg-red-500/40 text-red-400 rounded-lg transition-colors"
                          >
                            🗑
                          </button>
                        </div>
                      </div>
                      
                      <div className="flex flex-wrap gap-2 mt-3">
                        <span className="px-2 py-1 bg-white/10 rounded text-xs text-white/60">
                          {stats.totalCards} cards
                        </span>
                        <span className="px-2 py-1 bg-blue-500/20 rounded text-xs text-blue-400">
                          {stats.creatures} creatures
                        </span>
                        <span className="px-2 py-1 bg-[#C9A227]/20 rounded text-xs text-[#C9A227]">
                          Avg CMC: {stats.averageCMC}
                        </span>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Card Pool (left) */}
        <div className="lg:col-span-2">
          <div className="mb-4">
            <input
              type="text"
              placeholder="Search cards..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full px-4 py-2 rounded-lg bg-white/5 border border-white/20 text-white placeholder:text-white/40 focus:outline-none focus:border-[#0A6FA3]"
            />
          </div>

          <div className="flex flex-wrap gap-4">
            {filteredCards.map((card) => (
              <div key={card.id} className="relative group">
                <CardComponent card={card} size="sm" onClick={() => addToDeck(card)} />
                <button
                  onClick={() => addToDeck(card)}
                  className="absolute inset-0 bg-[#0A6FA3]/80 opacity-0 group-hover:opacity-100 flex items-center justify-center rounded-xl transition-opacity"
                >
                  <span className="text-white font-bold text-lg">+ Add</span>
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Deck Panel (right) */}
        <div className="lg:col-span-1">
          <div className="sticky top-24 bg-white/5 border border-white/10 rounded-xl p-4">
            {/* Deck Header */}
            <div className="mb-4">
              <input
                type="text"
                value={deckName}
                onChange={(e) => setDeckName(e.target.value)}
                className="w-full text-xl font-bold bg-transparent border-b border-white/20 pb-1 focus:outline-none focus:border-[#0A6FA3]"
              />
            </div>

            {/* Deck Stats */}
            <div className="grid grid-cols-2 gap-2 mb-4">
              <div className="bg-white/5 rounded-lg p-2 text-center">
                <div className="text-2xl font-bold text-[#0A6FA3]">{deckSize}</div>
                <div className="text-xs text-white/40">Cards</div>
              </div>
              <div className="bg-white/5 rounded-lg p-2 text-center">
                <div className="text-2xl font-bold text-[#C9A227]">{avgCMC}</div>
                <div className="text-xs text-white/40">Avg CMC</div>
              </div>
            </div>

            {/* Deck Validation */}
            <div className={`mb-4 p-2 rounded-lg text-sm ${
              deckSize >= 40 && deckSize <= 60
                ? 'bg-green-500/20 text-green-400'
                : deckSize > 60
                  ? 'bg-red-500/20 text-red-400'
                  : 'bg-yellow-500/20 text-yellow-400'
            }`}>
              {deckSize < 40 && `Need ${40 - deckSize} more cards (min 40)`}
              {deckSize >= 40 && deckSize <= 60 && '✓ Deck is valid'}
              {deckSize > 60 && `Remove ${deckSize - 60} cards (max 60)`}
            </div>

            {/* Deck List */}
            <div className="max-h-[400px] overflow-y-auto mb-4">
              {Object.entries(deckByType).map(([type, typeCards]) => (
                <div key={type} className="mb-3">
                  <div className="text-xs text-white/40 uppercase tracking-wider mb-1">
                    {type} ({typeCards.reduce((s, c) => s + c.count, 0)})
                  </div>
                  {typeCards.map(card => (
                    <div
                      key={card.id}
                      className="flex items-center justify-between py-1 px-2 rounded hover:bg-white/5 group"
                    >
                      <span className="text-sm truncate flex-1">
                        {card.count}x {card.name}
                      </span>
                      <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                        <button
                          onClick={() => removeFromDeck(card.id)}
                          className="w-6 h-6 bg-red-500/20 hover:bg-red-500/40 text-red-400 rounded text-sm"
                        >
                          -
                        </button>
                        <button
                          onClick={() => addToDeck(card)}
                          disabled={card.count >= 4}
                          className="w-6 h-6 bg-green-500/20 hover:bg-green-500/40 text-green-400 rounded text-sm disabled:opacity-30"
                        >
                          +
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              ))}

              {deck.length === 0 && (
                <div className="text-center py-8 text-white/30">
                  <div className="text-3xl mb-2">📦</div>
                  <p>Your deck is empty</p>
                  <p className="text-xs">Click cards to add them</p>
                </div>
              )}
            </div>

            {/* Actions */}
            <div className="grid grid-cols-3 gap-2">
              <button
                onClick={handleSaveDeck}
                disabled={deck.length === 0}
                className="py-2 bg-green-500/20 hover:bg-green-500/30 text-green-400 disabled:opacity-30 rounded-lg transition-colors"
              >
                💾 Save
              </button>
              <button
                onClick={exportDeck}
                disabled={deck.length === 0}
                className="py-2 bg-[#0A6FA3] hover:bg-[#0A6FA3]/80 disabled:opacity-30 rounded-lg transition-colors"
              >
                📤 Export
              </button>
              <button
                onClick={clearDeck}
                disabled={deck.length === 0}
                className="py-2 bg-white/10 hover:bg-white/20 disabled:opacity-30 rounded-lg transition-colors"
              >
                🗑 Clear
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
