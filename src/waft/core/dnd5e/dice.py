"""
D&D Dice Rolling - Wrapper around d20 Library

Provides dice rolling functionality using the d20 library, with error handling
and validation.
"""


import d20


class DnDRoller:
    """
    D&D dice rolling using d20 library.

    This class wraps the d20 library with error handling and validation.
    All dice operations go through this class to ensure consistent error handling.
    """

    @staticmethod
    def roll(expression: str) -> int:
        """
        Roll dice expression.

        Examples:
            - "1d20" → Roll 1d20
            - "2d6+3" → Roll 2d6, add 3
            - "4d6dl1" → Roll 4d6, drop lowest

        Args:
            expression: Dice expression (e.g., "1d20", "2d6+3")

        Returns:
            Total result (integer)

        Raises:
            ValueError: If expression is invalid or library fails
        """
        try:
            result = d20.roll(expression)
            return result.total
        except Exception as e:
            raise ValueError(f"Invalid dice expression '{expression}': {e}")

    @staticmethod
    def attack_roll(advantage: bool = False, disadvantage: bool = False) -> tuple[int, bool]:
        """
        Make an attack roll (d20).

        Handles advantage (roll twice, take higher) and disadvantage (roll twice, take lower).
        Advantage and disadvantage cancel each other out (normal roll).

        Args:
            advantage: Roll with advantage (default: False)
            disadvantage: Roll with disadvantage (default: False)

        Returns:
            Tuple of (roll_result, is_critical)
            - roll_result: The d20 roll result (1-20)
            - is_critical: True if natural 20 (critical hit)

        Raises:
            ValueError: If dice rolling fails
        """
        try:
            if advantage and not disadvantage:
                # Roll twice, take higher
                roll1 = d20.roll("1d20").total
                roll2 = d20.roll("1d20").total
                roll = max(roll1, roll2)
            elif disadvantage and not advantage:
                # Roll twice, take lower
                roll1 = d20.roll("1d20").total
                roll2 = d20.roll("1d20").total
                roll = min(roll1, roll2)
            else:
                # Normal roll (advantage and disadvantage cancel)
                roll = d20.roll("1d20").total

            is_critical = roll == 20
            return (roll, is_critical)
        except Exception as e:
            raise ValueError(f"Failed to make attack roll: {e}")

    @staticmethod
    def roll_damage(dice_expression: str) -> int:
        """
        Roll damage dice.

        Examples:
            - "1d6" → Roll 1d6 for damage
            - "2d8+4" → Roll 2d8, add 4
            - "4d6" → Roll 4d6

        Args:
            dice_expression: Damage dice expression (e.g., "1d6", "2d8+4")

        Returns:
            Total damage (integer)

        Raises:
            ValueError: If expression is invalid or library fails
        """
        return DnDRoller.roll(dice_expression)
