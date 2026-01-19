#import "@preview/shiroa:0.3.1": *
#show: book

#book-meta(
  title: "WAFT Command Discovery: A Journey Through System Capabilities",
  description: "A comprehensive guide documenting the exploration of WAFT's command ecosystem, the systematic discovery of available tools, and the methodical evolution of a unified command dashboard interface.",
  authors: ("WAFT System", "AI Assistant"),
  language: "en",
  repository: "https://github.com/ctavolazzi/waft",
  summary: [
    = Part I: Command Discovery Journey
    - #chapter("src/chapters/01-introduction.typ", section: "1")[Introduction]
    - #chapter("src/chapters/02-documentation-commands.typ", section: "2")[Documentation Commands]
    - #chapter("src/chapters/03-learning-research.typ", section: "3")[Learning & Research Tools]
    - #chapter("src/chapters/04-document-generation.typ", section: "4")[Document Generation]
    - #chapter("src/chapters/05-status-visualization.typ", section: "5")[Status & Visualization]
    
    = Part II: UI Evolution Process
    - #chapter("src/chapters/06-dashboard-need.typ", section: "6")[The Need for a Dashboard]
    - #chapter("src/chapters/07-design-process.typ", section: "7")[Methodical Design Process]
    - #chapter("src/chapters/08-technical-requirements.typ", section: "8")[Technical Requirements]
    - #chapter("src/chapters/09-wireframe.typ", section: "9")[Wireframe & Structure]
    - #chapter("src/chapters/10-implementation.typ", section: "10")[Implementation Roadmap]
    
    = Part III: System Integration
    - #chapter("src/chapters/11-command-registry.typ", section: "11")[Command Registry]
    - #chapter("src/chapters/12-artifact-management.typ", section: "12")[Artifact Management]
    - #chapter("src/chapters/13-work-effort-integration.typ", section: "13")[Work Effort Integration]
    - #chapter("src/chapters/14-status-monitoring.typ", section: "14")[Status Monitoring]
    
    = Part IV: Lessons & Insights
    - #chapter("src/chapters/15-discovery-patterns.typ", section: "15")[Command Discovery Patterns]
    - #chapter("src/chapters/16-design-learnings.typ", section: "16")[Design Process Learnings]
    - #chapter("src/chapters/17-future-enhancements.typ", section: "17")[Future Enhancements]
    - #chapter("src/chapters/18-conclusion.typ", section: "18")[Conclusion]
  ]
)
