import streamlit as st
from pymongo import MongoClient
from urllib.parse import quote_plus
from app import app  # Import your app function
from uuid import getnode as get_mac
from cryptography.fernet import Fernet


# Generate or load the encryption key
def load_or_generate_key():
    try:
        # حاول قراءة المفتاح من ملف إذا كان موجودًا
        with open('.env/key.key', 'rb') as key_file:
            key = key_file.read()
    except FileNotFoundError:
        # إذا لم يتم العثور على الملف، قم بإنشاء مفتاح جديد وحفظه
        key = Fernet.generate_key()
        with open('.env/key.key', 'wb') as key_file:
            key_file.write(key)

    return key

# استخدام المفتاح لإنشاء مثيل Fernet
key = load_or_generate_key()
cipher_suite = Fernet(key)

# قراءة وفك تشفير المتغيرات من الملف
def read_decrypted_data():
    try:
        with open('.env/encrypted_data.txt', 'rb') as file:
            encrypted_username = file.readline().strip()
            encrypted_password = file.readline().strip()
            encrypted_host = file.readline().strip()
            encrypted_client_name = file.readline().strip()
            encrypted_collection_name = file.readline().strip()

        username_mongo = cipher_suite.decrypt(encrypted_username).decode()
        password_mongo = cipher_suite.decrypt(encrypted_password).decode()
        host = cipher_suite.decrypt(encrypted_host).decode()
        client_name = cipher_suite.decrypt(encrypted_client_name).decode()
        collection_name = cipher_suite.decrypt(encrypted_collection_name).decode()

        return username_mongo, password_mongo, host, client_name, collection_name

    except Exception as e:
        print(f"Error reading decrypted data: {e}")
        return None, None, None, None, None


# دالة الاتصال بقاعدة البيانات
def connect_to_mongodb():
    try:
        username_mongo, password_mongo, host, client_name, collection_name = read_decrypted_data()
        
        if username_mongo is None or password_mongo is None or host is None or client_name is None or collection_name is None:
            print("Failed to load decrypted data.")
            return None
        
        username = quote_plus(username_mongo)
        password = quote_plus(password_mongo)
        connection_string = f"mongodb+srv://{username}:{password}@{host}/?retryWrites=true&w=majority"
        
        # إعدادات SSL/TLS لتعطيل التحقق من الشهادات
        client = MongoClient(connection_string, tls=True, tlsAllowInvalidCertificates=True)
        db = client[client_name]
        collection = db[collection_name]
        return collection
    except Exception as e:
        print(f"Error connecting to DataBase: {e}")
        return None


# دالة التحقق من مفتاح التفعيل
def check_activation(key):
    collection = connect_to_mongodb()
    if collection is not None:
        record = collection.find_one({"key": key})
        if record:
            activated_mac = record.get('activated_mac')
            if activated_mac:
                current_mac = get_mac()
                if current_mac == activated_mac:
                    return True
                else:
                    return False
            else:
                collection.update_one({"key": key}, {"$set": {"activated_mac": get_mac()}})
                return True
        else:
            return False
    else:
        return False

# إعداد الصفحة
def page_config():
    page_bg_img = '''
    <style>
    div[data-testid="stForm"] {
    font-family: Verdana;
    padding: 10px;
    border-radius: 30px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    background-color: rgba(0, 0, 0, 0.30) !important;
    backdrop-filter: blur(10px);
    background-color: transparent !important;
    }
    body {
        background-image: url("https://images8.alphacoders.com/135/1351040.png");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        font-family: system-ui;
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
    }
    .stButton > button:hover {
        background-color: white;
        animation: scaleAnimationHover 0.3s ease;
    }
    @keyframes scaleAnimation {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    @keyframes scaleAnimationHover {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    .stHeader {
        display: none;
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

    st.markdown("""
    <div class="center-image">
        <img src="https://i.ibb.co/k1VPtjB/Modern-Typography-Electronic-Logo-2.png" width="200">
    </div>
    """, unsafe_allow_html=True)

st.set_page_config(
    page_title="BounceHub",
    page_icon=":rocket:",
)

# صفحة تسجيل الدخول
def login():
    try:
        page_config()
        collection = connect_to_mongodb()
        if collection is not None:
            with st.form(key='login_form'):
                key_authentication = st.text_input("", placeholder='Please Enter authentication...',
                                                   help="Please enter the activation code for the program you obtained after purchase")
                submit_button = st.form_submit_button(label='Login')
                if submit_button:
                    with st.spinner("In progress..."):
    
                        if check_activation(key_authentication):
                            st.session_state.authenticated = True
                            st.success("The activation key has been successfully entered")
                            st.rerun()
                        else:
                            st.error("Authentication failed. Invalid key or already activated on another device.")
        else:
            st.error("Could not connect to the database.")
    except Exception as e:
        st.error(f"Error during login: {e}")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if st.session_state.authenticated:
    app()
else:
    login()