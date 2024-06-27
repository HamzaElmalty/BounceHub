from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
from Internet_check import Internet_check
import os
import streamlit as st

def mx_records(file_path):
    path_driver = ChromeDriverManager().install()
    user_agent = "Mozilla/5.0 (Macintosh; U; Mac OS X 10_6_1; en-US) AppleWebKit/530.5 (KHTML، مثل Gecko) Chrome/ Safari/530.5"
    options = webdriver.ChromeOptions()
    options.add_argument("--lang=en")  # Set browser language to English
    options.add_argument("--log-level=1")
    options.add_argument(f"user-agent={user_agent}")
    driver = webdriver.Chrome(service=Service(path_driver), options=options)

    # Create Result directory if it doesn't exist
    os.makedirs("./Result", exist_ok=True)

    valid_file_path = "./Result/valid_mx.txt"
    invalid_file_path = "./Result/bad_mx.txt"

    with open(file_path, "r") as file:
        emails = [line.strip() for line in file if line.strip()]

    for email in emails:
        email = email.strip()
        try:
            while not Internet_check():
                time.sleep(5)

            url = "https://www.nslookup.io/mx-lookup/"
            driver.get(url)
            input_email = WebDriverWait(driver, 40).until(
                EC.element_to_be_clickable((By.XPATH, "(//input[@id='inputDomain'])[1]"))
            )
            input_email.click()
            input_email.send_keys(email)
            input_email.send_keys(Keys.ENTER)
            time.sleep(random.randint(1, 3))

            try:
                WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".border-b-2")))
                with open(valid_file_path, "a") as file:
                    file.write(email + "\n")
                st.success(f'Valid email address: {email}')
            except:
                with open(invalid_file_path, 'a') as file:
                    file.write(email + "\n")
                st.error(f'Invalid Email : {email}')
        except Exception as e:
            print("Error", e)
        finally:
            time.sleep(random.uniform(1, 3))