import os
from dotenv import dotenv_values

env_values = {
    **dotenv_values(".env"),
    **os.environ,  # Override with OS
}

class DBConfig:
    host = env_values.get('DB_HOST')
    port = int(env_values.get('DB_PORT'))
    db_name = env_values.get('DB_DBNAME')
    username = env_values.get('DB_USERNAME')
    password = env_values.get('DB_PASSWORD')


# default config objects
db_config = DBConfig()