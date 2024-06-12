
import MySQLdb

db_config = {
    "host": "sql_server_ip",
    "user": "root",
    "passwd": "yourpassword",
    "db": "yourdatabase"
}

def connect_db():
    print("connect_db---------0")
    db = MySQLdb.connect(**db_config)
    cursor = db.cursor()
    return db, cursor

def initialize_db():    
    db_config_init = {
        "host": "sql_server_ip",
        "user": "root",
        "passwd": "yourpassword",
        #"db": "yourdatabase"
    }
    db = MySQLdb.connect(**db_config_init)
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS yourdatabase")
    cursor.execute("USE yourdatabase")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS T_fee (
            transaction_id VARCHAR(20) PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100),
            ...
            payment_status BOOLEAN DEFAULT FALSE
        )
    """)
    db.commit()
    cursor.close()
    db.close()
