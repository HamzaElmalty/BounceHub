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
from bs4 import BeautifulSoup
import os
import streamlit as st
import tempfile

def aol_valider(file_path):
    path_driver = ChromeDriverManager().install()
    user_agent = "Mozilla/5.0 (Macintosh; U; Mac OS X 10_6_1; en-US) AppleWebKit/530.5 (KHTML، مثل Gecko) Chrome/ Safari/530.5"
    options = webdriver.ChromeOptions()
    options.add_argument("--lang=en")  # Set browser language to English
    options.add_argument("--log-level=1")
    options.add_argument(f"user-agent={user_agent}")
    driver = webdriver.Chrome(service=Service(path_driver), options=options)

    # Create Result directory if it doesn't exist
    os.makedirs("./Result", exist_ok=True)

    # File paths for valid and invalid emails
    valid_file_path = "./Result/aol_valid.txt"
    invalid_file_path = "./Result/aol_invalid.txt"

    with open(file_path, "r") as file:
        emails = [line.strip() for line in file if line.strip()]  # قراءة البريد الإلكتروني والتخلص من الأسطر الفارغة

    for email in emails:
        email = email.strip().lower()
        email = email.replace("@aol.com", "")
        try:
            url = "https://login.aol.com/account/create"
            driver.get(url)
            WebDriverWait(driver, 40).until(EC.presence_of_all_elements_located((By.ID, "usernamereg-userId")))
            time.sleep(3)
            input_email = WebDriverWait(driver, 40).until(
                EC.element_to_be_clickable((By.ID, "usernamereg-userId"))
            )
            input_email.click()
            input_email.send_keys(email)
    
            confirmation_email = WebDriverWait(driver, 40).until(
                EC.element_to_be_clickable((By.ID, "usernamereg-password"))
            )
            confirmation_email.click()
            time.sleep(random.randint(1, 5))

            # استخدام BeautifulSoup لتحليل محتوى الصفحة
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            error_message = soup.find('div', class_="oneid-error-message")
            
            if error_message and "An AOL account already exists with this email address" in error_message.get_text():
                # إذا كان النص المطلوب موجودًا في الرسالة
                with open(valid_file_path, "a") as file:
                    file.write(email + "@aol.com" + '\n')
                st.success(f'Valid email address: {email}@aol.com')
            else:
                # إذا لم يكن النص المطلوب موجودًا في الرسالة
                with open(invalid_file_path, 'a') as file:
                    file.write(email + "@aol.com" + '\n')
                st.error(f'Invalid Email: {email}@aol.com')

        except Exception as e:
            st.error(f"An error occurred: {e}")