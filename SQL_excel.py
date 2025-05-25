import pandas as pd
from sqlalchemy import create_engine

# Database connection settings
DB_NAME = "4pl_data"
DB_USER = "postgres"
DB_PASSWORD = "Tissa11!!"
DB_HOST = "localhost"
DB_PORT = "5432"

# Create SQLAlchemy engine
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

# Load Excel file
excel_path = r"C:\Users\pokey\Downloads\20240626 - Customer Hit List (3).xlsx"
df = pd.read_excel(excel_path)

# Upload to PostgreSQL
df.to_sql("customers", engine, if_exists='replace', index=False)

print("Data uploaded to PostgreSQL!")
