import pandas as pd
import numpy as np
from .normalizer import DataNormalizer  # Import from the same directory


class PricePredictor:
    def __init__(self, model_loader, norm_min=1, norm_max=10, ranges=None):
        self.model_loader = model_loader
        self.normalizer = DataNormalizer(norm_min, norm_max, ranges)

    def predict_next_close(self, cryptocurrency, features):
        """
        Predict tomorrow's Close price for cryptocurrency

        Args:
            cryptocurrency: BTC, ETH, LTC, or XPR
            features: Dictionary of TODAY's feature values (not normalized)

        Returns:
            Predicted TOMORROW's Close price (denormalized)
        """
        # Get the model
        model = self.model_loader.get_model(cryptocurrency)

        # Normalize input features
        normalized_features = self.normalizer.normalize_features(features)

        # Create DataFrame with normalized features
        feature_df = pd.DataFrame([normalized_features])

        # Define required features (hardcoded for now)
        required_features = [
            "Open",
            "High",
            "Low",
            "Close",
            "Daily_Return",
            "Log_Return",
            "MA_7",
            "MA_14",
            "MA_30",
            "Volatility_7",
            "Volatility_14",
            "RSI",
            "MACD",
            "MACD_Signal",
        ]

        # Calculate any missing technical indicators
        for feature in required_features:
            if feature not in feature_df.columns:
                feature_df = self._calculate_technical_indicators(
                    feature_df, feature, normalized_features
                )

        # Ensure all columns exist and in correct order
        for feature in required_features:
            if feature not in feature_df.columns:
                feature_df[feature] = 5.5  # Default middle value

        # Reorder columns to match model training order
        feature_df = feature_df[required_features]

        # Debug: Print what we're sending to the model
        print(f"\nMaking prediction for {cryptocurrency}:")
        print(f"Original features: {features}")
        print(f"Normalized features: {normalized_features}")

        # Make prediction (model returns normalized value)
        try:
            normalized_prediction = model.predict(feature_df)
            normalized_price = float(normalized_prediction[0])

            # Denormalize the prediction back to actual price
            predicted_price = self.normalizer.denormalize_prediction(normalized_price)

            print(f"Model output (normalized): {normalized_price:.4f}")
            print(f"Denormalized prediction: ${predicted_price:.2f}")
            print(f"Today's close was: ${features.get('Close', 'N/A')}")

            return predicted_price
        except Exception as e:
            print(f"Prediction error: {str(e)}")
            print(f"Feature columns: {feature_df.columns.tolist()}")
            print(f"Feature values: {feature_df.iloc[0].to_dict()}")
            raise ValueError(f"Prediction failed: {str(e)}")

    def _calculate_technical_indicators(self, df, feature, normalized_features):
        """Calculate technical indicators if missing"""
        # Try to get from normalized features first
        if feature in normalized_features:
            df[feature] = normalized_features[feature]
            return df

        # If not available, calculate defaults
        if feature == "Daily_Return":
            df["Daily_Return"] = 0.0

        elif feature == "Log_Return":
            df["Log_Return"] = 5.5

        elif feature in ["MA_7", "MA_14", "MA_30"]:
            df[feature] = 5.5

        elif feature in ["Volatility_7", "Volatility_14"]:
            df[feature] = 3.0

        elif feature == "RSI":
            df["RSI"] = 5.5

        elif feature in ["MACD", "MACD_Signal"]:
            df[feature] = 5.5

        else:
            df[feature] = 5.5

        return df

    def predict(self, cryptocurrency, features):
        """Main prediction method"""
        return self.predict_next_close(cryptocurrency, features)

    def normalize_single_value(self, feature_name, value):
        """Helper to normalize a single value"""
        return self.normalizer.normalize_feature(feature_name, value)

    def denormalize_single_value(self, feature_name, normalized_value):
        """Helper to denormalize a single value"""
        return self.normalizer.denormalize_feature(feature_name, normalized_value)

    def update_normalizer(self, norm_min, norm_max, ranges):
        """Update normalizer configuration"""
        self.normalizer = DataNormalizer(norm_min, norm_max, ranges)
