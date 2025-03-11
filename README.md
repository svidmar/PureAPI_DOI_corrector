# Elsevier Pure DOI Corrector

## Overview

This script processes a list of UUIDs from an Excel file, fetches research outputs from the **Pure API**, extracts and cleans DOI values, and updates them back to the API. It ensures that DOIs are correctly formatted by removing unwanted prefixes and validating the structure.

## Features

- Fetches research output data using UUIDs.
- Extracts and corrects DOIs from the `electronicVersions` field.
- Ensures DOI validity using regex validation.
- Logs all actions (corrections, updates, errors) to `doi_correction.log`.
- Includes a **progress bar** for better visibility.
- Implements a **rate-limiting delay** to prevent excessive API calls.

## Requirements

### Prerequisites

- Python 3.7+
- Required libraries:
  ```bash
  pip install requests pandas tqdm openpyxl
  ```
- API key with **read and write** access to the Pure API.
- Excel file containing UUIDs with a column named `UUID`.

## Usage

### 1. Modify Configuration

- Set the **API base URL** in `API_BASE_URL`.
- Provide a **valid API key** in `API_KEY`.
- Ensure the **Excel file path** is correct in `pd.read_excel("mylist.xlsx")`.

### 2. Run the Script

```bash
python doicorrector.py
```

### 3. Monitor Progress

- The script will display a **progress bar** while processing.
- Check `doi_correction.log` for detailed logs.

## How It Works

1. Reads the list of UUIDs from the Excel file.
2. Queries the **Pure API** for research output metadata.
3. Extracts and cleans DOIs from `electronicVersions`.
4. Validates DOI format before updating.
5. Sends updated data back to the API (only if changes were made).
6. Waits **1 second** between API requests to prevent throttling.

## DOI Cleaning Rules

- Removes prefixes: `doi:`, `DOI:`, `https://doi.org/`, `DOI `.
- Ensures the DOI matches the **standard format**: `10.xxxx/...`.
- Skips invalid DOI formats and logs a warning.

## Example Log Entries

```log
2025-03-11 14:32:01 - INFO - Corrected DOI for UUID b17aad70-9c2d-11db-8ed6-000ea68e967b: doi:10.4203/ccp.76.56 → 10.4203/ccp.76.56
2025-03-11 14:32:02 - INFO - Successfully updated UUID b17aad70-9c2d-11db-8ed6-000ea68e967b
2025-03-11 14:32:05 - WARNING - Invalid DOI format detected: 10.xxx/invalid_doi
2025-03-11 14:32:07 - ERROR - Failed to fetch UUID abc123: 404 Not Found
```

## Customization

- **Change the delay:** Modify `time.sleep(1)` if the API allows faster/slower requests.
- **Add error handling:** Extend error logging for different API failures.
- **Export results:** Modify the script to save changes in an output file.

## License

This script is released under the **MIT License**. Contributions are welcome!

---

