"""
Being Decision System: Decision-making for Being entities.

Unlike BaseAgent which has OODA cycles, beings make simpler decisions about
skill learning, memory recording, goal pursuit, etc.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import random


class BeingDecisionSystem:
    """
    Decision-making system for Being entities.
    
    Unlike BaseAgent which has OODA cycles, beings make
    simpler decisions about skill learning, memory recording,
    goal pursuit, etc.
    """
    
    # Decision types
    DECISION_TYPES = [
        "learn_skill",
        "record_memory",
        "pursue_goal",
        "rest",
        "explore"
    ]
    
    async def make_decision(
        self,
        being: "Being",
        available_options: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Being makes a decision based on personality, goals, and state.
        
        Decision selection algorithm:
        1. Filter options based on being state (can't learn if sleeping, etc.)
        2. Weight options based on personality type
        3. Weight options based on goals
        4. Weight options based on current state (will_to_live, fatigue, etc.)
        5. Select decision using weighted random choice
        
        Args:
            being: Being instance making the decision
            available_options: Optional list of available decision types
                              (defaults to all DECISION_TYPES)
        
        Returns:
            Decision result with experience data
        
        Raises:
            ValueError: If being is sleeping or has no decision fatigue
        """
        from ..being import Being
        
        # Check if being can make decisions
        if being.is_sleeping:
            raise ValueError("Being is sleeping and cannot make decisions")
        
        if being.decision_fatigue <= 0:
            raise ValueError("Decision fatigue depleted - being must sleep")
        
        # Get available options
        if available_options is None:
            available_options = self.DECISION_TYPES.copy()
        
        # Filter options based on being state
        filtered_options = self._filter_options(being, available_options)
        
        if not filtered_options:
            # No valid options - default to rest
            filtered_options = ["rest"]
        
        # Weight options based on personality, goals, and state
        weights = self._calculate_weights(being, filtered_options)
        
        # Select decision using weighted random choice
        decision_type = self._weighted_choice(filtered_options, weights)
        
        # Execute decision and generate experience
        experience = self._execute_decision(being, decision_type)
        
        return {
            "decision_type": decision_type,
            "experience": experience,
            "decision_fatigue_remaining": being.decision_fatigue
        }
    
    def _filter_options(
        self,
        being: "Being",
        options: List[str]
    ) -> List[str]:
        """
        Filter available options based on being state.
        
        Args:
            being: Being instance
            options: List of decision types
        
        Returns:
            Filtered list of valid options
        """
        filtered = []
        
        for option in options:
            if option == "learn_skill":
                # Can always learn skills
                filtered.append(option)
            elif option == "record_memory":
                # Can always record memories
                filtered.append(option)
            elif option == "pursue_goal":
                # Can pursue goals if goals exist
                if being.goals:
                    filtered.append(option)
            elif option == "rest":
                # Can rest if will_to_live < 80.0
                if being.will_to_live < 80.0:
                    filtered.append(option)
            elif option == "explore":
                # Can always explore
                filtered.append(option)
        
        return filtered
    
    def _calculate_weights(
        self,
        being: "Being",
        options: List[str]
    ) -> List[float]:
        """
        Calculate weights for each option based on personality, goals, state, and ENERGY.
        
        Beings constantly choose between options based on internal energy state.
        Low stamina heavily influences decision-making (prefer rest, avoid costly actions).
        
        Args:
            being: Being instance
            options: List of decision types
        
        Returns:
            List of weights (same length as options)
        """
        weights = []
        stamina_ratio = being.get_stamina_ratio()
        stamina_depleted = being.is_stamina_depleted()
        
        # Action stamina costs (higher cost = less attractive when low stamina)
        action_costs = {
            "learn_skill": 8.0,
            "pursue_goal": 10.0,
            "explore": 7.0,
            "record_memory": 3.0,
            "rest": 0.0  # Rest actually regenerates stamina
        }
        
        for option in options:
            weight = 1.0  # Base weight
            
            # ENERGY-BASED WEIGHTING (most important when depleted)
            if stamina_depleted:
                # When depleted, heavily favor rest and low-cost actions
                if option == "rest":
                    weight *= 5.0  # Strongly prefer rest when depleted
                elif option == "record_memory":
                    weight *= 2.0  # Low cost, still viable
                else:
                    # High-cost actions are much less attractive
                    cost = action_costs.get(option, 5.0)
                    weight *= (0.1 + stamina_ratio * 0.3)  # Severely reduced weight
            else:
                # Normal energy state - scale by stamina ratio
                cost = action_costs.get(option, 5.0)
                if option == "rest":
                    # Rest is less attractive when energy is high
                    weight *= (0.3 + (1.0 - stamina_ratio) * 0.7)
                else:
                    # Higher stamina = more attractive for costly actions
                    weight *= (0.5 + stamina_ratio * 0.5)
            
            # Personality-based weighting
            if being.personality_type == "analytical":
                if option == "learn_skill":
                    weight *= 2.0
                elif option == "pursue_goal":
                    weight *= 1.5
            elif being.personality_type == "creative":
                if option == "explore":
                    weight *= 2.0
                elif option == "record_memory":
                    weight *= 1.5
            # "balanced" gets base weight for all
            
            # Goal-based weighting
            if option == "pursue_goal" and being.goals:
                weight *= 1.5  # Prefer pursuing goals if goals exist
            
            # State-based weighting
            if option == "rest" and being.will_to_live < 50.0:
                weight *= 2.0  # Prefer rest if will_to_live is low
            
            # Pain/Pleasure weighting (avoid pain, seek pleasure)
            if being.pain > 0.5:
                # High pain - prefer rest and low-cost actions
                if option == "rest":
                    weight *= 2.0  # Strongly prefer rest when in pain
                elif option in ["pursue_goal", "learn_skill"]:
                    weight *= 0.5  # Avoid high-cost actions when in pain
            
            if being.pleasure > 0.5:
                # High pleasure - prefer actions that maintain or increase pleasure
                if option == "pursue_goal":
                    weight *= 1.5  # Prefer goal pursuit when feeling good
                elif option == "explore":
                    weight *= 1.3  # Prefer exploration when feeling good
            
            # Alignment weighting (seek alignment, avoid misalignment)
            alignment_score = being.current_alignment_score
            if alignment_score > 0.7:
                # High alignment - prefer actions that maintain alignment
                if option in ["pursue_goal", "learn_skill"]:
                    weight *= 1.3  # Prefer goal-oriented actions when aligned
            elif alignment_score < 0.3:
                # Low alignment (misalignment) - prefer rest and low-cost actions
                if option == "rest":
                    weight *= 1.5  # Prefer rest when misaligned
                elif option in ["pursue_goal", "learn_skill"]:
                    weight *= 0.7  # Reduce high-cost actions when misaligned
            
            # Energy state weighting (low energy = prefer rest)
            energy_ratio = being.get_energy_ratio()
            if energy_ratio < 0.3:
                # Low energy - strongly prefer rest
                if option == "rest":
                    weight *= 3.0  # Strongly prefer rest when energy is low
                else:
                    weight *= 0.5  # Reduce other actions when energy is low
            elif energy_ratio > 0.7:
                # High energy - prefer high-value actions
                if option in ["pursue_goal", "learn_skill"]:
                    weight *= 1.2  # Prefer high-value actions when energy is high
            
            weights.append(weight)
        
        return weights
    
    def _weighted_choice(
        self,
        options: List[str],
        weights: List[float]
    ) -> str:
        """
        Select an option using weighted random choice.
        
        Args:
            options: List of decision types
            weights: List of weights (same length as options)
        
        Returns:
            Selected decision type
        """
        # Normalize weights
        total_weight = sum(weights)
        if total_weight == 0:
            # Fallback to uniform random
            return random.choice(options)
        
        normalized_weights = [w / total_weight for w in weights]
        
        # Weighted random choice
        return random.choices(options, weights=normalized_weights, k=1)[0]
    
    def _execute_decision(
        self,
        being: "Being",
        decision_type: str
    ) -> Dict[str, Any]:
        """
        Execute a decision and generate experience.
        
        Actions consume stamina and energy, and quality degrades when depleted.
        Action intensity is modulated by stamina (inverse relationship):
        - More Stamina = Less Intensity per Action (more control, efficient)
        - Less Stamina = More Intensity per Action (desperate, powerful but inefficient)
        
        Args:
            being: Being instance
            decision_type: Type of decision to execute
        
        Returns:
            Experience dict for pleasure/pain calculation
        """
        # Action stamina costs
        stamina_costs = {
            "learn_skill": 8.0,
            "pursue_goal": 10.0,
            "explore": 7.0,
            "record_memory": 3.0,
            "rest": 0.0  # Rest doesn't cost stamina, actually regenerates
        }
        
        # Action energy costs
        energy_costs = {
            "learn_skill": 5.0,
            "pursue_goal": 7.0,
            "explore": 4.0,
            "record_memory": 2.0,
            "rest": 0.0  # Rest doesn't cost energy
        }
        
        stamina_cost = stamina_costs.get(decision_type, 5.0)
        energy_cost = energy_costs.get(decision_type, 3.0)
        
        # Calculate action intensity from stamina (INVERSE relationship)
        stamina_ratio = being.get_stamina_ratio()
        # More stamina = less intensity per action (more control, efficient)
        # Less stamina = more intensity per action (desperate, powerful)
        intensity_modifier = 0.5  # Base modifier
        action_intensity = 1.0 - (stamina_ratio * intensity_modifier)
        # Clamp to reasonable range [0.3, 1.5]
        action_intensity = max(0.3, min(1.5, action_intensity))
        
        # Consume energy
        actual_energy_consumed = being.consume_energy(energy_cost)
        
        # Make decision (consumes stamina, applies depleted effects)
        decision_result = being.make_decision(decision_type, stamina_cost)
        experience = decision_result["experience"]
        
        # Apply action intensity to experience outcomes
        experience["action_intensity"] = action_intensity
        experience["energy_consumed"] = actual_energy_consumed
        
        # Enhance experience based on decision type
        # Apply action intensity to outcomes
        base_intensity = experience.get("intensity", 0.5)
        
        if decision_type == "learn_skill":
            experience["type"] = "positive"
            if not experience.get("stamina_depleted"):
                base_intensity = 0.6
                experience["description"] = "Learned a new skill"
            else:
                base_intensity = 0.3  # Reduced due to mistakes
                experience["description"] = "Attempted to learn a skill (made mistakes due to exhaustion)"
            # Apply intensity: high intensity = more skill gain, but less efficient
            experience["intensity"] = base_intensity * action_intensity
            # Adjust skill learning based on intensity
            if "skill_learned" in experience:
                experience["skill_learned"]["level_increase"] *= action_intensity
        
        elif decision_type == "record_memory":
            experience["type"] = "positive"
            if not experience.get("stamina_depleted"):
                base_intensity = 0.4
                experience["description"] = "Recorded a memory"
            else:
                base_intensity = 0.2
                experience["description"] = "Recorded a memory (incomplete due to exhaustion)"
            experience["intensity"] = base_intensity * action_intensity
        
        elif decision_type == "pursue_goal":
            experience["type"] = "positive"
            if not experience.get("stamina_depleted"):
                base_intensity = 0.7
                experience["description"] = "Pursued a lifetime goal"
            else:
                base_intensity = 0.3
                experience["description"] = "Attempted to pursue goal (poor execution due to exhaustion)"
            experience["intensity"] = base_intensity * action_intensity
            # High intensity = more goal progress, but less efficient
            if "goal_progress" in experience:
                experience["goal_progress"] *= action_intensity
        
        elif decision_type == "rest":
            # Resting regenerates stamina, energy, and will_to_live
            experience["type"] = "positive"
            base_intensity = 0.3
            experience["intensity"] = base_intensity
            experience["description"] = "Rested and recovered"
            # Regenerate stamina faster when resting
            stamina_regenerated = being.regenerate_stamina(being.stamina_regeneration_rate * 2.0)
            experience["stamina_regenerated"] = stamina_regenerated
            # Regenerate energy
            energy_regenerated = being.regenerate_energy(being.energy_regeneration_rate * 1.5)
            experience["energy_regenerated"] = energy_regenerated
            # Slight will_to_live regeneration
            being.will_to_live = min(100.0, being.will_to_live + 1.0)
        
        elif decision_type == "explore":
            experience["type"] = "positive"
            if not experience.get("stamina_depleted"):
                base_intensity = random.uniform(0.3, 0.6)
                experience["description"] = "Explored reality and discovered opportunities"
            else:
                base_intensity = random.uniform(0.1, 0.3)
                experience["description"] = "Explored reality (missed opportunities due to exhaustion)"
            experience["intensity"] = base_intensity * action_intensity
        
        return experience
