import pymongo
from sensor.constant.database import DATABASE_NAME
from sensor.constant.env_variable import *
import os
import certifi
ca = certifi.where()

class MongoDBClient:
    client = None
    def __init__(self, database_name = DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                # MongoDBClient.client = pymongo.MongoClient(MONGODB_URL, tlsCAFile = ca)
                MongoDBClient.client = pymongo.MongoClient(
                    "mongodb+srv://prathameshmohite96:Psm%4020696@clusterpm.jycq9ph.mongodb.net/?retryWrites=true&w=majority", 
                    tlsCAFile = ca
                    )

            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
        except Exception as e:
            raise e
