import cv2
import numpy as np
import os
from skimage.feature import hog
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
from config import *

image_folder = 'dataset/ship'
labels = SHIP_LABELS


def extract_features(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    height, width = image.shape
    resized_image = cv2.resize(image, (48, 24), interpolation=cv2.INTER_AREA)
    hog_features = hog(resized_image, block_norm='L2-Hys')
    return np.concatenate(([height, width], hog_features))


X = []
y = []
for label in labels:
    label_folder = os.path.join(image_folder, label)
    for filename in os.listdir(label_folder):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            image_path = os.path.join(label_folder, filename)
            features = extract_features(image_path)
            X.append(features)
            y.append(label)

X = np.array(X)
y = np.array(y)

scaler = StandardScaler()
X = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

joblib.dump(model, SHIP_CLASSIFICATION_MODEL_PATH)
joblib.dump(scaler, SHIP_CLASSIFICATION_SCALER_PATH)

y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))
