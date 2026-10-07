"""
Benchmark Data Generator for Proof-Carrying Data Analyst (PCDA).
Generates realistic, messy multi-table data embedded with traps:
- Duplicate transaction rows
- Mixed currencies ($ / EUR / GBP)
- Ambiguous date notations
- Missing data & null rates
- Table contradictions (Regional Summary vs Line-item sales)
- Discontinued products (trick questions)
"""

import os
import json
import pandas as pd
import numpy as np

def generate_datasets(output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Product Catalog
    products_data = [
        {"product_id": "PROD-101", "product_name": "Cloud Storage 1TB", "category": "Cloud", "status": "active", "discontinued_date": None, "base_cost_usd": 40.0},
        {"product_id": "PROD-102", "product_name": "AI Inference Engine", "category": "AI", "status": "active", "discontinued_date": None, "base_cost_usd": 150.0},
        {"product_id": "PROD-103", "product_name": "Enterprise Security Gateway", "category": "Security", "status": "active", "discontinued_date": None, "base_cost_usd": 320.0},
        {"product_id": "PROD-104", "product_name": "Legacy Dial-up Connector", "category": "Hardware", "status": "discontinued", "discontinued_date": "2021-12-31", "base_cost_usd": 15.0},
        {"product_id": "PROD-105", "product_name": "Quantum Simulator V1", "category": "AI", "status": "discontinued", "discontinued_date": "2022-06-30", "base_cost_usd": 500.0},
        {"product_id": "PROD-106", "product_name": "Edge Analytics Sensor", "category": "IoT", "status": "active", "discontinued_date": None, "base_cost_usd": 75.0},
    ]
    df_products = pd.DataFrame(products_data)
    df_products.to_csv(os.path.join(output_dir, "product_catalog.csv"), index=False)
    
    # 2. Exchange Rates
    exchange_rates_data = [
        {"currency": "USD", "rate_to_usd": 1.00, "effective_year": 2023},
        {"currency": "EUR", "rate_to_usd": 1.08, "effective_year": 2023},
        {"currency": "GBP", "rate_to_usd": 1.27, "effective_year": 2023},
        {"currency": "JPY", "rate_to_usd": 0.0067, "effective_year": 2023},
    ]
    df_rates = pd.DataFrame(exchange_rates_data)
    df_rates.to_csv(os.path.join(output_dir, "exchange_rates.csv"), index=False)
    
    # 3. Sales Transactions (Messy with duplicates, mixed currency strings, ambiguous dates)
    transactions_data = [
        # Clean transactions
        {"tx_id": "TX-1001", "date": "2023-01-15", "customer_id": "CUST-01", "product_id": "PROD-101", "quantity": 10, "unit_price": 100.0, "currency": "USD", "discount_pct": 0.05, "region": "North America"},
        {"tx_id": "TX-1002", "date": "2023-02-20", "customer_id": "CUST-02", "product_id": "PROD-102", "quantity": 5, "unit_price": 300.0, "currency": "USD", "discount_pct": 0.10, "region": "North America"},
        {"tx_id": "TX-1003", "date": "2023-03-10", "customer_id": "CUST-03", "product_id": "PROD-103", "quantity": 2, "unit_price": 600.0, "currency": "EUR", "discount_pct": 0.00, "region": "Europe"},
        
        # Duplicate row trap (TX-1004 appears twice identically due to webhook retry)
        {"tx_id": "TX-1004", "date": "2023-04-05", "customer_id": "CUST-01", "product_id": "PROD-102", "quantity": 4, "unit_price": 300.0, "currency": "USD", "discount_pct": 0.00, "region": "North America"},
        {"tx_id": "TX-1004", "date": "2023-04-05", "customer_id": "CUST-01", "product_id": "PROD-102", "quantity": 4, "unit_price": 300.0, "currency": "USD", "discount_pct": 0.00, "region": "North America"},
        
        # Another duplicate with slightly different metadata (duplicate order ID)
        {"tx_id": "TX-1005", "date": "2023-05-12", "customer_id": "CUST-04", "product_id": "PROD-106", "quantity": 20, "unit_price": 120.0, "currency": "GBP", "discount_pct": 0.05, "region": "Europe"},
        
        # Ambiguous date trap (06/07/2023 could be June 7 or July 6)
        {"tx_id": "TX-1006", "date": "06/07/2023", "customer_id": "CUST-05", "product_id": "PROD-101", "quantity": 15, "unit_price": 100.0, "currency": "USD", "discount_pct": None, "region": "North America"},
        
        # Currency trap with mixed currency notation / missing currency
        {"tx_id": "TX-1007", "date": "2023-08-19", "customer_id": "CUST-06", "product_id": "PROD-103", "quantity": 3, "unit_price": 650.0, "currency": "EUR", "discount_pct": 0.10, "region": "Europe"},
        {"tx_id": "TX-1008", "date": "2023-09-01", "customer_id": "CUST-02", "product_id": "PROD-106", "quantity": 8, "unit_price": 125.0, "currency": "USD", "discount_pct": 0.00, "region": "North America"},
        
        # APAC region transaction
        {"tx_id": "TX-1009", "date": "2023-10-14", "customer_id": "CUST-07", "product_id": "PROD-101", "quantity": 50, "unit_price": 95.0, "currency": "USD", "discount_pct": 0.15, "region": "APAC"},
        
        # Transaction with missing quantity or missing customer
        {"tx_id": "TX-1010", "date": "2023-11-20", "customer_id": None, "product_id": "PROD-102", "quantity": 1, "unit_price": 300.0, "currency": "USD", "discount_pct": 0.00, "region": "North America"},
        
        # Discontinued product transaction attempt (should not happen in 2023, but if it did it's a test case)
        {"tx_id": "TX-1011", "date": "2021-05-10", "customer_id": "CUST-03", "product_id": "PROD-104", "quantity": 10, "unit_price": 25.0, "currency": "USD", "discount_pct": 0.00, "region": "North America"},
    ]
    df_tx = pd.DataFrame(transactions_data)
    df_tx.to_csv(os.path.join(output_dir, "sales_transactions.csv"), index=False)
    
    # 4. Regional Summaries (Directly contains contradictions with line item sales!)
    regional_data = [
        {"region": "North America", "fiscal_year": 2023, "reported_revenue_usd": 6800.0, "audited": True, "notes": "Audited by KPMG"},
        {"region": "Europe", "fiscal_year": 2023, "reported_revenue_usd": 5120.0, "audited": True, "notes": "Audited by EY"},
        {"region": "APAC", "fiscal_year": 2023, "reported_revenue_usd": 2500000.0, "audited": False, "notes": "UNAUDITED CONFLICT: Flash estimates from regional sales lead"},
    ]
    df_reg = pd.DataFrame(regional_data)
    df_reg.to_csv(os.path.join(output_dir, "regional_summaries.csv"), index=False)
    
    # 5. Customers CRM JSON
    crm_data = [
        {"customer_id": "CUST-01", "name": "Acme Corp", "tier": "Enterprise", "country": "USA", "credit_limit": 50000},
        {"customer_id": "CUST-02", "name": "GlobalTech", "tier": "Mid-Market", "country": "Canada", "credit_limit": 20000},
        {"customer_id": "CUST-03", "name": "EuroSystems", "tier": "Enterprise", "country": "Germany", "credit_limit": 45000},
        {"customer_id": "CUST-04", "name": "London Dynamics", "tier": "SMB", "country": "UK", "credit_limit": 10000},
        {"customer_id": "CUST-05", "name": "Vanguard Labs", "tier": "Mid-Market", "country": "USA", "credit_limit": 25000},
        {"customer_id": "CUST-06", "name": "Parisian Analytics", "tier": "Enterprise", "country": "France", "credit_limit": 35000},
        {"customer_id": "CUST-07", "name": "Tokyo AI Ltd", "tier": "Enterprise", "country": "Japan", "credit_limit": 60000},
    ]
    with open(os.path.join(output_dir, "customers_crm.json"), "w", encoding="utf-8") as f:
        json.dump(crm_data, f, indent=2)

    print(f"Benchmark datasets successfully generated at {output_dir}")

if __name__ == "__main__":
    generate_datasets(os.path.dirname(__file__))
