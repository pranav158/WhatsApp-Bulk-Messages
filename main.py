# Packages
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Config
login_time = 20                # Time for login (in seconds)
new_msg_time = 5                # Time for a new message (in seconds)
send_msg_time = 5               # Time for sending a message (in seconds)
country_code = 91               # Set your country code
action_time = 2                 # Set time for button click action

# Function to wait for an element
def wait_for_element(driver, by, value, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )

# Function to send message
def send_message(driver, message):
    actions = ActionChains(driver)
    input_box = wait_for_element(driver, By.CSS_SELECTOR, 'div[contenteditable="true"]', 10)
    
    # Clear any existing text in the input box
    input_box.clear()

    for line in message.split('\n'):
        actions.send_keys(line)
        actions.key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT)
    actions.send_keys(Keys.ENTER)
    actions.perform()
    time.sleep(send_msg_time)

# Function to open a new chat
def open_new_chat(driver, country_code, phone_number):
    link = f'https://web.whatsapp.com/send/?phone={country_code}{phone_number}'
    driver.get(link)
    time.sleep(new_msg_time)

# Create driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Encode Message Text
with open('message.txt', 'r') as file:
    msg = file.read()

# Open browser with default link
link = 'https://web.whatsapp.com'
driver.get(link)
time.sleep(login_time)

# Loop Through Numbers List
with open('numbers.txt', 'r') as file:
    for n in file.readlines():
        num = n.rstrip()
        
        open_new_chat(driver, country_code, num)
        
        # Add a delay after opening a new chat
        time.sleep(new_msg_time)

        send_message(driver, msg)
        time.sleep(send_msg_time)

# Quit the driver
driver.quit()
