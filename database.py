from config import db_config
import psycopg2

class Database:
    conn = psycopg2.connect(host=db_config.host,
                            port=db_config.port,
                            database=db_config.db_name,
                            user=db_config.username,
                            password=db_config.password)

    cur = conn.cursor()

database = Database()