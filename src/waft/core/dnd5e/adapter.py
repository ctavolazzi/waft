"""
D&D 5e Stats Adapter - 4-Stat to 6-Stat Conversion

Adapter pattern for converting 4-stat systems (STR, DEX, INT, CON) to
D&D 6-stat format (STR, DEX, CON, INT, WIS, CHA).

This allows importing agents from other systems that use 4 stats.
"""


class StatsAdapter:
    """
    Adapter for converting 4-stat systems to D&D 6-stat format.

    Maps 4 core stats to 6 D&D stats, filling in WIS and CHA with
    class-based defaults or derived values.
    """

    # Class-based stat defaults for WIS and CHA
    CLASS_BASE_STATS = {
        "fighter": {
            "str_bonus": 2,
            "dex_penalty": -1,
            "con_bonus": 1,
            "wis_base": 10,
            "cha_base": 10,
        },
        "wizard": {
            "str_penalty": -1,
            "dex_base": 10,
            "con_base": 10,
            "int_bonus": 2,
            "wis_base": 12,
            "cha_base": 8,
        },
        "rogue": {
            "str_base": 10,
            "dex_bonus": 2,
            "con_base": 10,
            "int_base": 10,
            "wis_base": 11,
            "cha_base": 11,
        },
        "cleric": {
            "str_base": 10,
            "dex_base": 10,
            "con_base": 10,
            "int_base": 10,
            "wis_bonus": 2,
            "cha_base": 12,
        },
        "default": {
            "str_base": 10,
            "dex_base": 10,
            "con_base": 10,
            "int_base": 10,
            "wis_base": 10,
            "cha_base": 10,
        },
    }

    @staticmethod
    def convert_4_to_6(
        str_score: int, dex_score: int, int_score: int, con_score: int, char_class: str = "fighter"
    ) -> dict[str, int]:
        """
        Convert 4-stat system to 6-stat D&D format.

        Args:
            str_score: Strength score (4-stat system)
            dex_score: Dexterity score (4-stat system)
            int_score: Intelligence score (4-stat system)
            con_score: Constitution score (4-stat system)
            char_class: Character class (determines WIS/CHA defaults)

        Returns:
            Dictionary with 6 D&D ability scores:
            {
                "strength": int,
                "dexterity": int,
                "constitution": int,
                "intelligence": int,
                "wisdom": int,
                "charisma": int,
            }
        """
        base_stats = StatsAdapter.CLASS_BASE_STATS.get(
            char_class.lower(), StatsAdapter.CLASS_BASE_STATS["default"]
        )

        # Apply bonuses/penalties to 4 core stats
        strength = str_score + base_stats.get("str_bonus", 0) - base_stats.get("str_penalty", 0)
        if "str_base" in base_stats:
            strength = base_stats["str_base"]

        dexterity = dex_score + base_stats.get("dex_bonus", 0) - base_stats.get("dex_penalty", 0)
        if "dex_base" in base_stats:
            dexterity = base_stats["dex_base"]

        constitution = con_score + base_stats.get("con_bonus", 0)
        if "con_base" in base_stats:
            constitution = base_stats["con_base"]

        intelligence = int_score + base_stats.get("int_bonus", 0)
        if "int_base" in base_stats:
            intelligence = base_stats["int_base"]

        # WIS and CHA from class defaults
        wisdom = base_stats.get("wis_base", 10) + base_stats.get("wis_bonus", 0)
        charisma = base_stats.get("cha_base", 10) + base_stats.get("cha_bonus", 0)

        return {
            "strength": max(1, min(30, strength)),  # Clamp to valid range
            "dexterity": max(1, min(30, dexterity)),
            "constitution": max(1, min(30, constitution)),
            "intelligence": max(1, min(30, intelligence)),
            "wisdom": max(1, min(30, wisdom)),
            "charisma": max(1, min(30, charisma)),
        }
