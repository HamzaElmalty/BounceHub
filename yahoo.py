from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
import random
from Internet_check import Internet_check
import streamlit as st
import tempfile

def check_yahoo(file_path):
    path_driver = ChromeDriverManager().install()
    user_agent = "Mozilla/5.0 (Macintosh; U; Mac OS X 10_6_1; en-US) AppleWebKit/530.5 (KHTML, مثل Gecko) Chrome/ Safari/530.5"
    options = webdriver.ChromeOptions()
    options.add_argument("--lang=en")  # Set browser language to English
    options.add_argument("--log-level=1")
    options.add_argument(f"user-agent={user_agent}")
    driver = webdriver.Chrome(service=Service(path_driver), options=options)

    with open(file_path, "r") as file:
        emails = [line.strip() for line in file if line.strip()]

    for email in emails:
        email = email.strip()
        try:
            url = "https://login.yahoo.com/"
            driver.get(url)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#login-username")))
            email_input = WebDriverWait(driver, 40).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#login-username"))
            )
            email_input.click()
            email_input.send_keys(email)
            email_input.send_keys(Keys.ENTER)
            time.sleep(random.uniform(1, 3))  # انتظار عشوائي لتحميل الصفحة

            try:
                WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="username-error"]')))
                os.makedirs("./Result", exist_ok=True)
                with open("./Result/yahoo_Invalid.txt", "a") as Invalid:
                    Invalid.write(email + '\n')
                st.error(f'Invalid Email : {email}')

            except:
                try:
                    WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, "//h2[normalize-space()='Uh-oh...']")))
                    os.makedirs("./Result", exist_ok=True)
                    with open("./Result/yahoo_Invalid.txt", "a") as Invalid:
                        Invalid.write(email + '\n')
                    st.error(f'Invalid Email : {email}')

                except:
                    os.makedirs("./Result", exist_ok=True)
                    with open("./Result/yahoo_valid.txt", "a") as valid:
                        valid.write(email + '\n')
                    st.success(f'Valid Email : {email}')

        except Exception as e:
            print(f"Error processing email {email}: {e}")
        finally:
            time.sleep(random.uniform(1, 3))  # انتظار عشوائي بين الطلبات