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
def get_warehouse_stock(product_id: str, warehouse_id: str = None) -> List[Dict[str, Any]]:
    """
    Get stock levels across different distribution centers.
    
    Args:
        product_id (str): The product identifier.
        warehouse_id (str, optional): Specific warehouse ID to filter by.
        
    Returns:
        List[Dict[str, Any]]: Stock levels per warehouse.
    """
    warehouses = ["East Coast DC", "West Coast DC", "Midwest Hub", "European Central"]
    stock = []
    
    if warehouse_id:
        target_warehouses = [w for w in warehouses if w == warehouse_id]
        if not target_warehouses:
            target_warehouses = [warehouse_id] # Treat as custom ID
    else:
        target_warehouses = warehouses

    for w in target_warehouses:
        stock.append({
            "warehouse_id": fake.uuid4(),
            "warehouse_name": w,
            "quantity_on_hand": random.choice([0, 100, 500, 2500, 10000]),
            "reserved_quantity": random.randint(0, 50),
            "location": fake.city()
        })
    return stock

@tool
def check_bulk_availability(product_id: str, quantity: int) -> Dict[str, Any]:
    """
    Check if a large quantity is available for immediate shipment.
    
    Args:
        product_id (str): The product identifier.
        quantity (str): The required quantity.
        
    Returns:
        Dict[str, Any]: Availability status and partial fulfillment options.
    """
    available = random.choice([True, False])
    max_available = random.randint(quantity // 2, quantity * 2)
    
    return {
        "product_id": product_id,
        "requested_quantity": quantity,
        "available_immediately": available,
        "total_available_stock": max_available,
        "can_fulfill_partial": max_available > 0,
        "fulfillment_centers": random.randint(1, 3) if available else 0
    }

@tool
def get_lead_time_estimates(product_id: str, quantity: int) -> Dict[str, Any]:
    """
    Estimate manufacturing and shipping lead times for large orders.
    
    Args:
        product_id (str): The product identifier.
        quantity (int): The quantity ordered.
        
    Returns:
        Dict[str, Any]: Estimated days for production and delivery.
    """
    is_large_order = quantity > 1000
    production_days = random.randint(14, 45) if is_large_order else random.randint(1, 7)
    shipping_days = random.randint(3, 10)
    
    return {
        "product_id": product_id,
        "quantity": quantity,
        "production_lead_time_days": production_days,
        "shipping_lead_time_days": shipping_days,
        "estimated_arrival": (datetime.now() + timedelta(days=production_days + shipping_days)).date().isoformat(),
        "expedited_available": random.choice([True, False])
    }

@tool
def get_restocking_schedule(product_id: str) -> List[Dict[str, Any]]:
    """
    Get schedule of incoming shipments from manufacturers.
    
    Args:
        product_id (str): The product identifier.
        
    Returns:
        List[Dict[str, Any]]: List of incoming shipments.
    """
    shipments = []
    for _ in range(random.randint(1, 3)):
        shipments.append({
            "shipment_id": fake.uuid4(),
            "expected_date": (datetime.now() + timedelta(days=random.randint(7, 30))).date().isoformat(),
            "quantity": random.choice([1000, 5000, 10000]),
            "supplier": fake.company(),
            "status": random.choice(["In Transit", "Scheduled", "Customs Clearance"])
        })
    return shipments
