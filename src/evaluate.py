import pandas as pd
import pickle
from sklearn.metrics import accuracy_score
import yaml
import os
import mlflow

from urllib.parse import urlparse

## Setting up env for MLFLOW --(from dagshub)
os.environ['MLFLOW_TRACKING_URI'] = "https://dagshub.com/adiManethia/machinelearningpipeline.mlflow"
os.environ['MLFLOW_TRACKING_USERNAME'] = "adiManethia"
os.environ['MLFLOW_TRACKING_PASSWORD'] = "24f869c500ed280173dfee5bf0ca90e7594909cb"

## Load parameters from param.yaml
params = yaml.safe_load(open("params.yaml"))["train"]

def evaluate(data_path, model_path):
    data = pd.read_csv(data_path)
    X = data.drop(columns=["Outcome"])
    y = data["Outcome"]
    
    ## set tracking uri
    mlflow.set_tracking_uri("https://dagshub.com/adiManethia/machinelearningpipeline.mlflow")
    
    ## Load the model from disk
    model = pickle.load(open(model_path, 'rb'))
    
    predictions = model.predict(X)
    accuracy = accuracy_score(y, predictions)
    
    ## Log metrics to MLFLOW
    mlflow.log_metric("accuracy", accuracy)
    print("Model accuracy: {accuracy}")
    
    
if __name__ == "__main__":
    evaluate(params["data"], params["model"])