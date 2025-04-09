import os
import pandas as pd

# Input folder where original Excel files are stored
input_dir = "/Users/niharikabhatia/Desktop/npl_excels"

# Output folder to save cleaned Excel files
output_dir = "/Users/niharikabhatia/Desktop/npl_excels_cleaned"

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created output folder: {output_dir}")
else:
    print(f"Output folder already exists: {output_dir}")

# Go through each Excel file in the input folder
for filename in os.listdir(input_dir):
    if filename.endswith(".xlsx"):
        file_path = os.path.join(input_dir, filename)
        print(f"\nProcessing: {filename}")

        try:
            # Read the Excel file
            df = pd.read_excel(file_path)

            # ====== BEGIN CLEANING SECTION ======
            # Drop completely empty rows and columns
            df.dropna(how="all", inplace=True)
            df.dropna(axis=1, how="all", inplace=True)

            # Strip whitespace from column names
            df.columns = df.columns.str.strip()

            # Optional: Drop duplicate rows
            df.drop_duplicates(inplace=True)

            # Optional: Fill NaNs with empty string (customizable)
            df.fillna("", inplace=True)
            # ====== END CLEANING SECTION ======

            # Save the cleaned Excel file
            cleaned_file_path = os.path.join(output_dir, filename)
            df.to_excel(cleaned_file_path, index=False)
            print(f"Saved cleaned file to: {cleaned_file_path}")

        except Exception as e:
            print(f"Error processing {filename}: {e}")
