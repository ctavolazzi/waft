# AI-Scientist Repository Structure Analysis

**Date:** 2026-01-13  
**Repository:** https://github.com/ctavolazzi/AI-Scientist  
**Location:** `/Users/ctavolazzi/Code/active/AI-Scientist`

## Overview

The AI-Scientist is a comprehensive system for fully automatic scientific discovery, enabling Foundation Models (LLMs) to perform research independently. The system follows a pipeline: **Idea → Experiment → Analysis → Paper → Review**.

## Core Architecture

### Main Entry Point
- **`launch_scientist.py`** - Orchestrates the entire pipeline:
  - Idea generation
  - Novelty checking
  - Experiment execution
  - Paper writeup
  - Review (optional)

### Core Modules (`ai_scientist/`)

1. **`generate_ideas.py`** - Research idea generation
   - Uses LLM to generate research ideas with structured JSON output
   - Includes novelty checking via Semantic Scholar API
   - Supports reflection/iteration on ideas
   - Outputs ideas with ratings (Interestingness, Feasibility, Novelty)

2. **`perform_experiments.py`** - Experiment execution
   - Executes LLM-generated code
   - Manages experiment state and results
   - Handles code generation and execution

3. **`perform_writeup.py`** - Paper writing workflow
   - Generates scientific papers from experiment results
   - Uses LaTeX templates
   - Includes citation management
   - Creates structured research papers

4. **`perform_review.py`** - Peer review simulation
   - Reviews generated papers
   - Provides structured feedback
   - Scores papers (1-10 scale)
   - Makes accept/reject decisions

5. **`llm.py`** - LLM integration patterns
   - Unified interface for multiple LLM providers (OpenAI, Anthropic, DeepSeek, Google Gemini)
   - Handles API calls, retries, rate limiting
   - Supports batch responses for ensembling
   - Extracts JSON from responses

### Template System

The system uses a template-based approach where each research domain has:
- **`experiment.py`** - Core experiment code
- **`plot.py`** - Visualization/plotting
- **`prompt.json`** - Template metadata and prompts
- **`seed_ideas.json`** - Example ideas for few-shot learning
- **`latex/template.tex`** - LaTeX paper template

### Available Templates

1. **nanoGPT** - Transformer autoregressive models
2. **2d_diffusion** - Diffusion generative models
3. **grokking** - Generalization in neural networks
4. **Community templates** - seir, mobilenetV3, sketch_rnn, MACE, earthquake-prediction, tensorf, probes

## Key Design Patterns

### 1. Structured JSON Communication
- All LLM interactions use structured JSON outputs
- Ideas, experiments, and reviews follow defined schemas
- Enables programmatic parsing and processing

### 2. Reflection/Iteration Loops
- Ideas go through multiple reflection rounds
- Experiments can be refined based on results
- Papers can be improved based on reviews

### 3. Template-Based Architecture
- Domain-specific templates enable different research areas
- Templates define experiment structure, prompts, and paper format
- Easy to extend with new domains

### 4. Multi-LLM Support
- Unified interface across providers
- Supports OpenAI, Anthropic, DeepSeek, Google Gemini
- Handles different API patterns consistently

### 5. Automated Pipeline
- End-to-end automation from idea to paper
- Minimal human intervention required
- Parallel execution support for multiple ideas

## Workflow

```
1. Generate Ideas
   ├─ Load seed ideas (few-shot examples)
   ├─ Generate new idea with LLM
   ├─ Reflect and refine (multiple rounds)
   └─ Check novelty (Semantic Scholar)

2. Perform Experiments
   ├─ Generate experiment code
   ├─ Execute code
   ├─ Collect results
   └─ Generate plots/visualizations

3. Write Paper
   ├─ Structure paper sections
   ├─ Generate content from results
   ├─ Add citations (Semantic Scholar)
   └─ Compile LaTeX to PDF

4. Review (Optional)
   ├─ Load paper text
   ├─ Generate review with LLM
   ├─ Score and provide feedback
   └─ Make accept/reject decision
```

## Data Structures

### Idea Format
```json
{
  "Name": "idea_name",
  "Title": "Full Title",
  "Experiment": "Implementation outline",
  "Interestingness": 1-10,
  "Feasibility": 1-10,
  "Novelty": 1-10
}
```

### Review Format
```python
{
  "Overall": 1-10,  # Overall score
  "Decision": "Accept" | "Reject",
  "Weaknesses": ["weakness1", "weakness2", ...],
  # Additional structured feedback
}
```

## Integration Points for WAFT

1. **Study Gym** - Can use idea generation patterns for QUESTION phase
2. **Scientific Method Tool** - Can adapt experiment execution patterns
3. **Scientific Paper Generator** - Can enhance with AI-Scientist paper structure
4. **PDF Quality Analysis** - Can add peer review capabilities
5. **LLM Integration** - Can standardize LLM patterns across WAFT

## Notes

- System requires GPU for experiments (PyTorch/CUDA)
- Uses LaTeX for paper generation (requires texlive-full)
- Supports parallel execution across multiple GPUs
- Cost: ~$15 per paper with Claude Sonnet 3.5
- Success rate depends on template, model, and idea complexity
