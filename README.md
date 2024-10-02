# Table Data Extractor

This project is a Python script that automates the extraction of data from an HTML table on a specified website. The script uses Selenium for web automation, BeautifulSoup for parsing HTML, and pandas for data manipulation.

## Features
- Logs into a specified website using credentials from a YAML configuration file.
- Navigates through paginated results.
- Extracts data from an HTML table and stores it in a pandas DataFrame.
- Displays the head of the DataFrame on the first page and the current page number on subsequent pages.
- The `munge.ipynb` file processes the extracted CSV data to generate reports of files that exceed a specified similarity threshold or that failed to process on the online website.

## Requirements
- Python 3.x
- `Selenium`
- `pandas`
- `BeautifulSoup4`
- `lxml`

## Installation
1. Clone the repository:

2. Install the required packages:

```bash
    pip install selenium pandas beautifulsoup4 lxml
```

3. Ensure you have the appropriate web driver (e.g., [geckodriver for Firefox](https://github.com/mozilla/geckodriver/releases)) installed and included in your system's PATH.

## Configuration
1. Edit the `credentials.yml` file and ensure that `grabTable.py` is reading it in

## Data Processing with munge.ipynb

After extracting the data into a CSV file, you can use the `munge.ipynb` Jupyter notebook to process the data. This notebook generates reports for files that exceed a specified similarity threshold or that failed to process on the online website.

