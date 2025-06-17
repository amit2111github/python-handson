from client.pg import get_pool
from psycopg2.extras import RealDictCursor
from psycopg2.extras import RealDictCursor

async def get_user_from_email(email: str):
    pg = get_pool()
    async with pg.acquire() as conn:
        user = await conn.fetchrow("SELECT * FROM users WHERE email = $1", email)
        return dict(user).copy() if user else None
    

async def add_user(data):
    email = data["email"]
    password = data["password"]
    name = data["name"]
    pg = get_pool()
    async with pg.acquire() as conn:
        user = await conn.fetchrow("INSERT INTO users (name , email , password) values ($1 , $2 , $3) RETURNING *", name , email , password)
        return dict(user).copy()
    

async def update_user_from_id(id , data_to_update):
    pg = get_pool()
    set_clauses = []
    values = []
    idx = 1  

    for key, value in data_to_update.items():
        set_clauses.append(f"{key} = ${idx}")
        values.append(value)
        idx += 1

    set_clause = ", ".join(set_clauses)
    query = f"""UPDATE users SET {set_clause} WHERE id = ${idx} RETURNING * """
    values.append(id)  # Add id as last parameter
    async with pg.acquire() as conn:
        print(query , *values)
        user = await conn.fetchrow(query , *values)
        return user


