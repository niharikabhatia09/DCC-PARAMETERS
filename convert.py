import os
import pdfplumber
import pandas as pd

# Directories
pdf_dir = "/Users/niharikabhatia/Desktop/npl_pdfs"
excel_dir = "/Users/niharikabhatia/Desktop/npl_excels"
os.makedirs(excel_dir, exist_ok=True)

# Function to make column names unique
def make_unique_columns(columns):
    seen = {}
    new_cols = []
    for col in columns:
        if col in seen:
            seen[col] += 1
            new_cols.append(f"{col}_{seen[col]}")
        else:
            seen[col] = 0
            new_cols.append(col)
    return new_cols

# Process all PDF files
for filename in os.listdir(pdf_dir):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(pdf_dir, filename)
        excel_path = os.path.join(excel_dir, f"{os.path.splitext(filename)[0]}.xlsx")

        try:
            with pdfplumber.open(pdf_path) as pdf:
                all_tables = []
                for page in pdf.pages:
                    tables = page.extract_tables()
                    for table in tables:
                        df = pd.DataFrame(table)
                        if df.shape[0] > 1:
                            headers = df.iloc[0].tolist()
                            headers = make_unique_columns(headers)  # Ensure uniqueness
                            df.columns = headers
                            df = df[1:]  # Remove header row
                            all_tables.append(df)

                if all_tables:
                    combined_df = pd.concat(all_tables, ignore_index=True)
                    combined_df.to_excel(excel_path, index=False)
                    print(f"Saved: {excel_path}")
                else:
                    print(f"No structured tables found in: {filename}")

        except Exception as e:
            print(f"Error processing {filename}: {e}")
