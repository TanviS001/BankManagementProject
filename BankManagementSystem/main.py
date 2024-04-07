import streamlit as st
import mysql.connector
from mysql.connector import Error


def create_connection():
    try:
        connection = mysql.connector.connect(
            host="remote",
            user="root",
            password="tanvi@123",
            database="bank_db"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        st.error(f"Error: {e}")
        return None


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        return cursor.lastrowid
    except Error as e:
        st.error(f"Error executing query: {e}")
        return None


def execute_read_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        st.error(f"Error executing query: {e}")
        return None


def create_account():
    st.subheader("Create New Account")
    name = st.text_input("Enter Your Name:")
    balance = st.number_input("Enter Initial Balance:", min_value=0.0)
    if st.button("Create Account"):
        if not name or balance <= 0:
            st.error("Please fill in all fields correctly.")
        else:
            query = f"INSERT INTO accounts (name, balance) VALUES ('{name}', {balance})"
            account_id = execute_query(connection, query)
            if account_id:
                st.success(f"Account created successfully! Your Account ID is {account_id}")
            else:
                st.error("Failed to create account")


def deposit():
    st.subheader("Deposit Money")
    account_id = st.number_input("Enter Your Account ID:")
    amount = st.number_input("Enter Amount to Deposit:", min_value=0.0)
    if st.button("Deposit"):
        if account_id <= 0 or amount <= 0:
            st.error("Please fill in all fields correctly.")
        else:
            query = f"UPDATE accounts SET balance = balance + {amount} WHERE id = {account_id}"
            execute_query(connection, query)
            st.success("Amount deposited successfully!")


def withdraw():
    st.subheader("Withdraw Money")
    account_id = st.number_input("Enter Your Account ID:")
    amount = st.number_input("Enter Amount to Withdraw:", min_value=0.0)
    if st.button("Withdraw"):
        if account_id <= 0 or amount <= 0:
            st.error("Please fill in all fields correctly.")
        else:
            query = f"UPDATE accounts SET balance = balance - {amount} WHERE id = {account_id}"
            execute_query(connection, query)
            st.success("Amount withdrawn successfully!")


def check_balance():
    st.subheader("Check Account Balance")
    account_id = st.number_input("Enter Your Account ID:")
    if st.button("Check Balance"):
        if account_id <= 0:
            st.error("Please enter a valid Account ID.")
        else:
            query = f"SELECT balance FROM accounts WHERE id = {account_id}"
            balance = execute_read_query(connection, query)
            if balance:
                st.success(f"Your balance is: {balance[0][0]}")
            else:
                st.error("Account not found")


connection = create_connection()
if connection is None:
    st.error("Failed to connect to the database.")
    st.stop()

st.title("Bank Management System")

option = st.selectbox("Choose an Action:", ("Create Account", "Deposit", "Withdraw", "Check Balance"))

if option == "Create Account":
    create_account()
elif option == "Deposit":
    deposit()
elif option == "Withdraw":
    withdraw()
elif option == "Check Balance":
    check_balance()
