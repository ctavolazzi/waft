# Research Template: Karma Calculation Research

**Purpose**: Document karma calculation methods and formulas

---

## Experience Intensity Measurement

### Method 1: [Name]
- **Formula**: [Mathematical formula]
- **Inputs**: [What data is needed]
- **Outputs**: [What it produces]
- **Use Case**: [When to use this method]

### Method 2: [Name]
- **Formula**: [Mathematical formula]
- **Inputs**: [What data is needed]
- **Outputs**: [What it produces]
- **Use Case**: [When to use this method]

---

## Emotional Weight Factors

### Pain Experiences
- **Weight**: [Numerical value, e.g., +1.0]
- **Rationale**: [Why this weight]
- **Examples**: [What counts as pain]
- **Variations**: [How weight might vary]

### Pleasure Experiences
- **Weight**: [Numerical value, e.g., +0.5]
- **Rationale**: [Why this weight]
- **Examples**: [What counts as pleasure]
- **Variations**: [How weight might vary]

### Neutral Experiences
- **Weight**: [Numerical value, e.g., +0.1]
- **Rationale**: [Why this weight]
- **Examples**: [What counts as neutral]
- **Variations**: [How weight might vary]

---

## Duration Calculations

### Time-Based
- **Formula**: [How duration affects karma]
- **Units**: [What units we use]
- **Scaling**: [How it scales]

### Intensity Over Time
- **Formula**: [How intensity × duration works]
- **Integration Method**: [How we integrate over time]
- **Examples**: [Concrete examples]

---

## Gravity Accumulation Mechanisms

### Method 1: [Name]
- **How Gravity Accumulates**: [Description]
- **Formula**: [Mathematical representation]
- **Factors**: [What affects accumulation]
- **Implementation**: [Code structure]

### Method 2: [Name]
- **How Gravity Accumulates**: [Description]
- **Formula**: [Mathematical representation]
- **Factors**: [What affects accumulation]
- **Implementation**: [Code structure]

---

## Inertia and Energy Calculations

### Inertia Calculation
- **Formula**: [How inertia is calculated from karma]
- **Purpose**: [What inertia represents]
- **Units**: [Measurement units]
- **Examples**: [Concrete examples]

### Energy Calculation
- **Formula**: [How energy is calculated]
- **Purpose**: [What energy represents]
- **Relationship to Prana**: [How this relates to base prana cost]
- **Examples**: [Concrete examples]

---

## Implementation Code Structure

```python
class KarmaCalculator:
    """Karma calculation engine"""
    
    def calculate_experience_intensity(self, experience: Dict) -> float:
        """Calculate intensity of an experience"""
        pass
    
    def apply_emotional_weight(self, intensity: float, emotion: str) -> float:
        """Apply emotional weight to intensity"""
        pass
    
    def calculate_duration_factor(self, start: datetime, end: datetime) -> float:
        """Calculate duration factor"""
        pass
    
    def calculate_karma(self, life_log: List[Dict]) -> float:
        """Calculate total karma from life log"""
        pass
    
    def calculate_gravity(self, karma: float) -> float:
        """Calculate gravity from karma"""
        pass
    
    def calculate_inertia(self, gravity: float) -> float:
        """Calculate inertia from gravity"""
        pass
    
    def calculate_energy(self, karma: float) -> float:
        """Calculate energy from karma"""
        pass
```

---

## Testing Examples

### Example 1: [Scenario Name]
- **Input**: [Sample experience data]
- **Expected Output**: [Expected karma value]
- **Calculation Steps**: [Step-by-step breakdown]

### Example 2: [Scenario Name]
- **Input**: [Sample experience data]
- **Expected Output**: [Expected karma value]
- **Calculation Steps**: [Step-by-step breakdown]

---

## Edge Cases

### Edge Case 1: [Description]
- **Scenario**: [What happens]
- **Handling**: [How we handle it]
- **Rationale**: [Why this approach]

### Edge Case 2: [Description]
- **Scenario**: [What happens]
- **Handling**: [How we handle it]
- **Rationale**: [Why this approach]

---

## References

- [Source 1]
- [Source 2]
- [Source 3]

---

## Notes

[Additional observations, questions, or insights]
