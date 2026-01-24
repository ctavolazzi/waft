// WAFT Standard Border Helper
// ============================
// This file provides a standard border pattern for all WAFT Typst templates
// to ensure quick and easy identification of WAFT-generated documents.

#import "@preview/s6t5-page-bordering:1.0.0": s6t5-page-bordering

// Standard WAFT border configuration
// Use this in all WAFT templates for consistent identification
#let waft-border = s6t5-page-bordering.with(
  margin: (left: 0.75in, right: 0.75in, top: 1in, bottom: 1in),
  expand: 15pt,
  space-top: 15pt,
  space-bottom: 15pt,
  stroke-header: none,
  stroke-footer: none,
  header: "",
  footer: "",
)

// Alternative configurations for different document types

// For documents with headers/footers
#let waft-border-with-header = s6t5-page-bordering.with(
  margin: (left: 0.75in, right: 0.75in, top: 1in, bottom: 1in),
  expand: 15pt,
  space-top: 15pt,
  space-bottom: 15pt,
  stroke-header: 1pt + black,
  stroke-footer: 1pt + black,
  header: "",
  footer: "",
)

// For narrow margin documents
#let waft-border-narrow = s6t5-page-bordering.with(
  margin: (left: 0.5in, right: 0.5in, top: 0.75in, bottom: 0.75in),
  expand: 10pt,
  space-top: 10pt,
  space-bottom: 10pt,
  stroke-header: none,
  stroke-footer: none,
  header: "",
  footer: "",
)

// Usage example:
// #show: waft-border
// #set page(...)  // Your page settings
// #set text(...)  // Your text settings
// = Your Document Title
