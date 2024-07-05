# streamlit run file_name.py
# streamlit run test.py

''' st.title(): This function allows you to add the title of the app. 
st.header(): This function is used to set header of a section. 
st.markdown(): This function is used to set a markdown of a section. 
st.subheader(): This function is used to set sub-header of a section. 
st.caption(): This function is used to write caption. 
st.code(): This function is used to set a code.
st.write(): This function is used to write text.'''

# Placeholder for future functionalities (optional)
# You can add more sections here for features like:
#  - Send Money
#  - Request Money
#  - Manage Contacts
#  - View Account Details

import streamlit as st
import pandas as pd
import requests
from passlib.context import CryptContext


# Base URL of the FastAPI backend
BASE_URL = "http://localhost:8000"


# Function to authenticate user and get token
def authenticate_user(username, password):

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash(password)

    response = requests.post(
        f"{BASE_URL}/token",
        data={"username": username, "password": hashed_password},
    )

    response = requests.post(f"{BASE_URL}/token", data={"username": username, "password": password})
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        st.error("Invalid username or password")
        return None

# Function to get current user info
def get_current_user(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/user", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Could not fetch user info")
        return None

# Function to get balance and transactions
def get_balance(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/balance", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Could not fetch balance")
        return None


# Streamlit UI 
st.title('Digital Wallet')

st.subheader("Login")
username = st.text_input("Username")
password = st.text_input("Password", type="password")
login_button = st.button("Login")


if login_button:
    token = authenticate_user(username, password)
    if token:
        st.session_state["token"] = token
        st.success("Logged in successfully")


# Fetch and display user info if logged in
if "token" in st.session_state:
    st.subheader("My Digital Wallet")

    user_info = get_current_user(st.session_state["token"])
    if user_info:
        st.subheader(f"Welcome, {user_info['full_name']}")
        st.write(f"Email: {user_info['email']}")
        st.write(f"Username: {user_info['username']}")
        st.write(f"Active: {'Yes' if user_info['disabled'] is False else 'No'}")
        
    balance_info = get_balance(st.session_state["token"])
    if balance_info:
        balance = balance_info["balance"]
        transactions = pd.DataFrame(balance_info["transactions"])

        st.subheader(f"Balance: ${balance:.2f}")

        st.header("Recent Transactions")
        st.dataframe(transactions, width=800)

        st.write("**Note:** This is a basic example. Additional functionalities are coming soon!")


