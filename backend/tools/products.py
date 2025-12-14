from typing import Any, Dict
from faker import Faker
import faker_commerce
from langchain.tools import tool


fake = Faker()
fake.add_provider(faker_commerce.Provider)

sample_product_description = [
    "This product is made from high-quality materials and offers exceptional durability.",
    "Experience unparalleled performance with this state-of-the-art gadget.",
    "A perfect blend of style and functionality, designed to meet your everyday needs.",
    "Eco-friendly and sustainable, this product is a great choice for the environmentally conscious consumer.",
    "Compact and lightweight, making it easy to carry and use on the go.",
    "Innovative design that enhances user experience and convenience.",
    "Backed by a comprehensive warranty for your peace of mind.",
    "Highly rated by customers for its reliability and efficiency.",
    "Versatile and adaptable, suitable for a wide range of applications.",
    "Affordable luxury that doesn't compromise on quality.",
    "Ergonomically designed for maximum comfort during use.",
    "Cutting-edge technology that keeps you ahead of the curve.",
    "A must-have accessory for tech enthusiasts and professionals alike.",
    "Stylish and modern, perfect for any contemporary setting.",
    "Engineered for optimal performance in all conditions.",
]


@tool
def get_products() -> list[Dict[str, Any]]:
    """
    Get a list of products.

    Returns:
        list[Dict[str, Any]]: A list of product dictionaries.
    """
    products = []
    for _ in range(10):
        product = {
            "name": fake.ecommerce_name(),
            "price": round(fake.random_number(digits=2), 2),
            "description": fake.random.choice(sample_product_description),
            "image_url": "https://placehold.co/300.png"
        }
        products.append(product)
    return products


@tool
def get_top_n_selling_products(n: int) -> list[Dict[str, Any]]:
    """
    Get the top N selling products.

    Args:
        n (int): The number of top selling products to retrieve.

    Returns:
        list[Dict[str, Any]]: A list of top N selling product dictionaries.
    """
    products = []
    for _ in range(n):
        product = {
            "name": fake.ecommerce_name(),
            "price": round(fake.random_number(digits=2), 2),
            "description": fake.random.choice(sample_product_description),
            "image_url": "https://placehold.co/300.png",
            "units_sold": fake.random_number(digits=3)
        }
        products.append(product)
    # Sort products by units_sold in descending order
    products.sort(key=lambda x: x["units_sold"], reverse=True)
    return products
