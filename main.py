import argparse
from utils.classification import Classification
from utils.config import *
import joblib
import json

model = joblib.load(SHIP_CLASSIFICATION_MODEL_PATH)
scaler = joblib.load(SHIP_CLASSIFICATION_SCALER_PATH)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--avt_task_id', type=int, required=True, help='task id')
    parser.add_argument('--config_file', type=str, required=True, help='config file')
    args = parser.parse_args()
    preprocessing = Classification()
    config_data = json.load(open(args.config_file))
    preprocessing.process(args.avt_task_id, config_data, model, scaler)
