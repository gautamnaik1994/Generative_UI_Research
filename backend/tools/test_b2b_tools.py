import sys
import os

# Add the project root to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from backend.tools.products import get_products, get_product_specifications
from backend.tools.customers import get_business_client_profile, check_credit_limit
from backend.tools.orders import create_purchase_order, get_po_status
from backend.tools.inventory import get_warehouse_stock, check_bulk_availability
from backend.tools.analytics import get_revenue_analytics, get_top_customers_by_volume

def test_tools():
    print("Testing Products...")
    # LangChain tools need invoke or run
    products = get_products.invoke({})
    assert isinstance(products, list)
    assert len(products) > 0
    assert "moq" in products[0]
    print("Products OK. Sample:", products[0]['name'])
    
    specs = get_product_specifications.invoke({"product_id": products[0]['id']})
    assert "specifications" in specs
    print("Specs OK.")

    print("\nTesting Customers...")
    profile = get_business_client_profile.invoke({"client_id": "C123"})
    assert "tax_id" in profile
    print("Customer Profile OK. Industry:", profile['industry'])
    
    credit = check_credit_limit.invoke({"client_id": "C123"})
    assert "total_credit_limit" in credit
    print("Credit Check OK.")

    print("\nTesting Orders...")
    po = create_purchase_order.invoke({"client_id": "C123", "items": [{"product_id": "P1", "quantity": 100}], "po_number": "PO-999"})
    assert po['po_number'] == "PO-999"
    print("PO Creation OK.")
    
    print("\nTesting Inventory...")
    stock = get_warehouse_stock.invoke({"product_id": "P1"})
    assert isinstance(stock, list)
    print("Warehouse Stock OK.")

    print("\nTesting Analytics...")
    revenue = get_revenue_analytics.invoke({"period": "last_quarter", "breakdown": "monthly"})
    assert "total_revenue" in revenue
    print("Revenue Analytics OK. Total:", revenue['total_revenue'])

    customers = get_top_customers_by_volume.invoke({"period": "last_year"})
    assert isinstance(customers, list)
    assert len(customers) > 0
    print("Top Customers OK. Top 1:", customers[0]['company_name'])

    print("\nAll B2B tools, including Analytics, verified successfully!")

if __name__ == "__main__":
    test_tools()
