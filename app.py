from flask import Flask, render_template, request, jsonify, flash
from utils.model_loader import ModelLoader
from utils.predictor import PricePredictor
from utils.normalizer import DataNormalizer
import pandas as pd
import numpy as np

app = Flask(__name__)
app.config.from_object("config.Config")

model_loader = ModelLoader(
    models_dir=app.config["MODELS_DIR"], model_paths=app.config["MODEL_PATHS"]
)

# Load models immediately
model_loader.load_models()

predictor = None
normalizer = None

# Create an application context to initialize components
with app.app_context():
    # Initialize predictor with config values
    predictor = PricePredictor(
        model_loader,
        norm_min=app.config["NORM_MIN"],
        norm_max=app.config["NORM_MAX"],
        ranges=app.config["NORMALIZATION_RANGES"],
    )

    # Initialize normalizer
    normalizer = DataNormalizer(
        norm_min=app.config["NORM_MIN"],
        norm_max=app.config["NORM_MAX"],
        ranges=app.config["NORMALIZATION_RANGES"],
    )


@app.route("/")
def index():
    return render_template(
        "index.html",
        cryptocurrencies=app.config["CRYPTOCURRENCIES"],
        target_name=app.config["TARGET_NAME"],
        norm_min=app.config["NORM_MIN"],
        norm_max=app.config["NORM_MAX"],
    )


@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        try:
            # Get form data
            cryptocurrency = request.form.get("cryptocurrency")

            # Get feature values from form
            features = {}
            for feature in app.config["FEATURES"]:
                value = request.form.get(feature)
                if value and value.strip():
                    try:
                        features[feature] = float(value)
                    except ValueError:
                        # Use default if invalid
                        features[feature] = 0.0
                else:
                    features[feature] = 0.0

            # Validate required features
            required = ["Open", "High", "Low", "Close"]
            missing = [f for f in required if f not in features or features[f] == 0]
            if missing:
                flash(f"Please enter valid values for: {', '.join(missing)}", "danger")
                return render_template(
                    "predict.html",
                    cryptocurrencies=app.config["CRYPTOCURRENCIES"],
                    features=app.config["FEATURES"],
                    norm_ranges=app.config["NORMALIZATION_RANGES"],
                    norm_min=app.config["NORM_MIN"],
                    norm_max=app.config["NORM_MAX"],
                )

            # Make prediction
            prediction = predictor.predict(cryptocurrency, features)

            # Calculate percentage change from today's close
            today_close = features.get("Close", 0)
            if today_close:
                percent_change = ((prediction - today_close) / today_close) * 100
            else:
                percent_change = 0

            # Get normalized values for display
            normalized_features = {}
            for feature, value in features.items():
                try:
                    normalized_features[feature] = normalizer.normalize_feature(
                        feature, value
                    )
                except:
                    normalized_features[feature] = value

            return render_template(
                "results.html",
                cryptocurrency=cryptocurrency,
                prediction=prediction,
                today_close=today_close,
                percent_change=percent_change,
                features=features,
                normalized_features=normalized_features,
                target_name=app.config["TARGET_NAME"],
                norm_min=app.config["NORM_MIN"],
                norm_max=app.config["NORM_MAX"],
            )

        except Exception as e:
            flash(f"Prediction error: {str(e)}", "danger")
            return render_template(
                "predict.html",
                cryptocurrencies=app.config["CRYPTOCURRENCIES"],
                features=app.config["FEATURES"],
                norm_ranges=app.config["NORMALIZATION_RANGES"],
                norm_min=app.config["NORM_MIN"],
                norm_max=app.config["NORM_MAX"],
            )

    return render_template(
        "predict.html",
        cryptocurrencies=app.config["CRYPTOCURRENCIES"],
        features=app.config["FEATURES"],
        norm_ranges=app.config["NORMALIZATION_RANGES"],
        norm_min=app.config["NORM_MIN"],
        norm_max=app.config["NORM_MAX"],
    )


@app.route("/api/normalize", methods=["POST"])
def api_normalize():
    """API endpoint to normalize values"""
    try:
        data = request.get_json()
        feature = data.get("feature")
        value = data.get("value")

        if not feature or value is None:
            return jsonify({"error": "Feature and value required"}), 400

        normalized = normalizer.normalize_feature(feature, float(value))

        return jsonify(
            {
                "feature": feature,
                "original_value": value,
                "normalized_value": normalized,
                "range": normalizer.get_normalization_info(feature),
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/denormalize", methods=["POST"])
def api_denormalize():
    """API endpoint to denormalize values"""
    try:
        data = request.get_json()
        feature = data.get("feature")
        normalized_value = data.get("normalized_value")

        if not feature or normalized_value is None:
            return jsonify({"error": "Feature and normalized_value required"}), 400

        denormalized = normalizer.denormalize_feature(feature, float(normalized_value))

        return jsonify(
            {
                "feature": feature,
                "normalized_value": normalized_value,
                "denormalized_value": denormalized,
                "range": normalizer.get_normalization_info(feature),
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/predict", methods=["POST"])
def api_predict():
    try:
        data = request.get_json()
        cryptocurrency = data.get("cryptocurrency")
        features = data.get("features", {})

        if not cryptocurrency:
            return jsonify({"error": "Cryptocurrency is required"}), 400

        # Validate required features
        required = ["Open", "High", "Low", "Close"]
        missing = [f for f in required if f not in features]
        if missing:
            return jsonify({"error": f"Missing required features: {missing}"}), 400

        prediction = predictor.predict(cryptocurrency, features)

        return jsonify(
            {
                "cryptocurrency": cryptocurrency,
                "prediction": prediction,
                "prediction_type": "next_day_close",
                "features": features,
                "normalized_features": normalizer.normalize_features(features),
                "timestamp": pd.Timestamp.now().isoformat(),
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/models", methods=["GET"])
def get_models():
    return jsonify(
        {
            "available_models": app.config["CRYPTOCURRENCIES"],
            "features": app.config["FEATURES"],
            "normalization_range": {
                "min": app.config["NORM_MIN"],
                "max": app.config["NORM_MAX"],
            },
            "feature_ranges": app.config["NORMALIZATION_RANGES"],
            "target": app.config["TARGET_NAME"],
            "prediction_type": "next_day_close_price",
        }
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
