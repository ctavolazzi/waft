"""
Evolution Arena - Watch Agents Evolve in Real-Time

Combines the Evolution Engine with AI Town visualization to create
a live evolution simulation where you can watch natural selection happen.
"""

import streamlit as st
from pathlib import Path
import json
from datetime import datetime

# Optional plotly for visualization
try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

from waft.core.evolution_engine import EvolutionEngine
from waft.being import BeingSystem, Being


def initialize_evolution_arena(project_path: Path):
    """Initialize evolution arena in session state."""
    if 'evolution_arena' not in st.session_state:
        st.session_state.evolution_arena = {
            'engine': EvolutionEngine(project_path),
            'being_system': BeingSystem(project_path),
            'current_generation': 0,
            'population': [],
            'history': [],
            'running': False,
        }


def spawn_initial_population(num_beings: int = 10, reality_id: str = 'evolution-arena'):
    """Spawn initial population of beings."""
    arena = st.session_state.evolution_arena
    being_system = arena['being_system']

    # Create Adam (ancestor)
    adam = being_system.spawn_being(
        reality_id=reality_id,
        initial_skills={
            'reasoning': 50.0,
            'pattern_recognition': 50.0,
            'adaptation': 50.0,
            'sociability': 50.0,
        }
    )
    adam.fitness = 50.0
    being_system._save_being(adam)

    # Spawn initial variants
    population = []
    for i in range(num_beings):
        variant = being_system.spawn_being(
            reality_id=reality_id,
            parent_being_id=adam.being_id,
        )
        # Initialize fitness
        variant.fitness = 50.0
        being_system._save_being(variant)
        population.append(variant)

    arena['population'] = population
    arena['current_generation'] = 1

    return population


def evaluate_population_fitness(population: list[Being]):
    """Evaluate fitness of entire population using Scint Gym."""
    arena = st.session_state.evolution_arena
    gym = arena['engine'].scint_gym

    evaluations = []
    for being in population:
        eval_result = gym.evaluate_fitness(being)
        evaluations.append({
            'being_id': being.being_id,
            'fitness': eval_result['fitness_score'],
            'scints': eval_result['scints_detected'],
            'being': being,
        })

    return evaluations


def run_generation_cycle():
    """Run one generation cycle: evaluate, select, reproduce."""
    arena = st.session_state.evolution_arena

    # Evaluate current population
    evaluations = evaluate_population_fitness(arena['population'])

    # Sort by fitness
    evaluations.sort(key=lambda e: e['fitness'], reverse=True)

    # Selection: Keep top 50%
    survivors = evaluations[:len(evaluations) // 2]

    # Record generation stats
    gen_stats = {
        'generation': arena['current_generation'],
        'timestamp': datetime.now().isoformat(),
        'population_size': len(evaluations),
        'avg_fitness': sum(e['fitness'] for e in evaluations) / len(evaluations),
        'max_fitness': evaluations[0]['fitness'],
        'min_fitness': evaluations[-1]['fitness'],
        'total_scints': sum(e['scints'] for e in evaluations),
        'survivors': len(survivors),
    }
    arena['history'].append(gen_stats)

    # Reproduction: Spawn new variants from survivors
    being_system = arena['being_system']
    new_population = []

    for survivor_data in survivors:
        # Keep the survivor
        new_population.append(survivor_data['being'])

        # Spawn one offspring
        offspring = being_system.spawn_being(
            reality_id='evolution-arena',
            parent_being_id=survivor_data['being_id'],
        )
        offspring.fitness = 0.0  # Will be evaluated next generation
        being_system._save_being(offspring)
        new_population.append(offspring)

    # Update population
    arena['population'] = new_population
    arena['current_generation'] += 1

    return gen_stats


def render_evolution_arena():
    """Render the Evolution Arena interface."""
    st.markdown(
        """
        <style>
        .arena-header {
            font-size: 3rem;
            font-weight: bold;
            text-align: center;
            background: linear-gradient(90deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
        }
        .fitness-high {
            color: #4ade80;
            font-weight: bold;
        }
        .fitness-medium {
            color: #fbbf24;
        }
        .fitness-low {
            color: #f87171;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="arena-header">🧬 Evolution Arena</div>', unsafe_allow_html=True)
    st.markdown("**Watch agents evolve through natural selection in real-time**")

    project_path = Path.cwd()
    initialize_evolution_arena(project_path)
    arena = st.session_state.evolution_arena

    # Controls
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if arena['population']:
            st.metric("Generation", arena['current_generation'])
        else:
            st.metric("Generation", "Not Started")

    with col2:
        if arena['population']:
            st.metric("Population", len(arena['population']))
        else:
            st.metric("Population", 0)

    with col3:
        if arena['history']:
            avg_fitness = arena['history'][-1]['avg_fitness']
            st.metric("Avg Fitness", f"{avg_fitness:.1f}")
        else:
            st.metric("Avg Fitness", "-")

    with col4:
        if arena['history']:
            max_fitness = arena['history'][-1]['max_fitness']
            st.metric("Max Fitness", f"{max_fitness:.1f}")
        else:
            st.metric("Max Fitness", "-")

    st.markdown("---")

    # Action buttons
    col_a, col_b, col_c, col_d = st.columns(4)

    with col_a:
        if not arena['population']:
            num_beings = st.number_input("Initial Population", min_value=4, max_value=50, value=10, step=2)
            if st.button("🧬 Spawn Population", use_container_width=True):
                with st.spinner("Spawning initial population..."):
                    spawn_initial_population(num_beings)
                st.success(f"Spawned {num_beings} beings!")
                st.rerun()

    with col_b:
        if arena['population'] and not arena['running']:
            if st.button("▶️ Run Generation", use_container_width=True):
                with st.spinner("Running evolution cycle..."):
                    gen_stats = run_generation_cycle()
                st.success(f"Generation {gen_stats['generation']} complete!")
                st.rerun()

    with col_c:
        if arena['population']:
            num_generations = st.number_input("Auto Generations", min_value=1, max_value=20, value=5)
            if st.button("🚀 Auto Evolve", use_container_width=True):
                progress_bar = st.progress(0)
                status_text = st.empty()

                for i in range(num_generations):
                    status_text.text(f"Running generation {i+1}/{num_generations}...")
                    gen_stats = run_generation_cycle()
                    progress_bar.progress((i + 1) / num_generations)

                status_text.text(f"Completed {num_generations} generations!")
                st.success("Evolution complete!")
                st.rerun()

    with col_d:
        if arena['population']:
            if st.button("🔄 Reset", use_container_width=True):
                st.session_state.evolution_arena = {
                    'engine': EvolutionEngine(project_path),
                    'being_system': BeingSystem(project_path),
                    'current_generation': 0,
                    'population': [],
                    'history': [],
                    'running': False,
                }
                st.rerun()

    st.markdown("---")

    # Visualization
    if arena['population']:
        tab1, tab2, tab3 = st.tabs(["🗺️ Arena Map", "📊 Evolution Graph", "👥 Population List"])

        with tab1:
            render_arena_map(arena['population'])

        with tab2:
            render_evolution_graph(arena['history'])

        with tab3:
            render_population_list(arena['population'])


def render_arena_map(population: list[Being]):
    """Render visual map of beings with fitness indicators."""
    if not PLOTLY_AVAILABLE:
        st.warning("Install plotly for visualization: `uv add plotly`")
        return

    if not population:
        st.info("No beings to display")
        return

    # Create scatter plot
    fig = go.Figure()

    # Evaluate fitness for color coding
    arena = st.session_state.evolution_arena
    evaluations = evaluate_population_fitness(population)

    # Prepare data
    for eval_data in evaluations:
        being = eval_data['being']
        fitness = eval_data['fitness']

        # Position (random for now, could be based on skills)
        import random
        random.seed(hash(being.being_id))
        x = random.uniform(10, 90)
        y = random.uniform(10, 90)

        # Color based on fitness
        if fitness >= 80:
            color = '#4ade80'  # Green - high fitness
            size = 25
        elif fitness >= 60:
            color = '#fbbf24'  # Yellow - medium fitness
            size = 20
        else:
            color = '#f87171'  # Red - low fitness
            size = 15

        # Symbol based on scints
        symbol = 'star' if eval_data['scints'] == 0 else 'circle'

        fig.add_trace(go.Scatter(
            x=[x],
            y=[y],
            mode='markers+text',
            marker={
                'size': size,
                'color': color,
                'line': {'width': 2, 'color': 'white'},
                'symbol': symbol,
            },
            text=being.being_id[:8],
            textposition='top center',
            name=being.being_id[:8],
            hovertemplate=f"<b>{being.being_id[:12]}...</b><br>" +
                         f"Fitness: {fitness:.1f}<br>" +
                         f"Scints: {eval_data['scints']}<br>" +
                         f"Will to Live: {being.will_to_live:.1f}<br>" +
                         f"Luck: {being.luck:.1f}<br>" +
                         "<extra></extra>",
        ))

    fig.update_layout(
        title="🧬 Evolution Arena - Fitness Landscape",
        xaxis_title="Trait Axis 1",
        yaxis_title="Trait Axis 2",
        xaxis={'range': [0, 100], 'showgrid': True},
        yaxis={'range': [0, 100], 'showgrid': True},
        height=600,
        showlegend=False,
        hovermode='closest',
    )

    st.plotly_chart(fig, use_container_width=True)

    st.caption("🟢 Green = High Fitness (≥80) | 🟡 Yellow = Medium (60-79) | 🔴 Red = Low (<60)")
    st.caption("⭐ Star = Zero Scints (perfect) | ● Circle = Has Reality Fractures")


def render_evolution_graph(history: list[dict]):
    """Render evolution progress over generations."""
    if not PLOTLY_AVAILABLE or not history:
        return

    generations = [h['generation'] for h in history]
    avg_fitness = [h['avg_fitness'] for h in history]
    max_fitness = [h['max_fitness'] for h in history]
    min_fitness = [h['min_fitness'] for h in history]

    fig = go.Figure()

    # Max fitness
    fig.add_trace(go.Scatter(
        x=generations,
        y=max_fitness,
        mode='lines+markers',
        name='Max Fitness',
        line={'color': '#4ade80', 'width': 3},
    ))

    # Average fitness
    fig.add_trace(go.Scatter(
        x=generations,
        y=avg_fitness,
        mode='lines+markers',
        name='Avg Fitness',
        line={'color': '#60a5fa', 'width': 2},
    ))

    # Min fitness
    fig.add_trace(go.Scatter(
        x=generations,
        y=min_fitness,
        mode='lines+markers',
        name='Min Fitness',
        line={'color': '#f87171', 'width': 2, 'dash': 'dash'},
    ))

    fig.update_layout(
        title="📈 Fitness Evolution Over Generations",
        xaxis_title="Generation",
        yaxis_title="Fitness Score",
        yaxis={'range': [0, 105]},
        height=400,
        hovermode='x unified',
    )

    st.plotly_chart(fig, use_container_width=True)


def render_population_list(population: list[Being]):
    """Render list of all beings with stats."""
    arena = st.session_state.evolution_arena
    evaluations = evaluate_population_fitness(population)

    # Sort by fitness
    evaluations.sort(key=lambda e: e['fitness'], reverse=True)

    st.subheader(f"Population: {len(population)} beings")

    for i, eval_data in enumerate(evaluations):
        being = eval_data['being']
        fitness = eval_data['fitness']

        # Color code by fitness
        if fitness >= 80:
            fitness_class = 'fitness-high'
        elif fitness >= 60:
            fitness_class = 'fitness-medium'
        else:
            fitness_class = 'fitness-low'

        with st.expander(f"#{i+1} - {being.being_id[:12]}... (Fitness: {fitness:.1f})"):
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown(f"**Fitness:** <span class='{fitness_class}'>{fitness:.1f}</span>", unsafe_allow_html=True)
                st.write(f"**Scints:** {eval_data['scints']}")
                st.write(f"**Generation:** {arena['current_generation']}")

            with col2:
                st.write(f"**Will to Live:** {being.will_to_live:.1f}")
                st.write(f"**Luck:** {being.luck:.1f}")
                st.write(f"**Lifetimes:** {being.lifetimes}")

            with col3:
                st.write("**Skills:**")
                for skill, level in being.skills.items():
                    st.write(f"  • {skill}: {level:.1f}")


if __name__ == "__main__":
    render_evolution_arena()
