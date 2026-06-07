import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="stormsense_ai"
)

cursor = db.cursor()

print("✅ MySQL Connected Successfully")