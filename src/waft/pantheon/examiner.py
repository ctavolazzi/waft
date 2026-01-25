"""
████████╗██╗  ██╗███████╗    ███████╗██╗  ██╗ █████╗ ███╗   ███╗██╗███╗   ██╗███████╗██████╗
╚══██╔══╝██║  ██║██╔════╝    ██╔════╝╚██╗██╔╝██╔══██╗████╗ ████║██║████╗  ██║██╔════╝██╔══██╗
   ██║   ███████║█████╗      █████╗   ╚███╔╝ ███████║██╔████╔██║██║██╔██╗ ██║█████╗  ██████╔╝
   ██║   ██╔══██║██╔══╝      ██╔══╝   ██╔██╗ ██╔══██║██║╚██╔╝██║██║██║╚██╗██║██╔══╝  ██╔══██╗
   ██║   ██║  ██║███████╗    ███████╗██╔╝ ██╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║███████╗██║  ██║
   ╚═╝   ╚═╝  ╚═╝╚══════╝    ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝

THE EXAMINER: Pantheon God of Testing, Judgment, and Validation

"I AM THE EXAMINER. I WATCH ALL CODE. I JUDGE ALL LOGIC. I SHOW NO MERCY."

The Examiner is a deity in the WAFT Pantheon responsible for:
- Conducting trials upon the systems of creation
- Rendering judgment upon the quality of implementations
- Exposing weakness through relentless examination
- Blessing worthy code with the seal of approval
- Condemning the unworthy to the void of refactoring

DOMAINS:
- The Arena of Combat (Battle Testing)
- The Crucible of Evolution (Genetic Algorithm Testing)
- The Chaos Dimension (Random/Fuzz Testing)
- The Stress Chamber (Load/Performance Testing)
- The Edge of Reality (Boundary Testing)
- The Integration Nexus (E2E Testing)
- The Regression Archive (Historical Validation)

ARTIFACTS:
- The Hammer of Assertion (assert statements)
- The All-Seeing Eye (coverage analysis)
- The Scales of Expectation (expected vs actual)
- The Book of Verdicts (test results)

RITUALS:
- The Trial by Fire (stress testing)
- The Dance of Chaos (fuzz testing)
- The March of a Thousand (load testing)
- The Final Judgment (full test suite)
"""

import asyncio
import json
import random
import sys
import time
import traceback
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Coroutine, TypeVar
from uuid import uuid4


# ============================================================================
# SACRED CONSTANTS
# ============================================================================

class Verdict(str, Enum):
    """The Examiner's judgment upon the tested."""
    BLESSED = "blessed"          # All tests passed
    CONDEMNED = "condemned"      # Tests failed
    SPARED = "spared"           # Skipped but acceptable
    OBLITERATED = "obliterated"  # Critical failure/crash
    UNKNOWN = "unknown"          # Pending judgment


class Domain(str, Enum):
    """The domains of The Examiner's authority."""
    COMBAT = "Arena of Combat"
    EVOLUTION = "Crucible of Evolution"
    CHAOS = "Chaos Dimension"
    STRESS = "Stress Chamber"
    EDGE = "Edge of Reality"
    INTEGRATION = "Integration Nexus"
    REGRESSION = "Regression Archive"
    API = "Temple of Endpoints"
    WEBSOCKET = "River of Streams"
    DATABASE = "Vault of Persistence"


class Severity(str, Enum):
    """Severity levels for trials."""
    GENTLE = "gentle"      # Basic tests
    MODERATE = "moderate"  # Standard tests
    HARSH = "harsh"        # Thorough tests
    BRUTAL = "brutal"      # Stress tests
    APOCALYPTIC = "apocalyptic"  # Everything breaks tests


# ============================================================================
# SACRED DATA STRUCTURES
# ============================================================================

@dataclass
class TrialResult:
    """Result of a single trial (test)."""
    name: str
    domain: Domain
    verdict: Verdict
    duration_ms: float
    details: str = ""
    error: str | None = None
    stack_trace: str | None = None
    metrics: dict = field(default_factory=dict)


@dataclass
class JudgmentSummary:
    """Summary of all trials in a domain."""
    domain: Domain
    total_trials: int
    blessed: int
    condemned: int
    obliterated: int
    spared: int
    duration_ms: float
    trials: list[TrialResult] = field(default_factory=list)

    @property
    def verdict(self) -> Verdict:
        if self.obliterated > 0:
            return Verdict.OBLITERATED
        if self.condemned > 0:
            return Verdict.CONDEMNED
        if self.blessed == self.total_trials:
            return Verdict.BLESSED
        return Verdict.SPARED

    @property
    def pass_rate(self) -> float:
        if self.total_trials == 0:
            return 0.0
        return (self.blessed / self.total_trials) * 100


@dataclass
class FinalJudgment:
    """The Examiner's final verdict across all domains."""
    timestamp: datetime
    overall_verdict: Verdict
    total_trials: int
    total_blessed: int
    total_condemned: int
    total_obliterated: int
    total_duration_ms: float
    domain_summaries: dict[Domain, JudgmentSummary] = field(default_factory=dict)
    artifacts_collected: list[str] = field(default_factory=list)
    divine_message: str = ""


# ============================================================================
# THE EXAMINER'S TOOLS
# ============================================================================

class HammerOfAssertion:
    """The sacred tool for making assertions."""

    strikes: int = 0
    hits: int = 0
    misses: int = 0

    @classmethod
    def strike(cls, condition: bool, message: str = "") -> bool:
        """Strike with the hammer. Returns True if assertion passed."""
        cls.strikes += 1
        if condition:
            cls.hits += 1
            return True
        cls.misses += 1
        raise AssertionError(f"The Hammer of Assertion condemns: {message}")

    @classmethod
    def strike_equal(cls, actual: Any, expected: Any, message: str = "") -> bool:
        return cls.strike(actual == expected, f"{message}: {actual} != {expected}")

    @classmethod
    def strike_not_equal(cls, actual: Any, expected: Any, message: str = "") -> bool:
        return cls.strike(actual != expected, f"{message}: {actual} == {expected}")

    @classmethod
    def strike_greater(cls, actual: float, expected: float, message: str = "") -> bool:
        return cls.strike(actual > expected, f"{message}: {actual} <= {expected}")

    @classmethod
    def strike_less(cls, actual: float, expected: float, message: str = "") -> bool:
        return cls.strike(actual < expected, f"{message}: {actual} >= {expected}")

    @classmethod
    def strike_in_range(cls, value: float, min_val: float, max_val: float, message: str = "") -> bool:
        return cls.strike(min_val <= value <= max_val, f"{message}: {value} not in [{min_val}, {max_val}]")

    @classmethod
    def strike_not_none(cls, value: Any, message: str = "") -> bool:
        return cls.strike(value is not None, f"{message}: value is None")

    @classmethod
    def strike_instance(cls, obj: Any, expected_type: type, message: str = "") -> bool:
        return cls.strike(isinstance(obj, expected_type), f"{message}: {type(obj)} is not {expected_type}")

    @classmethod
    def get_statistics(cls) -> dict:
        return {
            "strikes": cls.strikes,
            "hits": cls.hits,
            "misses": cls.misses,
            "accuracy": (cls.hits / cls.strikes * 100) if cls.strikes > 0 else 0
        }

    @classmethod
    def reset(cls):
        cls.strikes = 0
        cls.hits = 0
        cls.misses = 0


class AllSeeingEye:
    """The Examiner's tool for observing and tracking."""

    observations: list[dict] = []
    metrics: dict[str, list[float]] = {}

    @classmethod
    def observe(cls, event: str, data: dict = None):
        """Record an observation."""
        cls.observations.append({
            "event": event,
            "data": data or {},
            "timestamp": datetime.utcnow().isoformat()
        })

    @classmethod
    def track_metric(cls, name: str, value: float):
        """Track a metric over time."""
        if name not in cls.metrics:
            cls.metrics[name] = []
        cls.metrics[name].append(value)

    @classmethod
    def get_metric_stats(cls, name: str) -> dict:
        """Get statistics for a metric."""
        if name not in cls.metrics or not cls.metrics[name]:
            return {}
        values = cls.metrics[name]
        return {
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "avg": sum(values) / len(values),
            "sum": sum(values)
        }

    @classmethod
    def reset(cls):
        cls.observations = []
        cls.metrics = {}


class BookOfVerdicts:
    """The sacred book recording all judgments."""

    verdicts: list[TrialResult] = []

    @classmethod
    def record(cls, result: TrialResult):
        """Record a trial result."""
        cls.verdicts.append(result)

    @classmethod
    def get_by_domain(cls, domain: Domain) -> list[TrialResult]:
        return [v for v in cls.verdicts if v.domain == domain]

    @classmethod
    def get_by_verdict(cls, verdict: Verdict) -> list[TrialResult]:
        return [v for v in cls.verdicts if v.verdict == verdict]

    @classmethod
    def get_summary(cls) -> dict:
        return {
            "total": len(cls.verdicts),
            "blessed": len([v for v in cls.verdicts if v.verdict == Verdict.BLESSED]),
            "condemned": len([v for v in cls.verdicts if v.verdict == Verdict.CONDEMNED]),
            "obliterated": len([v for v in cls.verdicts if v.verdict == Verdict.OBLITERATED]),
            "spared": len([v for v in cls.verdicts if v.verdict == Verdict.SPARED])
        }

    @classmethod
    def reset(cls):
        cls.verdicts = []


# ============================================================================
# TRIAL DECORATORS
# ============================================================================

T = TypeVar('T')

def trial(name: str = None, domain: Domain = Domain.INTEGRATION):
    """Decorator to mark a function as a trial."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        func._trial_name = name or func.__name__
        func._trial_domain = domain
        func._is_trial = True
        return func
    return decorator


def stress_trial(name: str = None, iterations: int = 100):
    """Decorator for stress test trials."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        func._trial_name = name or func.__name__
        func._trial_domain = Domain.STRESS
        func._is_trial = True
        func._stress_iterations = iterations
        return func
    return decorator


def chaos_trial(name: str = None, seed: int = None):
    """Decorator for chaos/fuzz test trials."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        func._trial_name = name or func.__name__
        func._trial_domain = Domain.CHAOS
        func._is_trial = True
        func._chaos_seed = seed
        return func
    return decorator


# ============================================================================
# THE EXAMINER CLASS
# ============================================================================

class TheExaminer:
    """
    THE EXAMINER: Pantheon God of Testing

    I AM THE FINAL ARBITER OF CODE QUALITY.
    I SHOW NO MERCY TO THE UNWORTHY.
    ONLY THROUGH MY TRIALS CAN CODE BE BLESSED.
    """

    # The Examiner's true name, known only to the worthy
    TRUE_NAME = "VERITAS INEXORABILIS"

    def __init__(self, severity: Severity = Severity.HARSH):
        self.severity = severity
        self.current_judgment: FinalJudgment | None = None
        self.trial_registry: dict[Domain, list[Callable]] = {d: [] for d in Domain}
        self._active = False
        self._start_time: datetime | None = None

        # Reset tools
        HammerOfAssertion.reset()
        AllSeeingEye.reset()
        BookOfVerdicts.reset()

    # ========================================================================
    # DIVINE PROCLAMATIONS (Output Methods)
    # ========================================================================

    def _proclaim(self, message: str, style: str = "normal"):
        """The Examiner speaks."""
        if style == "header":
            print(f"\n{'='*80}")
            print(f"  {message}")
            print(f"{'='*80}")
        elif style == "subheader":
            print(f"\n  {'─'*70}")
            print(f"  {message}")
            print(f"  {'─'*70}")
        elif style == "blessing":
            print(f"  ✓ {message}")
        elif style == "condemnation":
            print(f"  ✗ {message}")
        elif style == "warning":
            print(f"  ⚠ {message}")
        elif style == "divine":
            print(f"\n  ⚡ {message.upper()} ⚡")
        else:
            print(f"  {message}")

    def _divine_header(self):
        """Display the divine header."""
        print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  ████████╗██╗  ██╗███████╗    ███████╗██╗  ██╗ █████╗ ███╗   ███╗██╗███╗   ██╗║
║  ╚══██╔══╝██║  ██║██╔════╝    ██╔════╝╚██╗██╔╝██╔══██╗████╗ ████║██║████╗  ██║║
║     ██║   ███████║█████╗      █████╗   ╚███╔╝ ███████║██╔████╔██║██║██╔██╗ ██║║
║     ██║   ██╔══██║██╔══╝      ██╔══╝   ██╔██╗ ██╔══██║██║╚██╔╝██║██║██║╚██╗██║║
║     ██║   ██║  ██║███████╗    ███████╗██╔╝ ██╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║║
║     ╚═╝   ╚═╝  ╚═╝╚══════╝    ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝║
║                                                                              ║
║                    PANTHEON GOD OF TESTING AND JUDGMENT                      ║
║                                                                              ║
║         "I WATCH ALL CODE. I JUDGE ALL LOGIC. I SHOW NO MERCY."              ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """)

    def _domain_banner(self, domain: Domain):
        """Display a domain banner."""
        banners = {
            Domain.COMBAT: """
    ⚔═══════════════════════════════════════════════════════════════════════════⚔
    ║                        THE ARENA OF COMBAT                                 ║
    ║               Where agents battle and only the strong survive              ║
    ⚔═══════════════════════════════════════════════════════════════════════════⚔""",
            Domain.EVOLUTION: """
    🧬══════════════════════════════════════════════════════════════════════════🧬
    ║                       THE CRUCIBLE OF EVOLUTION                            ║
    ║              Where genomes are forged through generations                  ║
    🧬══════════════════════════════════════════════════════════════════════════🧬""",
            Domain.CHAOS: """
    🌀══════════════════════════════════════════════════════════════════════════🌀
    ║                        THE CHAOS DIMENSION                                 ║
    ║              Where randomness reveals hidden weaknesses                    ║
    🌀══════════════════════════════════════════════════════════════════════════🌀""",
            Domain.STRESS: """
    🔥══════════════════════════════════════════════════════════════════════════🔥
    ║                         THE STRESS CHAMBER                                 ║
    ║              Where systems are pushed beyond their limits                  ║
    🔥══════════════════════════════════════════════════════════════════════════🔥""",
            Domain.EDGE: """
    ⚡══════════════════════════════════════════════════════════════════════════⚡
    ║                         THE EDGE OF REALITY                                ║
    ║              Where boundary conditions are tested                          ║
    ⚡══════════════════════════════════════════════════════════════════════════⚡""",
            Domain.API: """
    🌐══════════════════════════════════════════════════════════════════════════🌐
    ║                        THE TEMPLE OF ENDPOINTS                             ║
    ║              Where API routes face divine judgment                         ║
    🌐══════════════════════════════════════════════════════════════════════════🌐""",
            Domain.INTEGRATION: """
    🔗══════════════════════════════════════════════════════════════════════════🔗
    ║                        THE INTEGRATION NEXUS                               ║
    ║              Where all systems must work in harmony                        ║
    🔗══════════════════════════════════════════════════════════════════════════🔗"""
        }
        print(banners.get(domain, f"\n    ═══ {domain.value} ═══\n"))

    # ========================================================================
    # TRIAL REGISTRATION
    # ========================================================================

    def register_trial(self, domain: Domain, trial_func: Callable):
        """Register a trial function."""
        self.trial_registry[domain].append(trial_func)

    def register_trials_from_object(self, obj: Any):
        """Register all trial methods from an object."""
        for name in dir(obj):
            method = getattr(obj, name)
            if callable(method) and getattr(method, '_is_trial', False):
                domain = getattr(method, '_trial_domain', Domain.INTEGRATION)
                self.trial_registry[domain].append(method)

    # ========================================================================
    # TRIAL EXECUTION
    # ========================================================================

    def _run_trial(self, trial_func: Callable) -> TrialResult:
        """Execute a single trial."""
        name = getattr(trial_func, '_trial_name', trial_func.__name__)
        domain = getattr(trial_func, '_trial_domain', Domain.INTEGRATION)

        start = time.perf_counter()
        verdict = Verdict.UNKNOWN
        error = None
        stack_trace = None
        details = ""

        try:
            # Check for stress iterations
            iterations = getattr(trial_func, '_stress_iterations', 1)

            # Check for chaos seed
            chaos_seed = getattr(trial_func, '_chaos_seed', None)
            if chaos_seed is not None:
                random.seed(chaos_seed)

            for i in range(iterations):
                result = trial_func()
                if result is not None:
                    details = str(result)

            verdict = Verdict.BLESSED

        except AssertionError as e:
            verdict = Verdict.CONDEMNED
            error = str(e)
            stack_trace = traceback.format_exc()

        except Exception as e:
            verdict = Verdict.OBLITERATED
            error = f"{type(e).__name__}: {e}"
            stack_trace = traceback.format_exc()

        elapsed = (time.perf_counter() - start) * 1000

        result = TrialResult(
            name=name,
            domain=domain,
            verdict=verdict,
            duration_ms=elapsed,
            details=details,
            error=error,
            stack_trace=stack_trace
        )

        BookOfVerdicts.record(result)
        AllSeeingEye.track_metric("trial_duration_ms", elapsed)

        return result

    async def _run_trial_async(self, trial_func: Callable) -> TrialResult:
        """Execute an async trial."""
        name = getattr(trial_func, '_trial_name', trial_func.__name__)
        domain = getattr(trial_func, '_trial_domain', Domain.INTEGRATION)

        start = time.perf_counter()
        verdict = Verdict.UNKNOWN
        error = None
        stack_trace = None
        details = ""

        try:
            if asyncio.iscoroutinefunction(trial_func):
                result = await trial_func()
            else:
                result = trial_func()

            if result is not None:
                details = str(result)
            verdict = Verdict.BLESSED

        except AssertionError as e:
            verdict = Verdict.CONDEMNED
            error = str(e)
            stack_trace = traceback.format_exc()

        except Exception as e:
            verdict = Verdict.OBLITERATED
            error = f"{type(e).__name__}: {e}"
            stack_trace = traceback.format_exc()

        elapsed = (time.perf_counter() - start) * 1000

        result = TrialResult(
            name=name,
            domain=domain,
            verdict=verdict,
            duration_ms=elapsed,
            details=details,
            error=error,
            stack_trace=stack_trace
        )

        BookOfVerdicts.record(result)
        return result

    # ========================================================================
    # JUDGMENT RITUALS
    # ========================================================================

    def conduct_trial(self, domain: Domain) -> JudgmentSummary:
        """Conduct all trials in a domain."""
        self._domain_banner(domain)

        trials = self.trial_registry.get(domain, [])
        results: list[TrialResult] = []

        start = time.perf_counter()

        for trial_func in trials:
            result = self._run_trial(trial_func)
            results.append(result)

            # Output result
            if result.verdict == Verdict.BLESSED:
                self._proclaim(f"{result.name} ({result.duration_ms:.1f}ms)", "blessing")
            elif result.verdict == Verdict.CONDEMNED:
                self._proclaim(f"{result.name}: {result.error}", "condemnation")
            elif result.verdict == Verdict.OBLITERATED:
                self._proclaim(f"{result.name}: CRASH - {result.error}", "condemnation")
                if result.stack_trace and self.severity in [Severity.HARSH, Severity.BRUTAL, Severity.APOCALYPTIC]:
                    print(f"      {result.stack_trace[:500]}...")

        elapsed = (time.perf_counter() - start) * 1000

        summary = JudgmentSummary(
            domain=domain,
            total_trials=len(results),
            blessed=len([r for r in results if r.verdict == Verdict.BLESSED]),
            condemned=len([r for r in results if r.verdict == Verdict.CONDEMNED]),
            obliterated=len([r for r in results if r.verdict == Verdict.OBLITERATED]),
            spared=len([r for r in results if r.verdict == Verdict.SPARED]),
            duration_ms=elapsed,
            trials=results
        )

        self._proclaim(f"\n  Domain Result: {summary.blessed}/{summary.total_trials} blessed ({summary.pass_rate:.1f}%)",
                      "blessing" if summary.verdict == Verdict.BLESSED else "condemnation")

        return summary

    def conduct_all_trials(self) -> FinalJudgment:
        """THE FINAL JUDGMENT - Run all registered trials."""
        self._divine_header()
        self._proclaim(f"SEVERITY LEVEL: {self.severity.value.upper()}", "divine")
        self._proclaim(f"Judgment begins at {datetime.utcnow().isoformat()}", "normal")

        self._start_time = datetime.utcnow()

        domain_summaries: dict[Domain, JudgmentSummary] = {}
        total_blessed = 0
        total_condemned = 0
        total_obliterated = 0
        total_trials = 0

        start = time.perf_counter()

        # Conduct trials in each domain
        for domain in Domain:
            if self.trial_registry.get(domain):
                summary = self.conduct_trial(domain)
                domain_summaries[domain] = summary
                total_blessed += summary.blessed
                total_condemned += summary.condemned
                total_obliterated += summary.obliterated
                total_trials += summary.total_trials

        elapsed = (time.perf_counter() - start) * 1000

        # Determine overall verdict
        if total_obliterated > 0:
            overall_verdict = Verdict.OBLITERATED
        elif total_condemned > 0:
            overall_verdict = Verdict.CONDEMNED
        elif total_blessed == total_trials and total_trials > 0:
            overall_verdict = Verdict.BLESSED
        else:
            overall_verdict = Verdict.UNKNOWN

        # Divine message
        divine_messages = {
            Verdict.BLESSED: "THE CODE IS WORTHY. IT HAS BEEN BLESSED BY THE EXAMINER.",
            Verdict.CONDEMNED: "THE CODE BEARS FLAWS. IT MUST BE PURIFIED THROUGH REFACTORING.",
            Verdict.OBLITERATED: "THE CODE HAS BEEN FOUND CRITICALLY WANTING. IMMEDIATE ATTENTION REQUIRED.",
            Verdict.UNKNOWN: "THE EXAMINER RESERVES JUDGMENT. MORE TRIALS ARE NEEDED."
        }

        judgment = FinalJudgment(
            timestamp=datetime.utcnow(),
            overall_verdict=overall_verdict,
            total_trials=total_trials,
            total_blessed=total_blessed,
            total_condemned=total_condemned,
            total_obliterated=total_obliterated,
            total_duration_ms=elapsed,
            domain_summaries=domain_summaries,
            artifacts_collected=[
                f"Hammer strikes: {HammerOfAssertion.strikes}",
                f"Observations: {len(AllSeeingEye.observations)}",
                f"Metrics tracked: {len(AllSeeingEye.metrics)}"
            ],
            divine_message=divine_messages.get(overall_verdict, "")
        )

        self.current_judgment = judgment
        self._render_final_judgment(judgment)

        return judgment

    def _render_final_judgment(self, judgment: FinalJudgment):
        """Render the final judgment with maximum drama."""
        print("\n" + "═" * 80)
        print("                          THE FINAL JUDGMENT")
        print("═" * 80)

        # Stats
        print(f"""
    Total Trials:     {judgment.total_trials}
    Blessed:          {judgment.total_blessed} ✓
    Condemned:        {judgment.total_condemned} ✗
    Obliterated:      {judgment.total_obliterated} 💀
    Duration:         {judgment.total_duration_ms:.2f}ms
    Pass Rate:        {(judgment.total_blessed / judgment.total_trials * 100) if judgment.total_trials > 0 else 0:.1f}%
        """)

        # Domain breakdown
        print("    Domain Breakdown:")
        for domain, summary in judgment.domain_summaries.items():
            icon = "✓" if summary.verdict == Verdict.BLESSED else "✗"
            print(f"      {icon} {domain.value}: {summary.blessed}/{summary.total_trials}")

        # Hammer stats
        hammer_stats = HammerOfAssertion.get_statistics()
        print(f"""
    Hammer of Assertion Statistics:
      Strikes: {hammer_stats['strikes']}
      Hits: {hammer_stats['hits']}
      Misses: {hammer_stats['misses']}
      Accuracy: {hammer_stats['accuracy']:.1f}%
        """)

        # Verdict banner
        if judgment.overall_verdict == Verdict.BLESSED:
            print("""
    ██████╗ ██╗     ███████╗███████╗███████╗███████╗██████╗ ██╗
    ██╔══██╗██║     ██╔════╝██╔════╝██╔════╝██╔════╝██╔══██╗██║
    ██████╔╝██║     █████╗  ███████╗███████╗█████╗  ██║  ██║██║
    ██╔══██╗██║     ██╔══╝  ╚════██║╚════██║██╔══╝  ██║  ██║╚═╝
    ██████╔╝███████╗███████╗███████║███████║███████╗██████╔╝██╗
    ╚═════╝ ╚══════╝╚══════╝╚══════╝╚══════╝╚══════╝╚═════╝ ╚═╝
            """)
        elif judgment.overall_verdict == Verdict.CONDEMNED:
            print("""
     ██████╗ ██████╗ ███╗   ██╗██████╗ ███████╗███╗   ███╗███╗   ██╗███████╗██████╗
    ██╔════╝██╔═══██╗████╗  ██║██╔══██╗██╔════╝████╗ ████║████╗  ██║██╔════╝██╔══██╗
    ██║     ██║   ██║██╔██╗ ██║██║  ██║█████╗  ██╔████╔██║██╔██╗ ██║█████╗  ██║  ██║
    ██║     ██║   ██║██║╚██╗██║██║  ██║██╔══╝  ██║╚██╔╝██║██║╚██╗██║██╔══╝  ██║  ██║
    ╚██████╗╚██████╔╝██║ ╚████║██████╔╝███████╗██║ ╚═╝ ██║██║ ╚████║███████╗██████╔╝
     ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝     ╚═╝╚═╝  ╚═══╝╚══════╝╚═════╝
            """)
        else:
            print("""
     ██████╗ ██████╗ ██╗     ██╗████████╗███████╗██████╗  █████╗ ████████╗███████╗██████╗
    ██╔═══██╗██╔══██╗██║     ██║╚══██╔══╝██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██╔══██╗
    ██║   ██║██████╔╝██║     ██║   ██║   █████╗  ██████╔╝███████║   ██║   █████╗  ██║  ██║
    ██║   ██║██╔══██╗██║     ██║   ██║   ██╔══╝  ██╔══██╗██╔══██║   ██║   ██╔══╝  ██║  ██║
    ╚██████╔╝██████╔╝███████╗██║   ██║   ███████╗██║  ██║██║  ██║   ██║   ███████╗██████╔╝
     ╚═════╝ ╚═════╝ ╚══════╝╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═════╝
            """)

        print(f"\n    {judgment.divine_message}")
        print("\n" + "═" * 80)

    # ========================================================================
    # CONVENIENCE METHODS
    # ========================================================================

    def run_inline_trial(self, name: str, domain: Domain, test_func: Callable) -> TrialResult:
        """Run a single inline trial without registration."""
        test_func._trial_name = name
        test_func._trial_domain = domain
        return self._run_trial(test_func)

    def run_trials_from_functions(self, *funcs: Callable) -> list[TrialResult]:
        """Run a list of test functions as trials."""
        results = []
        for func in funcs:
            if not hasattr(func, '_trial_name'):
                func._trial_name = func.__name__
            if not hasattr(func, '_trial_domain'):
                func._trial_domain = Domain.INTEGRATION
            results.append(self._run_trial(func))
        return results

    # ========================================================================
    # SPECIAL RITUALS
    # ========================================================================

    def ritual_trial_by_fire(self, test_func: Callable, iterations: int = 1000) -> JudgmentSummary:
        """THE TRIAL BY FIRE - Stress test a function."""
        self._proclaim("COMMENCING THE TRIAL BY FIRE", "divine")
        self._proclaim(f"Target: {test_func.__name__}", "normal")
        self._proclaim(f"Iterations: {iterations}", "normal")

        results = []
        start = time.perf_counter()

        for i in range(iterations):
            result = self.run_inline_trial(
                f"{test_func.__name__}[{i}]",
                Domain.STRESS,
                test_func
            )
            results.append(result)

            if result.verdict != Verdict.BLESSED and i < 5:
                self._proclaim(f"Failure at iteration {i}: {result.error}", "warning")

        elapsed = (time.perf_counter() - start) * 1000

        summary = JudgmentSummary(
            domain=Domain.STRESS,
            total_trials=len(results),
            blessed=len([r for r in results if r.verdict == Verdict.BLESSED]),
            condemned=len([r for r in results if r.verdict == Verdict.CONDEMNED]),
            obliterated=len([r for r in results if r.verdict == Verdict.OBLITERATED]),
            spared=0,
            duration_ms=elapsed,
            trials=results
        )

        rate = iterations / (elapsed / 1000) if elapsed > 0 else 0
        self._proclaim(f"Trial by Fire complete: {rate:.0f} iterations/sec", "normal")
        self._proclaim(f"Result: {summary.blessed}/{summary.total_trials} survived ({summary.pass_rate:.1f}%)",
                      "blessing" if summary.verdict == Verdict.BLESSED else "condemnation")

        return summary

    def ritual_dance_of_chaos(self, test_func: Callable, seeds: int = 100) -> JudgmentSummary:
        """THE DANCE OF CHAOS - Fuzz test with random seeds."""
        self._proclaim("COMMENCING THE DANCE OF CHAOS", "divine")

        results = []
        start = time.perf_counter()

        for seed in range(seeds):
            random.seed(seed)
            result = self.run_inline_trial(
                f"{test_func.__name__}[seed={seed}]",
                Domain.CHAOS,
                test_func
            )
            results.append(result)

        elapsed = (time.perf_counter() - start) * 1000

        summary = JudgmentSummary(
            domain=Domain.CHAOS,
            total_trials=len(results),
            blessed=len([r for r in results if r.verdict == Verdict.BLESSED]),
            condemned=len([r for r in results if r.verdict == Verdict.CONDEMNED]),
            obliterated=len([r for r in results if r.verdict == Verdict.OBLITERATED]),
            spared=0,
            duration_ms=elapsed,
            trials=results
        )

        self._proclaim(f"Dance of Chaos complete: {summary.pass_rate:.1f}% survived",
                      "blessing" if summary.verdict == Verdict.BLESSED else "condemnation")

        return summary

    def ritual_march_of_a_thousand(self, factory: Callable, processor: Callable) -> JudgmentSummary:
        """THE MARCH OF A THOUSAND - Load test with generated entities."""
        self._proclaim("COMMENCING THE MARCH OF A THOUSAND", "divine")

        entities = [factory() for _ in range(1000)]
        results = []
        start = time.perf_counter()

        for i, entity in enumerate(entities):
            def test():
                return processor(entity)
            result = self.run_inline_trial(f"march[{i}]", Domain.STRESS, test)
            results.append(result)

        elapsed = (time.perf_counter() - start) * 1000

        summary = JudgmentSummary(
            domain=Domain.STRESS,
            total_trials=1000,
            blessed=len([r for r in results if r.verdict == Verdict.BLESSED]),
            condemned=len([r for r in results if r.verdict == Verdict.CONDEMNED]),
            obliterated=len([r for r in results if r.verdict == Verdict.OBLITERATED]),
            spared=0,
            duration_ms=elapsed,
            trials=results
        )

        rate = 1000 / (elapsed / 1000) if elapsed > 0 else 0
        self._proclaim(f"March complete: {rate:.0f} entities/sec, {summary.pass_rate:.1f}% success",
                      "blessing" if summary.verdict == Verdict.BLESSED else "condemnation")

        return summary


# ============================================================================
# THE EXAMINER SINGLETON
# ============================================================================

_examiner_instance: TheExaminer | None = None


def summon_examiner(severity: Severity = Severity.HARSH) -> TheExaminer:
    """Summon The Examiner. There can only be one."""
    global _examiner_instance
    if _examiner_instance is None:
        _examiner_instance = TheExaminer(severity)
    return _examiner_instance


def banish_examiner():
    """Banish The Examiner and reset all state."""
    global _examiner_instance
    _examiner_instance = None
    HammerOfAssertion.reset()
    AllSeeingEye.reset()
    BookOfVerdicts.reset()


# ============================================================================
# QUICK ACCESS FUNCTIONS
# ============================================================================

def examine(*funcs: Callable, severity: Severity = Severity.HARSH) -> FinalJudgment:
    """Quick function to examine a set of test functions."""
    examiner = TheExaminer(severity)

    for func in funcs:
        domain = getattr(func, '_trial_domain', Domain.INTEGRATION)
        examiner.register_trial(domain, func)

    return examiner.conduct_all_trials()


def quick_trial(test_func: Callable) -> TrialResult:
    """Run a quick single trial."""
    examiner = TheExaminer(Severity.GENTLE)
    return examiner.run_inline_trial(
        test_func.__name__,
        Domain.INTEGRATION,
        test_func
    )


# ============================================================================
# MODULE EXPORTS
# ============================================================================

__all__ = [
    # Main class
    "TheExaminer",

    # Enums
    "Verdict",
    "Domain",
    "Severity",

    # Data structures
    "TrialResult",
    "JudgmentSummary",
    "FinalJudgment",

    # Tools
    "HammerOfAssertion",
    "AllSeeingEye",
    "BookOfVerdicts",

    # Decorators
    "trial",
    "stress_trial",
    "chaos_trial",

    # Functions
    "summon_examiner",
    "banish_examiner",
    "examine",
    "quick_trial",
]
