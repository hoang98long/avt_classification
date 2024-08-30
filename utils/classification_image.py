import numpy as np
import cv2
from skimage.feature import hog
from utils.config import *
import joblib


model = joblib.load(SHIP_CLASSIFICATION_MODEL_PATH)
scaler = joblib.load(SHIP_CLASSIFICATION_SCALER_PATH)


def extract_features(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    height, width = image.shape
    resized_image = cv2.resize(image, (50, 25), interpolation=cv2.INTER_AREA)
    hog_features = hog(resized_image, block_norm='L2-Hys')
    return np.concatenate(([height, width], hog_features))


class Classification_Image:
    def __init__(self):
        pass

    def classify(self, src_img_path):
        features = extract_features(src_img_path)
        features = scaler.transform([features])  # Chuẩn hóa dữ liệu
        prediction = model.predict(features)
        return prediction[0]
