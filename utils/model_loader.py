import joblib
import traceback
from flask import current_app
import os


class ModelLoader:
    def __init__(self):
        self.models = {}
        self.loaded = False

    def load_models(self):
        """Load all XGBoost models"""
        try:
            print(f"Models directory: {current_app.config['MODELS_DIR']}")
            print(
                f"Looking for models in: {current_app.config['MODELS_DIR'].resolve()}"
            )

            for crypto, path in current_app.config["MODEL_PATHS"].items():
                print(f"Looking for {crypto} at: {path.resolve()}")

                # Check if file exists (with or without .joblib extension)
                model_path = path
                if not path.exists():
                    # Try with .joblib extension
                    model_path = path.parent / f"{path.name}.joblib"
                    print(f"Trying alternative path: {model_path.resolve()}")

                if model_path.exists():
                    try:
                        self.models[crypto] = joblib.load(model_path)
                        print(f"✓ Successfully loaded model for {crypto}")
                    except Exception as e:
                        print(f"✗ Error loading {crypto} model: {str(e)}")
                else:
                    print(f"✗ Model file not found for {crypto}")

            self.loaded = True
            print(f"Loaded {len(self.models)} models: {list(self.models.keys())}")
            return True

        except Exception as e:
            print(f"Error loading models: {str(e)}")
            traceback.print_exc()
            return False

    def get_model(self, cryptocurrency):
        """Get model for specific cryptocurrency"""
        if not self.loaded:
            if not self.load_models():
                raise ValueError("Failed to load models")

        if cryptocurrency in self.models:
            return self.models[cryptocurrency]
        else:
            available = list(self.models.keys())
            raise ValueError(
                f"No model found for {cryptocurrency}. Available: {available}"
            )

    def get_available_models(self):
        """Get list of available models"""
        if not self.loaded:
            self.load_models()

        return list(self.models.keys())
