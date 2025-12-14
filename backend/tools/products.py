from typing import Any, Dict, List, Optional
from faker import Faker
import faker_commerce
from langchain.tools import tool
import random

DATA_REGISTRY: Dict[str, Any] = {}


fake = Faker()
fake.add_provider(faker_commerce.Provider)

sample_product_description = [
    "Industrial grade component designed for high-load applications.",
    "bulk raw material suitable for manufacturing and processing.",
    "High-efficiency unit optimized for commercial operations.",
    "Certified safety equipment meeting international IOS-9001 standards.",
    "Heavy-duty machinery part with 5-year commercial warranty.",
    "Wholesale package of premium grade materials.",
    "Enterprise server rack mount unit with redundant power supply.",
    "Construction grade cement mixture for large scale projects.",
    "Fleet maintenance supply kit for commercial vehicles.",
    "Commercial kitchen appliance for high-volume food service.",
]

sample_specs = {
    "Material": ["Stainless Steel 304", "Carbon Fiber", "Industrial Plastic", "Aluminum Alloy"],
    "Weight": ["50kg", "100kg", "500kg", "1 ton"],
    "Dimensions": ["10x10x10m", "2x2x2m", "Standard Pallet Size"],
    "Certification": ["ISO 9001", "CE", "UL", "RoHS"],
    "Power Rating": ["10kW", "50kW", "100kW", "N/A"],
    "Warranty": ["1 Year Commercial", "5 Year Limited", "Lifetime Structural"]
}

@tool
def get_products() -> list[Dict[str, Any]]:
    """
    Get a list of B2B products available for wholesale.

    Returns:
        list[Dict[str, Any]]: A list of product dictionaries with B2B details like MOQ.
    """
    products = []
    for _ in range(10):
        product_name = fake.ecommerce_name()
        product = {
            "id": fake.uuid4(),
            "name": product_name,
            "sku": f"SKU-{fake.bothify(text='??-#####')}",
            "price": round(fake.random_number(digits=3), 2),
            "currency": "USD",
            "description": fake.random.choice(sample_product_description),
            "image_url": "https://placehold.co/300.png",
            "moq": random.choice([10, 50, 100, 500]), # Minimum Order Quantity
            "category": fake.ecommerce_category(),
            "stock_status": random.choice(["In Stock", "Made to Order", "Low Stock"])
        }
        products.append(product)
    return products


@tool
def get_top_n_selling_products(n: int) -> list[Dict[str, Any]]:
    """
    Get the top N selling B2B products based on volume.

    Args:
        n (int): The number of top selling products to retrieve.

    Returns:
        list[Dict[str, Any]]: A list of top N selling product dictionaries.
    """
    products = []
    for _ in range(n):
        product = {
            "id": fake.uuid4(),
            "name": fake.ecommerce_name(),
            "sku": f"SKU-{fake.bothify(text='??-#####')}",
            "price": round(fake.random_number(digits=3), 2),
            "description": fake.random.choice(sample_product_description),
            "image_url": "https://placehold.co/300.png",
            "units_sold": fake.random_number(digits=4), # Higher numbers for B2B
            "moq": random.choice([50, 100, 1000])
        }
        products.append(product)
    # Sort products by units_sold in descending order
    products.sort(key=lambda x: x["units_sold"], reverse=True)
    return products

@tool
def get_product_specifications(product_id: str) -> Dict[str, Any]:
    """
    Get technical specifications for a specific product.
    
    Args:
        product_id (str): The unique identifier of the product.
        
    Returns:
        Dict[str, Any]: Technical specifications including materials, dimensions, etc.
    """
    specs = {k: random.choice(v) for k, v in sample_specs.items()}
    return {
        "product_id": product_id,
        "specifications": specs,
        "datasheet_url": f"https://example.com/datasheets/{product_id}.pdf",
        "compliance_docs": ["Safety Data Sheet (SDS)", "Certificate of Origin"]
    }

@tool
def get_bulk_pricing_tiers(product_id: str) -> List[Dict[str, Any]]:
    """
    Get bulk pricing tiers for volume discounts.
    
    Args:
        product_id (str): The unique identifier of the product.
        
    Returns:
        List[Dict[str, Any]]: List of pricing tiers based on quantity.
    """
    base_price = round(fake.random_number(digits=3), 2)
    return [
        {"min_quantity": 10, "price_per_unit": base_price},
        {"min_quantity": 50, "price_per_unit": round(base_price * 0.95, 2)},
        {"min_quantity": 100, "price_per_unit": round(base_price * 0.90, 2)},
        {"min_quantity": 500, "price_per_unit": round(base_price * 0.85, 2)},
    ]

@tool
def search_wholesale_products(query: str) -> List[Dict[str, Any]]:
    """
    Search for wholesale products by query string.
    
    Args:
        query (str): Search terms (e.g. "steel bolts", "server rack").
        
    Returns:
        List[Dict[str, Any]]: List of matching products.
    """
    # Mock search returning random results related to query concept
    results = []
    for i in range(5):
        results.append({
            "id": fake.uuid4(),
            "name": f"{query} - Model {fake.bothify(text='??#')}",
            "description": f"High quality {query} for industrial use.",
            "price": round(fake.random_number(digits=3), 2),
            "moq": 50
        })
    return results
