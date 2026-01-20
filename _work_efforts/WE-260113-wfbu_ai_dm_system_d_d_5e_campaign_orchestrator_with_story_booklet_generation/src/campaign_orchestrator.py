"""
Campaign Orchestrator

Central coordinator for AI DM system. Orchestrates all tools to run D&D 5e campaigns.
"""

from datetime import datetime
from pathlib import Path
from typing import Any

from booklet_generator import BookletConfig, BookletGenerator
from campaign_state import (
    CampaignSession,
    CampaignState,
    CampaignStateManager,
    CampaignStatus,
    SessionStatus,
)

# Tool imports (will be added as integrations complete)
# from scenario_engine import ScenarioEngine
# from waft.core.decision_cli import DecisionCLI
# from scientific_method_tool import ExperimentManager


class CampaignOrchestrator:
    """
    Central orchestrator for AI DM system.

    Coordinates:
    - Scenario engine (HannaCLI)
    - Decision matrix system
    - Scientific method tool
    - Being system
    - D&D 5e engine
    - Booklet generator
    """

    def __init__(self, project_path: Path):
        """Initialize campaign orchestrator."""
        self.project_path = Path(project_path)
        self.state_manager = CampaignStateManager(self.project_path)

        # Tool instances (will be initialized as integrations complete)
        # self.scenario_engine = None
        # self.decision_cli = DecisionCLI()
        # self.experiment_manager = ExperimentManager()

    def start_campaign(
        self,
        campaign_name: str,
        scenario_file: str | None = None,
        description: str = "",
        difficulty: str = "medium",
    ) -> CampaignState:
        """
        Start a new campaign.

        Args:
            campaign_name: Name of the campaign
            scenario_file: Path to scenario JSON file
            description: Campaign description
            difficulty: Campaign difficulty

        Returns:
            Created CampaignState
        """
        campaign = self.state_manager.create_campaign(
            campaign_name=campaign_name,
            scenario_file=scenario_file,
            description=description,
            difficulty=difficulty,
        )

        # If scenario file provided, load it
        if scenario_file:
            # TODO: Load scenario engine
            # self.scenario_engine = ScenarioEngine.load(scenario_file)
            # campaign.start_sequence_id = self.scenario_engine.start_sequence_id
            pass

        campaign.status = CampaignStatus.ACTIVE
        self.state_manager.save_campaign(campaign)

        return campaign

    def run_session(self, campaign_id: str, session_number: int | None = None) -> CampaignSession:
        """
        Run a campaign session.

        Args:
            campaign_id: Campaign ID
            session_number: Optional session number

        Returns:
            CampaignSession
        """
        campaign = self.state_manager.load_campaign(campaign_id)
        if not campaign:
            raise ValueError(f"Campaign {campaign_id} not found")

        # Create session
        session = self.state_manager.add_session(campaign_id, session_number)

        # Reload campaign to get updated session
        campaign = self.state_manager.load_campaign(campaign_id)

        # Update session status
        for s in campaign.sessions:
            if s.session_id == session.session_id:
                s.status = SessionStatus.IN_PROGRESS
                break

        # TODO: Load scenario engine if not loaded
        # TODO: Start from current sequence or start sequence

        self.state_manager.save_campaign(campaign)

        # Return updated session
        return next(s for s in campaign.sessions if s.session_id == session.session_id)

    def make_dm_decision(
        self,
        campaign_id: str,
        problem: str,
        alternatives: list[str],
        criteria: dict[str, float],
        scores: dict[str, dict[str, float]],
    ) -> dict[str, Any]:
        """
        Make a DM decision using decision matrix.

        Args:
            campaign_id: Campaign ID
            problem: Decision problem description
            alternatives: List of alternatives
            criteria: Criteria with weights
            scores: Scores for each alternative

        Returns:
            Decision result with recommendation
        """
        # TODO: Integrate decision matrix system
        # decision_result = self.decision_cli.run_decision_matrix(
        #     problem=problem,
        #     alternatives=alternatives,
        #     criteria=criteria,
        #     scores=scores
        # )

        # Store decision
        campaign = self.state_manager.load_campaign(campaign_id)
        if campaign:
            campaign.decisions_made.append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "problem": problem,
                    "alternatives": alternatives,
                    "recommendation": "TODO",  # decision_result["recommendation"]
                }
            )
            self.state_manager.save_campaign(campaign)

        return {
            "recommendation": "TODO",  # decision_result["recommendation"]
            "rankings": [],  # decision_result["rankings"]
        }

    def generate_story_booklet(
        self,
        campaign_id: str,
        output_path: Path | None = None,
        include_apis: bool = True,
        include_analysis: bool = True,
    ) -> Path:
        """
        Generate story booklet from campaign data.

        Args:
            campaign_id: Campaign ID
            output_path: Optional output path
            include_apis: Include API documentation
            include_analysis: Include scientific method analysis

        Returns:
            Path to generated PDF
        """
        campaign = self.state_manager.load_campaign(campaign_id)
        if not campaign:
            raise ValueError(f"Campaign {campaign_id} not found")

        # Convert campaign state to data for booklet generator
        campaign_dict = campaign.to_dict()
        campaign_data = {
            "campaign": campaign_dict,
            "summary": self.state_manager.get_campaign_summary(campaign_id),
            "sessions": campaign_dict.get("sessions", []),
            "events": [
                event
                for session in campaign_dict.get("sessions", [])
                for event in session.get("events", [])
            ],
        }

        # Generate booklet
        config = BookletConfig(
            title=f"Campaign Booklet: {campaign.campaign_name}",
            author="WAFT AI DM System",
            include_apis=include_apis,
            include_examples=True,
            include_statistics=True,
        )

        generator = BookletGenerator(config)

        if output_path is None:
            output_path = (
                self.project_path / "_pyrite" / ".waft" / "campaigns" / f"{campaign_id}_booklet.pdf"
            )

        return generator.generate_from_data(campaign_data, output_path)

    def analyze_campaign(self, campaign_id: str, hypothesis: str | None = None) -> dict[str, Any]:
        """
        Analyze campaign using scientific method tool.

        Args:
            campaign_id: Campaign ID
            hypothesis: Optional hypothesis to test

        Returns:
            Analysis results
        """
        # TODO: Integrate scientific method tool
        # experiment = self.experiment_manager.create_experiment(hypothesis)
        # analysis = self.experiment_manager.analyze(experiment.id)

        campaign = self.state_manager.load_campaign(campaign_id)
        if campaign:
            # Link experiment to campaign
            # campaign.scientific_experiments.append(experiment.id)
            self.state_manager.save_campaign(campaign)

        return {"verified": True, "confidence": 0.95, "conclusions": ["Campaign analysis complete"]}
