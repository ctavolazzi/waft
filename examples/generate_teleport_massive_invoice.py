"""
Generate Invoice for Teleport Massive Transaction

Creates a sample invoice using the invoice-maker Typst template.
"""

import sys
import uuid
from decimal import Decimal
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.waft.core.corporations.economics.transaction import (
    create_salary_transaction,
    create_vendor_invoice_transaction,
)
from src.waft.templates.typst.wrappers.invoice_maker import generate_invoice_from_transaction


def main():
    """Generate sample invoices for Teleport Massive."""
    project_path = Path.cwd()
    output_dir = (
        project_path
        / "_realms"
        / "bureaucracy_realm"
        / "corporations"
        / "teleport_massive_20250701"
        / "invoices"
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    print("📄 Generating Teleport Massive Invoices\n")

    # Create a salary transaction
    print("1. Generating salary payment invoice...")
    salary_transaction = create_salary_transaction(
        transaction_id=f"salary_{uuid.uuid4().hex[:8]}",
        employee_id="employee_001",
        amount=Decimal("8000.00"),  # Monthly salary
        period="monthly",
        description="Monthly salary payment - January 2026",
    )

    salary_invoice_path = generate_invoice_from_transaction(
        transaction=salary_transaction,
        corporation_name="Teleport Massive Corporation",
        corporation_address="123 Quantum Drive\nSan Francisco, CA 94105\nUnited States",
        output_dir=output_dir,
        recipient_name="Dr. Elena Voss",
        recipient_address="456 Research Avenue\nSan Francisco, CA 94105",
    )

    print(f"   ✓ Salary invoice: {salary_invoice_path}")

    # Create a vendor invoice (expense)
    print("\n2. Generating vendor invoice (expense)...")
    vendor_transaction = create_vendor_invoice_transaction(
        transaction_id=f"vendor_{uuid.uuid4().hex[:8]}",
        vendor_name="Quantum Equipment Supply Co.",
        amount=Decimal("45000.00"),
        description="Quantum entanglement measurement equipment",
        expense_account="equipment",
    )

    vendor_invoice_path = generate_invoice_from_transaction(
        transaction=vendor_transaction,
        corporation_name="Teleport Massive Corporation",
        corporation_address="123 Quantum Drive\nSan Francisco, CA 94105\nUnited States",
        output_dir=output_dir,
        recipient_name="Teleport Massive Corporation",
        recipient_address="123 Quantum Drive\nSan Francisco, CA 94105",
    )

    print(f"   ✓ Vendor invoice: {vendor_invoice_path}")

    # Compile invoices to PDF
    print("\n3. Compiling invoices to PDF...")
    try:
        import subprocess

        from src.waft.templates.typst.compiler import TypstCompiler

        compiler = TypstCompiler()

        try:
            salary_pdf = compiler.compile(salary_invoice_path)
            print(f"   ✓ Salary PDF: {salary_pdf}")
        except Exception as e:
            print(f"   ⚠️  Salary PDF compilation failed: {e}")
            print(f"   💡 Try manually: typst compile {salary_invoice_path}")

        try:
            vendor_pdf = compiler.compile(vendor_invoice_path)
            print(f"   ✓ Vendor PDF: {vendor_pdf}")
        except Exception as e:
            print(f"   ⚠️  Vendor PDF compilation failed: {e}")
            print(f"   💡 Try manually: typst compile {vendor_invoice_path}")
    except ImportError as e:
        print(f"   ⚠️  TypstCompiler not available: {e}")
        print("   💡 You can compile manually:")
        print(f"      typst compile {salary_invoice_path}")
        print(f"      typst compile {vendor_invoice_path}")

    print("\n✅ Invoice generation complete!")
    print(f"\n📁 Output directory: {output_dir}")


if __name__ == "__main__":
    main()
