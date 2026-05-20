import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",          # change if needed
        password="1234",  # put your MySQL password
        database="expense_manager"
    )
