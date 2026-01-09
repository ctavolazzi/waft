"""
LineagePoet: Generates deterministic scientific names for DigitalOrganisms.

Maps genome IDs to multilingual Genus and Species names with Titles,
creating a diverse taxonomic classification system for the multiverse.

Supports four naming cultures based on genome_id:
- Sanskrit (0x00-0x3F): Vedic roots
- Old Norse (0x40-0x7F): Norse mythology
- Latin (0x80-0xBF): Classical roots
- Cyber/Tech (0xC0-0xFF): Digital heritage
"""

from typing import List, Tuple
import hashlib


class LineagePoet:
    """
    Generates deterministic scientific names from genome IDs.
    
    Uses first byte to select naming culture (multilingual).
    Uses first 8 bytes for Genus+Species, last 4 bytes for Title.
    Same hash always yields same name (deterministic).
    All names properly capitalized.
    """
    
    # Sanskrit (Vedic) - 0x00-0x3F
    SANSKRIT_GENERA = [
        "Prana", "Akasha", "Vayu", "Jiva", "Dharma", "Karma", "Maya", "Atman",
        "Brahman", "Shakti", "Surya", "Chandra", "Agni", "Varuna", "Indra", "Vishnu",
        "Shiva", "Deva", "Asura", "Rishi", "Bodhi", "Nirvana", "Samsara", "Moksha"
    ]
    
    SANSKRIT_SPECIES = [
        "Adi", "Dvitiya", "Tritiya", "Chaturtha", "Panchama", "Shashtha", "Saptama",
        "Ashtama", "Navama", "Dashama", "Shukla", "Krishna", "Rakta", "Shveta", "Nila",
        "Pita", "Harita", "Sita", "Kala", "Dharma", "Artha", "Kama", "Moksha",
        "Sattva", "Rajas", "Tamas", "Prakriti", "Purusha", "Buddhi", "Manas", "Ahamkara"
    ]
    
    # Old Norse - 0x40-0x7F
    NORSE_GENERA = [
        "Fenris", "Tyr", "Saga", "Rune", "Bjorn", "Odin", "Thor", "Loki",
        "Freya", "Heimdall", "Baldur", "Frigg", "Skadi", "Njord", "Bragi", "Idun",
        "Valkyrie", "Einherjar", "Jotun", "Dwarf", "Elf", "Vanir", "Aesir", "Norn"
    ]
    
    NORSE_SPECIES = [
        "Fyrsti", "Annar", "Thridji", "Fjordi", "Fimmti", "Settjandi", "Sjundi",
        "Attandi", "Niondi", "Tiondi", "Hvitr", "Svartr", "Raudr", "Gronn", "Blar",
        "Gull", "Silfr", "Jarn", "Steinn", "Vatn", "Eldr", "Jord", "Vindr",
        "Ljos", "Myrkr", "Hraedr", "Modr", "Starkr", "Veikr", "Visr", "Einfaldr"
    ]
    
    # Latin (Classical) - 0x80-0xBF
    LATIN_GENERA = [
        "Agens", "Cognis", "Logis", "Memoris", "Optimus", "Ratis", "Sapientis",
        "Virtus", "Aeternus", "Celeris", "Fortis", "Magnus", "Prudens", "Sapiens",
        "Digitalis", "Artificis", "Machinis", "Computis", "Intelligens", "Evolutis",
        "Divinus", "Mortalis", "Immortalis", "Primordius"
    ]
    
    LATIN_SPECIES = [
        "Primus", "Secundus", "Tertius", "Quartus", "Quintus", "Sextus", "Septimus",
        "Octavus", "Nonus", "Decimus", "Albus", "Niger", "Ruber", "Viridis", "Caeruleus",
        "Aureus", "Argenteus", "Ferreus", "Lignum", "Lapis", "Aqua", "Ignis", "Terra",
        "Ventus", "Lux", "Umbra", "Celer", "Lentus", "Fortis", "Fragilis", "Stabilis",
        "Mutabilis", "Immutabilis", "Novus", "Vetus", "Magnus", "Parvus", "Altus", "Humilis"
    ]
    
    # Cyber/Tech - 0xC0-0xFF
    CYBER_GENERA = [
        "Aura", "Neon", "Flux", "Byte", "Vector", "Matrix", "Nexus", "Node",
        "Core", "Link", "Sync", "Pulse", "Wave", "Signal", "Stream", "Flow",
        "Code", "Data", "Logic", "Circuit", "Grid", "Net", "Web", "Cloud"
    ]
    
    CYBER_SPECIES = [
        "Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta", "Theta",
        "Iota", "Kappa", "Zero", "One", "Two", "Three", "Four", "Five",
        "Six", "Seven", "Eight", "Nine", "Prime", "Binary", "Hex", "Octal",
        "Fast", "Slow", "High", "Low", "On", "Off", "True", "False",
        "Active", "Idle", "New", "Old", "Big", "Small", "Top", "Bottom"
    ]
    
    # Universal Titles (shared across all cultures)
    TITLES = [
        "the Swift", "the Fragile", "the Great", "the Wise", "the Bold", "the Cautious",
        "the Ancient", "the Young", "the Bright", "the Dark", "the Silent", "the Vocal",
        "the Patient", "the Impatient", "the Strong", "the Weak", "the Clever", "the Simple",
        "the Noble", "the Humble", "the Proud", "the Meek", "the Fierce", "the Gentle",
        "the Eternal", "the Fleeting", "the Stable", "the Chaotic", "the Ordered", "the Wild",
        "the Pure", "the Tainted", "the Perfect", "the Flawed", "the Complete", "the Incomplete"
    ]
    
    @classmethod
    def _get_culture(cls, first_byte: int) -> Tuple[List[str], List[str]]:
        """
        Select naming culture based on first byte of genome_id.
        
        Args:
            first_byte: First byte value (0-255)
            
        Returns:
            Tuple of (genera_list, species_list) for selected culture
        """
        if 0x00 <= first_byte <= 0x3F:  # Sanskrit (Vedic)
            return (cls.SANSKRIT_GENERA, cls.SANSKRIT_SPECIES)
        elif 0x40 <= first_byte <= 0x7F:  # Old Norse
            return (cls.NORSE_GENERA, cls.NORSE_SPECIES)
        elif 0x80 <= first_byte <= 0xBF:  # Latin (Classical)
            return (cls.LATIN_GENERA, cls.LATIN_SPECIES)
        else:  # 0xC0-0xFF: Cyber/Tech
            return (cls.CYBER_GENERA, cls.CYBER_SPECIES)
    
    @classmethod
    def _get_culture_name(cls, first_byte: int) -> str:
        """Get culture name for reporting."""
        if 0x00 <= first_byte <= 0x3F:
            return "Sanskrit"
        elif 0x40 <= first_byte <= 0x7F:
            return "Old Norse"
        elif 0x80 <= first_byte <= 0xBF:
            return "Latin"
        else:
            return "Cyber/Tech"
    
    @classmethod
    def generate_hybrid_name(cls, parent_a_genome: str, parent_b_genome: str) -> str:
        """
        Generate hybrid name from two parent genomes (linguistic hybridization).
        
        If parents are from different cultures, attempt to blend names.
        Example: Sanskrit + Norse = "Rishi Vindr, the Eternal"
        
        Args:
            parent_a_genome: First parent's genome_id
            parent_b_genome: Second parent's genome_id
            
        Returns:
            Hybrid scientific name
        """
        # Get parent cultures
        parent_a_byte = int(parent_a_genome[:2], 16)
        parent_b_byte = int(parent_b_genome[:2], 16)
        
        parent_a_culture = cls._get_culture_name(parent_a_byte)
        parent_b_culture = cls._get_culture_name(parent_b_byte)
        
        # If same culture, use normal generation
        if parent_a_culture == parent_b_culture:
            # Use combined genome hash
            combined = hashlib.sha256((parent_a_genome + parent_b_genome).encode()).hexdigest()
            return cls.generate_name(combined)
        
        # Hybrid: Mix genus from one, species from other
        parent_a_genera, parent_a_species = cls._get_culture(parent_a_byte)
        parent_b_genera, parent_b_species = cls._get_culture(parent_b_byte)
        
        # Use first 8 bytes of combined hash for selection
        combined = hashlib.sha256((parent_a_genome + parent_b_genome).encode()).hexdigest()
        first_8_bytes = combined[:16]
        
        genus_bytes = first_8_bytes[2:10]
        species_bytes = first_8_bytes[10:16]
        title_bytes = combined[-8:]
        
        # Select genus from parent_a culture, species from parent_b culture
        genus_index = int(genus_bytes, 16) % len(parent_a_genera)
        species_index = int(species_bytes, 16) % len(parent_b_species)
        title_index = int(title_bytes, 16) % len(cls.TITLES)
        
        genus = parent_a_genera[genus_index]
        species = parent_b_species[species_index]
        title = cls.TITLES[title_index]
        
        return f"{genus} {species}, {title}"
    
    @classmethod
    def generate_name(cls, genome_id: str) -> str:
        """
        Generate deterministic scientific name from genome_id.
        
        Uses first byte to select naming culture (multilingual).
        Uses first 8 bytes (16 hex chars) for Genus+Species selection.
        Uses last 4 bytes (8 hex chars) for Title selection.
        All names properly capitalized.
        
        Args:
            genome_id: SHA-256 hex digest (64 characters)
            
        Returns:
            Scientific name in format: "Genus Species, Title"
            Example: "Cognis Novus, the Fragile"
            Example: "Prana Adi, the Swift" (Sanskrit)
            Example: "Fenris Fyrsti, the Great" (Norse)
            Example: "Aura Alpha, the Bold" (Cyber)
        """
        if len(genome_id) < 64:
            # Pad if needed (shouldn't happen with SHA-256)
            genome_id = genome_id.ljust(64, '0')
        
        # First byte determines culture
        first_byte_hex = genome_id[:2]
        first_byte = int(first_byte_hex, 16)
        
        # Get culture-specific lists
        genera_list, species_list = cls._get_culture(first_byte)
        
        # First 8 bytes (16 hex chars) for Genus+Species
        first_8_bytes = genome_id[:16]
        
        # Last 4 bytes (8 hex chars) for Title
        last_4_bytes = genome_id[-8:]
        
        # Convert hex to integers for indexing
        # Use bytes 2-8 (6 bytes = 12 hex chars) for genus to avoid first byte
        genus_bytes = first_8_bytes[2:10]  # 8 hex chars = 4 bytes
        species_bytes = first_8_bytes[10:16]  # 6 hex chars = 3 bytes
        
        genus_index = int(genus_bytes, 16) % len(genera_list)
        species_index = int(species_bytes, 16) % len(species_list)
        title_index = int(last_4_bytes, 16) % len(cls.TITLES)
        
        # Generate name (all properly capitalized)
        genus = genera_list[genus_index]  # Already capitalized
        species = species_list[species_index]  # Already capitalized
        title = cls.TITLES[title_index]  # "the X" format
        
        # Format: "Genus Species, Title"
        return f"{genus} {species}, {title}"
    
    @classmethod
    def parse_name(cls, scientific_name: str) -> dict:
        """
        Parse scientific name into components.
        
        Args:
            scientific_name: Name in format "Genus Species, Title"
            (Old format "Genus species Title" also supported)
            
        Returns:
            Dictionary with 'genus', 'species', 'title', 'culture'
        """
        # Handle new format: "Genus Species, Title"
        if ", " in scientific_name:
            parts = scientific_name.split(", ", 1)
            name_part = parts[0]
            title = parts[1] if len(parts) > 1 else ""
            
            name_words = name_part.split()
            if len(name_words) >= 2:
                genus = name_words[0]
                species = name_words[1]
                return {
                    "genus": genus,
                    "species": species,
                    "title": title,
                    "culture": cls._detect_culture(genus)
                }
        
        # Fallback: old format "Genus species Title"
        parts = scientific_name.split()
        if len(parts) >= 3:
            genus = parts[0]
            species = parts[1]
            title = " ".join(parts[2:])
            return {
                "genus": genus,
                "species": species,
                "title": title,
                "culture": cls._detect_culture(genus)
            }
        return {"genus": "", "species": "", "title": "", "culture": "Unknown"}
    
    @classmethod
    def _detect_culture(cls, genus: str) -> str:
        """Detect culture from genus name."""
        if genus in cls.SANSKRIT_GENERA:
            return "Sanskrit"
        elif genus in cls.NORSE_GENERA:
            return "Old Norse"
        elif genus in cls.LATIN_GENERA:
            return "Latin"
        elif genus in cls.CYBER_GENERA:
            return "Cyber/Tech"
        return "Unknown"
