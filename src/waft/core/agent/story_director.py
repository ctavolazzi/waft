"""
Story Director Agent - Specialized agent for narrative decision-making.

Extends BaseAgent to make autonomous decisions about story evolution,
plot direction, character actions, and narrative development.
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import random

from .base import BaseAgent
from .state import AgentState, AgentConfig
from ...evolution.story_state import StoryState
from ...evolution.narrative_decisions import NarrativeDecision, DecisionType, DecisionValidator
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...evolution.evolving_story import EvolvingStory


class StoryDirector(BaseAgent):
    """
    Agent specialized for directing story evolution.
    
    Observes story state, makes narrative decisions, and guides
    story development through the OODA loop.
    """
    
    def __init__(
        self,
        config: AgentConfig,
        project_path: Path,
        story: Optional[Any] = None  # EvolvingStory
    ):
        """
        Initialize Story Director.
        
        Args:
            config: Agent configuration
            project_path: Project path
            story: Evolving story to direct (can be set later)
        """
        super().__init__(config, project_path)
        self.story = story
        self.decision_history: List[NarrativeDecision] = []
    
    def set_story(self, story: Any) -> None:  # EvolvingStory
        """Set the story to direct."""
        self.story = story
    
    async def observe(self) -> Dict[str, Any]:
        """
        Observe current story state (OODA: Observe).
        
        Analyzes story state to understand current narrative situation.
        
        Returns:
            Dictionary with observed story state
        """
        if not self.story:
            return {
                "status": "error",
                "message": "No story set for director"
            }
        
        state = self.story.get_current_state()
        
        # Analyze story state
        observation = {
            "status": "success",
            "story_id": state.story_id,
            "generation": state.generation,
            "title": state.title,
            "characters": {
                name: {
                    "name": char.name,
                    "role": char.role,
                    "mentions": char.mentions,
                    "last_appearance": char.last_appearance.isoformat() if char.last_appearance else None
                }
                for name, char in state.characters.items()
            },
            "recent_events": [
                {
                    "description": event.description,
                    "character": event.character,
                    "category": event.category,
                    "timestamp": event.timestamp.isoformat()
                }
                for event in state.get_recent_events(limit=5)
            ],
            "timeline_length": len(state.timeline),
            "plot_points": len(state.plot_points),
            "coherence_score": state.coherence_score,
            "summary": state.summary
        }
        
        # Store in agent memory
        from .state import Message, MessageRole
        self.state.memory.append(Message(
            role=MessageRole.AGENT,
            content=f"Observed story state at generation {state.generation}",
            metadata={"observation": observation}
        ))
        
        return observation
    
    async def decide(self, state: AgentState) -> Dict[str, Any]:
        """
        Make narrative decision (OODA: Orient/Decide).
        
        Chooses what should happen next in the story.
        
        Args:
            state: Current agent state
            
        Returns:
            Dictionary with decision
        """
        if not self.story:
            return {
                "status": "error",
                "message": "No story set for director",
                "stop": True
            }
        
        story_state = self.story.get_current_state()
        
        # Analyze story to determine best decision type
        decision_type = self._choose_decision_type(story_state)
        decision_content = self._generate_decision_content(decision_type, story_state)
        
        # Create narrative decision
        decision = NarrativeDecision(
            decision_type=decision_type,
            agent_id=self.state.agent_id,
            generation=story_state.generation + 1,
            description=decision_content["description"],
            character=decision_content.get("character"),
            location=decision_content.get("location"),
            narrative_text=decision_content.get("narrative_text"),
            importance=decision_content.get("importance", 0.5),
            confidence=decision_content.get("confidence", 0.7),
            reasoning=decision_content.get("reasoning")
        )
        
        # Store decision in agent memory
        from .state import Message, MessageRole
        self.state.memory.append(Message(
            role=MessageRole.AGENT,
            content=f"Decided: {decision_type.value} - {decision.description}",
            metadata={"decision": decision.dict()}
        ))
        
        return {
            "status": "success",
            "decision": decision.dict(),
            "stop": False
        }
    
    async def act(self, decision: dict) -> Dict[str, Any]:
        """
        Apply decision to story (OODA: Act).
        
        Args:
            decision: Decision from decide() step
            
        Returns:
            Dictionary with action result
        """
        if decision.get("status") != "success" or "decision" not in decision:
            return {
                "status": "error",
                "message": "Invalid decision",
                "applied": False
            }
        
        # Reconstruct decision object
        decision_data = decision["decision"]
        narrative_decision = NarrativeDecision(**decision_data)
        
        # Apply to story
        applied = self.story.apply_decision(narrative_decision)
        
        if applied:
            self.decision_history.append(narrative_decision)
            
            # Store in agent memory
            from .state import Message, MessageRole
            self.state.memory.append(Message(
                role=MessageRole.AGENT,
                content=f"Applied decision: {narrative_decision.description}",
                metadata={"decision_id": narrative_decision.decision_id}
            ))
        
        return {
            "status": "success" if applied else "failed",
            "applied": applied,
            "decision_id": narrative_decision.decision_id,
            "generation": self.story.state.generation
        }
    
    async def reflect(self, result: dict) -> Dict[str, Any]:
        """
        Reflect on story evolution (OODA: Reflect).
        
        Evaluates story quality and coherence after decision.
        
        Args:
            result: Result from act() step
            
        Returns:
            Dictionary with reflection
        """
        if not self.story:
            return {
                "status": "error",
                "message": "No story set for director"
            }
        
        story_state = self.story.get_current_state()
        
        # Evaluate story quality
        reflection = {
            "status": "success",
            "generation": story_state.generation,
            "coherence_score": story_state.coherence_score,
            "characters_count": len(story_state.characters),
            "events_count": len(story_state.timeline),
            "quality_assessment": self._assess_story_quality(story_state),
            "suggestions": self._generate_suggestions(story_state)
        }
        
        # Store in agent memory
        from .state import Message, MessageRole
        self.state.memory.append(Message(
            role=MessageRole.AGENT,
            content=f"Reflected on generation {story_state.generation}",
            metadata={"reflection": reflection}
        ))
        
        return reflection
    
    async def evolve_story(self, story: Optional[Any] = None) -> NarrativeDecision:  # Optional[EvolvingStory]
        """
        Complete OODA cycle to evolve story.
        
        Convenience method that runs observe -> decide -> act -> reflect
        and returns the decision made.
        
        Args:
            story: Story to evolve (uses self.story if None)
            
        Returns:
            NarrativeDecision that was applied
        """
        if story:
            self.set_story(story)
        
        if not self.story:
            raise ValueError("No story set for director")
        
        # Run OODA cycle
        await self.step()
        
        # Return most recent decision
        if self.decision_history:
            return self.decision_history[-1]
        else:
            raise RuntimeError("No decision was made")
    
    def _choose_decision_type(self, story_state: StoryState) -> DecisionType:
        """Choose appropriate decision type based on story state."""
        # Simple heuristic: vary decision types based on story phase
        if len(story_state.timeline) < 3:
            # Early story: focus on character actions and world building
            return random.choice([
                DecisionType.CHARACTER_ACTION,
                DecisionType.WORLD_BUILDING,
                DecisionType.CHARACTER_DEVELOPMENT
            ])
        elif len(story_state.timeline) < 10:
            # Middle story: introduce conflict and plot twists
            return random.choice([
                DecisionType.CHARACTER_ACTION,
                DecisionType.PLOT_TWIST,
                DecisionType.CONFLICT_ESCALATION,
                DecisionType.RELATIONSHIP_CHANGE
            ])
        else:
            # Later story: resolve conflicts and develop characters
            return random.choice([
                DecisionType.CHARACTER_ACTION,
                DecisionType.CONFLICT_RESOLUTION,
                DecisionType.CHARACTER_DEVELOPMENT,
                DecisionType.PLOT_TWIST
            ])
    
    def _generate_decision_content(
        self,
        decision_type: DecisionType,
        story_state: StoryState
    ) -> Dict[str, Any]:
        """Generate decision content based on type and story state."""
        content = {
            "description": "",
            "narrative_text": "",
            "importance": 0.5,
            "confidence": 0.7
        }
        
        # Get available characters
        characters = list(story_state.characters.keys())
        character = random.choice(characters) if characters else None
        
        if decision_type == DecisionType.CHARACTER_ACTION:
            actions = [
                "explored the mysterious location",
                "discovered something unexpected",
                "made a difficult choice",
                "encountered a new challenge",
                "reflected on recent events"
            ]
            action = random.choice(actions)
            content["description"] = f"{character} {action}" if character else f"Someone {action}"
            content["narrative_text"] = f"{character} {action}. " if character else f"Someone {action}. "
            content["character"] = character
        
        elif decision_type == DecisionType.PLOT_TWIST:
            twists = [
                "A hidden truth was revealed",
                "An unexpected ally appeared",
                "A betrayal changed everything",
                "A long-lost connection was discovered",
                "The situation was not what it seemed"
            ]
            twist = random.choice(twists)
            content["description"] = twist
            content["narrative_text"] = f"{twist}. "
            content["importance"] = 0.8
        
        elif decision_type == DecisionType.WORLD_EVENT:
            events = [
                "A storm approached",
                "The environment changed",
                "Time passed",
                "The world shifted",
                "Something in the world reacted"
            ]
            event = random.choice(events)
            content["description"] = event
            content["narrative_text"] = f"{event}. "
            content["importance"] = 0.4
        
        elif decision_type == DecisionType.CHARACTER_DEVELOPMENT:
            developments = [
                "gained new insight",
                "learned something important",
                "grew as a person",
                "changed their perspective",
                "discovered their true nature"
            ]
            development = random.choice(developments)
            content["description"] = f"{character} {development}" if character else f"Someone {development}"
            content["narrative_text"] = f"{character} {development}. " if character else f"Someone {development}. "
            content["character"] = character
            content["importance"] = 0.6
        
        elif decision_type == DecisionType.CONFLICT_ESCALATION:
            escalations = [
                "Tension increased",
                "The conflict deepened",
                "Stakes were raised",
                "The situation became more dangerous",
                "Opposing forces clashed"
            ]
            escalation = random.choice(escalations)
            content["description"] = escalation
            content["narrative_text"] = f"{escalation}. "
            content["importance"] = 0.7
        
        elif decision_type == DecisionType.CONFLICT_RESOLUTION:
            resolutions = [
                "The conflict was resolved",
                "A compromise was reached",
                "Peace was restored",
                "The tension eased",
                "Understanding was achieved"
            ]
            resolution = random.choice(resolutions)
            content["description"] = resolution
            content["narrative_text"] = f"{resolution}. "
            content["importance"] = 0.7
        
        else:
            # Default
            content["description"] = "The story continued"
            content["narrative_text"] = "The story continued. "
        
        content["reasoning"] = f"Chose {decision_type.value} to advance the narrative"
        
        return content
    
    def _assess_story_quality(self, story_state: StoryState) -> str:
        """Assess story quality."""
        if story_state.coherence_score > 0.8:
            return "excellent"
        elif story_state.coherence_score > 0.6:
            return "good"
        elif story_state.coherence_score > 0.4:
            return "fair"
        else:
            return "needs_improvement"
    
    def _generate_suggestions(self, story_state: StoryState) -> List[str]:
        """Generate suggestions for story improvement."""
        suggestions = []
        
        if len(story_state.characters) < 2:
            suggestions.append("Consider adding more characters")
        
        if len(story_state.timeline) < 5:
            suggestions.append("Story could use more events")
        
        if story_state.coherence_score < 0.6:
            suggestions.append("Focus on maintaining story coherence")
        
        if not story_state.plot_points:
            suggestions.append("Consider adding plot points for structure")
        
        return suggestions
