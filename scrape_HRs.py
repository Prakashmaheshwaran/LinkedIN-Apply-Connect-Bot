from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import csv

def scroll_to_bottom(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def write_to_csv(profile_links, mode='a'):
    with open('linkedin_profiles.csv', mode, newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if mode == 'w':
            writer.writerow(['Profile URL'])  
        for link in profile_links:
            writer.writerow([link])

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

base_url = "https://www.linkedin.com/search/results/people/?keywords=ai%20recruiter&origin=SWITCH_SEARCH_VERTICAL"
time.sleep(45)
write_to_csv([], 'w')

for page in range(1, 6):  
    search_url = f"{base_url}&page={page}&sid=5%2C0"
    driver.get(search_url)
    time.sleep(5) 
    
    scroll_to_bottom(driver)  
    links = driver.find_elements(By.XPATH, '//a[contains(@class, "app-aware-link")]')
    page_links = [link.get_attribute('href') for link in links]
    
    write_to_csv(page_links)
    time.sleep(1) 

driver.quit()

file_path = 'linkedin_profiles.csv' 
df = pd.read_csv(file_path)
profile_links = df[df['Profile URL'].str.contains('/in/')]
profile_links = profile_links.drop_duplicates()
cleaned_file_path = 'linkedin_profiles.csv' 
profile_links.to_csv(cleaned_file_path, index=False)
