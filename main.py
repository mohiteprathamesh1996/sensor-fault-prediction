from sensor.configuration.mongo_db_connection import MongoDBClient
from sensor.exception import SensorException
import os,sys
import numpy as np
from sensor.entity.artifact_entity import DataValidationArtifact
from sensor.logger import logging
from sensor.pipeline import training_pipeline
from sensor.pipeline.training_pipeline import TrainPipeline
import pandas as pd
from sensor.utils.main_utils import read_yaml_file
from sensor.constant.training_pipeline import SAVED_MODEL_DIR
from sensor.constant.training_pipeline import TARGET_COLUMN
from sensor.constant import training_pipeline
from fastapi import FastAPI, UploadFile, File
from sensor.constant.application import APP_HOST, APP_PORT
from starlette.responses import RedirectResponse
from uvicorn import run as app_run
from fastapi.responses import Response
from sensor.ml.model.estimator import ModelResolver,TargetValueMapping
from sensor.utils.main_utils import load_object
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import io

directory = training_pipeline.ARTIFACT_DIR




app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:

        train_pipeline = TrainPipeline()
        if train_pipeline.is_pipeline_running:
            return Response("Training pipeline is already running.")
        train_pipeline.run_pipeline()
        return Response("Training successful !!")
    except Exception as e:
        return Response(f"Error Occurred! {e}")

class InputData(BaseModel):
    features: dict

@app.get("/predict")
async def predict_route():
    try:
        #get data from user csv file
        #conver csv file to dataframe

        df = pd.read_csv("aps_failure_training_set1.csv")
        model_resolver = ModelResolver(model_dir=SAVED_MODEL_DIR)

        if not model_resolver.is_model_exists():
            return Response("Model is not available")
        
        best_model_path = model_resolver.get_best_model_path()
        model = load_object(file_path=best_model_path)

        y_pred = model.predict(x = df.drop(columns="class").replace('na', np.nan))

        #decide how to return file to user.
        return y_pred
        
    except Exception as e:
        raise Response(f"Error Occured! {e}")




def main():
    try:
        training_pipeline = TrainPipeline()
        training_pipeline.run_pipeline()
    except Exception as e:
        print(e)
        logging.exception(e)


if __name__=="__main__":
    main()
    app_run(app, host=APP_HOST, port=APP_PORT)