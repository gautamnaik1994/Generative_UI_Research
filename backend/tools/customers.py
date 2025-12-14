from typing import Any, Dict, List
from faker import Faker
import faker_commerce
from langchain.tools import tool
import random

DATA_REGISTRY: Dict[str, Any] = {}

fake = Faker()
fake.add_provider(faker_commerce.Provider)

@tool
def get_business_client_profile(client_id: str) -> Dict[str, Any]:
    """
    Get detailed business profile for a corporate client.
    
    Args:
        client_id (str): The unique identifier of the corporate client.
        
    Returns:
        Dict[str, Any]: Business details including tax ID, industry, and size.
    """
    company = fake.company()
    return {
        "client_id": client_id,
        "company_name": company,
        "tax_id": fake.bothify(text='##-#######'),
        "industry": random.choice(["Manufacturing", "Logistics", "Retail", "Healthcare", "technology"]),
        "employee_count": random.choice(["10-50", "51-200", "201-500", "500+"]),
        "hq_address": fake.address(),
        "billing_contact": {
            "name": fake.name(),
            "email": fake.company_email(),
            "phone": fake.phone_number()
        },
        "shipping_addresses": [fake.address() for _ in range(random.randint(1, 3))]
    }

@tool
def check_credit_limit(client_id: str) -> Dict[str, Any]:
    """
    Check credit limit and payment terms for a client.
    
    Args:
        client_id (str): The unique identifier of the corporate client.
        
    Returns:
        Dict[str, Any]: Credit details and payment terms.
    """
    credit_limit = random.choice([10000, 50000, 100000, 500000])
    used = round(random.uniform(0, 0.8) * credit_limit, 2)
    return {
        "client_id": client_id,
        "currency": "USD",
        "total_credit_limit": credit_limit,
        "available_credit": credit_limit - used,
        "outstanding_balance": used,
        "payment_terms": random.choice(["Net 30", "Net 60", "Net 90"]),
        "credit_status": "Good" if used < credit_limit * 0.9 else "Warning"
    }

@tool
def get_active_contracts(client_id: str) -> List[Dict[str, Any]]:
    """
    Get list of active negotiated rate contracts.
    
    Args:
        client_id (str): The unique identifier of the corporate client.
        
    Returns:
        List[Dict[str, Any]]: Active contracts.
    """
    contracts = []
    for _ in range(random.randint(1, 3)):
        contracts.append({
            "contract_id": fake.uuid4(),
            "title": f"Annual Supply Agreement - {random.choice(['2024', '2025'])}",
            "start_date": fake.date_this_year().isoformat(),
            "end_date": fake.date_between(start_date='+1y', end_date='+2y').isoformat(),
            "discount_tier": random.choice(["Tier 1 (5%)", "Tier 2 (10%)", "Platinum (15%)"]),
            "status": "Active"
        })
    return contracts

@tool
def get_account_manager(client_id: str) -> Dict[str, Any]:
    """
    Get contact information for the assigned account manager.
    
    Args:
        client_id (str): The unique identifier of the corporate client.
        
    Returns:
        Dict[str, Any]: Account manager details.
    """
    return {
        "client_id": client_id,
        "manager_name": fake.name(),
        "title": "Senior Account Executive",
        "email": fake.email(),
        "phone": fake.phone_number(),
        "availability": "Mon-Fri 9am-5pm EST"
    }
