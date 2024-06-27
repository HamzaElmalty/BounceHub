from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from Internet_check import Internet_check
import time
import os
import streamlit as st
import random
import tempfile

def microsoft(file_path):
    # التأكد من أن هناك اتصال بالإنترنت
    while not Internet_check():
        time.sleep(5)

    # إعداد متصفح Chrome
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--log-level=1")
    options.add_argument("--lang=en")  # تعيين لغة المتصفح إلى الإنجليزية
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(service=service, options=options)

    try:
        with open(file_path, "r") as file:
            emails = [line.strip() for line in file if line.strip()]  # قراءة البريد الإلكتروني والتخلص من الأسطر الفارغة

        for email in emails:
            driver.get('https://login.live.com')

            try:
                # الانتظار حتى يصبح إدخال البريد الإلكتروني قابلاً للنقر عليه
                email_input = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "(//input[@id='i0116'])[1]"))
                )
                email_input.clear()
                email_input.send_keys(email, Keys.ENTER)

                try:
                    # الانتظار حتى يظهر عنصر التأكيد للبريد الإلكتروني الصحيح
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#i0118")))
                    os.makedirs("./Result", exist_ok=True)
                    with open("./Result/outlook_valid.txt", "a") as valid:
                        valid.write(email + "\n")
                    st.success(f"Valid Email: {email}")
                except:
                    try:
                        # الانتظار حتى يظهر عنصر الخطأ للبريد الإلكتروني غير الصحيح
                        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#i0116Error")))
                        os.makedirs("./Result", exist_ok=True)
                        with open("./Result/outlook_Invalid.txt", "a") as invalid:
                            invalid.write(email + "\n")
                        st.error(f"Invalid Email: {email}")
                    except:
                        os.makedirs("./Result", exist_ok=True)
                        with open("./Result/outlook_Unknown.txt", "a") as unknown:
                            unknown.write(email + "\n")
                        st.warning(f"Unknown Status: {email}")
            except Exception as e:
                st.error(f"Error processing email {email}: {e}")

            time.sleep(random.randint(1, 3))

    except Exception as e:
        st.error(f"An error occurred: {e}")