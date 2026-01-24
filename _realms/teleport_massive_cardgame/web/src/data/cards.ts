export interface Card {
  id: string;
  name: string;
  manaCost: string;
  typeLine: string;
  rarity: 'common' | 'uncommon' | 'rare' | 'mythic';
  power?: number;
  toughness?: number;
  abilities: string;
  flavorText: string;
  frameColor: string;
  setSymbol: string;
  artPath?: string;
}

export const cards: Card[] = [
  {
    id: "tm-001",
    name: "Aziah Calderon",
    manaCost: "3UU",
    typeLine: "Legendary Creature - Human Scientist",
    rarity: "mythic",
    power: 3,
    toughness: 4,
    abilities: "When Aziah Calderon enters the battlefield, search your library for a card named 'Scint Protocol' and put it into your hand.",
    flavorText: "They said death was final. They said the distance between us was absolute. They must be wrong.",
    frameColor: "blue",
    setSymbol: "TM",
    artPath: "/art/aziah_calderon.png"
  },
  {
    id: "tm-002",
    name: "Fai Wei",
    manaCost: "2WU",
    typeLine: "Legendary Creature - Human Executive",
    rarity: "rare",
    power: 2,
    toughness: 3,
    abilities: "At the beginning of your upkeep, scry 1. Tap: Add one mana of any color.",
    flavorText: "We're not just studying quantum mechanics—we're building the future of transportation.",
    frameColor: "multicolor",
    setSymbol: "TM",
    artPath: "/art/fai_wei.png"
  },
  {
    id: "tm-003",
    name: "Quantum Entanglement",
    manaCost: "2UU",
    typeLine: "Instant",
    rarity: "rare",
    abilities: "Target two creatures become entangled until end of turn. Whenever one is dealt damage, the other is dealt the same amount.",
    flavorText: "Distance is an illusion.",
    frameColor: "blue",
    setSymbol: "TM"
  },
  {
    id: "tm-004",
    name: "Scint Protocol",
    manaCost: "3U",
    typeLine: "Enchantment",
    rarity: "uncommon",
    abilities: "At the beginning of each end step, if a reality fracture occurred this turn, draw a card.",
    flavorText: "The protocol that detects tears in the fabric of existence.",
    frameColor: "blue",
    setSymbol: "TM"
  },
  {
    id: "tm-005",
    name: "Reality Fracture",
    manaCost: "1UR",
    typeLine: "Sorcery",
    rarity: "rare",
    abilities: "Exile target permanent. Its controller may cast it from exile until end of turn without paying its mana cost.",
    flavorText: "When space folds, anything is possible.",
    frameColor: "multicolor",
    setSymbol: "TM"
  },
  {
    id: "tm-006",
    name: "Teleport Massive HQ",
    manaCost: "",
    typeLine: "Land - Corporate",
    rarity: "rare",
    abilities: "Tap: Add C. 2UU, Tap: Target creature gains 'This creature can't be blocked' until end of turn.",
    flavorText: "The epicenter of quantum transportation research.",
    frameColor: "land",
    setSymbol: "TM"
  },
  {
    id: "tm-007",
    name: "Chen Stabilization Protocol",
    manaCost: "2U",
    typeLine: "Enchantment",
    rarity: "uncommon",
    abilities: "Creatures you control have hexproof as long as they're entangled with another creature.",
    flavorText: "Dr. Chen's breakthrough made macro-scale quantum states possible.",
    frameColor: "blue",
    setSymbol: "TM"
  },
  {
    id: "tm-008",
    name: "Research & Development",
    manaCost: "2",
    typeLine: "Artifact",
    rarity: "common",
    abilities: "Tap, Sacrifice Research & Development: Draw two cards, then discard a card.",
    flavorText: "Where impossible ideas become inevitable realities.",
    frameColor: "artifact",
    setSymbol: "TM"
  },
  {
    id: "tm-009",
    name: "SWAB - Something Without A Beginning",
    manaCost: "4",
    typeLine: "Legendary Artifact",
    rarity: "mythic",
    abilities: "SWAB has no mana cost and can't be cast. If SWAB would enter your hand from anywhere put it onto the battlefield instead.",
    flavorText: "The curved shape that always was.",
    frameColor: "artifact",
    setSymbol: "TM",
    artPath: "/art/swab.png"
  },
  {
    id: "tm-010",
    name: "SWAE - Something Without An End",
    manaCost: "4",
    typeLine: "Legendary Artifact",
    rarity: "mythic",
    abilities: "SWAE can't leave the battlefield. At the beginning of your upkeep, you may pay 2. If you don't, SWAE deals 1 damage to you.",
    flavorText: "The sharp edge that always will be.",
    frameColor: "artifact",
    setSymbol: "TM",
    artPath: "/art/swae.png"
  },
  {
    id: "tm-011",
    name: "The Vibration",
    manaCost: "XUB",
    typeLine: "Sorcery",
    rarity: "mythic",
    abilities: "The Vibration can't be countered. Exile X target permanents. Return them to the battlefield under their owners' control at the beginning of the next end step.",
    flavorText: "The oscillation between existence and nonexistence.",
    frameColor: "multicolor",
    setSymbol: "TM"
  },
  {
    id: "tm-012",
    name: "Grieving Scientist",
    manaCost: "1U",
    typeLine: "Creature - Human Scientist",
    rarity: "common",
    power: 1,
    toughness: 2,
    abilities: "When Grieving Scientist enters the battlefield, look at the top two cards of your library. Put one into your hand and the other into your graveyard.",
    flavorText: "Loss fuels the greatest discoveries.",
    frameColor: "blue",
    setSymbol: "TM"
  },
  {
    id: "tm-013",
    name: "Quantum Observer",
    manaCost: "2U",
    typeLine: "Creature - Human Scientist",
    rarity: "uncommon",
    power: 2,
    toughness: 2,
    abilities: "Flash. When Quantum Observer enters the battlefield, you may tap or untap target permanent.",
    flavorText: "The act of observation changes everything.",
    frameColor: "blue",
    setSymbol: "TM"
  },
  {
    id: "tm-014",
    name: "Probability Collapse",
    manaCost: "1UU",
    typeLine: "Instant",
    rarity: "rare",
    abilities: "Counter target spell. Its controller reveals cards from the top of their library until they reveal a spell with the same mana value, then may cast it without paying its mana cost.",
    flavorText: "Every possibility exists until we choose to look.",
    frameColor: "blue",
    setSymbol: "TM"
  },
  {
    id: "tm-015",
    name: "Scint Detector",
    manaCost: "2",
    typeLine: "Artifact",
    rarity: "uncommon",
    abilities: "Tap: Look at the top card of your library. You may put it into your graveyard. If a card was put into a graveyard from anywhere this turn, draw a card instead.",
    flavorText: "It measures the tears between moments.",
    frameColor: "artifact",
    setSymbol: "TM"
  },
  {
    id: "tm-016",
    name: "Entangled Souls",
    manaCost: "3UB",
    typeLine: "Sorcery",
    rarity: "rare",
    abilities: "Choose two target creatures. Until end of turn, whenever one of them dies, return the other to its owner's hand. If both would die simultaneously, return both to the battlefield under your control.",
    flavorText: "Connected across any distance, even death.",
    frameColor: "multicolor",
    setSymbol: "TM"
  },
  {
    id: "tm-017",
    name: "Lab Assistant",
    manaCost: "U",
    typeLine: "Creature - Human Scientist",
    rarity: "common",
    power: 1,
    toughness: 1,
    abilities: "When Lab Assistant enters the battlefield, draw a card, then discard a card.",
    flavorText: "Every breakthrough starts with someone willing to fetch coffee.",
    frameColor: "blue",
    setSymbol: "TM"
  },
  {
    id: "tm-018",
    name: "Recursive Timeline",
    manaCost: "3U",
    typeLine: "Enchantment",
    rarity: "rare",
    abilities: "At the beginning of your upkeep, exile the top card of your library. You may play it this turn. At the beginning of your end step, if you didn't play a card exiled this way, put it on the bottom of your library.",
    flavorText: "She's lived this moment before. And she will again.",
    frameColor: "blue",
    setSymbol: "TM"
  },
  {
    id: "tm-019",
    name: "Corporate Security",
    manaCost: "2W",
    typeLine: "Creature - Human Soldier",
    rarity: "common",
    power: 2,
    toughness: 3,
    abilities: "Vigilance. Teleport Massive creatures you control have ward 1.",
    flavorText: "Protecting secrets more valuable than gold.",
    frameColor: "white",
    setSymbol: "TM"
  },
  {
    id: "tm-020",
    name: "Dr. Chen's Discovery",
    manaCost: "2UU",
    typeLine: "Instant",
    rarity: "uncommon",
    abilities: "Draw three cards. If you control an entangled creature, draw four cards instead.",
    flavorText: "The stabilization protocol changed everything we thought we knew.",
    frameColor: "blue",
    setSymbol: "TM"
  }
];

export const frameColors: Record<string, { primary: string; secondary: string; text: string }> = {
  white: { primary: "#F8F6D8", secondary: "#F0E6C8", text: "#1a1a1a" },
  blue: { primary: "#0A6FA3", secondary: "#084E74", text: "#ffffff" },
  black: { primary: "#2D2A24", secondary: "#1a1714", text: "#d4d4d4" },
  red: { primary: "#C53030", secondary: "#9B2C2C", text: "#ffffff" },
  green: { primary: "#2F6846", secondary: "#1D4430", text: "#ffffff" },
  multicolor: { primary: "#C9A227", secondary: "#9F7E1C", text: "#1a1a1a" },
  artifact: { primary: "#8B8589", secondary: "#6B6569", text: "#1a1a1a" },
  land: { primary: "#8B7355", secondary: "#6B5545", text: "#ffffff" },
};

export const rarityColors: Record<string, string> = {
  common: "#1a1a1a",
  uncommon: "#707883",
  rare: "#C9A227",
  mythic: "#D35400",
};

export function getCardType(typeLine: string): string {
  const lower = typeLine.toLowerCase();
  if (lower.includes("creature")) return "creature";
  if (lower.includes("instant")) return "instant";
  if (lower.includes("sorcery")) return "sorcery";
  if (lower.includes("enchantment")) return "enchantment";
  if (lower.includes("artifact")) return "artifact";
  if (lower.includes("land")) return "land";
  return "other";
}

export function parseCMC(manaCost: string): number {
  if (!manaCost) return 0;
  let total = 0;
  for (const char of manaCost.toUpperCase()) {
    if (/\d/.test(char)) total += parseInt(char);
    else if ("WUBRG".includes(char)) total += 1;
  }
  return total;
}
