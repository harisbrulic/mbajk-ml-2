import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error, explained_variance_score
from joblib import dump
from keras.models import load_model
import joblib
import os

model = load_model("models/mbajk_GRU_model.keras")
scaler = joblib.load("models/minmax_scaler.gz")

def evaluate_model(X, y, scaler, model, set_name="test"):
    predictions = model.predict(X)
    predictions = predictions.reshape(-1, 1)
    predictions_inverse = scaler.inverse_transform(predictions)
    y_inverse = scaler.inverse_transform(y)

    mae = mean_absolute_error(y_inverse, predictions_inverse)
    mse = mean_squared_error(y_inverse, predictions_inverse)
    evs = explained_variance_score(y_inverse, predictions_inverse)
    
    print(f"{set_name} - MAE: {mae}, MSE: {mse}, EVS: {evs}")
    
    if not os.path.exists('reports'):
        os.makedirs('reports')
    
    filename = f"reports/{set_name}_metrics.txt"
    
    # Save metrics to a text file
    with open(filename, "w") as f:
        f.write(f"MAE: {mae}\n")
        f.write(f"MSE: {mse}\n")
        f.write(f"EVS: {evs}\n")
        
    plt.figure(figsize=(10, 5))
    plt.plot(y_inverse.flatten(), label='Actual Values')
    plt.plot(predictions_inverse.flatten(), label='Predicted Values', alpha=0.75)
    plt.title(f'{set_name.capitalize()} Set Predictions vs Actuals')
    plt.xlabel('Sample Index')
    plt.ylabel('Available Bike Stands')
    plt.legend()
    plt.show()