import boto3
import os
from dotenv import load_dotenv

# Load env
load_dotenv()

ssm = boto3.client('ssm')
response = ssm.get_parameter(
  Name='/myapp/MONGODB_URL', 
  WithDecryption=True
)

pymongvar = response["Parameter"]["Value"]
os.environ['MONGODB_URL'] = pymongvar
os.environ['MONGO_DB_URL'] = pymongvar

MONGODB_URL = os.getenv('MONGODB_URL')
MONGO_DB_URL = os.getenv('MONGO_DB_URL')
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")
