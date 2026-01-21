# Public APIs for Being Personality Generation

**Date**: 2026-01-21
**Work Effort**: WE-260121-CAMPAIGN_EVOLUTION_CORP
**Purpose**: Identify and document public APIs for generating Being personalities
**Status**: API Research Complete

---

## Overview

This document identifies free/open public APIs that can be used to generate realistic personalities, backgrounds, and demographic data for WAFT Beings in the Campaign Evolution Corporation.

---

## Primary APIs (MVP)

### 1. Random User Generator API ⭐ (Primary for MVP)

**URL**: https://randomuser.me/

**Description**: Generates random user data including photos, names, addresses, and more.

**Why This API**:
- ✅ Completely free, no API key required
- ✅ No rate limits for reasonable use
- ✅ High-quality profile photos
- ✅ Realistic names from multiple nationalities
- ✅ Demographic data (age, gender, location)
- ✅ JSON response, easy to parse

**Example Request**:
```bash
curl https://randomuser.me/api/
```

**Example Response**:
```json
{
  "results": [
    {
      "gender": "female",
      "name": {
        "title": "Miss",
        "first": "Jennie",
        "last": "Nichols"
      },
      "location": {
        "street": {
          "number": 8929,
          "name": "Valwood Pkwy"
        },
        "city": "Billings",
        "state": "Michigan",
        "country": "United States",
        "postcode": "63104"
      },
      "email": "jennie.nichols@example.com",
      "dob": {
        "date": "1992-03-08T15:13:16.688Z",
        "age": 30
      },
      "phone": "(272) 790-0888",
      "picture": {
        "large": "https://randomuser.me/api/portraits/women/75.jpg",
        "medium": "https://randomuser.me/api/portraits/med/women/75.jpg",
        "thumbnail": "https://randomuser.me/api/portraits/thumb/women/75.jpg"
      },
      "nat": "US"
    }
  ]
}
```

**Data We'll Use**:
- `name.first` + `name.last` → Being name
- `dob.age` → Demographics
- `nat` → Nationality
- `picture.large` → Profile photo URL
- `gender` → Gender
- `location.city` → Location

**Rate Limits**: None for reasonable use (they request you cache locally if making many calls)

**Integration**:
```python
import httpx

async def fetch_random_user():
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://randomuser.me/api/")
        data = resp.json()["results"][0]

        return {
            "name": f"{data['name']['first']} {data['name']['last']}",
            "age": data['dob']['age'],
            "nationality": data['nat'],
            "photo_url": data['picture']['large'],
            "gender": data['gender'],
            "location": data['location']['city']
        }
```

---

## Personality Trait Generation (MVP Approach)

### Option 1: Template-Based (RECOMMENDED for MVP)

**Approach**: Use pre-defined YAML templates with randomization

**Why This Approach**:
- ✅ Zero API costs
- ✅ No rate limits
- ✅ Deterministic and testable
- ✅ Fast (no network calls)
- ✅ Full control over personality types

**Implementation**:
```yaml
# config/personality_templates.yaml

scenario_designer:
  big_five:
    openness: [0.7, 0.9]        # Range for random selection
    conscientiousness: [0.6, 0.8]
    extraversion: [0.5, 0.7]
    agreeableness: [0.5, 0.7]
    neuroticism: [0.2, 0.4]

  skills:
    campaign_design: [6.0, 9.0]
    encounter_balance: [5.0, 8.0]
    creativity: [7.0, 9.0]

  quirks_pool:
    - "Always adds a plot twist to every scenario"
    - "Loves designing morally ambiguous villains"
    - "Has a notebook full of unused encounter ideas"
    - "Detail-oriented about monster stat blocks"
    - "Constantly asks 'but what if...?'"
    - "Prefers dungeon crawls over political intrigue"

  backstory_templates:
    - "Former adventurer turned scenario designer after {event}"
    - "Lifelong D&D fan who {achievement}"
    - "Studied {field} before joining Dungeon Forge Studios"

  backstory_variables:
    event:
      - "retiring from adventuring"
      - "a legendary campaign experience"
      - "realizing their true calling"
    achievement:
      - "DMed 500+ sessions"
      - "created viral homebrew content"
      - "won a scenario design competition"
    field:
      - "game design"
      - "creative writing"
      - "mythology and folklore"
```

**Generator**:
```python
import random
import yaml

class TemplatePersonalityGenerator:
    def __init__(self, templates_path):
        with open(templates_path, 'r') as f:
            self.templates = yaml.safe_load(f)

    def generate(self, role):
        template = self.templates[role]

        # Randomize Big Five traits
        big_five = {}
        for trait, (min_val, max_val) in template['big_five'].items():
            big_five[trait] = random.uniform(min_val, max_val)

        # Randomize skills
        skills = {}
        for skill, (min_val, max_val) in template['skills'].items():
            skills[skill] = random.uniform(min_val, max_val)

        # Select random quirks (2-3)
        quirks = random.sample(template['quirks_pool'], k=random.randint(2, 3))

        # Generate backstory
        backstory_template = random.choice(template['backstory_templates'])
        variables = {
            key: random.choice(values)
            for key, values in template['backstory_variables'].items()
        }
        backstory = backstory_template.format(**variables)

        return {
            'big_five': big_five,
            'skills': skills,
            'quirks': quirks,
            'backstory': backstory
        }
```

**Pros**:
- Simple, reliable, fast
- No external dependencies
- Easy to customize
- Deterministic for testing

**Cons**:
- Less variety than AI-generated
- Requires manual template creation

---

## Secondary APIs (Post-MVP / Optional)

### Option 2: AI-Generated Personalities (Future Enhancement)

**If you want richer personalities in future versions, use**:

#### 2a. OpenAI API (GPT-4)

**URL**: https://api.openai.com/v1/chat/completions

**Cost**: ~$0.01-0.03 per personality (GPT-4-turbo)

**Pros**:
- Rich, creative personalities
- Natural language output
- Highly customizable

**Cons**:
- Costs money (token-based)
- Requires API key
- Rate limits
- Network latency

**Example**:
```python
import openai

async def generate_ai_personality(role, demographics):
    prompt = f"""
    Generate a detailed personality profile for a Being employee.

    Role: {role}
    Demographics: {demographics}

    Provide:
    1. Big Five personality traits (0.0-1.0)
    2. D&D alignment
    3. Backstory (2-3 paragraphs)
    4. Skills relevant to role (0-10 scale)
    5. Quirks (3-5)
    6. Personal goals

    Format as JSON.
    """

    response = await openai.ChatCompletion.acreate(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": "You are a character creator for D&D campaigns."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )

    return json.loads(response.choices[0].message.content)
```

#### 2b. Anthropic Claude API

**URL**: https://api.anthropic.com/v1/messages

**Cost**: ~$0.015-0.075 per personality (Claude 3)

**Similar to OpenAI but with Claude's personality generation capabilities.**

#### 2c. Hugging Face Inference API (Free Tier)

**URL**: https://api-inference.huggingface.co/

**Models**: Various open-source LLMs (Mistral, Llama 2, etc.)

**Pros**:
- Free tier available
- Open-source models
- No vendor lock-in

**Cons**:
- Lower quality than GPT-4/Claude
- Slower inference
- Rate limits on free tier

---

## Other Potentially Useful APIs (Future)

### 3. Job Title Generator APIs

**Random Job Title Generator** (Community Projects):
- https://random-word-api.herokuapp.com/word?number=1
- Combine with role templates for creative titles

**Example**: "Senior Campaign Architect", "Lead Worldbuilding Engineer"

### 4. Name Generators (if Random User not sufficient)

**Behind the Name API**: https://www.behindthename.com/api/
- Fantasy name generation
- Multiple cultures/languages
- Free tier available

### 5. D&D 5e API (for validation)

**D&D 5e API**: https://www.dnd5eapi.co/
- Official D&D SRD data
- Spells, monsters, classes, races
- Use for validating campaign content

**Example**:
```python
# Validate that a monster exists in D&D SRD
async def validate_monster(monster_name):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"https://www.dnd5eapi.co/api/monsters/{monster_name}")
        return resp.status_code == 200
```

---

## MVP Recommendation

### For MVP (Minimal Viable Product):

**Use This Stack**:

1. **Demographics**: Random User API (https://randomuser.me/)
   - Name, age, nationality, photo, location

2. **Personality Traits**: Template-Based (YAML config)
   - Big Five traits (randomized within ranges)
   - Role-specific skills (randomized within ranges)
   - Quirks (random selection from pool)
   - Backstory (template with variable substitution)

**Why This Stack**:
- ✅ Zero cost
- ✅ No API keys needed
- ✅ No rate limits
- ✅ Fast and reliable
- ✅ Deterministic and testable
- ✅ Good enough for MVP
- ✅ Easy to enhance later with AI

**Implementation Plan**:
```
1. Create personality_templates.yaml with 3 role types
2. Implement TemplatePersonalityGenerator class
3. Integrate with Random User API for demographics
4. Combine demographics + template traits = full personality
5. Create Being with complete personality profile
```

---

## Future Enhancements (Post-MVP)

**v2.0+**:
- Add OpenAI/Claude API for richer personalities
- Add personality evolution (Beings change over time)
- Add team dynamics (personalities affect collaboration)
- Add D&D 5e API validation (check campaign against SRD)
- Add photo generation (AI-generated portraits instead of Random User photos)

---

## API Usage Best Practices

### 1. Caching

```python
import json
from pathlib import Path
from datetime import datetime, timedelta

class CachedAPIClient:
    def __init__(self, cache_dir: Path, cache_ttl_hours: int = 24):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(exist_ok=True)
        self.cache_ttl = timedelta(hours=cache_ttl_hours)

    async def get_cached_or_fetch(self, key: str, fetch_fn):
        cache_file = self.cache_dir / f"{key}.json"

        # Check if cache exists and is fresh
        if cache_file.exists():
            cache_data = json.loads(cache_file.read_text())
            cached_at = datetime.fromisoformat(cache_data['cached_at'])

            if datetime.utcnow() - cached_at < self.cache_ttl:
                return cache_data['data']

        # Fetch fresh data
        data = await fetch_fn()

        # Cache it
        cache_data = {
            'cached_at': datetime.utcnow().isoformat(),
            'data': data
        }
        cache_file.write_text(json.dumps(cache_data, indent=2))

        return data
```

### 2. Error Handling

```python
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
async def fetch_with_retry(url: str):
    """Fetch with automatic retry on failures."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.json()
```

### 3. Rate Limiting

```python
import asyncio
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, max_requests_per_minute: int):
        self.max_requests = max_requests_per_minute
        self.requests = []

    async def acquire(self):
        now = datetime.utcnow()
        cutoff = now - timedelta(minutes=1)

        # Remove old requests
        self.requests = [t for t in self.requests if t > cutoff]

        if len(self.requests) >= self.max_requests:
            # Wait until we can make another request
            wait_until = self.requests[0] + timedelta(minutes=1)
            wait_seconds = (wait_until - now).total_seconds()
            if wait_seconds > 0:
                await asyncio.sleep(wait_seconds)

        self.requests.append(datetime.utcnow())
```

---

## Summary

**MVP Stack**:
- Demographics: Random User API (free, no key)
- Personalities: Template-based (YAML config, zero cost)

**Future Enhancements**:
- AI-generated personalities (OpenAI/Claude/Hugging Face)
- D&D 5e API validation
- Advanced personality evolution

**Implementation Files**:
- `src/waft/core/dnd_scenario/being_personality_generator.py`
- `config/personality_templates.yaml`
- `tests/test_personality_generation.py`

---

**Status**: ✅ API Research Complete
**Recommended Stack**: Random User API + Template-Based Personalities
**Ready For**: Implementation in Phase 2
