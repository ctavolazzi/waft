# Component Evolution System: Design Document

**Work Effort**: WE-260111-jr7r  
**Created**: 2026-01-11  
**Status**: Design Phase

---

## Vision

Create an evolutionary system where page components (sections, headers, lists, paragraphs, code blocks) evolve over time to maximize content density and adapt to usage patterns. Components will have genomes, track fitness, spawn variants, and evolve based on performance - all using the genetic ancestry system.

---

## Core Concept: Components as Digital Organisms

### Component Types

Each component type is a distinct organism that can evolve:

1. **Sections** (`story-section`, `boxed-section`, `highlight-section`, `minimal-section`)
2. **Headers** (`h1`, `h2`, `h3`, `h4`) with variants (`boxed`, `highlight`, `underlined`)
3. **Lists** (`ul`, `ol`) with variants (`custom-bullets`, `checkmarks`, `dashed`, `boxed`)
4. **Paragraphs** with variants (`indented`, `highlight`, `compact`)
5. **Code Blocks** with variants (`boxed`, `minimal`)

### Component Genome

Each component instance has a "genome" - a complete description of its configuration:

```python
@dataclass
class ComponentGenome:
    # Identity
    genome_id: str  # SHA-256 hash of component config
    component_type: str  # 'section', 'header', 'list', 'paragraph', 'code'
    style_variant: str  # Specific style (e.g., 'boxed-section', 'highlight')
    
    # Configuration (what makes this component unique)
    config: Dict[str, Any]  # Font size, margins, spacing, colors, etc.
    
    # Metrics (how well it performs)
    content_density: float  # Words/chars per page area
    space_efficiency: float  # Percentage of space used effectively
    readability_score: float  # Readability metric (0-1)
    usage_count: int  # How many times used
    
    # Lineage (genetic ancestry)
    parent_id: Optional[str]  # Parent genome ID
    generation: int  # Generation number (0 = genesis)
    lineage_path: List[str]  # Path from genesis to this genome
    
    # Fitness
    fitness_score: float  # Overall fitness (0-1)
    last_evaluated: datetime  # When fitness was last calculated
    
    # Metadata
    created_at: datetime
    last_used: datetime
```

### Genome ID Generation

```python
def compute_component_genome_id(component_type: str, style_variant: str, config: Dict[str, Any]) -> str:
    """Compute SHA-256 hash of component configuration."""
    import hashlib
    import json
    
    # Create deterministic representation
    genome_data = {
        "component_type": component_type,
        "style_variant": style_variant,
        "config": sorted(config.items()),  # Sort for determinism
        "schema_version": "1.0"  # For future compatibility
    }
    
    genome_str = json.dumps(genome_data, sort_keys=True)
    return hashlib.sha256(genome_str.encode()).hexdigest()
```

---

## Fitness Function

### Fitness Metrics

Components are evaluated on multiple dimensions:

1. **Content Density** (40% weight)
   - Measures how much content fits in the space
   - Formula: `(words_per_component / space_used) * normalization_factor`
   - Higher is better

2. **Space Efficiency** (30% weight)
   - Measures wasted space (margins, padding, empty areas)
   - Formula: `(content_area / total_area) * 100`
   - Higher is better

3. **Readability Score** (20% weight)
   - Measures readability (font size, line height, contrast)
   - Based on readability formulas (Flesch, etc.)
   - Higher is better

4. **Usage Frequency** (10% weight)
   - Measures how often component is used
   - Formula: `log(usage_count + 1) / max_usage`
   - Higher is better

### Fitness Calculation

```python
def calculate_fitness(genome: ComponentGenome) -> float:
    """Calculate overall fitness score."""
    density_score = genome.content_density * 0.40
    efficiency_score = genome.space_efficiency * 0.30
    readability_score = genome.readability_score * 0.20
    usage_score = (math.log(genome.usage_count + 1) / 10.0) * 0.10
    
    return density_score + efficiency_score + readability_score + usage_score
```

### Fitness Threshold

- **Fitness >= 0.5**: Component survives (SURVIVAL event)
- **Fitness < 0.5**: Component dies (DEATH event) - not used in future generations

---

## Evolutionary Events

### SPAWN: Component Reproduction

When a component is used, it can spawn variants with mutations:

```python
def spawn_variant(parent_genome: ComponentGenome, mutation_type: str) -> ComponentGenome:
    """Spawn a variant with a specific mutation."""
    # Create new config with mutation
    new_config = parent_genome.config.copy()
    
    if mutation_type == "font_size_increase":
        new_config["font_size"] = parent_genome.config["font_size"] * 1.1
    elif mutation_type == "margin_reduction":
        new_config["margin"] = parent_genome.config["margin"] * 0.9
    elif mutation_type == "spacing_optimization":
        new_config["line_height"] = parent_genome.config["line_height"] * 0.95
    elif mutation_type == "style_variant":
        new_config["style"] = random.choice(available_styles)
    
    # Create new genome
    variant = ComponentGenome(
        genome_id=compute_component_genome_id(
            parent_genome.component_type,
            new_config.get("style_variant", parent_genome.style_variant),
            new_config
        ),
        component_type=parent_genome.component_type,
        style_variant=new_config.get("style_variant", parent_genome.style_variant),
        config=new_config,
        parent_id=parent_genome.genome_id,
        generation=parent_genome.generation + 1,
        lineage_path=parent_genome.lineage_path + [parent_genome.genome_id],
        # ... other fields
    )
    
    # Record SPAWN event
    record_evolutionary_event(
        event_type=EvolutionaryEventType.SPAWN,
        genome_id=variant.genome_id,
        parent_id=parent_genome.genome_id,
        payload={"mutation_type": mutation_type, "config_change": new_config}
    )
    
    return variant
```

### MUTATE: Component Evolution (Hot-Swap)

After evaluating fitness of spawned variants, the best can replace the current component:

```python
def evolve_component(current_genome: ComponentGenome, variants: List[ComponentGenome]) -> ComponentGenome:
    """Evolve component by hot-swapping to best variant."""
    # Evaluate fitness of all variants
    for variant in variants:
        variant.fitness_score = calculate_fitness(variant)
    
    # Select best variant
    best_variant = max(variants, key=lambda g: g.fitness_score)
    
    # Only evolve if better
    if best_variant.fitness_score > current_genome.fitness_score:
        # Preserve old genome in flight recorder
        record_evolutionary_event(
            event_type=EvolutionaryEventType.MUTATE,
            genome_id=best_variant.genome_id,
            parent_id=current_genome.genome_id,
            payload={
                "old_genome": current_genome.genome_id,
                "new_genome": best_variant.genome_id,
                "fitness_improvement": best_variant.fitness_score - current_genome.fitness_score
            }
        )
        
        return best_variant
    
    return current_genome
```

### GYM_EVAL: Fitness Evaluation

Components are evaluated after each one-pager generation:

```python
def evaluate_component(genome: ComponentGenome, usage_context: Dict[str, Any]) -> Dict[str, Any]:
    """Evaluate component fitness in context."""
    # Measure actual performance
    content_density = measure_content_density(usage_context)
    space_efficiency = measure_space_efficiency(usage_context)
    readability_score = measure_readability(usage_context)
    
    # Update genome metrics
    genome.content_density = content_density
    genome.space_efficiency = space_efficiency
    genome.readability_score = readability_score
    genome.usage_count += 1
    genome.last_used = datetime.utcnow()
    
    # Calculate fitness
    fitness = calculate_fitness(genome)
    genome.fitness_score = fitness
    genome.last_evaluated = datetime.utcnow()
    
    # Record evaluation event
    record_evolutionary_event(
        event_type=EvolutionaryEventType.GYM_EVAL,
        genome_id=genome.genome_id,
        fitness_metrics={
            "content_density": content_density,
            "space_efficiency": space_efficiency,
            "readability_score": readability_score,
            "overall_fitness": fitness
        }
    )
    
    # Record survival or death
    if fitness >= 0.5:
        record_evolutionary_event(
            event_type=EvolutionaryEventType.SURVIVAL,
            genome_id=genome.genome_id
        )
    else:
        record_evolutionary_event(
            event_type=EvolutionaryEventType.DEATH,
            genome_id=genome.genome_id
        )
    
    return {
        "fitness": fitness,
        "metrics": {
            "content_density": content_density,
            "space_efficiency": space_efficiency,
            "readability_score": readability_score
        }
    }
```

---

## Component Registry

### Storage

```python
class ComponentRegistry:
    """Registry for tracking all component genomes."""
    
    def __init__(self, registry_path: Path):
        self.registry_path = registry_path
        self.genomes: Dict[str, ComponentGenome] = {}
        self.load()
    
    def register(self, genome: ComponentGenome):
        """Register a component genome."""
        self.genomes[genome.genome_id] = genome
        self.save()
    
    def get_best_components(self, component_type: str, limit: int = 10) -> List[ComponentGenome]:
        """Get best performing components of a type."""
        components = [g for g in self.genomes.values() if g.component_type == component_type]
        components.sort(key=lambda g: g.fitness_score, reverse=True)
        return components[:limit]
    
    def get_family_tree(self, genome_id: str) -> Dict[str, Any]:
        """Get family tree for a component genome."""
        genome = self.genomes[genome_id]
        tree = {
            "genome_id": genome_id,
            "lineage": genome.lineage_path,
            "generation": genome.generation,
            "children": self._find_children(genome_id),
            "fitness": genome.fitness_score
        }
        return tree
    
    def _find_children(self, parent_id: str) -> List[str]:
        """Find children of a parent genome."""
        return [g.genome_id for g in self.genomes.values() if g.parent_id == parent_id]
```

---

## Integration with OnePager

### Current System (Static Style Rotation)

```python
# Current: Static rotation
section_styles = ['story-section', 'boxed-section', 'highlight-section', 'minimal-section']
style = section_styles[section_count % len(section_styles)]
```

### Evolutionary System (Dynamic Component Selection)

```python
# New: Evolutionary selection
def get_best_component(component_type: str, context: Dict[str, Any]) -> ComponentGenome:
    """Get best performing component for context."""
    registry = ComponentRegistry.get_instance()
    
    # Get candidates
    candidates = registry.get_best_components(component_type, limit=5)
    
    # Spawn variants from best candidates
    variants = []
    for candidate in candidates[:3]:  # Top 3
        variants.extend(spawn_variants(candidate, mutation_types=["font_size", "margin", "spacing"]))
    
    # Evaluate variants in context
    for variant in variants:
        evaluate_component(variant, context)
    
    # Select best variant
    best = max(variants, key=lambda g: g.fitness_score)
    
    # Evolve if better than current
    current = get_current_component(component_type)
    if best.fitness_score > current.fitness_score:
        return evolve_component(current, variants)
    
    return current
```

### Usage in OnePager

```python
class OnePager:
    def _markdown_to_html(self, markdown: str) -> str:
        # ... existing code ...
        
        # Instead of static rotation, use evolutionary selection
        registry = ComponentRegistry.get_instance()
        
        for line in lines:
            if line.startswith('## '):
                # Get best section component
                context = {"content_length": len(line), "previous_components": ...}
                section_genome = get_best_component("section", context)
                
                # Use component's style
                style = section_genome.style_variant
                html_parts.append(f'<div class="{style}">')
                
                # Track usage
                registry.register_usage(section_genome.genome_id, context)
```

---

## Implementation Plan

### Phase 1: Foundation
1. Create `ComponentGenome dataclass`
2. Implement genome ID computation
3. Create ComponentRegistry
4. Basic metrics tracking

### Phase 2: Fitness System
1. Implement fitness calculation
2. Create measurement functions (density, efficiency, readability)
3. Implement GYM_EVAL events
4. SURVIVAL/DEATH event recording

### Phase 3: Evolution
1. Implement SPAWN events
2. Mutation types (font, margin, spacing, style)
3. Implement MUTATE events (hot-swap)
4. Variant evaluation and selection

### Phase 4: Integration
1. Integrate with OnePager class
2. Replace static rotation with evolutionary selection
3. Automatic component tracking
4. Backward compatibility

### Phase 5: Analysis
1. Family tree visualization
2. Pattern analysis
3. Best component recommendations
4. Evolution reports

---

## Expected Outcomes

1. **Components evolve to maximize content density** - Components that fit more content score higher
2. **Components adapt to usage patterns** - Frequently used components evolve faster
3. **Better space utilization** - Components optimize margins, spacing, font sizes
4. **Maintained readability** - Evolution doesn't sacrifice readability
5. **Complete lineage tracking** - Every component has a family tree
6. **Scientific data** - All evolution events recorded for analysis

---

## Scientific Value

This system enables:
- **Phylogenetic Analysis**: Study component evolution relationships
- **Mutation Impact**: Measure effect of specific mutations (font size, margin changes)
- **Fitness Landscape**: Map fitness scores across component space
- **Convergence Analysis**: Identify optimal component configurations
- **Dead End Detection**: Identify component configurations that don't work

---

**Status**: Design complete, ready for implementation  
**Next Action**: Begin Phase 1 - Foundation
