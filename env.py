import os
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY')
DB_HOST=os.getenv('DB_HOST')
DB_NAME=os.getenv('DB_NAME')
DB_USER=os.getenv('DB_USER')
DB_PASSWORD=os.getenv('DB_PASSWORD')