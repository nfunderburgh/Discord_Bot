import mysql.connector
from mysql.connector import pooling
import os

mysql_pool = None


def initialize_mysql_connector():
    try:
        global mysql_pool

        mysql_pool = pooling.MySQLConnectionPool(
            pool_name="mysql_pool",
            pool_size=int(os.getenv("MY_SQL_DB_CONNECTION_LIMIT", 5)),
            pool_reset_session=True,
            host=os.getenv("MY_SQL_DB_HOST"),
            port=int(os.getenv("MY_SQL_DB_PORT", 3306)),
            user=os.getenv("MY_SQL_DB_USER"),
            password=os.getenv("MY_SQL_DB_PASSWORD"),
            database=os.getenv("MY_SQL_DB_DATABASE")
        )

        print('MySQL Connector Pool initialized successfully')

        # Checking a connection from the pool
        connection = mysql_pool.get_connection()
        connection.close()
        print('MySQL connection made and released')

    except Exception as e:
        print('[mysql.connector][initialize_mysql_connector][Error]:', e)
        raise Exception('Failed to initialize MySQL Connector Pool')


# Initialize MySQL Connector Pool
initialize_mysql_connector()


def execute(query, params):
    try:
        connection = mysql_pool.get_connection()

        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params)
        result = cursor.fetchall()

        cursor.close()
        connection.close()

        return result

    except Exception as e:
        print('[mysql.connector][execute][Error]:', e)
        raise Exception('Failed to execute MySQL query')
