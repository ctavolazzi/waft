#import "@preview/shiroa:0.3.1": *
#show: book

#book-meta(
  title: "WAFT Auto-Work: Autonomous Work Effort Execution Guide",
  description: "A comprehensive guide to the WAFT Auto-Work feature, covering its functionality, priority scoring algorithm, safety mechanisms, and integration with Empirica, Pantheon, Campfire, and D&D campaign systems.",
  authors: ("WAFT System", "AI Assistant"),
  language: "en",
  repository: "https://github.com/ctavolazzi/waft",
  summary: [
    = Part I: Introduction & Overview
    - #chapter("src/chapters/01-introduction.typ", section: "1")[Introduction]
    - #chapter("src/chapters/02-what-is-auto-work.typ", section: "2")[What is Auto-Work?]
    - #chapter("src/chapters/03-key-features.typ", section: "3")[Key Features]

    = Part II: How It Works
    - #chapter("src/chapters/04-architecture.typ", section: "4")[System Architecture]
    - #chapter("src/chapters/05-priority-scoring.typ", section: "5")[Priority Scoring Algorithm]
    - #chapter("src/chapters/06-selection-process.typ", section: "6")[Work Effort Selection]
    - #chapter("src/chapters/07-action-determination.typ", section: "7")[Action Determination]
    - #chapter("src/chapters/08-execution-phase.typ", section: "8")[Execution Phase]

    = Part III: Integration & Safety
    - #chapter("src/chapters/09-empirica-integration.typ", section: "9")[Empirica Integration]
    - #chapter("src/chapters/10-pantheon-integration.typ", section: "10")[Pantheon Integration]
    - #chapter("src/chapters/11-campfire-integration.typ", section: "11")[Campfire Storytelling]
    - #chapter("src/chapters/12-dnd-campaign.typ", section: "12")[D&D Campaign Integration]
    - #chapter("src/chapters/13-safety-mechanisms.typ", section: "13")[Safety Mechanisms]

    = Part IV: Usage Guide
    - #chapter("src/chapters/14-basic-usage.typ", section: "14")[Basic Usage]
    - #chapter("src/chapters/15-command-options.typ", section: "15")[Command Options]
    - #chapter("src/chapters/16-walkthrough.typ", section: "16")[Step-by-Step Walkthrough]
    - #chapter("src/chapters/17-examples.typ", section: "17")[Usage Examples]
    - #chapter("src/chapters/18-troubleshooting.typ", section: "18")[Troubleshooting]

    = Part V: Advanced Topics
    - #chapter("src/chapters/19-customization.typ", section: "19")[Customization & Configuration]
    - #chapter("src/chapters/20-best-practices.typ", section: "20")[Best Practices]
    - #chapter("src/chapters/21-future-enhancements.typ", section: "21")[Future Enhancements]
    - #chapter("src/chapters/22-conclusion.typ", section: "22")[Conclusion]
  ]
)
