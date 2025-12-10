import numpy as np


class DataNormalizer:
    def __init__(self, norm_min=1, norm_max=10, ranges=None):
        """
        Initialize normalizer with configuration

        Args:
            norm_min: Minimum normalized value (default: 1)
            norm_max: Maximum normalized value (default: 10)
            ranges: Dictionary of feature ranges
        """
        self.norm_min = norm_min
        self.norm_max = norm_max
        self.ranges = ranges or {}

    def normalize_feature(self, feature_name, value):
        """Normalize a single feature value to range [norm_min, norm_max]"""
        if feature_name not in self.ranges:
            # If no range defined, return value as-is with warning
            print(f"Warning: No normalization range defined for {feature_name}")
            return float(value)

        min_val, max_val = self.ranges[feature_name]

        # Handle case where min == max (avoid division by zero)
        if max_val == min_val:
            return self.norm_min

        # Clip value to range
        clipped_value = np.clip(value, min_val, max_val)

        # Normalize to [0, 1]
        normalized = (clipped_value - min_val) / (max_val - min_val)

        # Scale to [norm_min, norm_max]
        scaled = normalized * (self.norm_max - self.norm_min) + self.norm_min

        return float(scaled)

    def denormalize_feature(self, feature_name, normalized_value):
        """Denormalize a value from [norm_min, norm_max] back to original range"""
        if feature_name not in self.ranges:
            print(f"Warning: No denormalization range defined for {feature_name}")
            return float(normalized_value)

        min_val, max_val = self.ranges[feature_name]

        # Handle case where min == max
        if max_val == min_val:
            return min_val

        # Scale from [norm_min, norm_max] to [0, 1]
        normalized = (normalized_value - self.norm_min) / (
            self.norm_max - self.norm_min
        )

        # Denormalize to original range
        denormalized = normalized * (max_val - min_val) + min_val

        return float(denormalized)

    def normalize_features(self, features_dict):
        """Normalize all features in a dictionary"""
        normalized = {}
        for feature, value in features_dict.items():
            normalized[feature] = self.normalize_feature(feature, value)
        return normalized

    def denormalize_prediction(self, normalized_prediction):
        """Denormalize the predicted price (assuming it's Close price)"""
        return self.denormalize_feature("Close", normalized_prediction)

    def get_normalization_info(self, feature_name):
        """Get min/max range for a feature"""
        if feature_name in self.ranges:
            return self.ranges[feature_name]
        return None

    def set_ranges(self, ranges):
        """Update normalization ranges"""
        self.ranges = ranges
