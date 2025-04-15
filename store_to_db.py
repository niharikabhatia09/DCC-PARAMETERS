import os
import pandas as pd
from sqlalchemy import create_engine

# ---------------------- Configuration ----------------------
db_user = "niharikabhatia"
db_password = "niharika"   
db_host = "localhost"
db_port = "5432"
db_name = "npl_data"

# Directory where cleaned Excel/CSV files are stored
input_dir = "/Users/niharikabhatia/Desktop/npl_excels_cleaned"

# Create PostgreSQL connection engine using SQLAlchemy
engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")

# ---------------------- Store Cleaned Files ----------------------
for filename in os.listdir(input_dir):
    if filename.endswith(".xlsx") or filename.endswith(".csv"):
        file_path = os.path.join(input_dir, filename)

        # Clean and generate a valid SQL table name
        base_name = os.path.splitext(filename)[0]
        table_name = base_name.lower().replace(" ", "_").replace("-", "_").replace(".", "_")

        try:
            # Load the file into DataFrame
            if filename.endswith(".xlsx"):
                df = pd.read_excel(file_path)
            else:
                df = pd.read_csv(file_path)

            # Drop fully empty rows/columns
            df.dropna(how="all", inplace=True)
            df.dropna(axis=1, how="all", inplace=True)

            # Clean column names
            df.columns = [col.strip().lower().replace(" ", "_").replace("-", "_") for col in df.columns]

            # Fill remaining NaNs with empty string
            df.fillna("", inplace=True)

            # Store the DataFrame into PostgreSQL
            df.to_sql(table_name, engine, if_exists="replace", index=False)
            print(f"✅ Successfully stored table: {table_name}")

        except Exception as e:
            print(f"❌ Error storing {filename}: {e}")
