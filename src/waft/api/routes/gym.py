"""
Gym/RPG endpoint - serves battle logs and gym data.
"""

import json
from fastapi import APIRouter, Request
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

router = APIRouter()


@router.get("/gym/battle-logs")
async def get_battle_logs(request: Request, limit: int = 20):
    """
    Get recent battle logs from gym sessions.
    
    Reads from loot files in _pyrite/gym_logs/loot/ and reconstructs
    battle log information including Scint detection and stabilization.
    
    Args:
        limit: Maximum number of battle logs to return
        
    Returns:
        List of battle log entries with Scint and stabilization data
    """
    project_path: Path = request.app.state.project_path
    loot_dir = project_path / "_pyrite" / "gym_logs" / "loot"
    
    battle_logs = []
    
    if loot_dir.exists():
        # Read all loot files (sorted by modification time, newest first)
        loot_files = sorted(loot_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
        
        for loot_file in loot_files[:limit]:
            try:
                with open(loot_file, 'r') as f:
                    loot_data = json.load(f)
                
                # Reconstruct battle log from loot data
                battle_log = {
                    "quest_name": loot_data.get("quest_name", "Unknown"),
                    "timestamp": loot_data.get("timestamp", datetime.now().isoformat()),
                    "hero_name": loot_data.get("hero_name", "Unknown"),
                    "input_prompt": loot_data.get("prompt", ""),
                    "agent_response": loot_data.get("response", ""),
                    "success": True,  # Loot files are only saved on success
                    "result": "stabilized" if loot_data.get("stabilization_attempts", 0) > 0 else "hit",
                    "xp_gained": 0,
                    # Scint & Stabilization data
                    "scints_detected": loot_data.get("scints_detected"),
                    "max_severity": loot_data.get("max_severity"),
                    "stabilization_attempted": loot_data.get("stabilization_attempted", False),
                    "stabilization_successful": loot_data.get("stabilization_successful", False),
                    "stabilization_attempts": loot_data.get("stabilization_attempts", 0),
                    "corrected_response": loot_data.get("corrected_response"),
                    "original_response": loot_data.get("original_response"),
                    "agent_call_count": loot_data.get("stabilization_attempts", 0) + 1,
                    "validated_matrix": loot_data.get("validated_matrix"),
                }
                
                battle_logs.append(battle_log)
            except Exception as e:
                # Skip invalid files
                continue
    
    return {
        "battle_logs": battle_logs,
        "total": len(battle_logs),
        "limit": limit
    }


@router.get("/gym/stats")
async def get_gym_stats(request: Request):
    """
    Get aggregated gym statistics.
    
    Returns summary statistics about quest attempts, Scint detection,
    stabilization success rates, and hero progression.
    """
    project_path: Path = request.app.state.project_path
    loot_dir = project_path / "_pyrite" / "gym_logs" / "loot"
    
    stats = {
        "total_quests": 0,
        "successful_quests": 0,
        "stabilized_quests": 0,
        "scints_detected": 0,
        "scint_types": {},
        "stabilization_success_rate": 0.0,
        "average_severity": 0.0,
        "total_agent_calls": 0,
    }
    
    if loot_dir.exists():
        loot_files = list(loot_dir.glob("*.json"))
        stats["total_quests"] = len(loot_files)
        
        stabilized_count = 0
        stabilization_attempts = 0
        total_severity = 0.0
        severity_count = 0
        
        for loot_file in loot_files:
            try:
                with open(loot_file, 'r') as f:
                    loot_data = json.load(f)
                
                if loot_data.get("stabilization_successful", False):
                    stabilized_count += 1
                
                if loot_data.get("stabilization_attempted", False):
                    stabilization_attempts += 1
                
                if loot_data.get("scints_detected"):
                    stats["scints_detected"] += len(loot_data["scints_detected"])
                    for scint_type in loot_data["scints_detected"]:
                        stats["scint_types"][scint_type] = stats["scint_types"].get(scint_type, 0) + 1
                
                if loot_data.get("max_severity"):
                    total_severity += loot_data["max_severity"]
                    severity_count += 1
                
                stats["total_agent_calls"] += loot_data.get("stabilization_attempts", 0) + 1
                
            except Exception:
                continue
        
        stats["successful_quests"] = len(loot_files)  # All loot files are successes
        stats["stabilized_quests"] = stabilized_count
        stats["stabilization_attempts"] = stabilization_attempts
        
        if stabilization_attempts > 0:
            stats["stabilization_success_rate"] = stabilized_count / stabilization_attempts
        
        if severity_count > 0:
            stats["average_severity"] = total_severity / severity_count
    
    return stats
