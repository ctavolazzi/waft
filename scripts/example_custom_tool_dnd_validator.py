#!/usr/bin/env python3
"""
Example: Custom D&D Character Validator Tool for OpenHands

This is an example of how you could create a custom tool for game development.
For the initial game generation, this is NOT needed - built-in tools are sufficient.

This example shows the pattern for creating a custom tool that validates
D&D 5e character data.
"""

import os
from collections.abc import Sequence
from pathlib import Path

from pydantic import Field, SecretStr

from openhands.sdk import (
    LLM,
    Action,
    Agent,
    Conversation,
    Observation,
    TextContent,
    ToolDefinition,
)
from openhands.sdk.tool import Tool, ToolExecutor, register_tool
from openhands.tools.file_editor import FileEditorTool
from openhands.tools.terminal import TerminalExecutor, TerminalTool


# --- Action / Observation ---


class ValidateCharacterAction(Action):
    """Action for validating D&D 5e character data."""
    character_data: dict = Field(description="Character data dictionary to validate")
    strict: bool = Field(
        default=False, description="Use strict validation (reject minor issues)"
    )


class ValidateCharacterObservation(Observation):
    """Observation containing validation results."""
    valid: bool = Field(default=False)
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    score: int = Field(default=0, description="Character level/score")

    @property
    def to_llm_content(self) -> Sequence[TextContent]:
        """Format validation results for LLM."""
        if self.valid:
            status = f"✅ Character is valid (Level {self.score})"
        else:
            status = f"❌ Character validation failed"
        
        errors_text = "\n".join(f"  - {e}" for e in self.errors) if self.errors else "  None"
        warnings_text = "\n".join(f"  - {w}" for w in self.warnings) if self.warnings else "  None"
        
        result = (
            f"{status}\n\n"
            f"Errors:\n{errors_text}\n\n"
            f"Warnings:\n{warnings_text}"
        )
        return [TextContent(text=result)]


# --- Executor ---


class ValidateCharacterExecutor(ToolExecutor[ValidateCharacterAction, ValidateCharacterObservation]):
    """Executor that validates D&D 5e character data."""
    
    def __init__(self):
        # No terminal needed for this tool
        pass
    
    def __call__(self, action: ValidateCharacterAction, conversation=None) -> ValidateCharacterObservation:
        """Validate character data according to D&D 5e rules."""
        data = action.character_data
        errors = []
        warnings = []
        
        # Validate ability scores (3-18 range)
        abilities = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]
        for ability in abilities:
            if ability in data:
                score = data[ability]
                if not isinstance(score, int) or score < 3 or score > 18:
                    errors.append(f"{ability} must be between 3 and 18, got {score}")
        
        # Validate HP
        if "hp" in data and "max_hp" in data:
            if data["hp"] > data["max_hp"]:
                errors.append(f"Current HP ({data['hp']}) cannot exceed max HP ({data['max_hp']})")
            if data["max_hp"] < 1:
                errors.append(f"Max HP must be at least 1, got {data['max_hp']}")
        
        # Validate level
        level = data.get("level", 1)
        if not isinstance(level, int) or level < 1 or level > 20:
            warnings.append(f"Level {level} is outside typical D&D range (1-20)")
        
        # Calculate score (simplified)
        score = level
        
        # Character is valid if no errors
        valid = len(errors) == 0
        
        return ValidateCharacterObservation(
            valid=valid,
            errors=errors,
            warnings=warnings,
            score=score,
        )


# Tool description
_VALIDATOR_DESCRIPTION = """D&D 5e Character Validator Tool.
* Validates character data according to D&D 5e rules
* Checks ability scores (3-18 range)
* Validates HP (current <= max, max >= 1)
* Warns about unusual levels
* Returns validation results with errors and warnings
* Use this tool when you need to validate character data before using it in the game
"""


# --- Tool Definition ---


class ValidateCharacterTool(ToolDefinition[ValidateCharacterAction, ValidateCharacterObservation]):
    """A custom tool that validates D&D 5e character data."""

    @classmethod
    def create(cls, conv_state) -> Sequence[ToolDefinition]:
        """Create ValidateCharacterTool instance."""
        executor = ValidateCharacterExecutor()
        
        return [
            cls(
                description=_VALIDATOR_DESCRIPTION,
                action_type=ValidateCharacterAction,
                observation_type=ValidateCharacterObservation,
                executor=executor,
            )
        ]


# Example usage (commented out - not needed for initial development)
if __name__ == "__main__":
    # This is just an example - not needed for game generation
    print("This is an example custom tool.")
    print("For game development, built-in tools are sufficient.")
    print("Custom tools can be added later if needed.")
    
    # Uncomment to test:
    # api_key = os.getenv("LLM_API_KEY")
    # if not api_key:
    #     print("Set LLM_API_KEY to test")
    #     exit(1)
    # 
    # llm = LLM(
    #     model=os.getenv("LLM_MODEL", "anthropic/claude-sonnet-4-5-20250929"),
    #     api_key=SecretStr(api_key),
    # )
    # 
    # def _make_tools(conv_state):
    #     terminal_executor = TerminalExecutor(working_dir=conv_state.workspace.working_dir)
    #     terminal_tool = TerminalTool.create(conv_state, executor=terminal_executor)[0]
    #     validator_tool = ValidateCharacterTool.create(conv_state)[0]
    #     return [terminal_tool, validator_tool]
    # 
    # register_tool("GameDevTools", _make_tools)
    # 
    # agent = Agent(
    #     llm=llm,
    #     tools=[
    #         Tool(name=FileEditorTool.name),
    #         Tool(name="GameDevTools"),
    #     ],
    # )
    # 
    # conversation = Conversation(agent=agent, workspace=os.getcwd())
    # conversation.send_message("Validate this character: {'strength': 15, 'dexterity': 13, 'hp': 20, 'max_hp': 20, 'level': 1}")
    # conversation.run()