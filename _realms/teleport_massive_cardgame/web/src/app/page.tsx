import Link from 'next/link';
import CardComponent from '@/components/CardComponent';
import { cards } from '@/data/cards';

export default function Home() {
  // Featured cards (mythics)
  const featuredCards = cards.filter(c => c.rarity === 'mythic').slice(0, 3);

  return (
    <div className="relative">
      {/* Hero Section */}
      <section className="relative overflow-hidden py-20 px-4">
        {/* Background effects */}
        <div className="absolute inset-0 quantum-lines" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-[#0A6FA3]/10 rounded-full blur-[100px]" />
        
        <div className="relative max-w-6xl mx-auto text-center">
          <div className="inline-block mb-6 px-4 py-1.5 rounded-full bg-[#0A6FA3]/20 border border-[#0A6FA3]/30 text-[#0A6FA3] text-sm">
            Season 1 • The Calderon Protocol
          </div>
          
          <h1 className="text-5xl md:text-7xl font-bold mb-6 tracking-tight">
            <span className="text-white">TELEPORT</span>
            <br />
            <span className="bg-gradient-to-r from-[#0A6FA3] to-[#C9A227] bg-clip-text text-transparent">
              MASSIVE
            </span>
          </h1>
          
          <p className="text-xl text-white/60 max-w-2xl mx-auto mb-10 leading-relaxed">
            A collectible card game where quantum mechanics meets human ambition.
            Build decks. Bend reality. Rewrite existence.
          </p>
          
          <div className="flex flex-wrap justify-center gap-4">
            <Link
              href="/cards"
              className="px-8 py-3 bg-[#0A6FA3] hover:bg-[#0A6FA3]/80 text-white font-medium rounded-lg transition-all glow-blue"
            >
              Browse Cards
            </Link>
            <Link
              href="/deckbuilder"
              className="px-8 py-3 bg-white/5 hover:bg-white/10 text-white font-medium rounded-lg border border-white/20 transition-all"
            >
              Build a Deck
            </Link>
          </div>
        </div>
      </section>

      {/* Featured Cards */}
      <section className="py-16 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-3">Featured Cards</h2>
            <p className="text-white/60">Legendary cards from the Teleport Massive universe</p>
          </div>
          
          <div className="flex flex-wrap justify-center gap-8">
            {featuredCards.map((card) => (
              <div key={card.id} className="animate-float" style={{ animationDelay: `${Math.random() * 0.5}s` }}>
                <CardComponent card={card} size="md" />
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Story Teaser */}
      <section className="py-16 px-4 bg-gradient-to-b from-transparent via-[#0A6FA3]/5 to-transparent">
        <div className="max-w-4xl mx-auto text-center">
          <blockquote className="text-2xl md:text-3xl italic text-white/80 mb-6 leading-relaxed">
            &ldquo;They said death was final. They said the distance between us was absolute.
            <span className="text-[#0A6FA3]"> They must be wrong.</span>&rdquo;
          </blockquote>
          <p className="text-white/40">— Aziah Calderon, Lead Quantum Physicist</p>
          
          <Link
            href="/lore"
            className="inline-block mt-8 text-[#0A6FA3] hover:text-[#C9A227] transition-colors"
          >
            Discover the Story →
          </Link>
        </div>
      </section>

      {/* Stats */}
      <section className="py-16 px-4">
        <div className="max-w-4xl mx-auto">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            {[
              { value: '20', label: 'Cards' },
              { value: '4', label: 'Mythics' },
              { value: '6', label: 'Card Types' },
              { value: '∞', label: 'Possibilities' },
            ].map((stat, i) => (
              <div key={i} className="text-center p-6 rounded-xl bg-white/5 border border-white/10">
                <div className="text-3xl font-bold text-[#C9A227] mb-1">{stat.value}</div>
                <div className="text-white/60 text-sm">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-bold mb-4">Ready to Bend Reality?</h2>
          <p className="text-white/60 mb-8">
            Start building your deck and explore the quantum frontier.
          </p>
          <Link
            href="/deckbuilder"
            className="inline-block px-10 py-4 bg-gradient-to-r from-[#0A6FA3] to-[#C9A227] text-white font-medium rounded-lg transition-all hover:opacity-90"
          >
            Start Building
          </Link>
        </div>
      </section>
    </div>
  );
}
