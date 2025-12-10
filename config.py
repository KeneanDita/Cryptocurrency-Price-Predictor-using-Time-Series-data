import os
from pathlib import Path


class Config:
    MODELS_DIR = Path.cwd() / "Models"

    # Model paths
    MODEL_PATHS = {
        "BTC": MODELS_DIR / "xgboost_model_BTC.joblib",
        "ETH": MODELS_DIR / "xgboost_model_ETH.joblib",
        "LTC": MODELS_DIR / "xgboost_model_LTC.joblib",
        "XPR": MODELS_DIR / "xgboost_model_XPR.joblib",
    }

    # Supported cryptocurrencies
    CRYPTOCURRENCIES = ["BTC", "ETH", "LTC", "XPR"]

    # Features used in the model
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

    # Normalization ranges
    NORMALIZATION_RANGES = {
        "Open": (0, 100000),  # Example range - adjust based on your data
        "High": (0, 100000),
        "Low": (0, 100000),
        "Close": (0, 100000),
        "Daily_Return": (-20, 20),  # -20% to +20%
        "Log_Return": (-0.2, 0.2),
        "MA_7": (0, 100000),
        "MA_14": (0, 100000),
        "MA_30": (0, 100000),
        "Volatility_7": (0, 0.5),  # 0-50% volatility
        "Volatility_14": (0, 0.5),
        "RSI": (0, 100),  # RSI range 0-100
        "MACD": (-1000, 1000),
        "MACD_Signal": (-1000, 1000),
    }

    # Normalization target range
    NORM_MIN = 1
    NORM_MAX = 10

    TARGET_NAME = "Next_Close_Price"
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-in-production"
