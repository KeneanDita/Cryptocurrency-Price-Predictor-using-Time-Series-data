import joblib
import traceback
import os


class ModelLoader:
    def __init__(self, models_dir=None, model_paths=None):
        self.models = {}
        self.loaded = False
        self.models_dir = models_dir
        self.model_paths = model_paths or {}

    def load_models(self, models_dir=None, model_paths=None):
        """Load all XGBoost models"""
        if models_dir:
            self.models_dir = models_dir
        if model_paths:
            self.model_paths = model_paths

        if not self.models_dir or not self.model_paths:
            raise ValueError("Models directory and paths must be provided")

        try:
            print(f"Models directory: {self.models_dir}")
            print(f"Looking for models in: {self.models_dir}")

            for crypto, path in self.model_paths.items():
                print(f"Looking for {crypto} at: {path}")

                # Check if file exists (with or without .joblib extension)
                model_path = path
                if not path.exists():
                    # Try with .joblib extension if not already present
                    if not str(path).endswith(".joblib"):
                        model_path = path.parent / f"{path.name}.joblib"
                    print(f"Trying alternative path: {model_path}")

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
            raise ValueError("Models not loaded. Call load_models() first.")

        if cryptocurrency in self.models:
            return self.models[cryptocurrency]
        else:
            available = list(self.models.keys())
            raise ValueError(
                f"No model found for {cryptocurrency}. Available: {available}"
            )

    def get_available_models(self):
        """Get list of available models"""
        return list(self.models.keys())
