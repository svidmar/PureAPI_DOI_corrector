import requests
import pandas as pd
import re
import time
import logging
from tqdm import tqdm


# Configure logging
logging.basicConfig(filename='doi_correction.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration
API_BASE_URL = "https://pure123.com/ws/api/research-outputs/" #Replace with URL for Pure instance
API_KEY = "myapikey"  # Replace with Pure API key with read/write permissions
HEADERS = {
    "accept": "application/json",
    "api-key": API_KEY,
    "Content-Type": "application/json"
}

# Load the Excel file with UUIDS to iterate through
df = pd.read_excel("mylist.xlsx") #Replace with file name/loctaion of excel file. Needs a column named 'UUID'

def clean_doi(doi):
    """Removes prefixes like doi:, DOI:, https://doi.org/, dx.doi.org/ and validates DOI format."""
    if pd.isna(doi):
        return None
    
    cleaned_doi = re.sub(r"^(doi:|DOI:|https://doi.org/|dx.doi.org/|DOI\s+)", "", doi, flags=re.IGNORECASE).strip()
    
    # Validate DOI format
    doi_pattern = r"^10\.\d{4,9}/[-._;()/:a-zA-Z0-9]+$"
    if not re.match(doi_pattern, cleaned_doi):
        logging.warning(f"Invalid DOI format detected: {cleaned_doi}")
        return None  # Ignore invalid DOIs
    
    return cleaned_doi

# Progress bar
for index, row in tqdm(df.iterrows(), total=len(df), desc="Processing DOIs"):
    uuid = row["UUID"]
    
    # Fetch data from Pure's API
    response = requests.get(f"{API_BASE_URL}{uuid}", headers=HEADERS)
    
    if response.status_code == 200:
        data = response.json()
        
        if "electronicVersions" in data:
            updated = False
            
            for ev in data["electronicVersions"]:
                if "doi" in ev:
                    old_doi = ev["doi"]
                    corrected_doi = clean_doi(old_doi)
                    
                    if corrected_doi and old_doi != corrected_doi:
                        ev["doi"] = corrected_doi
                        updated = True
                        logging.info(f"Corrected DOI for UUID {uuid}: {old_doi} → {corrected_doi}")
            
            if updated:
                # Update the research output DOI using Pure's API
                update_response = requests.put(f"{API_BASE_URL}{uuid}", headers=HEADERS, json=data)
                
                if update_response.status_code == 200:
                    logging.info(f"Successfully updated UUID {uuid}")
                else:
                    logging.error(f"Failed to update UUID {uuid}: {update_response.text}")
            else:
                logging.info(f"No changes needed for UUID {uuid}")
        else:
            logging.warning(f"No electronicVersions found for UUID {uuid}")
    else:
        logging.error(f"Failed to fetch UUID {uuid}: {response.text}")
    
    # Go easy on the Pure API
    time.sleep(1)

logging.info("Processing complete.")
print("Processing complete. Check doi_correction.log for details.")
