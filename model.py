import pandas as pd
from sklearn.linear_model import LinearRegression

def train_and_predict(data: pd.DataFrame):
    """
    Trains a simple linear regression model and predicts the next day's closing price.

    Args:
        data (pd.DataFrame): DataFrame with historical stock data (must include OHLCV columns).

    Returns:
        float: The predicted closing price for the next day.
    """
    # --- 1. Feature Engineering ---
    # We create a 'Target' column, which is the next day's 'Close' price.
    # .shift(-1) moves each value in the 'Close' column up by one row.
    data['Target'] = data['Close'].shift(-1)

    # --- 2. Data Cleaning ---
    # The last row will have a NaN (Not a Number) value for 'Target' because there's no next day.
    # We remove this row before training the model.
    data.dropna(inplace=True)

    # --- 3. Define Features (X) and Target (y) ---
    # The features are the inputs our model will use to make a prediction.
    features = ['Open', 'High', 'Low', 'Close', 'Volume']
    X = data[features]

    # The target is the value we want to predict.
    y = data['Target']

    # --- 4. Train the Model ---
    # We create an instance of the Linear Regression model.
    model = LinearRegression()

    # We train the model on our entire historical dataset.
    model.fit(X, y)

    # --- 5. Make a Prediction ---
    # We use the very last row of the original data (before we dropped NaN) to predict the future.
    # We select the features and reshape it because the model expects a 2D array.
    last_row = data.tail(1)[features]
    prediction = model.predict(last_row)

    # The model returns an array, so we get the first (and only) item.
    return prediction[0]

# You can add a test block here if you want, similar to data_fetcher.py
# if __name__ == '__main__':
#     from data_fetcher import get_stock_data
#     sample_data = get_stock_data("TSLA")
#     if sample_data is not None:
#         predicted_price = train_and_predict(sample_data.copy()) # Use a copy to avoid modifying original
#         print(f"Predicted Next Day Close for TSLA: ${predicted_price:.2f}")