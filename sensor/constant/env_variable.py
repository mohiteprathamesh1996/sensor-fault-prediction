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

#pymongvar = response["Parameter"]["Value"]

pymongvar = "mongodb+srv://prathameshmohite96:Psm%4020696@clusterpm.jycq9ph.mongodb.net/?retryWrites=true&w=majority"

os.environ['MONGODB_URL'] = pymongvar
os.environ['MONGO_DB_URL'] = pymongvar

MONGODB_URL = os.getenv('MONGODB_URL')
MONGO_DB_URL = os.getenv('MONGO_DB_URL')
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")
