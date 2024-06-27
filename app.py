import streamlit as st
from streamlit_option_menu import option_menu
from pymongo import MongoClient
from urllib.parse import quote_plus
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import tempfile
import os
from outlook import microsoft
from aol import aol_valider
from mx import mx_records
from yahoo import check_yahoo
from cryptography.fernet import Fernet

# تحميل المفتاح
def load_key():
    with open('.gitignore/key_smtp.key', 'rb') as key_file:
        key = key_file.read()
    return key

key = load_key()
cipher_suite = Fernet(key)

# قراءة وفك تشفير المعلومات
with open('.gitignore/smtp_encrypted_data.txt', 'rb') as file:
    encrypted_sender_email = file.readline().strip()
    encrypted_receiver_email = file.readline().strip()
    encrypted_password = file.readline().strip()

sender_email = cipher_suite.decrypt(encrypted_sender_email).decode()
receiver_email = cipher_suite.decrypt(encrypted_receiver_email).decode()
password = cipher_suite.decrypt(encrypted_password).decode()

def send_email(name, email, message):

    # Create the email content
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Contact Form Submission"

    body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp-mail.outlook.com', 587)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        return "Email sent successfully!"
    except Exception as e:
        return f"Error: {str(e)}"
    




def page_config():
    page_bg_img = '''
    <style>
    div[data-testid="stForm"] {
    font-family: Verdana;
    padding: 10px;
    border-radius: 30px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    background-color: rgba(0, 0, 0, 0.30) !important; /* لون خلفية الشريط بنسبة شفافية 50% */
    backdrop-filter: blur(10px); /* تطبيق تأثير ضبابي على الخلفية */
    background-color: transparent !important; /* جعل الخلفية شفافة */
    }

    
    body {
        background-image: url("https://images8.alphacoders.com/135/1351040.png");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        
    }
    .stApp {
        background: rgba(0, 0, 0, 0.5);
        border-radius: 10px;
        padding: 40px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        color: #ffffff;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
    }
    .option-menu .stButton {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: rgba(255, 255, 255, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 5px;
        margin-right: 10px;
        cursor: pointer;
        padding: 10px 20px;
        transition: background-color 0.3s, color 0.3s;
    }
    .option-menu .stButton:hover {
        background-color: rgba(255, 255, 255, 0.2) !important;
    }
    .stButton > button {
        background-color: #210dbc;
        color: white;
        border: none;
        padding: 12px 50px;
        text-align: center;
        text-decoration: none;
        display: block;
        font-size: 16px;
        margin: 20px auto;
        cursor: pointer;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.4);
        transition: background-color 0.3s, box-shadow 0.3s;
        font-family: Verdana;
    }
    .stButton > button:hover {
        background-color: white;
        animation: scaleAnimationHover 0.3s ease;
    }
    @keyframes scaleAnimation {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
        background-color: rgba(0, 0, 0, 0.0) !important; /* لون خلفية الشريط بنسبة شفافية 50% */
        backdrop-filter: blur(2px); /* تطبيق تأثير ضبابي على الخلفية */
    }
    @keyframes scaleAnimationHover {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    .stHeader {
        display: none;
    }
    [data-testid="stSidebar"] {
    background-color: transparent !important; /* جعل الخلفية شفافة */
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background-color: rgba(0, 0, 0, 0.0) !important; /* لون خلفية الشريط بنسبة شفافية 50% */
        backdrop-filter: blur(2px); /* تطبيق تأثير ضبابي على الخلفية */
    }
    

    .footer-text {
        text-align: center;
        color: #f4f4f4;
        font-size: 14px;
        margin-top: 20px;
        cursor: pointer;
    }
    .footer-text:hover {
        color: #ff6347;
    }
    .center-image {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        padding: 20px 0;
    }
    .center-image img {
        max-width: 100%;
        height: auto;
    }
    .hidden-label .stTextInput > label {
        display: none;
    }
       .custom-text {
       font-family: Verdana;
       font-size: 25px;
       color: #ffff;
       line-height: 1.6;
       background-color: rgba(0, 0, 0, 0.30) !important; /* لون خلفية الشريط بنسبة شفافية 50% */
       backdrop-filter: blur(10px); /* تطبيق تأثير ضبابي على الخلفية */
       background-color: transparent !important; /* جعل الخلفية شفافة */

       
    }
    
    .custom-heading {
        color: #210dbc;
        font-size: 25px;
        font-weight: bold;
        font-family: Verdana;

    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

    hide_header_style = """
    <style>
    .stApp header {
        visibility: hidden;
    }
    </style>
    """
    st.markdown(hide_header_style, unsafe_allow_html=True)
    


def app():

    # Sidebar content using option_menu
    with st.sidebar:
        page_config()
        st.markdown("""
        <div class="center-image">
           <img src="https://i.ibb.co/k1VPtjB/Modern-Typography-Electronic-Logo-2.png" width="250" height="250">
        </div>
        """, unsafe_allow_html=True)
        selected = option_menu(
                menu_title="Main Menu",  # required
                options=["Home","Outlook", "Yahoo", "Aol", "Mx Records","Support"],  # required
                icons=["house-door-fill", "envelope-check-fill","envelope-check-fill","envelope-check-fill","envelope-check-fill","telephone-fill"],  # optional
                menu_icon="cast",  # optional
                default_index=0,  # optional
                 styles={
        "nav-link-selected": {"background-color": "#702d4d"},
        "nav-link": {"font-size": "17px", "text-align": "left", "margin":"0px", "--hover-color": "#210dbc","font-family": "Verdana","font-weight": "bold"},

    }
            )
        
    if selected == "Home":
        
        # تعليمات استخدام البرنامج
         st.markdown("""

    <div class="custom-text">
    <span class="custom-heading">How to Use ScanBox App</span>
    <p></p>
    <p><strong>ScanBox App</strong> allows you to verify the validity of email addresses across various services including Outlook, Yahoo, AOL, and more. Below are the steps and features available:</p>

    <p><strong>Instructions:</strong></p>
    <ul>
        <li><strong>Upload a file:</strong> Click on "Add a list username file" to upload a text file containing email addresses, one per line.</li>
        <li><strong>Scan Emails:</strong> Click "Add Emails" to start the verification process.</li>
        <li><strong>Results Storage:</strong> The results will be saved on your desktop in the following files:
            <ul>
                <li><strong>Valid.txt:</strong> Contains valid email addresses.</li>
                <li><strong>Invalid.txt:</strong> Contains invalid email addresses.</li>
                <li><strong>Unknown_Status.txt:</strong> Contains emails with an unknown status.</li>
            </ul>
        </li>
    </ul>

    <p><strong>Supported Services:</strong></p>
    <ul>
        <li><strong>Outlook</strong></li>
        <li><strong>Yahoo</strong></li>
        <li><strong>AOL</strong></li>
        <li><strong>MX Records</strong></li>
        <li>And many more ISPs to be added soon.</li>
    </ul>

    <p><strong>Future Updates:</strong></p>
    <ul>
        <li>Additional services and verification methods will be included in future updates. Stay tuned for new features and improvements!</li>
    </ul>

    <p><strong>Note:</strong> Ensure you have a stable internet connection to perform the email verification.</p>
    </div>
    """, unsafe_allow_html=True)
   
    elif selected == "Support":
        try:

        
            st.markdown("""
                <h3 style="text-align:center;"><span style="color:#210dbc;font-family:Verdana, Geneva, sans-serif;">Want to talk? <strong>We’re here to help</strong></span></h3>
                            """, unsafe_allow_html=True)
            with st.form(key='login_form'):
            
                name = st.text_input("",placeholder="Name")
                email = st.text_input("",placeholder="Email")
                message = st.text_area("",placeholder="Message",help="If you have any problem with the program, please contact the team. Or if you have any question about the service, we would be happy to respond to you")
                if st.form_submit_button(label='Send'):
                    if name and email and message:
                        response = send_email(name, email, message)
                        st.success(response)
                    else:
                        st.error("Please fill out all fields.")
        except:
            pass
    

    elif selected == "Outlook":
        try:

            with st.form(key='Outlook'):
                st.image('image/outlook.png')
                file_paths = st.file_uploader("Add Outlook email list:", type=["txt"], accept_multiple_files=False, help="Add a txt file that contains all the emails you want to check, and each email should be followed by another email without any commas")
                button = st.form_submit_button('Check')
                if button and file_paths:
                    with st.spinner("Please wait"):
                        try:
                            temp_file_path = None
                            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file_paths.name)[1]) as temp_file:
                                temp_file.write(file_paths.read())
                                temp_file_path = temp_file.name
            
                            microsoft(temp_file_path)
                        except Exception as e:
                            st.error(f"Error checking emails: {e}")

        except:
            pass
    

    elif selected == "Yahoo":
        try:

            with st.form(key='Yahoo'):
                st.image('image/yahoo.svg')
                file_paths = st.file_uploader("Add Yahoo email list:", type=["txt"], accept_multiple_files=False, help="Add a txt file that contains all the emails you want to check, and each email should be followed by another email without any commas")
                button = st.form_submit_button('Check')
                if button and file_paths:
                    with st.spinner("Please wait"):
                        try:
                            temp_file_path = None
                            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file_paths.name)[1]) as temp_file:
                                temp_file.write(file_paths.read())
                                temp_file_path = temp_file.name
            
                            check_yahoo(temp_file_path)
                        except Exception as e:
                            st.error(f"Error checking emails: {e}")
        except:
            pass
    elif selected == "Aol":
        try:
            with st.form(key='AOL'):
                st.image('image/aol.png')
                file_paths = st.file_uploader("Add AOL email list:", type=["txt"], accept_multiple_files=False, help="Add a txt file that contains all the emails you want to check, and each email should be followed by another email without any commas")
                button = st.form_submit_button('Check')
                if button and file_paths:
                    with st.spinner("Please wait"):
                        try:
                            temp_file_path = None
                            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file_paths.name)[1]) as temp_file:
                                temp_file.write(file_paths.read())
                                temp_file_path = temp_file.name
            
                            aol_valider(temp_file_path)
                        except Exception as e:
                            st.error(f"Error checking emails: {e}")

        except:
            pass

    elif selected == "Mx Records":
        try:

            with st.form(key='MX'):
                st.image('image/mx.png')
                file_paths = st.file_uploader("Add email list:", type=["txt"], accept_multiple_files=False, help="Add a txt file that contains all the emails you want to check, and each email should be followed by another email without any commas")
                button = st.form_submit_button('Check')
                if button and file_paths:
                    with st.spinner("Please wait"):
                        try:
                            temp_file_path = None
                            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file_paths.name)[1]) as temp_file:
                                temp_file.write(file_paths.read())
                                temp_file_path = temp_file.name
            
                            mx_records(temp_file_path)
                        except Exception as e:
                            st.error(f"Error checking emails: {e}")
        except:
            pass
