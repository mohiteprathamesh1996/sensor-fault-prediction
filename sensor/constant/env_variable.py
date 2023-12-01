import os
from dotenv import load_dotenv

# Load env
load_dotenv()

MONGODB_URL = os.environ.get('MONGO_DB_URL')
MONGO_DB_URL = os.environ.get('MONGO_DB_URL')
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")
