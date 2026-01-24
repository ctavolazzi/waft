import Image from 'next/image';
import CardComponent from '@/components/CardComponent';
import { cards } from '@/data/cards';

export default function LorePage() {
  const aziah = cards.find(c => c.name === 'Aziah Calderon')!;
  const faiWei = cards.find(c => c.name === 'Fai Wei')!;
  const swab = cards.find(c => c.name.includes('SWAB'))!;
  const swae = cards.find(c => c.name.includes('SWAE'))!;

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      {/* Title */}
      <div className="text-center mb-16">
        <div className="text-[#0A6FA3] text-sm tracking-widest mb-3">THE STORY OF</div>
        <h1 className="text-5xl font-bold mb-6">TELEPORT MASSIVE</h1>
        <p className="text-white/60 text-lg">A tale of loss, ambition, and the nature of existence itself.</p>
      </div>

      {/* Chapter 1 */}
      <section className="mb-20">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-8 h-8 rounded-full bg-[#0A6FA3] flex items-center justify-center font-bold">1</div>
          <h2 className="text-2xl font-bold">The Beginning</h2>
        </div>
        
        <div className="prose prose-invert max-w-none">
          <p className="text-white/80 leading-relaxed mb-6">
            In the year 2087, <span className="text-[#C9A227]">Teleport Massive</span> revolutionized 
            human transportation. Founded by the visionary <span className="text-[#0A6FA3]">Fai Wei</span>, 
            the corporation achieved what was once thought impossible: practical quantum teleportation.
          </p>
          
          <p className="text-white/80 leading-relaxed mb-6">
            What began as instantaneous travel across continents evolved into something far more 
            profound. The technology didn&apos;t just move matter—it deconstructed reality at its most 
            fundamental level and reconstructed it elsewhere.
          </p>

          <div className="flex justify-center my-10">
            <CardComponent card={faiWei} size="lg" />
          </div>

          <blockquote className="border-l-4 border-[#0A6FA3] pl-6 py-2 my-8 text-white/70 italic">
            &ldquo;We&apos;re not just studying quantum mechanics—we&apos;re building the future of transportation.&rdquo;
            <span className="block text-white/40 mt-2 not-italic">— Fai Wei, Founder & CEO</span>
          </blockquote>
        </div>
      </section>

      {/* Chapter 2 */}
      <section className="mb-20">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-8 h-8 rounded-full bg-[#0A6FA3] flex items-center justify-center font-bold">2</div>
          <h2 className="text-2xl font-bold">The Loss</h2>
        </div>
        
        <div className="prose prose-invert max-w-none">
          <p className="text-white/80 leading-relaxed mb-6">
            <span className="text-[#0A6FA3]">Dr. Aziah Calderon</span> was Teleport Massive&apos;s 
            brightest mind—a quantum physicist whose understanding of entanglement borders on intuition. 
            Her work on the Scint Protocol allowed the company to detect tears in the fabric of 
            existence itself.
          </p>

          <p className="text-white/80 leading-relaxed mb-6">
            Then came the accident. During a routine teleportation, someone Aziah loved was lost—not 
            dead, but scattered across quantum states, existing everywhere and nowhere simultaneously.
          </p>

          <div className="flex justify-center my-10">
            <CardComponent card={aziah} size="lg" />
          </div>

          <blockquote className="border-l-4 border-[#C9A227] pl-6 py-2 my-8 text-white/70 italic">
            &ldquo;They said death was final. They said the distance between us was absolute. 
            They must be wrong. I will come back to her, even if I have to rewrite Time Itself.&rdquo;
            <span className="block text-white/40 mt-2 not-italic">— Aziah Calderon</span>
          </blockquote>
        </div>
      </section>

      {/* Chapter 3 */}
      <section className="mb-20">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-8 h-8 rounded-full bg-[#0A6FA3] flex items-center justify-center font-bold">3</div>
          <h2 className="text-2xl font-bold">The Artifacts</h2>
        </div>
        
        <div className="prose prose-invert max-w-none">
          <p className="text-white/80 leading-relaxed mb-6">
            Aziah&apos;s research led her to discover something impossible: two artifacts that existed 
            outside of time itself. <span className="text-[#C9A227]">SWAB</span>—Something Without A 
            Beginning—and <span className="text-[#C9A227]">SWAE</span>—Something Without An End.
          </p>

          <p className="text-white/80 leading-relaxed mb-6">
            These objects don&apos;t obey the laws of causality. SWAB cannot be cast or summoned—it 
            simply appears. SWAE cannot be destroyed or removed—it simply persists. Together, they 
            represent the boundaries of existence: the alpha and omega of reality.
          </p>

          <div className="flex justify-center gap-8 my-10 flex-wrap">
            <CardComponent card={swab} size="md" />
            <CardComponent card={swae} size="md" />
          </div>

          <p className="text-white/80 leading-relaxed">
            Aziah believes these artifacts hold the key to her quest. If she can understand how 
            something can exist without beginning or end, perhaps she can find where her beloved 
            exists—scattered but not gone.
          </p>
        </div>
      </section>

      {/* Chapter 4 */}
      <section className="mb-20">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-8 h-8 rounded-full bg-[#0A6FA3] flex items-center justify-center font-bold">4</div>
          <h2 className="text-2xl font-bold">The Vibration</h2>
        </div>
        
        <div className="prose prose-invert max-w-none">
          <p className="text-white/80 leading-relaxed mb-6">
            At the heart of Aziah&apos;s research lies <span className="text-[#C9A227]">The Vibration</span>—
            a phenomenon she discovered that exists at the boundary between being and non-being. 
            It&apos;s the oscillation of existence itself, the rhythm that determines what is real and 
            what is merely possible.
          </p>

          <p className="text-white/80 leading-relaxed mb-6">
            Her colleagues call it dangerous. The board calls it unprofitable. But Aziah knows 
            that if she can master The Vibration, she can reach across the quantum void and 
            bring back what was lost.
          </p>

          <div className="bg-gradient-to-r from-[#0A6FA3]/20 via-[#C9A227]/20 to-[#0A6FA3]/20 p-8 rounded-xl my-10 text-center">
            <div className="text-3xl mb-4">〰️</div>
            <p className="text-white/80 italic">
              &ldquo;The oscillation between existence and nonexistence.&rdquo;
            </p>
          </div>
        </div>
      </section>

      {/* To Be Continued */}
      <section className="text-center py-16">
        <div className="inline-block px-6 py-3 rounded-full bg-white/5 border border-white/10 mb-6">
          <span className="text-white/60">Season 1</span>
          <span className="mx-2 text-white/20">•</span>
          <span className="text-[#0A6FA3]">The Calderon Protocol</span>
        </div>
        
        <h3 className="text-2xl font-bold mb-4">To Be Continued...</h3>
        <p className="text-white/60 max-w-md mx-auto">
          The story of Teleport Massive unfolds with each new card set. 
          Will Aziah succeed in her quest? Or will her obsession tear 
          apart the fabric of reality itself?
        </p>
      </section>
    </div>
  );
}
