'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function Header() {
  const pathname = usePathname();
  
  const navItems = [
    { href: '/', label: 'Home' },
    { href: '/cards', label: 'Cards' },
    { href: '/deckbuilder', label: 'Deck Builder' },
    { href: '/lore', label: 'Lore' },
  ];

  return (
    <header className="sticky top-0 z-50 bg-[#0d0d15]/95 backdrop-blur-sm border-b border-[#333340]">
      <div className="max-w-7xl mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-3 group">
            <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-[#0A6FA3] to-[#084E74] flex items-center justify-center text-xl font-bold glow-blue group-hover:scale-110 transition-transform">
              TM
            </div>
            <div>
              <div className="font-bold text-lg tracking-wide">TELEPORT MASSIVE</div>
              <div className="text-[10px] text-[#0A6FA3] tracking-widest">CARD GAME</div>
            </div>
          </Link>

          {/* Navigation */}
          <nav className="flex items-center gap-1">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className={`px-4 py-2 rounded-lg transition-all ${
                  pathname === item.href
                    ? 'bg-[#0A6FA3]/20 text-[#0A6FA3] font-medium'
                    : 'text-white/70 hover:text-white hover:bg-white/5'
                }`}
              >
                {item.label}
              </Link>
            ))}
          </nav>
        </div>
      </div>
    </header>
  );
}
