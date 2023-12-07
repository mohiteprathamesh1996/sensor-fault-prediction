import os
import io

import numpy as np
import pandas as pd
from fastapi import FastAPI, UploadFile, File
from starlette.responses import RedirectResponse
from uvicorn import run as app_run
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware

from sensor.logger import logging
from sensor.pipeline.training_pipeline import TrainPipeline
from sensor.constant.training_pipeline import (
    DATA_INGESTION_DIR_NAME,
    DATA_INGESTION_INGESTED_DIR,
    TRAIN_FILE_NAME,
    SAVED_MODEL_DIR,
    TARGET_COLUMN
)
from sensor.constant.training_pipeline import ARTIFACT_DIR
from sensor.constant.application import APP_HOST, APP_PORT
from sensor.ml.model.estimator import ModelResolver
from sensor.utils.main_utils import load_object

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


@app.post("/predict")
async def predict_route(file: UploadFile = File(...)):
    try:
        contents = await file.read()  # Read the contents of the uploaded file
        # Use io.BytesIO to read bytes as CSV
        df = pd.read_csv(io.BytesIO(contents))
        # Process the DataFrame (e.g., perform operations, save to disk, etc.)
        directory = ARTIFACT_DIR
        files_with_timestamps = [
            (
                filename,
                os.path.getctime(os.path.join(directory, filename))
            )
            for filename in os.listdir(directory)
        ]

        latest_file = max(files_with_timestamps, key=lambda x: x[1])[
            0] if files_with_timestamps else None

        latest_file_path_csv = os.path.join(
            directory,
            latest_file,
            DATA_INGESTION_DIR_NAME,
            DATA_INGESTION_INGESTED_DIR,
            TRAIN_FILE_NAME
        )

        cols_to_include = list(pd.read_csv(latest_file_path_csv).columns)

        model_resolver = ModelResolver(model_dir=SAVED_MODEL_DIR)

        if not model_resolver.is_model_exists():
            return Response("Model is not available")

        best_model_path = model_resolver.get_best_model_path()
        model = load_object(file_path=best_model_path)
        y_pred = model.predict(
            x=df[cols_to_include].drop(
                columns=TARGET_COLUMN
            ).replace('na', np.nan)
        )

    except Exception as e:
        return Response(f"Error Occurred! {e}")

    return {"predictions": y_pred.tolist()}


def main():
    try:
        training_pipeline = TrainPipeline()
        training_pipeline.run_pipeline()
    except Exception as e:
        print(e)
        logging.exception(e)


if __name__ == "__main__":
    main()
    app_run(app, host=APP_HOST, port=APP_PORT)
