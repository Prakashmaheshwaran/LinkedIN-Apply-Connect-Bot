import logging, time, random,yaml,csv
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Configuring CSV
with open("joblinks.csv", 'w', newline='') as csvfile:
    pass 

with open("output.csv", 'r') as infile, open("joblinks.csv", 'a', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
                
        for row in reader:
            if len(row) > 1:  
                writer.writerow([row[1]])

# Configure logging
dt: str = datetime.strftime(datetime.now(), "%m_%d_%y %H_%M_%S ")
logging.basicConfig(filename='./logs/' + str(dt) + '--job_connect.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('selenium_script')

href_links = []

def read_config_file(file_path="config.yaml"):
    try:
        with open(file_path, 'r') as stream:
            parameters = yaml.safe_load(stream)

        # Provide default values for missing keys
        default_config = {
            'username': None,
            'password': None,
        }

        # Update the default config with the loaded parameters
        config_data = {**default_config, **parameters}

        assert config_data['username'] is not None
        assert config_data['password'] is not None

        return config_data
    except yaml.YAMLError as exc:
        raise exc

# Function to add a delay
def custom_delay(delay_lvl):
    if delay_lvl == 'A':
        x: int=random.uniform(2, 3)
        time.sleep(x)
    elif delay_lvl == 'B':
        x: int=random.uniform(4, 6)
        time.sleep(x)
    elif delay_lvl == 'C':
        x: int=random.uniform(20, 30)
        time.sleep(x)
    else:
        time.sleep(120)

# Function to log messages
def custom_log(message, log_level=logging.INFO):
    if log_level == logging.INFO:
        logger.info(message)
    elif log_level == logging.ERROR:
        logger.error(message)
    elif log_level == logging.WARNING:
        logger.warning(message)
    elif log_level == logging.DEBUG:
        logger.debug(message)
    else:
        logger.info(message)  

# Function to start WebDriver
def start_webdriver():
    options = Options()
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.9999.0 Safari/537.36")
    options.add_argument("--start-maximized")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-extensions")

    # Disable webdriver flags or you will be easily detectable
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")

    service = Service(ChromeDriverManager().install())
    service.hide_command_prompt_window = True
    driver = webdriver.Chrome(service=service, options=options)
    custom_log("Chrome WebDriver initialized successfully.")
    return driver

def get_job_links():
    link_file = 'joblinks.CSV'

    with open(link_file, 'r') as file:
        csv_reader = csv.reader(file)
        job_links = []
        for row in csv_reader:
            link = "https://www.linkedin.com/jobs/view/" + str(row[0])
            print(link)
            job_links.append(link)

    return job_links


def open_and_login(driver):
    driver = driver
    driver.get('https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin')
    custom_log("Navigated to LinkedIn website.")
    config_data = read_config_file("config.yaml")
    username = config_data['username']
    password = config_data['password']
    user_field = driver.find_element(By.ID,"username")
    pw_field = driver.find_element(By.ID,"password")
    login_button = driver.find_element(By.XPATH,'//*[@id="organic-div"]/form/div[3]/button')
    user_field.send_keys(username)
    user_field.send_keys(Keys.TAB)
    time.sleep(1)
    pw_field.send_keys(password)
    time.sleep(1)
    login_button.click()
    custom_delay('C')

def collect_links(driver):
    # Change this link based on your search, bcaz this code doesnt have auto customisation
    link_start = "https://www.linkedin.com/search/results/people/?geoUrn=%5B%22100811329%22%2C%22105214831%22%2C%22101436253%22%2C%22115702354%22%5D&industry=%5B%2211%22%2C%2296%22%2C%22137%22%5D&keywords=recruiter&origin=FACETED_SEARCH&page="
    link_end = "&sid=P%3As"
    for i in range (10,100):
        link = link_start + str(i) + link_end
        driver.get(link)
        anchor_elements = driver.find_elements(By.CSS_SELECTOR,".reusable-search__entity-result-list.list-style-none .app-aware-link.scale-down")
        for element in anchor_elements:
            href_links.append(element.get_attribute('href'))
        custom_delay('A')

def connect_and_message(driver,link,content):
    print(link)
    driver.get(link)
    time.sleep(3)
    wait = WebDriverWait(driver, 5)

    # job_poster = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[2]/div/div[2]/div[2]/a/span"))) 
    # print(job_poster)
    # job_poster.click()
    # time.sleep(2)

    more_button = driver.find_element(By.XPATH,'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/div[2]/button')
    more_button.click()
    custom_delay('A')

    connect_button = driver.find_element("xpath",'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/div[2]/div/div/ul/li[3]/div')
    connect_button.click()
    custom_delay('A')

    add_note_button = driver.find_element(By.XPATH,'/html/body/div[3]/div/div/div[3]/button[1]')
    add_note_button.click()
    custom_delay('A')

    text_area = driver.find_element(By.XPATH,'/html/body/div[3]/div/div/div[2]/div/textarea')
    text_area.send_keys(content)
    custom_delay('A')

    send_button = driver.find_element(By.XPATH,'/html/body/div[3]/div/div/div[3]/button[2]')
    send_button.click()
    custom_delay('A')


msg_content = """I\'ve admired your achievements in Information Technology and would like to connect on LinkedIn. Your expertise is inspiring, and I believe your guidance could benefit my IT career. I'd appreciate your connection and any insights you're willing to share."""

driver = start_webdriver()
open_and_login(driver)
# job_links = get_job_links()
collect_links(driver)
print(href_links)
for i in href_links:
    try:
        connect_and_message(driver,i,msg_content)
    except Exception as e:
        print(e)
        continue