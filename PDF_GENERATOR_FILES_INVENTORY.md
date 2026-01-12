# PDF Generator Files Inventory

**Generated:** 2026-01-11 21:31:13 PST  
**Purpose:** Complete list of all PDF generator-related files in the WAFT codebase

---

## Core Generator Classes

### Main Generators
1. **`src/waft/evolution/pdf_generator.py`**
   - `PDFGenerator` class - Composable PDF generator with presets
   - Simple API for generating PDFs with minimal boilerplate
   - Uses ChatDistiller, StylingGenome, and TwoPageGenerator

2. **`src/waft/evolution/scientific_pdf_generator.py`**
   - `ScientificPDFGenerator` class - Extends PDFGenerator
   - Research tools and self-examination features
   - Scientific paper generation capabilities

3. **`src/waft/evolution/component_generator.py`**
   - `ComponentPDFGenerator` class - Component-based adaptive generation
   - `FoundationComponentGenerator` - WAFT-integrated component generator
   - Component-based document creation

4. **`src/waft/evolution/two_page_generator.py`**
   - `TwoPageGenerator` class - Main implementation (adaptive constraint enforcement)
   - Core PDF generation engine with two-page layout

5. **`src/waft/evolution/two_page_generator_legacy.py`**
   - `TwoPageGeneratorLegacy` class - Legacy version (kept for backward compatibility)

6. **`src/waft/evolution/document_evolution_engine.py`**
   - `DocumentEvolutionEngine` class - Evolutionary document creation with learning
   - Adaptive document generation system

7. **`src/waft/evolution/latex_generator.py`**
   - `LaTeXGenerator` class - LaTeX document generator
   - `generate_latex()` function - Quick LaTeX generation

8. **`src/waft/evolution/scientific_paper_generator.py`**
   - Scientific paper generation functionality

### Foundation System
9. **`src/waft/foundation.py`**
   - `DocumentEngine` class - Reusable Research Documentation Library
   - Block-based PDF generation using FPDF2
   - Content-agnostic PDF generation engine

---

## Supporting/Utility Files

10. **`src/waft/evolution/pdf_image_converter.py`**
    - `pdf_to_pngs()` - Convert PDF to PNG images
    - `pngs_to_pdf()` - Convert PNG images to PDF
    - `convert_pdf_to_images()` - Image conversion utilities
    - `convert_images_to_pdf()` - PDF creation from images
    - `PageSize` enum

11. **`src/waft/evolution/pdf_metrics.py`**
    - `PDFMetrics` class - Metrics data class
    - `PDFMetricsCollector` class - Metrics collector

12. **`src/waft/evolution/pdf_research_tool.py`**
    - PDF research tool functionality

13. **`src/waft/pdf_redactor.py`**
    - PDF redaction functionality

14. **`src/waft/evolution/chat_distiller.py`**
    - `ChatDistiller` class - Extracts ideas from chat content
    - `DistilledChat` class - Distilled chat data structure
    - `IdeaGene` class - Individual idea representation
    - Used by PDF generators for content extraction

15. **`src/waft/evolution/styling_genome.py`**
    - `StylingGenome` class - Evolutionary styling system
    - `StylingGene`, `FontGene`, `MarginGene`, `ColorGene`, `LayoutGene` classes
    - `StylingGenomeRegistry` class
    - Used by PDF generators for styling

---

## Template System (WeasyPrint + HTML)

16. **`src/waft/templates/field_guide.py`**
    - Field guide template

17. **`src/waft/templates/lab_notes.py`**
    - Lab notebook template

18. **`src/waft/templates/one_pager.py`**
    - One-pager template

19. **`src/waft/templates/personal_memo.py`**
    - Personal memo template

20. **`src/waft/templates/tm_report.py`**
    - Technical memo template

21. **`src/waft/evolution/templates/scientific_research_paper.md`**
    - Scientific research paper template (Markdown)

---

## Scripts Using PDF Generators

22. **`scripts/generate_documentation_pdfs.py`**
    - Markdown to PDF converter using Foundation system

23. **`scripts/generate_status_pdf.py`**
    - Status PDF generation script

24. **`scripts/generate_architecture_docs.py`**
    - Architecture documentation PDF generation

25. **`scripts/generate_latex_feature_docs.py`**
    - LaTeX feature documentation generation

26. **`scripts/generate_research_simulation_waft.py`**
    - Research simulation PDF generation

27. **`scripts/generate_enhanced_research_report.py`**
    - Enhanced research report generation

28. **`scripts/generate_comprehensive_feature_showcase.py`**
    - Comprehensive feature showcase PDF generation

29. **`scripts/generate_feature_showcase.py`**
    - Feature showcase PDF generation

30. **`scripts/generate_chat_one_pager_document.py`**
    - Chat one-pager document generation

31. **`scripts/create_chat_one_pager.py`**
    - Chat one-pager creation script

32. **`scripts/generate_test_summary.py`**
    - Test summary PDF generation

33. **`scripts/generate_improvements_summary.py`**
    - Improvements summary PDF generation

34. **`scripts/research_simulation_server.py`**
    - Research simulation server with PDF generation endpoint

35. **`scripts/pngs_to_pdf_binder.py`**
    - PNG to PDF binder utility

36. **`scripts/test_self_examination.py`**
    - Self-examination testing script

37. **`scripts/test_batch_with_wager.py`**
    - Batch testing with wager (uses PDF generators)

38. **`scripts/seed_reincarnation_demo.py`**
    - Seed reincarnation demo (uses PDF generators)

39. **`scripts/evolve_research_ui.py`**
    - Research UI evolution script

40. **`scripts/test_latex_generator.py`**
    - LaTeX generator testing script

41. **`tools/pdf_binder_organizer/organize_pdfs.py`**
    - PDF organization utility

42. **`_work_efforts/WE-260111-dr0f_evolutionary_iteration_process_pdf_png_screenshot_workflow/tools/generate_test_pdfs.py`**
    - Test PDF generation tool for work effort

43. **`WAFT-Mac-Shortcuts-Research/generate_session_pdf.py`**
    - Session PDF generation script

---

## Example Files

44. **`examples/generate_session_recap_pdf.py`**
    - Basic session recap PDF generation

45. **`examples/generate_session_recap_pdf_simple.py`**
    - Simple session recap PDF generation

46. **`examples/generate_session_recap_pdf_full.py`**
    - Full session recap PDF generation

47. **`examples/generate_session_recap_pdf_final.py`**
    - Final session recap PDF generation

48. **`examples/generate_session_recap_pdf_premium.py`**
    - Premium session recap PDF generation

49. **`examples/generate_session_recap_pdf_waft.py`**
    - WAFT session recap PDF generation

50. **`examples/generate_session_recap_pdf_clinical_standard.py`**
    - Clinical standard session recap PDF generation

51. **`examples/generate_session_recap_pdf_peak.py`**
    - Peak session recap PDF generation

52. **`examples/generate_session_recap_simple.py`**
    - Simple session recap generation

53. **`examples/generate_session_recap_final.py`**
    - Final session recap generation

54. **`examples/generate_scientific_session_recap.py`**
    - Scientific session recap generation

55. **`examples/generate_waft_intro_one_pager.py`**
    - WAFT intro one-pager generation

56. **`examples/generate_waft_intro_one_pager_bw.py`**
    - WAFT intro one-pager (black & white) generation

57. **`examples/test_component_generator.py`**
    - Component generator testing example

58. **`examples/test_evolution_engine.py`**
    - Evolution engine testing example

59. **`examples/demo_one_pager_evolution.py`**
    - One-pager evolution demo

60. **`examples/generate_flight_moment.py`**
    - Flight moment generation example

61. **`examples/enable_pdf_metrics.py`**
    - PDF metrics enabling example

62. **`examples/evolve_constraint.py`**
    - Constraint evolution example

---

## Test Files

63. **`tests/test_pdf_image_converter.py`**
    - PDF image converter tests

64. **`tests/test_foundation.py`**
    - Foundation system tests

---

## Documentation Files

65. **`docs/PDF_GENERATOR_API.md`**
    - PDF Generator API documentation

66. **`docs/PDF_SCIENTIFIC_EVOLUTION.md`**
    - Scientific PDF evolution documentation

67. **`docs/PDF_SCIENTIFIC_EVOLUTION_OBSERVER.md`**
    - Scientific PDF evolution observer documentation

68. **`docs/PDF_METRICS_COLLECTION.md`**
    - PDF metrics collection documentation

69. **`docs/PDF_PNG_CONVERSION.md`**
    - PDF to PNG conversion documentation

70. **`docs/PDF_LIBRARY_COMPARISON.md`**
    - PDF library comparison documentation

71. **`docs/EVOLUTIONARY_ITERATION_PROCESS.md`**
    - Evolutionary iteration process documentation

72. **`docs/STATUS_COMPONENTS_GUIDE.md`**
    - Status components guide

73. **`docs/SCIENTIFIC_RESEARCH_PAPER_TEMPLATE.md`**
    - Scientific research paper template documentation

74. **`WIKI_PDF_Generation_Guide.md`**
    - Wiki PDF generation guide

75. **`WIKI_PDF_PNG_Conversion.md`**
    - Wiki PDF to PNG conversion guide

76. **`WAFT-PDF-PNG-Conversion-Research/hypothesis.md`**
    - PDF PNG conversion research hypothesis

77. **`WAFT-PDF-PNG-Conversion-Research/test_suite.py`**
    - PDF PNG conversion test suite

---

## Work Effort Documentation

78. **`_work_efforts/PDF_GENERATOR_MODULARIZATION_COMPLETE.md`**
    - PDF generator modularization completion documentation

79. **`_work_efforts/PDF_SCIENTIFIC_EVOLUTION_COMPLETE.md`**
    - PDF scientific evolution completion documentation

80. **`_work_efforts/PDF_SCIENTIFIC_EVOLUTION_PLAN.md`**
    - PDF scientific evolution plan

81. **`_work_efforts/DEMO_PDF_GENERATION_COMPLETE.md`**
    - Demo PDF generation completion documentation

82. **`_work_efforts/CHECKPOINT_2026-01-11_PDF_SCIENTIFIC_EVOLUTION.md`**
    - PDF scientific evolution checkpoint

83. **`_work_efforts/CHECKPOINT_2026-01-11_PDF_PNG_TESTING_RESEARCH.md`**
    - PDF PNG testing research checkpoint

84. **`_work_efforts/NEXT_STEPS_2026-01-11_PDF_SCIENTIFIC_EVOLUTION.md`**
    - Next steps for PDF scientific evolution

85. **`_work_efforts/REFLECTION_2026-01-11_PDF_SCIENTIFIC_EVOLUTION.md`**
    - Reflection on PDF scientific evolution

86. **`_work_efforts/SCIENTIFIC_RESEARCH_PAPER_TEMPLATE_COMPLETE.md`**
    - Scientific research paper template completion

87. **`_work_efforts/METRICS_COLLECTION_IMPLEMENTATION.md`**
    - Metrics collection implementation documentation

---

## Module Exports

88. **`src/waft/evolution/__init__.py`**
    - Exports all PDF generator classes and utilities
    - Main entry point for evolution system

---

## Summary Statistics

- **Core Generator Classes:** 8 files
- **Supporting/Utility Files:** 6 files
- **Template System Files:** 6 files
- **Scripts Using Generators:** 22 files
- **Example Files:** 19 files
- **Test Files:** 2 files
- **Documentation Files:** 13 files
- **Work Effort Documentation:** 10 files
- **Module Exports:** 1 file

**Total: 87 PDF generator-related files**

---

## Key Generator Classes Hierarchy

```
PDFGenerator (base)
├── ScientificPDFGenerator (extends PDFGenerator)
├── ComponentPDFGenerator (component-based)
│   └── FoundationComponentGenerator (WAFT-integrated)
├── TwoPageGenerator (core engine)
│   └── TwoPageGeneratorLegacy (backward compatibility)
├── DocumentEvolutionEngine (evolutionary)
├── LaTeXGenerator (LaTeX output)
└── DocumentEngine (foundation.py - FPDF2-based)
```

---

## Technology Stack

1. **WeasyPrint** - Template system (HTML → PDF)
2. **FPDF2** - Foundation system (pure Python)
3. **ReportLab** - Used in some generators
4. **LaTeX** - LaTeX generator output
5. **Pillow/PIL** - Image conversion (PDF ↔ PNG)

---

## Notes

- The main entry point for most users is `src/waft/evolution/pdf_generator.py`
- Scientific features are in `src/waft/evolution/scientific_pdf_generator.py`
- Component-based generation is in `src/waft/evolution/component_generator.py`
- Legacy Foundation system is in `src/waft/foundation.py`
- Template system uses WeasyPrint and is in `src/waft/templates/`
- All generators support automatic PNG conversion (v0.5.2+)
