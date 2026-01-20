#import "@preview/aero-check:0.1.1": *

#show: checklist.with(
  title: "WAFT System Pre-Flight Checklist",
  disclaimer: "Complete all items before proceeding with document generation operations.",
  style: 0,
)

#topic("Pre-Flight Inspection")[
  #section("System Status")[
    #step("Verify Typst CLI is installed and accessible", "Check")
    #step("Confirm Python environment is active", "Check")
    #step("Validate all required dependencies are installed", "Check")
    #step("Check available disk space (minimum 1GB free)", "Check")
    #step("Verify network connectivity for package downloads", "Check")
  ]
  
  #section("Template Registry")[
    #step("Confirm template registry is accessible", "Check")
    #step("Verify template discovery system is operational", "Check")
    #step("Check for template conflicts or duplicates", "Check")
    #step("Validate template metadata extraction", "Check")
  ]
]

#colbreak()

#topic("Document Generation")[
  #section("Input Validation")[
    #step("Verify input data format is correct", "Check")
    #step("Confirm all required fields are present", "Check")
    #step("Validate file paths and permissions", "Check")
    #step("Check for special characters or encoding issues", "Check")
  ]
  
  #section("Compilation")[
    #step("Initialize Typst compiler instance", "Check")
    #step("Load template and dependencies", "Check")
    #step("Execute compilation process", "Check")
    #step("Verify PDF output was generated", "Check")
    #step("Validate PDF file integrity", "Check")
  ]
]

#topic("Post-Flight")[
  #section("Quality Assurance")[
    #step("Review generated document for formatting errors", "Check")
    #step("Verify all content is present and correct", "Check")
    #step("Check page numbering and layout", "Check")
    #step("Confirm metadata is embedded correctly", "Check")
    #step("Validate file size is within expected range", "Check")
  ]
  
  #section("Cleanup")[
    #step("Archive temporary files", "Check")
    #step("Update work effort documentation", "Check")
    #step("Log generation metrics", "Check")
    #step("Clear compilation cache if needed", "Check")
  ]
]
