#!/usr/bin/env python3
"""
Download and integrate PixelLab-generated assets into the game
"""

import os
import json
import requests
import time
from pathlib import Path
from typing import Dict, List, Optional

# Asset IDs from PixelLab generation
CHARACTER_IDS = {
    'glitch_guard': 'ce370ece-d940-464f-adbf-e27781101755',
    'heavy_guard': '1252c1a9-d9fb-4dd7-959d-5f5f58e49a7e',
    'security_drone': 'a04c5445-324a-4a8a-be39-06829bfdc42e',
    'chief_vex': '4cec2fa4-6b16-4c76-81b2-c2356ba30022',
    'core_boss': 'f49739fe-ca67-43ab-840e-b2550596a218'
}

MAP_OBJECT_IDS = {
    'access_card': '0aa08363-d735-4183-98f4-df6510c9918a',
    'health_kit': '7d2668c1-8ef1-47bc-85dd-7242a458dcee',
    'server_rack': '36f81b7b-da06-4c9a-b22c-d5ebae849795',
    'energy_drink': 'b62dc902-f506-4f77-b10e-cac1a1d8db49',
    'security_checkpoint': '3a8a51e0-3afb-4aeb-ae5b-7449d586e8bf',
    'executive_desk': '7e8780c8-4f39-4358-af25-4b92eecae57b',
    'portal': '087128d4-213c-45f8-b731-44970ca803c9',
    'cooling_unit': '16c3ffe3-f0be-46c9-95df-4dd8c586c386'
}

BASE_DIR = Path(__file__).parent.parent
ASSETS_DIR = BASE_DIR / 'assets'
CHARACTERS_DIR = ASSETS_DIR / 'characters'
OBJECTS_DIR = ASSETS_DIR / 'objects'

def check_character_status(character_id: str) -> Optional[Dict]:
    """Check if character is ready using PixelLab MCP"""
    # This would use the MCP tool in practice
    # For now, return placeholder
    return None

def download_image(url: str, output_path: Path) -> bool:
    """Download an image from URL"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        print(f"✓ Downloaded: {output_path.name}")
        return True
    except Exception as e:
        print(f"✗ Failed to download {output_path.name}: {e}")
        return False

def extract_character_frames(character_data: Dict, character_name: str):
    """Extract and save character frames"""
    char_dir = CHARACTERS_DIR / f"{character_name}_extracted"
    frames_dir = char_dir / 'frames'
    rotations_dir = char_dir / 'rotations'
    
    frames_dir.mkdir(parents=True, exist_ok=True)
    rotations_dir.mkdir(parents=True, exist_ok=True)
    
    # Download frames
    if 'frames' in character_data:
        for direction, frame_url in character_data['frames'].items():
            frame_path = frames_dir / f"{character_name}_{direction}.png"
            download_image(frame_url, frame_path)
    
    # Download rotations (if available)
    if 'rotations' in character_data:
        for direction, rotation_url in character_data['rotations'].items():
            rotation_path = rotations_dir / f"{direction}.png"
            download_image(rotation_url, rotation_path)
    
    # Save metadata
    metadata = {
        'name': character_name,
        'character_id': character_data.get('id'),
        'directions': list(character_data.get('frames', {}).keys()),
        'animations': list(character_data.get('animations', {}).keys())
    }
    
    with open(char_dir / 'metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"✓ Extracted character: {character_name}")

def extract_map_object(object_data: Dict, object_name: str):
    """Extract and save map object"""
    object_path = OBJECTS_DIR / f"{object_name}.png"
    object_obj_path = OBJECTS_DIR / f"{object_name}_obj.png"
    
    # Download main image
    if 'image_url' in object_data:
        download_image(object_data['image_url'], object_path)
        # Also create _obj version (same image for now)
        download_image(object_data['image_url'], object_obj_path)
    
    print(f"✓ Extracted object: {object_name}")

def main():
    """Main download script"""
    print("=" * 60)
    print("PixelLab Asset Downloader")
    print("=" * 60)
    print()
    print("NOTE: This script requires manual execution via MCP tools")
    print("Use get_character() and get_map_object() MCP tools to retrieve assets")
    print()
    print("Character IDs to check:")
    for name, char_id in CHARACTER_IDS.items():
        print(f"  {name}: {char_id}")
    print()
    print("Map Object IDs to check:")
    for name, obj_id in MAP_OBJECT_IDS.items():
        print(f"  {name}: {obj_id}")
    print()
    print("=" * 60)
    print("To download assets, use:")
    print("  call_mcp_tool('user-pixellab', 'get_character', {'character_id': '...'})")
    print("  call_mcp_tool('user-pixellab', 'get_map_object', {'object_id': '...'})")
    print("=" * 60)

if __name__ == '__main__':
    main()
