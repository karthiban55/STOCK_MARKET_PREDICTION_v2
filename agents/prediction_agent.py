import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Dropout
import os
from huggingface_hub import HfApi, HfFolder
import tempfile
import joblib

class PredictionAgent:
    def __init__(self):
        self.model_repo = "Karthiban55/Stock_Predictor"  # Your HF repo
        self.api = HfApi()
        self.token = os.getenv("HF_TOKEN")  # Set your token as env var
        if self.token:
            HfFolder.save_token(self.token)

    def load_model_from_hf(self):
        try:
            # Download model.h5 and scaler.pkl from HF
            model_path = self.api.hf_hub_download(repo_id=self.model_repo, filename="model.h5")
            scaler_path = self.api.hf_hub_download(repo_id=self.model_repo, filename="scaler.pkl")
            model = load_model(model_path)
            scaler = joblib.load(scaler_path)
            return model, scaler
        except Exception as e:
            print(f"Failed to load model from HF: {e}")
            return None, None

    def save_model_to_hf(self, model, scaler):
        if not self.token:
            print("No HF token, skipping upload")
            return
        with tempfile.TemporaryDirectory() as tmpdir:
            model_path = os.path.join(tmpdir, "model.h5")
            scaler_path = os.path.join(tmpdir, "scaler.pkl")
            model.save(model_path)
            joblib.dump(scaler, scaler_path)
            try:
                self.api.upload_file(path_or_fileobj=model_path, path_in_repo="model.h5", repo_id=self.model_repo)
                self.api.upload_file(path_or_fileobj=scaler_path, path_in_repo="scaler.pkl", repo_id=self.model_repo)
                print("Model uploaded to HF")
            except Exception as e:
                print(f"Failed to upload to HF: {e}")
                # Save locally
                os.makedirs("trained_models", exist_ok=True)
                model.save("trained_models/model.h5")
                joblib.dump(scaler, "trained_models/scaler.pkl")
                print("Model saved locally in trained_models/")

    def run(self, data: pd.DataFrame) -> float:
        """
        Loads or trains an LSTM model and predicts the next day's closing price.
        """
        print("LSTM Prediction Agent: Starting...")

        # Try to load model from HF
        model, scaler = self.load_model_from_hf()
        if model is None or scaler is None:
            print("No pre-trained model found, training new one...")
            # --- 1. Data Preparation ---
            close_data = data.filter(['Close']).values 
            
            scaler = MinMaxScaler(feature_range=(0, 1))
            scaled_data = scaler.fit_transform(close_data)

            # --- 2. Create Training Sequences ---
            look_back_period = 60
            X_train, y_train = [], []

            for i in range(look_back_period, len(scaled_data)):
                X_train.append(scaled_data[i-look_back_period:i, 0])
                y_train.append(scaled_data[i, 0])
            
            X_train, y_train = np.array(X_train), np.array(y_train)
            X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
            
            print(f"LSTM Prediction Agent: Prepared {len(X_train)} training sequences.")

            # --- 3. Build and Train the LSTM Model ---
            model = Sequential([
                LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)),
                Dropout(0.2),
                LSTM(units=50, return_sequences=False),
                Dropout(0.2),
                Dense(units=25),
                Dense(units=1)
            ])
            
            model.compile(optimizer='adam', loss='mean_squared_error')
            
            print("LSTM Prediction Agent: Training model...")
            model.fit(X_train, y_train, batch_size=1, epochs=5)
            print("LSTM Prediction Agent: Model training complete.")

            # Save to HF
            self.save_model_to_hf(model, scaler)
        else:
            print("Loaded pre-trained model from HF")
            # Assume scaler is already fitted, but for new data, we need to scale with the same scaler
            # But since data is different, this might not work well, but for demo
            close_data = data.filter(['Close']).values 
            scaled_data = scaler.transform(close_data)  # Use transform, not fit_transform

        # --- 4. Make a Prediction ---
        look_back_period = 60
        last_60_days = scaled_data[-look_back_period:]
        X_test = np.reshape(last_60_days, (1, look_back_period, 1))
        
        predicted_price_scaled = model.predict(X_test)
        
        predicted_price = scaler.inverse_transform(predicted_price_scaled)
        
        print(f"LSTM Prediction Agent: Predicted price: {predicted_price[0][0]}")
        return float(predicted_price[0][0])