"""
Being-to-CV Mapper

Maps Being attributes (skills, memories, experiences) to CV sections
for the brilliant-cv Typst template.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from ...being import Being


def map_being_to_cv_data(being: "Being") -> Dict[str, Any]:
    """
    Map Being object to CV data structure for brilliant-cv template.
    
    Args:
        being: Being instance to map
        
    Returns:
        Dictionary with CV sections (personal, experience, skills, education, etc.)
    """
    # Personal Information
    personal = {
        "firstname": being.custom_name.split()[0] if being.custom_name and " " in being.custom_name else (being.custom_name or being.being_id.split("_")[0]),
        "lastname": " ".join(being.custom_name.split()[1:]) if being.custom_name and " " in being.custom_name else (being.being_id.split("_")[-1] if "_" in being.being_id else ""),
        "email": f"{being.being_id.replace('_', '.')}@waft.reality",
        "location": being.reality_id.replace("_", " ").title(),
        "phone": None,
        "website": None,
        "github": None,
        "linkedin": None,
    }
    
    # Summary/About (from personality)
    summary = ""
    if being.personality:
        traits = being.personality.get("traits", [])
        if traits:
            summary = f"Dynamic entity with {', '.join(traits[:3])}."
        elif being.personality.get("description"):
            summary = being.personality.get("description")
    
    if not summary:
        summary = f"Timeful Being with {len(being.skills)} skills and {len(being.memories)} memories. Lineage: {' → '.join(being.ancestral_chain[-3:])}"
    
    # Experience (from Memories)
    experience = []
    for memory in being.memories[:10]:  # Limit to 10 most recent
        memory_type = memory.get("type", "")
        metadata = memory.get("metadata", {})
        
        if memory_type in ["work", "experience", "achievement"] or "experience" in metadata.get("tags", []):
            experience.append({
                "title": metadata.get("title", memory.get("content", "Experience")[:50]),
                "institution": metadata.get("context", "Reality"),
                "date": metadata.get("timestamp", memory.get("recorded_at", being.created_at))[:10] if metadata.get("timestamp") or memory.get("recorded_at") else being.created_at[:10],
                "location": metadata.get("reality_id", being.reality_id),
                "subtitle": metadata.get("subtitle"),
                "bullets": metadata.get("details", []) if isinstance(metadata.get("details"), list) else [memory.get("content", "")[:100]],
            })
    
    # If no experience from memories, create from skills
    if not experience and being.skills:
        top_skills = sorted(being.skills.items(), key=lambda x: x[1], reverse=True)[:3]
        experience.append({
            "title": "Being Evolution",
            "institution": "Source Consciousness",
            "date": being.created_at[:10],
            "location": being.reality_id,
            "subtitle": "Skill Development",
            "bullets": [f"Developed expertise in {skill} (Level {level:.1f})" for skill, level in top_skills],
        })
    
    # Skills
    technical_skills = []
    soft_skills = []
    
    for skill_name, skill_level in being.skills.items():
        skill_entry = {
            "name": skill_name.replace("_", " ").title(),
            "level": min(100, max(0, int(skill_level))),  # 0-100 scale
        }
        
        # Categorize skills (technical if level > 50, soft otherwise)
        if skill_level > 50.0:
            technical_skills.append(skill_entry)
        else:
            soft_skills.append(skill_entry)
    
    # Education (from Ancestral Chain)
    education = []
    if being.ancestral_chain:
        education.append({
            "degree": "Being Evolution",
            "institution": "Source Consciousness",
            "date": being.created_at[:10],
            "location": being.reality_id,
            "description": f"Lineage: {' → '.join(being.ancestral_chain[-3:])}",
        })
    
    # Projects/Achievements (from Lessons Learned)
    projects = []
    for lesson in being.lessons_learned[:5]:  # Top 5 lessons
        projects.append({
            "title": lesson.get("title", "Learning"),
            "description": lesson.get("description", str(lesson.get("lesson", ""))),
            "technologies": lesson.get("tags", []),
        })
    
    # Languages (from personality or default)
    languages = []
    if being.personality and being.personality.get("languages"):
        languages = being.personality.get("languages")
    else:
        languages = [{"name": "Reality Script", "level": "Native"}]
    
    # Interests (from goals)
    interests = []
    if being.goals:
        interests = [goal.get("title", str(goal)) for goal in being.goals[:5]]
    
    return {
        "personal": personal,
        "summary": summary,
        "experience": experience,
        "technical_skills": technical_skills,
        "soft_skills": soft_skills,
        "education": education,
        "projects": projects,
        "languages": languages,
        "interests": interests,
        "fitness": being.fitness,
        "lifetimes": being.lifetimes,
        "state": being.state.value,
    }
