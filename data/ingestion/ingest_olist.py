import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
import os

# Configuration (In production, use env vars)
DB_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/olist_db")
DATA_DIR = "data/raw" # Path where Olist CSVs would be placed

def ingest_data():
    """Ingests Olist CSV files into PostgreSQL."""
    try:
        engine = create_engine(DB_URL)
        print(f"Connecting to database at {DB_URL}...")
        
        # List of Olist files to ingest
        files = {
            "products": "olist_products_dataset.csv",
            "orders": "olist_orders_dataset.csv",
            "order_items": "olist_order_items_dataset.csv",
            "sellers": "olist_sellers_dataset.csv",
            "customers": "olist_customers_dataset.csv"
        }
        
        for table_name, file_name in files.items():
            file_path = os.path.join(DATA_DIR, file_name)
            if os.path.exists(file_path):
                print(f"Ingesting {file_name} into {table_name}...")
                df = pd.read_csv(file_path)
                df.to_sql(table_name, engine, if_exists='replace', index=False)
            else:
                print(f"Skipping {file_name}: File not found in {DATA_DIR}")
                
        print("Data ingestion complete.")
    except Exception as e:
        print(f"Error during ingestion: {e}")

if __name__ == "__main__":
    ingest_data()
