---
name: Invoice Generator Integration for KarmaMarket
overview: Install and test the invoice-generator React app, extract its PDF generation logic, and integrate it into KarmaMarket's Python codebase to generate invoices for lifetime purchases, treasure purchases, and other karma transactions.
todos:
  - id: install_invoice_generator
    content: Clone invoice-generator repo to _experiments/ and install dependencies
    status: pending
  - id: test_invoice_generator
    content: Run invoice-generator locally and test with sample data to understand structure
    status: pending
  - id: analyze_invoice_logic
    content: Document invoice generation logic, data structure, and PDF creation process
    status: pending
  - id: design_python_generator
    content: Design KarmaInvoiceGenerator class structure and integration points with KarmaMarket
    status: pending
  - id: implement_invoice_generator
    content: Create src/waft/invoice_generator.py with invoice generation using WeasyPrint or ReportLab
    status: pending
  - id: integrate_karmamarket
    content: Add generate_invoice() methods to KarmaMarket and AfterlifeKarmaMarket classes
    status: pending
  - id: create_invoice_templates
    content: Create HTML templates or ReportLab layouts for invoice formatting
    status: pending
  - id: test_lifetime_invoices
    content: Test invoice generation for lifetime purchases
    status: pending
  - id: test_treasure_invoices
    content: Test invoice generation for treasure purchases
    status: pending
  - id: write_tests
    content: Create unit and integration tests for invoice generator
    status: pending
  - id: manual_testing
    content: Manually test invoice generation with real KarmaMarket transactions
    status: pending
---

# Invoice Generator Integration for KarmaMarket

## Overview

Install and test the invoice-generator React app (https://github.com/johnuberbacher/invoice-generator.git), extract its PDF generation logic, and create a Python-based invoice generator integrated with KarmaMarket to produce invoices for:

- Lifetime purchases
- Treasure purchases from Afterlife Karma Market
- Karma transactions
- Transaction summaries

## Analysis

### Current State

- **KarmaMarket**: Python-based system in `src/waft/karma_market.py`
- **PDF Generation**: Multiple systems available (WeasyPrint, FPDF2, ReportLab)
- **Invoice Generator**: React app using jspdf-react for PDF generation
- **Integration Point**: Need to generate invoices from Python for KarmaMarket transactions

### Invoice Generator Structure

From the GitHub repo:

- React app with modal-based invoice entry
- Uses jspdf-react to capture canvas and convert to PDF
- Features: itemized items, quantities, prices, tax rates, discounts
- Bootstrap UI for invoice form

### Integration Approach

Extract the core invoice generation logic and create a Python equivalent using existing PDF libraries (WeasyPrint or ReportLab) that can:

1. Generate invoices from KarmaMarket transaction data
2. Support itemized billing (lifetimes, treasures, tools, etc.)
3. Calculate totals, taxes, discounts
4. Format professionally for karma transactions

## Implementation Plan

### Phase 1: Installation and Testing

**1.1 Clone and Install Invoice Generator**

- Clone repo to `_experiments/invoice-generator/`
- Install dependencies (`npm install`)
- Run the app locally (`npm start`)
- Test invoice generation with sample data
- Document the invoice structure and data format

**1.2 Analyze Invoice Generation Logic**

- Review React components for invoice structure
- Identify jspdf-react usage patterns
- Document invoice fields and calculations
- Map invoice data structure to KarmaMarket transaction format

**Files to examine:**

- `src/` directory structure
- Invoice form components
- PDF generation logic
- Data model and state management

### Phase 2: Extract Core Logic

**2.1 Document Invoice Structure**

- Invoice header (from/to, date, invoice number)
- Itemized line items (description, quantity, price, total)
- Subtotals, taxes, discounts
- Grand total
- Footer/notes

**2.2 Map to KarmaMarket Data**

- Lifetime purchase → invoice line items
- Treasure purchase → invoice line items
- Tool purchases → invoice line items
- Karma costs → pricing
- Transaction metadata → invoice header/footer

**2.3 Design Python Invoice Generator**

- Class: `KarmaInvoiceGenerator` in `src/waft/karma_market.py` or new file
- Methods:
  - `generate_invoice(transaction_data)` → PDF path
  - `_format_invoice_data(transaction)` → invoice dict
  - `_calculate_totals(items)` → totals dict
- Use WeasyPrint or ReportLab for PDF generation

### Phase 3: Python Implementation

**3.1 Create Invoice Generator Class**

- Location: `src/waft/invoice_generator.py` (new file)
- Dependencies: WeasyPrint (preferred) or ReportLab
- Structure:
  ```python
  class KarmaInvoiceGenerator:
      def generate_invoice(
          self,
          transaction: Dict[str, Any],
          output_path: Optional[Path] = None
      ) -> Path:
          """Generate PDF invoice from KarmaMarket transaction."""
  ```


**3.2 Implement Invoice Templates**

- HTML template for invoice layout (if using WeasyPrint)
- Or Platypus flowables (if using ReportLab)
- Support for:
  - Header with KarmaMarket branding
  - Transaction details (lifetime_id, soul_id, timestamp)
  - Itemized line items
  - Karma calculations
  - Footer with transaction ID

**3.3 Integrate with KarmaMarket**

- Add `generate_invoice()` method to `KarmaMarket` class
- Add `generate_invoice()` method to `AfterlifeKarmaMarket` class
- Generate invoices automatically on purchase
- Store invoices in `_hidden/.truth/invoices/`

### Phase 4: Integration Points

**4.1 Lifetime Purchase Invoice**

- Trigger: After `purchase_lifetime()` completes
- Data: Lifetime object, soul_id, karma_cost, timestamp
- Invoice items:
  - Base lifetime cost
  - Tool costs (if custom)
  - Personality costs (if custom)
  - Total karma cost

**4.2 Treasure Purchase Invoice**

- Trigger: After `purchase_treasure()` completes
- Data: Treasure type, treasure_id, soul_id, karma_cost
- Invoice items:
  - Treasure name
  - Treasure type
  - Karma cost
  - Applied to soul record

**4.3 Transaction Summary Invoice**

- Optional: Generate summary invoices for multiple transactions
- Aggregate purchases over time period
- Show karma balance changes

### Phase 5: Testing

**5.1 Unit Tests**

- Test invoice generation with sample transactions
- Verify invoice structure and calculations
- Test edge cases (zero karma, multiple items, etc.)

**5.2 Integration Tests**

- Test with actual KarmaMarket purchases
- Verify invoice files are created
- Check invoice content accuracy

**5.3 Manual Testing**

- Purchase a lifetime → verify invoice generated
- Purchase a treasure → verify invoice generated
- Review invoice PDFs for formatting and accuracy

## File Structure

```
waft/
├── _experiments/
│   └── invoice-generator/          # Cloned React app for analysis
│       ├── src/
│       ├── package.json
│       └── README.md
├── src/waft/
│   ├── karma_market.py             # Add invoice generation methods
│   └── invoice_generator.py        # NEW: Invoice generator class
├── _hidden/.truth/
│   └── invoices/                    # NEW: Generated invoice PDFs
│       └── {transaction_id}.pdf
└── tests/
    └── test_invoice_generator.py   # NEW: Invoice generator tests
```

## Dependencies

**New Python Dependencies:**

- `weasyprint` (if using WeasyPrint) - Already available in codebase
- OR `reportlab` (if using ReportLab) - May need to install

**No new Node.js dependencies needed** (invoice-generator is for analysis only)

## Integration Code Examples

### Example 1: Generate Invoice for Lifetime Purchase

```python
from src.waft.karma_market import KarmaMarket
from pathlib import Path

market = KarmaMarket()
lifetime = market.purchase_lifetime("basic_qa", soul_id="waft_001")

# Generate invoice
invoice_path = market.generate_invoice(
    transaction_type="lifetime_purchase",
    transaction_id=lifetime.lifetime_id,
    soul_id=lifetime.soul_id,
    items=[
        {
            "description": "Basic Q&A Session",
            "quantity": 1,
            "unit_price": 50.0,
            "total": 50.0
        }
    ],
    total_karma=50.0
)
```

### Example 2: Generate Invoice for Treasure Purchase

```python
from src.waft.karma_market import AfterlifeKarmaMarket

afterlife_market = AfterlifeKarmaMarket()
result = afterlife_market.purchase_treasure(
    treasure_type="tools",
    treasure_id="advanced_codebase_search",
    soul_id="waft_001"
)

# Generate invoice
invoice_path = afterlife_market.generate_invoice(
    transaction_type="treasure_purchase",
    transaction_id=result["purchased_at"],
    soul_id=result["soul_id"],
    items=[
        {
            "description": "Advanced Codebase Search Tool",
            "quantity": 1,
            "unit_price": 100.0,
            "total": 100.0
        }
    ],
    total_karma=100.0
)
```

## Success Criteria

1. ✅ Invoice generator installed and tested locally
2. ✅ Core invoice logic extracted and documented
3. ✅ Python invoice generator class created
4. ✅ Integration with KarmaMarket complete
5. ✅ Invoices generated automatically on purchases
6. ✅ Invoice PDFs stored in `_hidden/.truth/invoices/`
7. ✅ Tests passing for invoice generation
8. ✅ Manual testing confirms invoice accuracy

## Risks and Mitigations

**Risk 1**: Invoice-generator uses React-specific libraries (jspdf-react)

- **Mitigation**: Extract logic, not code. Reimplement in Python using WeasyPrint/ReportLab

**Risk 2**: Invoice format may not match React app exactly

- **Mitigation**: Focus on functionality over pixel-perfect matching. Ensure all data is present and calculations are correct.

**Risk 3**: Performance impact of PDF generation

- **Mitigation**: Generate invoices asynchronously or on-demand, not blocking purchase operations.

## Next Steps After Completion

1. Add invoice generation to CLI commands (`waft-market buy --invoice`)
2. Create invoice templates for different transaction types
3. Add invoice history viewing (`waft-market invoices list`)
4. Integrate with TavernKeeper for invoice tracking
5. Add email/Slack notification with invoice attachments (future)

## References

- Invoice Generator Repo: https://github.com/johnuberbacher/invoice-generator.git
- KarmaMarket Code: `src/waft/karma_market.py`
- PDF Generation Systems: `docs/PDF_LIBRARY_COMPARISON.md`
- WeasyPrint Docs: Already used in `src/waft/document_builder.py`