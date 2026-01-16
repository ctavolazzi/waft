"""
Prime Directive System: The Central Organizing Principle of WAFT

The Prime Directive serves as the foundational principle that everything in WAFT
points back to. It is housed within a CelestialBody structure at the Heart of
TreasureTavern, integrated with TheOne Being, and recorded in an hourglass/torus
evolution structure that cycles generation after generation forevermore.

Components:
- PrimeDirective: Core principles and rules
- CelestialBody: Heart (Prime Directive), Mind, Body, Spirit
- HourglassTorus: Eternal evolution tracking structure
- Guardian Beings: MaintenanceStaff, SecurityTeam, Curator
- Karma Museum: Evolution history documentation
"""

from .directive import PrimeDirective
from .celestial_body import CelestialBody, CelestialMind, CelestialSpirit
from .hourglass_torus import HourglassTorus
from .guardians import MaintenanceStaff, SecurityTeam, Curator
from .museum import KarmaMuseum

__all__ = [
    "PrimeDirective",
    "CelestialBody",
    "CelestialMind",
    "CelestialSpirit",
    "HourglassTorus",
    "MaintenanceStaff",
    "SecurityTeam",
    "Curator",
    "KarmaMuseum",
]

# Prime Directive Constants
PRIME_DIRECTIVE_BEING_IDS = {
    "maintenance_staff": "maintenance_staff_prime_directive",
    "security_team": "security_team_prime_directive",
    "curator": "curator_prime_directive",
}
