from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import pandas as pd
import time
import csv

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--start-maximized")
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")

service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.linkedin.com/login")
time.sleep(45)  

def connect_with_profile(profile_url):
    try:
        driver.get(profile_url)
        time.sleep(5)  

        name = driver.find_element(By.XPATH, "//h1[contains(@class, 'text-heading-xlarge')]")

        try:
            # Try the primary Connect button
            connect_button = driver.find_element(By.XPATH, "//button[contains(@class, 'artdeco-button--primary') and contains(., 'Connect')]")
            connect_button.click()
            time.sleep(2)  # Wait for any modal/dialog

            # Click 'Add a note' button
            add_note_button = driver.find_element(By.XPATH, "//button[contains(., 'Add a note')]")
            add_note_button.click()
            time.sleep(2)  # Wait for the note area to appear

            # Enter message in the textarea
            message_area = driver.find_element(By.ID, "custom-message")
            message_area.send_keys(f"Hello {name}, Happy New Year! I am MS in artificial intelligent student looking to apply for internship role at your company. Would you be willing to look at my resume or refer me? Thanks!")

            # Click 'Send' button
            send_button = driver.find_element(By.XPATH, "//button[contains(., 'Send')]")
            send_button.click()
            time.sleep(2)  # Wait for the message to be sent

        except (NoSuchElementException, ElementClickInterceptedException):
            # If primary button not found or not clickable, try the dropdown
            try:
                dropdown_button = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'More actions')]")
                dropdown_button.click()
                time.sleep(2)  # Wait for dropdown to open

                connect_button = driver.find_element(By.XPATH, "//div[contains(@aria-label, 'Invite')]//span[contains(text(), 'Connect')]")
                connect_button.click()
                time.sleep(2)

                # Click 'Add a note' button
                add_note_button = driver.find_element(By.XPATH, "//button[contains(., 'Add a note')]")
                add_note_button.click()
                time.sleep(2)  # Wait for the note area to appear

                # Enter message in the textarea
                message_area = driver.find_element(By.ID, "custom-message")
                message_area.send_keys(f"Hello {name}, Happy New Year! I am MS in artificial intelligent student looking to apply for internship role at your company. Would you be willing to look at my resume or refer me? Thanks!")

                # Click 'Send' button
                send_button = driver.find_element(By.XPATH, "//button[contains(., 'Send')]")
                send_button.click()
                time.sleep(2)  # Wait for the message to be sent

            except (NoSuchElementException, ElementClickInterceptedException):
                print(f"No connect option found for {profile_url}")

    except Exception as e:
        print(f"Error processing profile {profile_url}: {e}")

csv_file_path = 'linkedin_profiles.csv'  # Replace with your CSV file path
profiles_df = pd.read_csv(csv_file_path)

for profile_url in profiles_df['Profile URL'].tolist():
    connect_with_profile(profile_url)
    # Remove the URL from the DataFrame and write back to the CSV
    profiles_df = profiles_df[profiles_df['Profile URL'] != profile_url]
    profiles_df.to_csv(csv_file_path, index=False)
    print(f"Processed and removed {profile_url} from the list.")

driver.quit()