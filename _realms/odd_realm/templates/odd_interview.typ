// ODD Interview Template
// Template for creating interview transcripts between ODD Beings
//
// Usage:
//   #import "odd_components.typ": *
//   #show: odd-interview.with(
//     interview-id: "ODD-INT-001",
//     participants: ("ARCHIVIST-001", "WITNESS-001"),
//     classification: "WITNESSED"
//   )

#import "odd_components.typ": *

// Re-export the template and components for easy importing

// Example structure for an interview:
//
// #speaker("ARCHIVIST-001")
// Your question here.
//
// #speaker("WITNESS-001")
// The response.
//
// #odd-note[
//   Editorial note about the conversation
// ]
//
// #speaker("ARCHIVIST-001")
// Follow-up question.
//
// #archive-ref("NX-INT-XXXX", stability: 0.94)

// Template is defined in odd_components.typ
// This file serves as documentation and entry point
