import sqlite3
import random
import base64
from datetime import datetime, timedelta
from pathlib import Path

# Connect to SQLite database (or create it if it doesn't exist)
base_path = Path.cwd().parent
db_path = r"c:\Users\Indugu Rao\myrepos\google-gemini-agents\database\testdb.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create tables based on the DDL in dataload.sql
ddl = """
CREATE TABLE IF NOT EXISTS campaign_fact (
    event_date TEXT,
    member_number TEXT,
    campaign_product TEXT,
    campaign_cosa TEXT,
    converted_product TEXT,
    converted_cosa TEXT,
    campaign_nm TEXT,
    conversion_channel_nm TEXT,
    quote_start INTEGER,
    quote_COMPLETE INTEGER,
    APP_START INTEGER,
    APP_COMPLETE INTEGER,
    impression_channel TEXT,
    impression_qty INTEGER,
    click_qty INTEGER,
    campaign_funding_source TEXT,
    FOREIGN KEY (member_number) REFERENCES member_dim(member_number),
    FOREIGN KEY (campaign_nm) REFERENCES campaign_dim(campaign_nm)
);

CREATE TABLE IF NOT EXISTS member_dim (
    member_number TEXT, 
    age_group TEXT,
    marital_status TEXT, 
    state TEXT
);

CREATE TABLE IF NOT EXISTS campaign_dim (
    campaign_nm TEXT, 
    campaign_cosa TEXT,
    campaign_product TEXT,
    campaign_funding_source TEXT,
    spent_amt TEXT,
    campaign_start_date TEXT,
    campaign_end_date TEXT
);
"""
cursor.executescript(ddl)

# Generate test data for member_dim
us_states = [
     "California", "Florida", "New Mexico", "Texas"
]
member_dim_data = [
    (
        base64.b64encode(str(random.randint(10000000, 99999999)).encode()).decode(),
        random.choice(["18-24", "25-34", "35-44", "45-54", "55-64", "65+"]),
        random.choice(["Single", "Married", "Divorced", "Widowed"]),
        random.choice(us_states)
    )
    for _ in range(100)
]
cursor.executemany("INSERT INTO member_dim VALUES (?, ?, ?, ?)", member_dim_data)

# Generate test data for campaign_dim
campaign_products = ["Auto Insurance", "Homeowners", "Renters", "Credit Card", "Deposits", "Consumer Loans"]
campaign_cosas = {
    "Auto Insurance": "P&C", "Homeowners": "P&C", "Renters": "P&C",
    "Credit Card": "Bank", "Deposits": "Bank", "Consumer Loans": "Bank"
}
campaign_dim_data = [
    (
        f"{cosa}_{product}_Campaign_{i}",
        cosa,
        product,
        f"{cosa} {product}",
        f"${random.randint(1000, 10000)}",
        (datetime.now() - timedelta(days=random.randint(30, 90))).strftime("%Y-%m-%d"),
        (datetime.now() + timedelta(days=random.randint(30, 90))).strftime("%Y-%m-%d")
    )
    for product, cosa in campaign_cosas.items()
    for i in range(1, 3)
]
cursor.executemany("INSERT INTO campaign_dim VALUES (?, ?, ?, ?, ?, ?, ?)", campaign_dim_data)

# Generate test data for campaign_fact
conversion_channels = ["Internet", "Mobile", "Offline"]
aquisition_activities = ["Quote Start", "Quote Complete", "App Start", "App Complete", "Prod Acq"]
campaign_fact_data = [
    (
        (datetime.now() - timedelta(days=random.randint(0, 90))).strftime("%Y-%m-%d"),
        random.choice(member_dim_data)[0],
        random.choice(campaign_products),
        random.choice(list(campaign_cosas.values())),
        random.choice(campaign_products),
        random.choice(list(campaign_cosas.values())),
        random.choice(campaign_dim_data)[0],
        random.choice(conversion_channels),
        random.randint(40, 49),
        random.randint(30, 39),
        random.randint(20, 29),
        random.randint(10, 19),
        random.choice(["Paid Search", "Paid Display", "Paid Social", "Direct Mail", "Email"]),
        random.randint(81, 200),
        random.randint(60, 80),
        f"{random.choice(list(campaign_cosas.values()))} {random.choice(campaign_products)}"
    )
    for _ in range(2000)
]
cursor.executemany("INSERT INTO campaign_fact VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", campaign_fact_data)

# Commit and close the connection
conn.commit()
conn.close()

print("Test data generated and loaded successfully!")