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
def get_revenue_analytics(period: str, breakdown: str) -> Dict[str, Any]:
    """
    Get revenue analytics over a specific period.
    
    Args:
        period (str): Time period (e.g., 'last_30_days', 'last_quarter', 'ytd').
        breakdown (str): How to break down the data (e.g., 'by_product', 'by_region', 'by_category').
        
    Returns:
        Dict[str, Any]: Revenue data points and summary.
    """
    days_map = {'last_30_days': 30, 'last_quarter': 90, 'ytd': 180}
    days = days_map.get(period, 30)
    
    data_points = []
    current_date = datetime.now()
    
    total_revenue = 0.0
    
    if breakdown == 'by_category':
        categories = ["Industrial", "Electronics", "Automotive", "Construction"]
        for cat in categories:
            rev = round(random.uniform(10000, 500000), 2)
            total_revenue += rev
            data_points.append({"label": cat, "revenue": rev})
    else:
        # Default trends over time
        for i in range(days // 7): # Weekly data points
            date_label = (current_date - timedelta(weeks=i)).date().isoformat()
            rev = round(random.uniform(5000, 20000), 2)
            total_revenue += rev
            data_points.append({"date": date_label, "revenue": rev})
            
    return {
        "period": period,
        "breakdown": breakdown,
        "total_revenue": round(total_revenue, 2),
        "currency": "USD",
        "growth_rate_vs_prev_period": f"{random.choice(['+', '-'])}{random.randint(1, 15)}%",
        "data": data_points
    }

@tool
def get_top_customers_by_volume(period: str) -> List[Dict[str, Any]]:
    """
    Identify key B2B accounts by order volume.
    
    Args:
        period (str): Time period (e.g., 'last_month', 'last_year').
        
    Returns:
        List[Dict[str, Any]]: List of top customers and their spend.
    """
    customers = []
    for i in range(5):
        customers.append({
            "rank": i + 1,
            "company_name": fake.company(),
            "client_id": fake.uuid4(),
            "total_spend": round(random.uniform(50000, 1000000), 2),
            "total_orders": random.randint(10, 200),
            "primary_industry": random.choice(["Retail", "Manufacturing", "Tech"])
        })
    return customers

@tool
def get_inventory_turnover_rate(product_id: str) -> Dict[str, Any]:
    """
    Calculate inventory turnover rate for supply chain efficiency.
    
    Args:
        product_id (str): The product identifier.
        
    Returns:
        Dict[str, Any]: Turnover metrics.
    """
    turnover_ratio = round(random.uniform(2.0, 12.0), 1)
    avg_days_to_sell = round(365 / turnover_ratio, 0)
    
    return {
        "product_id": product_id,
        "turnover_ratio": turnover_ratio,
        "avg_days_to_sell": avg_days_to_sell,
        "performance_rating": "High" if turnover_ratio > 8 else "Average" if turnover_ratio > 4 else "Low",
        "holding_cost_estimate": f"${random.randint(100, 1000)}/month"
    }

@tool
def get_sales_forecast(product_id: str, months: int) -> Dict[str, Any]:
    """
    Get AI-based demand prediction for future sales.
    
    Args:
        product_id (str): The product identifier.
        months (int): Number of months to forecast.
        
    Returns:
        Dict[str, Any]: Forecasted demand.
    """
    forecast = []
    current_month = datetime.now()
    
    base_demand = random.randint(100, 1000)
    
    for i in range(months):
        month_label = (current_month + timedelta(days=30 * (i+1))).strftime("%Y-%m")
        predicted = int(base_demand * random.uniform(0.9, 1.2))
        forecast.append({"month": month_label, "predicted_units": predicted})
        
    return {
        "product_id": product_id,
        "forecast_period_months": months,
        "confidence_score": f"{random.randint(80, 99)}%",
        "predicted_trend": random.choice(["Stable", "Increasing", "Seasonal Spike"]),
        "forecast_data": forecast
    }
