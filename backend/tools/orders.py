from typing import Any, Dict, List, Optional
from faker import Faker
import faker_commerce
from langchain.tools import tool
import random
from datetime import datetime, timedelta

DATA_REGISTRY: Dict[str, Any] = {}

fake = Faker()
fake.add_provider(faker_commerce.Provider)

@tool
def create_purchase_order(client_id: str, items: List[Dict[str, Any]], po_number: str) -> Dict[str, Any]:
    """
    Create a new Purchase Order (PO) for a business client.
    
    Args:
        client_id (str): The corporate client ID.
        items (List[Dict]): List of items with 'product_id' and 'quantity'.
        po_number (str): The client's internal PO reference number.
        
    Returns:
        Dict[str, Any]: The created order confirmation details.
    """
    order_id = fake.uuid4()
    total_amount = sum([item.get('quantity', 1) * round(random.uniform(10, 1000), 2) for item in items])
    
    return {
        "order_id": order_id,
        "client_id": client_id,
        "po_number": po_number,
        "status": "Submitted",
        "created_at": datetime.now().isoformat(),
        "total_amount": round(total_amount, 2),
        "currency": "USD",
        "items_count": len(items),
        "estimated_delivery": (datetime.now() + timedelta(days=14)).date().isoformat()
    }

@tool
def get_po_status(po_number: str) -> Dict[str, Any]:
    """
    Track the status of a specific Purchase Order.
    
    Args:
        po_number (str): The client's PO reference number.
        
    Returns:
        Dict[str, Any]: Status and tracking details.
    """
    status = random.choice(["Processing", "Manufacturing", "Quality Check", "Shipped", "Delivered"])
    return {
        "po_number": po_number,
        "status": status,
        "updated_at": datetime.now().isoformat(),
        "tracking_number": fake.bothify(text='TRK-#########') if status in ["Shipped", "Delivered"] else None,
        "carrier": "Global Freight Logistics" if status in ["Shipped", "Delivered"] else None
    }

@tool
def get_invoice_details(invoice_id: str) -> Dict[str, Any]:
    """
    Retrieve invoice details for accounting and reconciliation.
    
    Args:
        invoice_id (str): The unique invoice identifier.
        
    Returns:
        Dict[str, Any]: Invoice line items and payment status.
    """
    return {
        "invoice_id": invoice_id,
        "po_number": fake.bothify(text='PO-####-####'),
        "issue_date": (datetime.now() - timedelta(days=random.randint(1, 30))).date().isoformat(),
        "due_date": (datetime.now() + timedelta(days=30)).date().isoformat(),
        "amount_due": round(fake.random_number(digits=4), 2),
        "status": random.choice(["Paid", "Unpaid", "Overdue", "Draft"]),
        "line_items": [
            {"description": fake.ecommerce_name(), "quantity": random.randint(10, 100), "amount": round(fake.random_number(digits=3), 2)}
            for _ in range(3)
        ]
    }

@tool
def list_recurring_orders(client_id: str) -> List[Dict[str, Any]]:
    """
    List active monitoring/replenishment orders for a client.
    
    Args:
        client_id (str): The corporate client ID.
        
    Returns:
        List[Dict[str, Any]]: List of recurring order configurations.
    """
    orders = []
    for _ in range(random.randint(1, 3)):
        orders.append({
            "recurring_id": fake.uuid4(),
            "product_name": fake.ecommerce_name(),
            "frequency": random.choice(["Weekly", "Monthly", "Quarterly"]),
            "quantity": random.choice([100, 500, 1000]),
            "next_shipment": (datetime.now() + timedelta(days=random.randint(5, 20))).date().isoformat(),
            "status": "Active"
        })
    return orders
