import asyncpg
from env import DB_HOST,DB_NAME,DB_USER,DB_PASSWORD

db_pool = None

async def init_db_pool():
    global db_pool
    db_pool = await asyncpg.create_pool(
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        host=DB_HOST,
        min_size=1,
        max_size=10
    )
async def close_db_connection():
    if db_pool:
        await db_pool.close()
    else:
        print("Db Connection was not initalized , failed to close")


def get_pool():
    if db_pool:
        return db_pool
    raise Exception("Database Not initalized")