import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Step 1: Target URL
url = 'https://www.nplindia.org/index.php/commercial-services/calibration-testing/'

# Step 2: Set up headers for the request
headers = {'User-Agent': 'Mozilla/5.0'}

# Step 3: Request the page content
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# Step 4: Find all PDF links
pdf_links = []
for link in soup.find_all('a', href=True):
    href = link['href']
    if href.endswith('.pdf'):
        full_url = href if href.startswith('http') else f'https://www.nplindia.org{href}'
        pdf_links.append({
            'File Name': os.path.basename(full_url),
            'URL': full_url
        })

# Step 5: Create a folder to save PDFs
os.makedirs('npl_pdfs', exist_ok=True)

# Step 6: Download the PDFs
for pdf in pdf_links:
    file_path = os.path.join('npl_pdfs', pdf['File Name'])
    print(f"⬇️ Downloading: {pdf['File Name']}")
    with open(file_path, 'wb') as f:
        f.write(requests.get(pdf['URL'], headers=headers).content)

# Step 7: Save the PDF info to Excel
df = pd.DataFrame(pdf_links)
df.to_excel('npl_calibration_testing_pdfs.xlsx', index=False)

print("✅ All PDFs downloaded and Excel file created!")
