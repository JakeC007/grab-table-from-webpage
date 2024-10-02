""""
Grab table from HTML page and save to csv file
10/2/2024
J. Chanenson
"""

import yaml
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from bs4 import BeautifulSoup

# Step 1: Load login credentials from the YAML file
with open('credentials.yml', 'r') as file:
    config = yaml.safe_load(file)

username = config['login']['username']
password = config['login']['password']

# Step 2: Set up Selenium with Firefox
driver_path = '/path/to/geckodriver'
driver = webdriver.Firefox(executable_path=driver_path)

# Step 3: Log in to the website using credentials from the YAML file
driver.get('https://example.com/login')  # Replace with the actual URL

# Find and fill login form fields using credentials from the YAML file
username_field = driver.find_element(By.ID, 'username_id')  # Replace with actual ID
password_field = driver.find_element(By.ID, 'password_id')  # Replace with actual ID
login_button = driver.find_element(By.ID, 'login_button_id')  # Replace with actual ID

# Enter the credentials from the YAML file
username_field.send_keys(username)
password_field.send_keys(password)
login_button.click()

# Wait for the page to load
time.sleep(5)

# Step 4: Initialize an empty list to hold all data
all_data = []

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
    
    # Print the current DataFrame to verify (optional)
    print(df.head())
    
    # Step 7: Check for the presence of a "Next" button
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
    
    except:
        # If there's no "Next" button or it cannot be clicked, exit the loop
        break

# Step 8: Combine all the dataframes into one
final_df = pd.concat(all_data, ignore_index=True)

# Step 9: Save the combined DataFrame to a CSV file
final_df.to_csv('extracted_table_data.csv', index=False)

# Optional: Close the browser after the process is complete
driver.quit()

print("Data extraction complete. Saved to 'extracted_table_data.csv'.")
