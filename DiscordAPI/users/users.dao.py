from mysql.connector import pooling
from typing import List
from prayers_queries import prayer_queries


def execute(query, params):
    connection = mysql_pool.get_connection()

    cursor = connection.cursor(dictionary=True)
    cursor.execute(query, params)
    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result


async def read_prayers():
    return execute(prayer_queries.read_prayers, [])


async def create_prayer(prayer):
    return execute(prayer_queries.create_prayer,
                   [prayer['name'], prayer['anonymous'], prayer['prayerRequest']])


async def update_prayer(prayer):
    return execute(prayer_queries.update_prayer,
                   [prayer['name'], prayer['anonymous'], prayer['prayerRequest'], prayer['prayerId']])


async def delete_prayer(prayer_id):
    return execute(prayer_queries.delete_prayer, [prayer_id])
