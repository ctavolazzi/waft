'use client';

import Image from 'next/image';
import { Card, frameColors, rarityColors } from '@/data/cards';

interface CardComponentProps {
  card: Card;
  size?: 'sm' | 'md' | 'lg';
  onClick?: () => void;
}

export default function CardComponent({ card, size = 'md', onClick }: CardComponentProps) {
  const colors = frameColors[card.frameColor] || frameColors.artifact;
  const rarityColor = rarityColors[card.rarity];
  
  const sizeClasses = {
    sm: 'w-[180px] h-[252px]',
    md: 'w-[250px] h-[350px]',
    lg: 'w-[300px] h-[420px]',
  };
  
  const textSizes = {
    sm: { name: 'text-xs', type: 'text-[9px]', body: 'text-[8px]', pt: 'text-xs' },
    md: { name: 'text-sm', type: 'text-[11px]', body: 'text-[11px]', pt: 'text-sm' },
    lg: { name: 'text-base', type: 'text-xs', body: 'text-xs', pt: 'text-base' },
  };

  const isCreature = card.typeLine.toLowerCase().includes('creature');
  const ts = textSizes[size];

  return (
    <div
      className={`${sizeClasses[size]} rounded-xl border border-[#333] flex flex-col overflow-hidden card-hover cursor-pointer`}
      style={{
        background: `linear-gradient(135deg, ${colors.primary} 0%, ${colors.secondary} 100%)`,
        color: colors.text,
      }}
      onClick={onClick}
    >
      {/* Header */}
      <div className="flex justify-between items-center px-3 py-2 bg-black/20">
        <span className={`font-bold ${ts.name} truncate flex-1`}>{card.name}</span>
        <span className={`font-mono ${ts.name} bg-white/15 px-1.5 py-0.5 rounded ml-2`}>
          {card.manaCost || '—'}
        </span>
      </div>

      {/* Art */}
      <div className="flex-shrink-0 mx-2 mt-1 bg-black/30 border border-white/20 rounded flex items-center justify-center overflow-hidden"
           style={{ height: size === 'sm' ? '90px' : size === 'md' ? '130px' : '160px' }}>
        {card.artPath ? (
          <Image
            src={card.artPath}
            alt={card.name}
            width={size === 'sm' ? 80 : size === 'md' ? 120 : 150}
            height={size === 'sm' ? 80 : size === 'md' ? 120 : 150}
            className="pixel-art object-contain"
          />
        ) : (
          <div className="text-white/30 text-center p-2">
            <div className="text-2xl mb-1">✨</div>
            <div className="text-[10px]">Art Coming</div>
          </div>
        )}
      </div>

      {/* Type Line */}
      <div className={`${ts.type} italic px-3 py-1.5 bg-black/15 border-t border-white/10`}>
        {card.typeLine}
      </div>

      {/* Body */}
      <div className={`flex-1 px-3 py-2 ${ts.body} leading-relaxed overflow-y-auto`}>
        <div className="mb-2">{card.abilities}</div>
        {card.flavorText && (
          <div className="italic opacity-80 pt-2 border-t border-white/15 text-[10px]">
            {card.flavorText}
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="flex justify-between items-center px-3 py-1.5 bg-black/20">
        <span 
          className={`${ts.type} font-bold`}
          style={{ color: rarityColor }}
        >
          {card.setSymbol}
        </span>
        {isCreature && card.power !== undefined && (
          <div className={`bg-black/40 px-2 py-1 rounded font-bold ${ts.pt}`}>
            {card.power}/{card.toughness}
          </div>
        )}
      </div>
    </div>
  );
}
