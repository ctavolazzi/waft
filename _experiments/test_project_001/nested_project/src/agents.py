"""
CrewAI Agents - Starter Template

This file provides a starter template for setting up CrewAI agents.
Customize this to fit your project's needs.
"""

from crewai import Agent, Task, Crew
from typing import List, Optional


def create_agent(
    role: str,
    goal: str,
    backstory: str,
    verbose: bool = True,
) -> Agent:
    """
    Create a CrewAI agent.

    Args:
        role: The agent's role
        goal: The agent's goal
        backstory: The agent's backstory
        verbose: Whether to enable verbose output

    Returns:
        Configured Agent instance
    """
    return Agent(
        role=role,
        goal=goal,
        backstory=backstory,
        verbose=verbose,
        allow_delegation=False,
    )


def create_crew(agents: List[Agent], tasks: List[Task]) -> Crew:
    """
    Create a CrewAI crew.

    Args:
        agents: List of agents
        tasks: List of tasks

    Returns:
        Configured Crew instance
    """
    return Crew(
        agents=agents,
        tasks=tasks,
        verbose=True,
    )


# Example usage:
if __name__ == "__main__":
    # Create agents
    researcher = create_agent(
        role="Researcher",
        goal="Research and gather information",
        backstory="You are a research specialist...",
    )

    writer = create_agent(
        role="Writer",
        goal="Write clear and engaging content",
        backstory="You are a content writer...",
    )

    # Create tasks
    research_task = Task(
        description="Research the topic",
        agent=researcher,
    )

    writing_task = Task(
        description="Write about the research findings",
        agent=writer,
    )

    # Create crew and execute
    crew = create_crew(
        agents=[researcher, writer],
        tasks=[research_task, writing_task],
    )

    result = crew.kickoff()
    print(result)
