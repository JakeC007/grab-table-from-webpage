""""
Grab table from HTML page and save to csv file

This script automates the process of logging into a website, navigating through paginated results, 
and extracting data from an HTML table into a pandas DataFrame. The extracted data is then stored 
in a list, and you can modify it to save to a file as needed.

Requirements:
- Selenium
- pandas
- BeautifulSoup4
- lxml

Usage:
1. Ensure you have the required libraries installed:
   pip install selenium pandas beautifulsoup4 lxml

2. Configure your login credentials in the `config.yaml` file in the same directory.

3. Run the script:
   python grabTable.py

4. The script will log into the website, extract table data, and print the current page number 
   while iterating through the pages.

Note:
- Update the table ID and pagination selectors according to the website's structure.

10/2/2024
J. Chanenson
"""

import yaml
from selenium import webdriver
from selenium.webdriver.firefox.service import Service  # Import the Service class
from selenium.webdriver.firefox.options import Options  # Import FirefoxOptions
from selenium.webdriver.common.by import By
import time, os
import pandas as pd
from bs4 import BeautifulSoup

# Step 1: Load login credentials from the YAML file
cred_f = "cred.yml"
with open(cred_f, 'r') as file:
    config = yaml.safe_load(file)

username = config['login']['username']
password = config['login']['password']

print(f"Loaded creds from {cred_f}")

# Step 2: Set up Selenium with Firefox
driver_path = 'geckodriver.exe'

## Because selenium is being fussy 
# Set the path to the Firefox binary
firefox_binary_path = r'C:\Program Files\Mozilla Firefox\firefox.exe'
# Create a Service object with the path to geckodriver
service = Service(executable_path=driver_path)
# Create Firefox options and set the binary location
options = Options()
options.binary_location = firefox_binary_path

# Initialize the WebDriver with the service object and options
driver = webdriver.Firefox(service=service, options=options)


# Step 3: Log in to the website using credentials from the YAML file
driver.get('https://example.com')  

# Find and fill login form fields using credentials from the YAML file
username_field = driver.find_element(By.ID, 'username')  
password_field = driver.find_element(By.ID, 'password') 
login_button = driver.find_element(By.XPATH, '//input[@value="Login"]') 

# Enter the credentials from the YAML file
username_field.send_keys(username)
password_field.send_keys(password)
login_button.click()

# Wait for the page to load
time.sleep(5)

# Step 4: Initialize an empty list to hold all data
all_data = []
page_counter = 1

# Step 5: Pagination loop - keep going while there's a "Next" button
while True:
    # Parse the current page with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Step 6: Extract the table with Pandas using table ID or XPath
    table = soup.find('table', {'id': 'docs'})  # The ID of the table

    # Convert the HTML table into a pandas DataFrame
    df = pd.read_html(str(table))[0]
    
    # Append the DataFrame to the list
    all_data.append(df)
    
    # Step 7: Display Data and Handle Pagination
    if page_counter == 1:
        # On the first page, display the head of the DataFrame
        print(df.head())
    else:
        # For subsequent pages, clear the screen and print the page number
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen (Windows: 'cls', Unix-like: 'clear')
        print(f"Currently on page {page_counter}")
    
    # Step 8: Check for the presence of a "Next" button
    try:
        # Locate the "Next" button and click if it exists
        next_button = driver.find_element(By.LINK_TEXT, 'Next')  # Adjust this if the button has a different text or XPath
        
        # If the "Next" button is disabled or not clickable, break the loop
        if 'disabled' in next_button.get_attribute('class'):
            break
        
        # Click the "Next" button to go to the next page
        next_button.click()
        
        # Wait for the next page to load
        time.sleep(3)

        # Increment the page counter
        page_counter += 1
    
    except:
        # If there's no "Next" button or it cannot be clicked, exit the loop
        break

print(f"Final page grabbed is {page_counter}")

# Step 9: Combine all the dataframes into one
final_df = pd.concat(all_data, ignore_index=True)

# Step 10: Save the combined DataFrame to a CSV file
final_df.to_csv('extracted_table_data.csv', index=False)

# Close the browser after the process is complete
driver.quit()

print("Data extraction complete. Saved to 'extracted_table_data.csv'.")
