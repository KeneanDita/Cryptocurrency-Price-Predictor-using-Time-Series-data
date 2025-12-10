from flask import Flask, render_template, request, jsonify
from utils.model_loader import ModelLoader
from utils.predictor import PricePredictor
import pandas as pd

app = Flask(__name__)
app.config.from_object("config.Config")

# Initialize model loader and predictor
model_loader = ModelLoader()
predictor = PricePredictor(model_loader)


@app.route("/")
def index():
    return render_template(
        "index.html", cryptocurrencies=app.config["CRYPTOCURRENCIES"]
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
                if value:
                    features[feature] = float(value)

            # Make prediction
            prediction = predictor.predict(cryptocurrency, features)

            return render_template(
                "results.html",
                cryptocurrency=cryptocurrency,
                prediction=prediction,
                features=features,
            )

        except Exception as e:
            return render_template(
                "predict.html",
                error=str(e),
                cryptocurrencies=app.config["CRYPTOCURRENCIES"],
                features=app.config["FEATURES"],
            )

    return render_template(
        "predict.html",
        cryptocurrencies=app.config["CRYPTOCURRENCIES"],
        features=app.config["FEATURES"],
    )


@app.route("/api/predict", methods=["POST"])
def api_predict():
    try:
        data = request.get_json()
        cryptocurrency = data.get("cryptocurrency")
        features = data.get("features", {})

        if not cryptocurrency:
            return jsonify({"error": "Cryptocurrency is required"}), 400

        prediction = predictor.predict(cryptocurrency, features)

        return jsonify(
            {
                "cryptocurrency": cryptocurrency,
                "prediction": prediction,
                "features": features,
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
        }
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
