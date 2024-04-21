import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, explained_variance_score
from keras.models import Sequential
from keras.layers import GRU, Dense, Dropout
from keras.optimizers import Adam
import joblib
import os
import glob

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT_DIR, '..', '..', 'data', 'processed')

data_files = glob.glob(os.path.join(DATA_DIR, '*.csv'))

for file_path in data_files:
    print(file_path)
    df = pd.read_csv(file_path)

    avg_values = df.drop(columns=['date']).mean()
    df.fillna(avg_values, inplace=True)

    df = df.drop(columns=['date'])

    multivariate_features = df[
        ['available_bike_stands', 'temperature', 'relative_humidity', 'apparent_temperature', 'rain']]

    scaler = MinMaxScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(multivariate_features), columns=multivariate_features.columns,
                             index=multivariate_features.index)

    num_features = 5

    numpy_array = df_scaled.to_numpy()

    split_index = int(0.6 * len(numpy_array))

    train_data = numpy_array[:split_index]
    test_data = numpy_array[split_index:]

    window_size = 5

    def prepare_sequences(data, window, future_steps=7):
        windows = []
        labels = []
        for i in range(window, len(data) - future_steps + 1):
            x = data[i - window:i, :]
            y = data[i:i + future_steps, 0]
            windows.append(x)
            labels.append(y)
        return np.array(windows), np.array(labels)

    X_train, y_train = prepare_sequences(train_data, window_size)
    X_test, y_test = prepare_sequences(test_data, window_size)

    X_train = np.reshape(X_train, (X_train.shape[0], window_size, num_features))
    X_test = np.reshape(X_test, (X_test.shape[0], window_size, num_features))

    print(X_train.shape)
    print(y_train.shape)
    print(X_test.shape)
    print(y_test.shape)

    learning_rate = 0.001
    optimizer = Adam(learning_rate=learning_rate)

    model_gru = Sequential([
        GRU(8, activation='relu', input_shape=(window_size, num_features)),
        Dropout(0.5),
        Dense(8, activation='relu'), 
        Dropout(0.3),
        Dense(7) 
    ])

    optimizer = Adam(learning_rate)
    model_gru.compile(optimizer=optimizer, loss='mean_squared_error')

    history = model_gru.fit(X_train, y_train, epochs=50, batch_size=4, validation_data=(X_test, y_test), verbose=1)

    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Model Training History')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()
    
    predictions = model_gru.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    evs = explained_variance_score(y_test, predictions)

    train_predictions = model_gru.predict(X_train)
    train_mae = mean_absolute_error(y_train, train_predictions)
    train_mse = mean_squared_error(y_train, train_predictions)
    train_evs = explained_variance_score(y_train, train_predictions)

    train_metrics_text = f"MAE: {train_mae}\nMSE: {train_mse}\nEVS: {train_evs}"
    test_metrics_text = f"MAE: {mae}\nMSE: {mse}\nEVS: {evs}"

    model_name = os.path.basename(file_path).replace('.csv', '')
    model_path = os.path.join(ROOT_DIR, '..', '..', 'models', model_name + '_model.h5')
    train_metrics_path = os.path.join(ROOT_DIR, '..', '..', 'reports', model_name, 'train_metrics.txt')
    test_metrics_path = os.path.join(ROOT_DIR, '..', '..', 'reports', model_name, 'test_metrics.txt')

    os.makedirs(os.path.dirname(train_metrics_path), exist_ok=True)

    model_gru.save(model_path)

    scaler_dir = os.path.join(ROOT_DIR, '..', '..', 'models', 'scalers')
    os.makedirs(scaler_dir, exist_ok=True)

    scaler_path = os.path.join(scaler_dir, model_name + '_scaler.pkl')
    joblib.dump(scaler, scaler_path)

    with open(train_metrics_path, "w") as file:
        file.write(train_metrics_text)

    with open(test_metrics_path, "w") as file:
        file.write(test_metrics_text)