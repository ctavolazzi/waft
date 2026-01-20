"""
Invoice & Contract Template
============================

Professional business invoice and contract template.
Tests precise tables, legal formatting, signature blocks.

Features:
- Company letterhead
- Invoice itemization with calculations
- Contract terms and conditions
- Legal formatting
- Signature blocks with dates
- Payment terms
- Professional business aesthetic
"""

from pathlib import Path

from jinja2 import Template
from weasyprint import HTML

INVOICE_CONTRACT_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>

    <style>
        @page {
            size: letter;
            margin: 0.75in 1in;

            @bottom-center {
                content: "Page " counter(page) " of " counter(pages);
                font-family: 'Arial', sans-serif;
                font-size: 9pt;
                color: #666;
            }
        }

        body {
            font-family: 'Arial', 'Helvetica', sans-serif;
            font-size: 10pt;
            line-height: 1.4;
            color: #000;
        }

        /* Company Letterhead */
        .letterhead {
            border-bottom: 3px solid {{ accent_color }};
            padding-bottom: 0.15in;
            margin-bottom: 0.3in;
        }

        .company-name {
            font-size: 20pt;
            font-weight: bold;
            color: {{ accent_color }};
            margin-bottom: 0.05in;
        }

        .company-info {
            font-size: 9pt;
            color: #666;
            line-height: 1.3;
        }

        /* Document Header */
        .doc-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 0.3in;
        }

        .doc-type {
            font-size: 18pt;
            font-weight: bold;
            color: {{ accent_color }};
        }

        .doc-number {
            text-align: right;
            font-size: 10pt;
        }

        .doc-number strong {
            display: inline-block;
            width: 0.8in;
        }

        /* Parties Section */
        .parties {
            margin-bottom: 0.3in;
        }

        .party-box {
            border: 1px solid #999;
            padding: 0.15in;
            margin-bottom: 0.15in;
            background: #f9f9f9;
        }

        .party-label {
            font-weight: bold;
            font-size: 9pt;
            text-transform: uppercase;
            color: #666;
            margin-bottom: 0.05in;
        }

        /* Invoice Table */
        table.invoice-table {
            width: 100%;
            border-collapse: collapse;
            margin: 0.2in 0;
            font-size: 10pt;
        }

        table.invoice-table th {
            background: {{ accent_color }};
            color: #fff;
            border: 1px solid #333;
            padding: 0.1in;
            text-align: left;
            font-weight: bold;
        }

        table.invoice-table td {
            border: 1px solid #999;
            padding: 0.08in;
        }

        table.invoice-table tr:nth-child(even) {
            background: #f9f9f9;
        }

        table.invoice-table .number {
            text-align: right;
        }

        table.invoice-table .total-row {
            background: #e6e6e6;
            font-weight: bold;
        }

        /* Totals Section */
        .totals {
            width: 3.5in;
            margin-left: auto;
            margin-top: 0.2in;
        }

        .total-line {
            display: flex;
            justify-content: space-between;
            padding: 0.05in 0;
            border-bottom: 1px solid #ddd;
        }

        .total-line.grand-total {
            border-top: 2px solid #000;
            border-bottom: 3px double #000;
            font-size: 12pt;
            font-weight: bold;
            color: {{ accent_color }};
            padding-top: 0.1in;
            margin-top: 0.1in;
        }

        /* Terms & Conditions */
        .terms {
            margin-top: 0.3in;
            font-size: 9pt;
            line-height: 1.5;
        }

        .terms h3 {
            font-size: 11pt;
            font-weight: bold;
            margin-top: 0.2in;
            margin-bottom: 0.1in;
            color: {{ accent_color }};
        }

        .terms-box {
            border: 1px solid #999;
            background: #fffef8;
            padding: 0.15in;
            margin: 0.15in 0;
        }

        .clause {
            margin-bottom: 0.1in;
        }

        .clause-number {
            font-weight: bold;
            display: inline-block;
            width: 0.4in;
        }

        /* Signature Blocks */
        .signatures {
            margin-top: 0.5in;
            display: flex;
            justify-content: space-between;
            page-break-inside: avoid;
        }

        .signature-block {
            width: 45%;
        }

        .signature-line {
            border-top: 1px solid #000;
            margin-top: 0.5in;
            padding-top: 0.05in;
        }

        .signature-label {
            font-size: 9pt;
            color: #666;
        }

        .signature-name {
            font-weight: bold;
        }

        .signature-date {
            font-size: 9pt;
            color: #666;
            margin-top: 0.1in;
        }

        /* Payment Info Box */
        .payment-info {
            background: #e6f3ff;
            border: 2px solid {{ accent_color }};
            padding: 0.15in;
            margin: 0.2in 0;
        }

        .payment-info h4 {
            margin: 0 0 0.1in 0;
            color: {{ accent_color }};
        }

        /* Emphasis */
        strong {
            font-weight: bold;
        }

        em {
            font-style: italic;
        }

        .highlight {
            background: #ffeb3b;
            padding: 0.02in 0.05in;
        }

        /* Page break */
        .page-break {
            page-break-before: always;
        }
    </style>
</head>
<body>
    <!-- Letterhead -->
    <div class="letterhead">
        <div class="company-name">{{ company_name }}</div>
        <div class="company-info">
            {{ company_address | safe }}<br>
            {% if company_phone %}Phone: {{ company_phone }} | {% endif %}
            {% if company_email %}Email: {{ company_email }}{% endif %}
            {% if company_website %} | {{ company_website }}{% endif %}
        </div>
    </div>

    <!-- Document Header -->
    <div class="doc-header">
        <div class="doc-type">{{ doc_type }}</div>
        <div class="doc-number">
            {% if doc_number %}<div><strong>Number:</strong> {{ doc_number }}</div>{% endif %}
            {% if date %}<div><strong>Date:</strong> {{ date }}</div>{% endif %}
            {% if due_date %}<div><strong>Due Date:</strong> {{ due_date }}</div>{% endif %}
        </div>
    </div>

    <!-- Parties (if contract) -->
    {% if show_parties %}
    <div class="parties">
        <div class="party-box">
            <div class="party-label">{{ party1_label }}</div>
            {{ party1_info | safe }}
        </div>
        <div class="party-box">
            <div class="party-label">{{ party2_label }}</div>
            {{ party2_info | safe }}
        </div>
    </div>
    {% endif %}

    <!-- Main Content -->
    <div class="content">
        {{ content | safe }}
    </div>

    <!-- Signatures (if contract) -->
    {% if show_signatures %}
    <div class="signatures">
        <div class="signature-block">
            <div class="signature-line">
                <div class="signature-label">{{ party1_label }} Signature</div>
                <div class="signature-name">{{ party1_signatory }}</div>
                <div class="signature-date">Date: _______________</div>
            </div>
        </div>
        <div class="signature-block">
            <div class="signature-line">
                <div class="signature-label">{{ party2_label }} Signature</div>
                <div class="signature-name">{{ party2_signatory }}</div>
                <div class="signature-date">Date: _______________</div>
            </div>
        </div>
    </div>
    {% endif %}
</body>
</html>
"""


def generate_invoice_contract(
    content: str,
    output_path: Path,
    title: str = "Invoice",
    doc_type: str = "INVOICE",
    company_name: str = "ACME Corporation",
    company_address: str = "123 Business St, Suite 100, City, ST 12345",
    company_phone: str = None,
    company_email: str = None,
    company_website: str = None,
    doc_number: str = None,
    date: str = None,
    due_date: str = None,
    accent_color: str = "#2c3e50",
    show_parties: bool = False,
    party1_label: str = "SELLER",
    party1_info: str = "",
    party1_signatory: str = "",
    party2_label: str = "BUYER",
    party2_info: str = "",
    party2_signatory: str = "",
    show_signatures: bool = False,
) -> Path:
    """
    Generate a business invoice or contract.

    Args:
        content: Main content (HTML)
        output_path: Where to save PDF
        title: Document title
        doc_type: Type (INVOICE, CONTRACT, etc.)
        company_name: Company name
        company_address: Company address
        company_phone: Phone number
        company_email: Email
        company_website: Website
        doc_number: Document number
        date: Date
        due_date: Due date (for invoices)
        accent_color: Brand color
        show_parties: Show parties section (for contracts)
        party1_label: First party label
        party1_info: First party information (HTML)
        party1_signatory: First party signatory name
        party2_label: Second party label
        party2_info: Second party information (HTML)
        party2_signatory: Second party signatory name
        show_signatures: Show signature blocks

    Returns:
        Path to generated PDF
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    template = Template(INVOICE_CONTRACT_TEMPLATE)
    html_output = template.render(
        title=title,
        content=content,
        doc_type=doc_type,
        company_name=company_name,
        company_address=company_address,
        company_phone=company_phone,
        company_email=company_email,
        company_website=company_website,
        doc_number=doc_number,
        date=date,
        due_date=due_date,
        accent_color=accent_color,
        show_parties=show_parties,
        party1_label=party1_label,
        party1_info=party1_info,
        party1_signatory=party1_signatory,
        party2_label=party2_label,
        party2_info=party2_info,
        party2_signatory=party2_signatory,
        show_signatures=show_signatures,
    )

    HTML(string=html_output).write_pdf(output_path)
    return output_path
