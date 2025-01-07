import psycopg2
try:
    connection = psycopg2.connect(
        dbname="tourist_guide_db",
        user="postgres",
        password="Sql@1122",
        host="localhost",
        port="5432"
    )
    print("Connection successful!")
except Exception as e:
    print("Error:", e)
