'use client';

import { useState, useMemo } from 'react';
import CardComponent from '@/components/CardComponent';
import { cards, Card, getCardType, rarityColors } from '@/data/cards';

export default function CardsPage() {
  const [search, setSearch] = useState('');
  const [typeFilter, setTypeFilter] = useState<string>('all');
  const [rarityFilter, setRarityFilter] = useState<string>('all');
  const [selectedCard, setSelectedCard] = useState<Card | null>(null);

  const cardTypes = ['all', 'creature', 'instant', 'sorcery', 'enchantment', 'artifact', 'land'];
  const rarities = ['all', 'common', 'uncommon', 'rare', 'mythic'];

  const filteredCards = useMemo(() => {
    return cards.filter(card => {
      const matchesSearch = card.name.toLowerCase().includes(search.toLowerCase()) ||
                           card.abilities.toLowerCase().includes(search.toLowerCase());
      const matchesType = typeFilter === 'all' || getCardType(card.typeLine) === typeFilter;
      const matchesRarity = rarityFilter === 'all' || card.rarity === rarityFilter;
      return matchesSearch && matchesType && matchesRarity;
    });
  }, [search, typeFilter, rarityFilter]);

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="text-center mb-10">
        <h1 className="text-4xl font-bold mb-3">Card Gallery</h1>
        <p className="text-white/60">Browse all cards in the Teleport Massive set</p>
      </div>

      {/* Filters */}
      <div className="mb-8 p-4 rounded-xl bg-white/5 border border-white/10">
        <div className="flex flex-wrap gap-4 items-center">
          {/* Search */}
          <div className="flex-1 min-w-[200px]">
            <input
              type="text"
              placeholder="Search cards..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full px-4 py-2 rounded-lg bg-white/5 border border-white/20 text-white placeholder:text-white/40 focus:outline-none focus:border-[#0A6FA3]"
            />
          </div>

          {/* Type Filter */}
          <select
            value={typeFilter}
            onChange={(e) => setTypeFilter(e.target.value)}
            className="px-4 py-2 rounded-lg bg-white/5 border border-white/20 text-white focus:outline-none focus:border-[#0A6FA3]"
          >
            {cardTypes.map(type => (
              <option key={type} value={type} className="bg-[#1a1a24]">
                {type === 'all' ? 'All Types' : type.charAt(0).toUpperCase() + type.slice(1)}
              </option>
            ))}
          </select>

          {/* Rarity Filter */}
          <select
            value={rarityFilter}
            onChange={(e) => setRarityFilter(e.target.value)}
            className="px-4 py-2 rounded-lg bg-white/5 border border-white/20 text-white focus:outline-none focus:border-[#0A6FA3]"
          >
            {rarities.map(rarity => (
              <option key={rarity} value={rarity} className="bg-[#1a1a24]">
                {rarity === 'all' ? 'All Rarities' : rarity.charAt(0).toUpperCase() + rarity.slice(1)}
              </option>
            ))}
          </select>

          {/* Results count */}
          <div className="text-white/40 text-sm">
            {filteredCards.length} card{filteredCards.length !== 1 ? 's' : ''}
          </div>
        </div>
      </div>

      {/* Card Grid */}
      <div className="flex flex-wrap justify-center gap-6">
        {filteredCards.map((card) => (
          <CardComponent
            key={card.id}
            card={card}
            size="md"
            onClick={() => setSelectedCard(card)}
          />
        ))}
      </div>

      {filteredCards.length === 0 && (
        <div className="text-center py-20 text-white/40">
          <div className="text-4xl mb-4">🔍</div>
          <p>No cards found matching your filters</p>
        </div>
      )}

      {/* Card Detail Modal */}
      {selectedCard && (
        <div
          className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4"
          onClick={() => setSelectedCard(null)}
        >
          <div
            className="bg-[#1a1a24] rounded-2xl p-6 max-w-2xl w-full max-h-[90vh] overflow-y-auto border border-white/10"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex flex-col md:flex-row gap-6">
              {/* Card Preview */}
              <div className="flex-shrink-0 flex justify-center">
                <CardComponent card={selectedCard} size="lg" />
              </div>

              {/* Card Details */}
              <div className="flex-1">
                <h2 className="text-2xl font-bold mb-2">{selectedCard.name}</h2>
                <p className="text-white/60 mb-4">{selectedCard.typeLine}</p>

                <div className="space-y-4">
                  <div>
                    <div className="text-white/40 text-sm mb-1">Mana Cost</div>
                    <div className="font-mono text-lg">{selectedCard.manaCost || 'None'}</div>
                  </div>

                  <div>
                    <div className="text-white/40 text-sm mb-1">Rarity</div>
                    <div 
                      className="inline-block px-3 py-1 rounded-full text-sm font-medium"
                      style={{ 
                        backgroundColor: `${rarityColors[selectedCard.rarity]}20`,
                        color: rarityColors[selectedCard.rarity]
                      }}
                    >
                      {selectedCard.rarity.charAt(0).toUpperCase() + selectedCard.rarity.slice(1)}
                    </div>
                  </div>

                  <div>
                    <div className="text-white/40 text-sm mb-1">Abilities</div>
                    <div className="text-white/90 leading-relaxed">{selectedCard.abilities}</div>
                  </div>

                  {selectedCard.flavorText && (
                    <div>
                      <div className="text-white/40 text-sm mb-1">Flavor Text</div>
                      <div className="italic text-white/60">{selectedCard.flavorText}</div>
                    </div>
                  )}

                  {selectedCard.power !== undefined && (
                    <div>
                      <div className="text-white/40 text-sm mb-1">Power/Toughness</div>
                      <div className="text-xl font-bold">{selectedCard.power}/{selectedCard.toughness}</div>
                    </div>
                  )}
                </div>

                <button
                  onClick={() => setSelectedCard(null)}
                  className="mt-6 w-full py-2 bg-white/10 hover:bg-white/20 rounded-lg transition-colors"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
