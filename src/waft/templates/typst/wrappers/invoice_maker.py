"""
invoice-maker Typst Template Wrapper

Generates Typst content for invoice-maker template from transaction data.
Supports vendor invoices, customer invoices, and salary payment records.
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
from decimal import Decimal

from ...core.corporations.economics.transaction import Transaction, TransactionType


def generate_invoice_maker(
    transaction: Transaction,
    sender: Dict[str, Any],
    recipient: Dict[str, Any],
    output_dir: Path,
    language: str = "en",
    invoice_id: Optional[str] = None,
    issue_date: Optional[datetime] = None,
    due_date: Optional[datetime] = None,
    banner_image: Optional[str] = None,
    items: Optional[List[Dict[str, Any]]] = None,
    discounts: Optional[Dict[str, Any]] = None,
    taxes: Optional[Dict[str, Any]] = None,
    footer_text: Optional[str] = None
) -> Path:
    """
    Generate invoice-maker Typst content from transaction data.
    
    Args:
        transaction: Transaction to generate invoice for
        sender: Sender information (name, address, tax_id, etc.)
        recipient: Recipient information (name, address, etc.)
        output_dir: Directory to write Typst file
        language: Language code (en, de) - default: en
        invoice_id: Invoice ID (defaults to transaction_id)
        issue_date: Issue date (defaults to transaction timestamp)
        due_date: Due date (optional)
        banner_image: Path to banner/logo image (optional)
        items: Invoice line items (auto-generated from transaction if not provided)
        discounts: Discount information (optional)
        taxes: Tax information (optional)
        footer_text: Footer text (optional)
        
    Returns:
        Path to generated invoice.typ file
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate invoice ID
    if invoice_id is None:
        invoice_id = transaction.transaction_id
    
    # Generate issue date
    if issue_date is None:
        issue_date = transaction.timestamp
    
    # Generate items if not provided
    if items is None:
        items = _generate_items_from_transaction(transaction)
    
    # Generate Typst content
    invoice_content = _create_invoice_typ(
        language=language,
        invoice_id=invoice_id,
        issue_date=issue_date,
        due_date=due_date,
        sender=sender,
        recipient=recipient,
        items=items,
        discounts=discounts,
        taxes=taxes,
        footer_text=footer_text,
        banner_image=banner_image
    )
    
    # Write invoice file
    invoice_path = output_dir / f"invoice_{invoice_id}.typ"
    invoice_path.write_text(invoice_content, encoding="utf-8")
    
    return invoice_path


def _generate_items_from_transaction(transaction: Transaction) -> List[Dict[str, Any]]:
    """Generate invoice items from transaction."""
    items = []
    
    if transaction.transaction_type == TransactionType.SALARY:
        # Salary payment
        items.append({
            "description": transaction.description or "Salary payment",
            "quantity": 1,
            "unit": "payment",
            "price": float(transaction.amount),
            "vat_rate": 0.0  # Salaries typically don't have VAT
        })
    
    elif transaction.transaction_type == TransactionType.VENDOR_INVOICE:
        # Vendor invoice (expense)
        items.append({
            "description": transaction.description or "Vendor service",
            "quantity": transaction.metadata.get("quantity", 1),
            "unit": transaction.metadata.get("unit", "item"),
            "price": float(transaction.amount),
            "vat_rate": transaction.metadata.get("vat_rate", 0.0)
        })
    
    elif transaction.transaction_type == TransactionType.CUSTOMER_INVOICE:
        # Customer invoice (revenue)
        items.append({
            "description": transaction.description or "Service provided",
            "quantity": transaction.metadata.get("quantity", 1),
            "unit": transaction.metadata.get("unit", "item"),
            "price": float(transaction.amount),
            "vat_rate": transaction.metadata.get("vat_rate", 0.0)
        })
    
    else:
        # Generic transaction
        items.append({
            "description": transaction.description or "Transaction",
            "quantity": 1,
            "unit": "item",
            "price": float(transaction.amount),
            "vat_rate": 0.0
        })
    
    return items


def _create_invoice_typ(
    language: str,
    invoice_id: str,
    issue_date: datetime,
    sender: Dict[str, Any],
    recipient: Dict[str, Any],
    items: List[Dict[str, Any]],
    due_date: Optional[datetime] = None,
    discounts: Optional[Dict[str, Any]] = None,
    taxes: Optional[Dict[str, Any]] = None,
    footer_text: Optional[str] = None,
    banner_image: Optional[str] = None
) -> str:
    """Generate invoice.typ content."""
    
    # Format sender
    sender_str = _format_party(sender, "sender")
    
    # Format recipient
    recipient_str = _format_party(recipient, "recipient")
    
    # Format items
    items_str = _format_items(items)
    
    # Format dates
    issue_date_str = _format_datetime(issue_date)
    due_date_str = _format_datetime(due_date) if due_date else None
    
    # Format banner image
    banner_str = ""
    if banner_image:
        banner_str = f'  banner_image: image("{banner_image}", width: 8em),\n'
    
    # Format discounts
    discounts_str = ""
    if discounts:
        discounts_str = "  discounts: (\n"
        if "percentage_discount" in discounts:
            discounts_str += f'    percentage_discount: {discounts["percentage_discount"]},\n'
        if "fixed_discount" in discounts:
            discounts_str += f'    fixed_discount: {discounts["fixed_discount"]},\n'
        discounts_str += "  ),\n"
    
    # Format taxes
    taxes_str = ""
    if taxes:
        taxes_str = "  taxes: (\n"
        if taxes.get("include_vat", False):
            taxes_str += "    include_vat: true,\n"
        taxes_str += "  ),\n"
    
    # Format footer
    footer_str = ""
    if footer_text:
        footer_str = f'  footer_text: "{_escape_typst(footer_text)}",\n'
    
    # Format due date
    due_date_str_formatted = ""
    if due_date_str:
        due_date_str_formatted = f"  due_date: {due_date_str},\n"
    
    return f"""#import "@preview/invoice-maker:1.1.0": *

#show: invoice.with(
  language: "{language}",
{banner_str}  invoice_id: "{invoice_id}",
  issue_date: {issue_date_str},
{due_date_str_formatted}{sender_str}{recipient_str}  items: (
{items_str}  ),
{discounts_str}{taxes_str}{footer_str})
"""


def _format_party(party: Dict[str, Any], party_name: str) -> str:
    """Format party (sender/recipient) information."""
    name = party.get("name", "")
    address = party.get("address", "")
    tax_id = party.get("tax_id")
    
    result = f"  {party_name}: (\n"
    result += f'    name: "{_escape_typst(name)}",\n'
    result += f'    address: "{_escape_typst(address).replace(chr(10), "\\n")}",\n'
    if tax_id:
        result += f'    tax_id: "{_escape_typst(tax_id)}",\n'
    result += "  ),\n"
    
    return result


def _format_items(items: List[Dict[str, Any]]) -> str:
    """Format invoice items."""
    if not items:
        return "    (description: \"No items\", quantity: 1, price: 0.0),\n"
    
    item_strs = []
    for item in items:
        description = item.get("description", "")
        quantity = item.get("quantity", 1)
        unit = item.get("unit", "")
        price = item.get("price", 0.0)
        vat_rate = item.get("vat_rate", 0.0)
        
        item_str = "    (\n"
        item_str += f'      description: "{_escape_typst(description)}",\n'
        item_str += f"      quantity: {quantity},\n"
        if unit:
            item_str += f'      unit: "{_escape_typst(unit)}",\n'
        item_str += f"      price: {price:.2f},\n"
        if vat_rate > 0:
            item_str += f"      vat_rate: {vat_rate},\n"
        item_str += "    ),\n"
        item_strs.append(item_str)
    
    return "".join(item_strs)


def _format_datetime(dt: datetime) -> str:
    """Format datetime for Typst."""
    return f"datetime(year: {dt.year}, month: {dt.month}, day: {dt.day})"


def _escape_typst(text: str) -> str:
    """Escape special characters for Typst."""
    if not text:
        return ""
    
    # Escape quotes and backslashes
    text = text.replace("\\", "\\\\")
    text = text.replace('"', '\\"')
    
    return text


def generate_invoice_from_transaction(
    transaction: Transaction,
    corporation_name: str,
    corporation_address: str,
    output_dir: Path,
    recipient_name: Optional[str] = None,
    recipient_address: Optional[str] = None
) -> Path:
    """
    Generate invoice from a transaction with default formatting.
    
    Args:
        transaction: Transaction to generate invoice for
        corporation_name: Corporation name (sender)
        corporation_address: Corporation address
        output_dir: Directory to write invoice
        recipient_name: Recipient name (defaults from transaction)
        recipient_address: Recipient address (optional)
        
    Returns:
        Path to generated invoice.typ file
    """
    # Determine sender/recipient based on transaction type
    if transaction.transaction_type == TransactionType.SALARY:
        # Salary payment: corporation pays employee
        sender = {
            "name": corporation_name,
            "address": corporation_address
        }
        recipient = {
            "name": recipient_name or transaction.to_party or "Employee",
            "address": recipient_address or ""
        }
    
    elif transaction.transaction_type == TransactionType.VENDOR_INVOICE:
        # Vendor invoice: vendor bills corporation
        sender = {
            "name": transaction.to_party or "Vendor",
            "address": recipient_address or ""
        }
        recipient = {
            "name": corporation_name,
            "address": corporation_address
        }
    
    elif transaction.transaction_type == TransactionType.CUSTOMER_INVOICE:
        # Customer invoice: corporation bills customer
        sender = {
            "name": corporation_name,
            "address": corporation_address
        }
        recipient = {
            "name": transaction.from_party or "Customer",
            "address": recipient_address or ""
        }
    
    else:
        # Generic: corporation as sender
        sender = {
            "name": corporation_name,
            "address": corporation_address
        }
        recipient = {
            "name": recipient_name or transaction.to_party or "Recipient",
            "address": recipient_address or ""
        }
    
    return generate_invoice_maker(
        transaction=transaction,
        sender=sender,
        recipient=recipient,
        output_dir=output_dir,
        invoice_id=transaction.transaction_id,
        issue_date=transaction.timestamp
    )
