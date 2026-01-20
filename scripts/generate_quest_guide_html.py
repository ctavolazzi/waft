#!/usr/bin/env python3
"""Generate complete QUEST_GUIDE.html from quest data."""

import sys
from pathlib import Path

# Import quest data from the implementation script
sys.path.insert(0, str(Path(__file__).parent))
from quest_guide_implementation import create_quests

def generate_quest_card_html(quest_id, quest, checkpoints, tests, project_path):
    """Generate HTML for a single quest card."""
    status_map = {
        'locked': ('locked', 'Locked'),
        'available': ('available', 'Available'),
        'in_progress': ('in-progress', 'In Progress'),
        'completed': ('completed', 'Completed')
    }
    
    # Determine initial status
    initial_status = 'locked' if quest.prerequisites else 'available'
    status_class, status_text = status_map[initial_status]
    
    # Generate checkpoints HTML
    checkpoints_html = []
    for cp_id in quest.checkpoints:
        cp = checkpoints.get(cp_id)
        if cp:
            checkpoints_html.append(f'<li><a href="#{cp_id}">{cp_id}</a> - {cp.name}</li>')
    checkpoints_html = '\n                                '.join(checkpoints_html) if checkpoints_html else '<li>None</li>'
    
    # Generate tests HTML
    tests_html = []
    for test_id in quest.tests:
        test = tests.get(test_id)
        if test:
            tests_html.append(f'<li><a href="#{test_id}">{test_id}</a> - {test.name}</li>')
    tests_html = '\n                                '.join(tests_html) if tests_html else '<li>None</li>'
    
    # Generate achievements HTML
    achievements_html = '\n                                    '.join([f'<li>{ach}</li>' for ach in quest.achievements])
    
    # Generate prerequisites HTML
    prereqs_html = '\n                                    '.join([f'<li><a href="#{prereq}">{prereq}</a></li>' for prereq in quest.prerequisites]) if quest.prerequisites else '<li>None - Start here!</li>'
    
    # Generate difficulty stars
    stars = '⭐ ' * quest.difficulty
    
    return f'''                    <div class="quest-card" id="{quest_id}" data-status="{initial_status}">
                        <span class="quest-status status-{status_class}">{status_text}</span>
                        <div class="quest-header">
                            <div>
                                <h3 class="quest-title">{quest.name}</h3>
                                <div class="quest-meta">
                                    <span class="quest-id">{quest_id}</span>
                                    <span class="difficulty">{stars}</span>
                                    <span class="xp">+{quest.xp_reward} XP</span>
                                </div>
                            </div>
                        </div>
                        <div class="quest-description">{quest.description}</div>
                        <div class="quest-details">
                            <div class="detail-section">
                                <h4>Checkpoints</h4>
                                <ul>
                                    {checkpoints_html}
                                </ul>
                            </div>
                            <div class="detail-section">
                                <h4>Tests</h4>
                                <ul>
                                    {tests_html}
                                </ul>
                            </div>
                            <div class="detail-section">
                                <h4>Achievements</h4>
                                <ul>
                                    {achievements_html}
                                </ul>
                            </div>
                            <div class="detail-section">
                                <h4>Prerequisites</h4>
                                <ul>
                                    {prereqs_html}
                                </ul>
                            </div>
                        </div>
                    </div>'''

def main():
    project_path = Path(__file__).parent.parent
    quests, checkpoints, tests = create_quests(project_path)
    
    # Phase organization
    phases = {
        'Phase 1: Foundation': ['quest_1', 'quest_2', 'quest_3', 'quest_4'],
        'Phase 2: LLM Integration': ['quest_5', 'quest_6'],
        'Phase 3: Evaluation System': ['quest_7', 'quest_8', 'quest_9'],
        'Phase 4: Advanced Features (Optional)': ['quest_10', 'quest_11'],
        'Phase 5: Integration & Polish': ['quest_12', 'quest_13', 'quest_14', 'quest_15'],
        'Phase 6: Documentation & Testing': ['quest_16', 'quest_17']
    }
    
    # Read the base HTML template (the improved version I created)
    html_file = project_path / 'scripts' / 'QUEST_GUIDE.html'
    
    # For now, just print that we'd generate it
    # In practice, we'd read the template and inject the quest cards
    print("Quest data loaded successfully!")
    print(f"Total quests: {len(quests)}")
    print(f"Total checkpoints: {len(checkpoints)}")
    print(f"Total tests: {len(tests)}")
    print(f"Total phases: {len(phases)}")

if __name__ == '__main__':
    main()