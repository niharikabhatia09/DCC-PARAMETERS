import os
import pandas as pd
from sqlalchemy import create_engine

# ---------------------- Configuration ----------------------
# Database connection parameters
db_user = "niharikabhatia"       # Your PostgreSQL username
db_host = "localhost"            # Host (local machine)
db_port = "5432"                 # Default PostgreSQL port
db_name = "npl_data"             # The name of your database

# Directory containing cleaned Excel files
cleaned_excel_dir = "/Users/niharikabhatia/Desktop/npl_excels_cleaned"

# Create the SQLAlchemy database engine (connection)
# This will allow pandas to communicate with your PostgreSQL DB
engine = create_engine(f"postgresql+psycopg2://{db_user}@{db_host}:{db_port}/{db_name}")

# ---------------------- Main Script ----------------------
# Loop through each file in the cleaned Excel directory
for filename in os.listdir(cleaned_excel_dir):
    if filename.endswith(".xlsx"):  # Only process Excel files
        file_path = os.path.join(cleaned_excel_dir, filename)

        # Generate a table name from the filename
        # Replace special characters for valid SQL table names
        table_name = os.path.splitext(filename)[0].lower().replace("-", "_").replace(".", "_")

        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(file_path)

        # Clean up column names: lowercase, remove extra spaces, replace symbols
        df.columns = [col.strip().lower().replace(" ", "_").replace("-", "_") for col in df.columns]

        # Store the DataFrame into the PostgreSQL database as a table
        try:
            df.to_sql(table_name, engine, if_exists="replace", index=False)
            print(f"✅ Stored table: {table_name}")
        except Exception as e:
            print(f"❌ Failed to store table {table_name}: {e}")
