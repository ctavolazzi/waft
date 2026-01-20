// WAFT TROUBLESHOOTING
// Common Issues and Solutions

#import "@preview/showybox:2.0.4": showybox

#set document(title: "Troubleshooting Guide", author: "WAFT Support")
#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 10pt)

#let danger = rgb("#e53e3e")
#let warning = rgb("#dd6b20")
#let success = rgb("#38a169")

#align(center)[
  #rect(fill: danger, width: 100%, inset: 2em)[
    #text(fill: white, size: 24pt, weight: "bold")[TROUBLESHOOTING]
    #v(0.3em)
    #text(fill: white.darken(10%), size: 12pt)[WAFT | Common Issues and Solutions]
  ]
]

#v(1em)

= Installation Issues

== "Command not found: waft"

#showybox(frame: (border-color: danger, body-color: danger.lighten(95%)))[
  *Problem:* WAFT not in PATH after installation.
  
  *Solutions:*
  1. If using `uv`: Run `uv tool install waft` again
  2. If using `pip`: Ensure `~/.local/bin` is in PATH
  3. Try: `python -m waft` instead
]

== "Module not found" errors

#showybox(frame: (border-color: warning, body-color: warning.lighten(95%)))[
  *Problem:* Dependencies not installed correctly.
  
  *Solutions:*
  1. Run `uv sync` or `pip install -e .` in WAFT directory
  2. Check Python version (3.11+ required)
  3. Try fresh virtual environment
]

= Runtime Issues

== "API key not found"

#showybox(frame: (border-color: danger, body-color: danger.lighten(95%)))[
  *Problem:* LLM API key not configured.
  
  *Solutions:*
  1. Set `OPENAI_API_KEY` environment variable
  2. Or configure in `waft.toml`:
     ```toml
     [llm]
     api_key = "sk-..."
     ```
]

== Evolution stalls at 0% fitness

#showybox(frame: (border-color: warning, body-color: warning.lighten(95%)))[
  *Problem:* All agents failing Scint Gym.
  
  *Solutions:*
  1. Check agent code for syntax errors
  2. Verify LLM connectivity
  3. Lower difficulty settings in config
  4. Check logs: `waft flight list --type GYM_EVAL`
]

== "Timeout" errors during evaluation

#showybox(frame: (border-color: warning, body-color: warning.lighten(95%)))[
  *Problem:* Gym scenarios taking too long.
  
  *Solutions:*
  1. Increase timeout in config:
     ```toml
     [gym]
     timeout_seconds = 600
     ```
  2. Use faster LLM model
  3. Simplify agent logic
]

= Performance Issues

== Evolution too slow

#showybox(frame: (border-color: warning, body-color: warning.lighten(95%)))[
  *Causes and solutions:*
  - Large population → Reduce to 10-20
  - Complex scenarios → Use simpler gym config
  - Slow LLM → Use faster model or local
  - Serial execution → Enable parallel:
    ```toml
    [gym]
    parallel_workers = 4
    ```
]

== High memory usage

#showybox(frame: (border-color: warning, body-color: warning.lighten(95%)))[
  *Causes and solutions:*
  - Large population history → Prune old generations
  - Flight Recorder growth → Archive old data
  - Agent memory leaks → Check custom agent code
]

= Getting Help

#showybox(frame: (border-color: success, body-color: success.lighten(95%)))[
  1. Check logs: `waft flight list`
  2. Run diagnostics: `waft verify --verbose`
  3. Search issues: github.com/ctavolazzi/waft/issues
  4. Open new issue with:
     - WAFT version (`waft --version`)
     - Error message
     - Steps to reproduce
]

#v(1em)

#align(center)[
  #rect(fill: danger, inset: 1em)[
    #text(fill: white)[TROUBLESHOOTING | We've Got You Covered]
  ]
]
