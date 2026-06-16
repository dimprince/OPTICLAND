import psycopg2

def get_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="CENTRE_OPTICLABS",
        user="postgres",
        password="mc2007mc",
        port="5432"
    )
    return conn