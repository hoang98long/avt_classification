import argparse
from utils.classification import Classification
from utils.config import *
import joblib

model = joblib.load(SHIP_CLASSIFICATION_MODEL_PATH)
scaler = joblib.load(SHIP_CLASSIFICATION_SCALER_PATH)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--avt_task_id', type=int, required=True, help='task id')
    args = parser.parse_args()
    preprocessing = Classification()
    preprocessing.process(args.avt_task_id, model, scaler)
