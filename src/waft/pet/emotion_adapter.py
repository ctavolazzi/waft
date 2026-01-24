"""
Emotion adapter for mapping Being state to pet emotions.
"""

from waft.being import BeingState

from .pet_being import PetBeing


class EmotionAdapter:
    @staticmethod
    def get_emotion(pet: PetBeing) -> str:
        if pet.state == BeingState.DEAD:
            return "dead"
        if pet.is_sleeping:
            return "sleeping"
        if pet.pain > 50:
            return "sad"
        if pet.pleasure > 70:
            return "excited"
        if pet.decision_fatigue < 3:
            return "tired"
        if pet.will_to_live < 30:
            return "depressed"
        return "content"
