import os
from pathlib import Path


class Config:
    MODELS_DIR = Path.cwd() / "Models"  # Go up one level to reach Models folder

    # Model paths (with .joblib extension)
    MODEL_PATHS = {
        "BTC": MODELS_DIR / "xgboost_model_BTC.joblib",
        "ETH": MODELS_DIR / "xgboost_model_ETH.joblib",
        "LTC": MODELS_DIR / "xgboost_model_LTC.joblib",
        "XPR": MODELS_DIR / "xgboost_model_XPR.joblib",
    }

    # Supported cryptocurrencies
    CRYPTOCURRENCIES = ["BTC", "ETH", "LTC", "XPR"]

    # Actual features from your trained models
    FEATURES = [
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

    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-in-production"
