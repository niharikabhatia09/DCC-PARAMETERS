import os
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

# ---------------------- Configuration ----------------------
DB_USER = "niharikabhatia"
DB_PASSWORD = ""
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "npl_data"

EXCEL_FOLDER = "/Users/niharikabhatia/Desktop/npl_excels_cleaned"

# ---------------------- Create DB Engine ----------------------
connection_string = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(connection_string)

# ---------------------- Detect Service Type ----------------------
def detect_service_type(filename):
    name = filename.lower()
    if "calibration" in name:
        return "calibration"
    elif "testing" in name:
        return "testing"
    elif "fabrication" in name:
        return "fabrication"
    elif "bnd" in name:
        return "bnd"
    else:
        return "misc"

# ---------------------- Sanitize Table Name ----------------------
def sanitize_table_name(filename):
    name = os.path.splitext(filename)[0]
    return name.lower().replace(" ", "_").replace("-", "_").replace(".", "_")

# ---------------------- Main Function ----------------------
def store_excel_tables():
    if not os.path.exists(EXCEL_FOLDER):
        print(f"❌ Folder not found: {EXCEL_FOLDER}")
        return

    for file in os.listdir(EXCEL_FOLDER):
        if file.endswith(".xlsx"):
            filepath = os.path.join(EXCEL_FOLDER, file)
            try:
                service_type = detect_service_type(file)
                base_name = sanitize_table_name(file)
                table_name = f"{service_type}_{base_name}"

                print(f"\n📂 Processing: {file}")
                df = pd.read_excel(filepath)

                # Clean column names
                df.columns = [col.strip().lower().replace(" ", "_").replace("-", "_") for col in df.columns]

                df.to_sql(table_name, engine, if_exists="replace", index=False)

                print(f"✅ [{datetime.now().strftime('%H:%M:%S')}] Stored as: {table_name}")
            except Exception as e:
                print(f"❌ Failed to process {file}: {e}")

# ---------------------- Run ----------------------
if __name__ == "__main__":
    store_excel_tables()
