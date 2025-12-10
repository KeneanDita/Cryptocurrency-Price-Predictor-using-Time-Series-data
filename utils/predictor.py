import pandas as pd
import numpy as np
from flask import current_app


class PricePredictor:
    def __init__(self, model_loader):
        self.model_loader = model_loader

    def predict(self, cryptocurrency, features):
        """
        Make prediction for cryptocurrency price

        Args:
            cryptocurrency: BTC, ETH, LTC, or XPR
            features: Dictionary of feature values

        Returns:
            Predicted price
        """
        # Get the model
        model = self.model_loader.get_model(cryptocurrency)

        # Create DataFrame with features
        feature_df = pd.DataFrame([features])

        # Ensure all required features are present
        required_features = current_app.config["FEATURES"]
        for feature in required_features:
            if feature not in feature_df.columns:
                # Try to calculate missing features if we have basic data
                feature_df = self._calculate_missing_features(feature_df, feature)

        # Reorder columns to match model expectations
        feature_df = feature_df[required_features]

        # Make prediction
        try:
            prediction = model.predict(feature_df)
            return float(prediction[0])
        except Exception as e:
            raise ValueError(f"Prediction failed: {str(e)}. Check feature values.")

    def _calculate_missing_features(self, df, feature):
        """Calculate missing features if possible"""
        if feature == "Daily_Return" and "Close" in df.columns and "Open" in df.columns:
            df["Daily_Return"] = (df["Close"] - df["Open"]) / df["Open"] * 100
        elif feature == "Log_Return" and "Close" in df.columns:
            # For single prediction, assume previous close is Close - small amount
            df["Log_Return"] = np.log(df["Close"] / (df["Close"] * 0.99))
        elif feature == "MA_7" and "Close" in df.columns:
            df["MA_7"] = df["Close"]
        elif feature == "MA_14" and "Close" in df.columns:
            df["MA_14"] = df["Close"]
        elif feature == "MA_30" and "Close" in df.columns:
            df["MA_30"] = df["Close"]
        elif feature == "Volatility_7" and "Close" in df.columns:
            df["Volatility_7"] = 0.02  # Default volatility
        elif feature == "Volatility_14" and "Close" in df.columns:
            df["Volatility_14"] = 0.02  # Default volatility
        elif feature == "RSI" and "Close" in df.columns:
            df["RSI"] = 50.0  # Neutral RSI
        elif feature == "MACD" and "Close" in df.columns:
            df["MACD"] = 0.0
        elif feature == "MACD_Signal" and "Close" in df.columns:
            df["MACD_Signal"] = 0.0
        else:
            df[feature] = 0.0  # Default value

        return df
