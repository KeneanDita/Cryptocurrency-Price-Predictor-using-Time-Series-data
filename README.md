# Cryptocurrency Price Prediction

A Flask web application that predicts **tomorrow's closing prices** for cryptocurrencies using trained XGBoost models. The application uses historical market data with technical indicators to make predictions for BTC, ETH, LTC, and XPR.

The models predict **tomorrow's closing price** based on today's market data (Target = Close.shift(-1)).

* Screenshot of Landing page

![Landing Page](/static/ff.png)

## Features

- **Next-Day Price Prediction**: Predicts tomorrow's closing price based on today's market data
- **Multiple Cryptocurrencies**: Supports BTC, ETH, LTC, and XPR
- **Technical Indicators**: Uses 14 technical features including RSI, MACD, Moving Averages
- **Auto-Calculation**: Automatically calculates missing technical indicators
- **Sample Data**: Quick fill buttons for testing with realistic data

## Project Structure

```.
CRYPTOCURRENCY-PRICE-PREDICTION/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── config.py                   # Configuration settings
├── test_models.py              # Model loading test script
│
├── utils/                      # Utility modules
│   ├── __init__.py
│   ├── model_loader.py         # Loads XGBoost models
│   └── predictor.py            # Handles predictions
│
├── static/                     # Static assets
│   ├── css/
│   │   └── style.css           # Custom styles
│   └── js/
│       └── script.js           # Frontend JavaScript
│
├── templates/                  # Jinja2 templates
│   ├── base.html              # Base template
│   ├── index.html             # Home page
│   ├── predict.html           # Prediction form
│   └── results.html           # Results display
│
└── Models/                     # Trained models (outside project)
    ├── xgboost_model_BTC_joblib
    ├── xgboost_model_ETH_joblib
    ├── xgboost_model_LTC_joblib
    └── xgboost_model_XPR_joblib
```

## Technical Features

### Model Features (14 total)

1. **Price Data**: Open, High, Low, Close
2. **Returns**: Daily_Return, Log_Return
3. **Moving Averages**: MA_7, MA_14, MA_30
4. **Volatility**: Volatility_7, Volatility_14
5. **Technical Indicators**: RSI, MACD, MACD_Signal

### How It Works

1. User enters today's market data (Open, High, Low, Close)
2. System calculates/uses technical indicators
3. XGBoost model predicts tomorrow's closing price
4. Results display with percentage change and trading insights

## Quick Start

### 1. Clone & Setup

```bash
git clone https://github.com/KeneanDita/Cryptocurrency-Price-Predictor-using-Time-Series-data
cd Cryptocurrency-Price-Predictor-using-Time-Series-data
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Verify Model Files

Ensure your XGBoost models are in the `Models/` directory with names:

- `xgboost_model_BTC.joblib`
- `xgboost_model_ETH.joblib`
- `xgboost_model_LTC.joblib`
- `xgboost_model_XPR.joblib`

### 4. Run the Application

```bash
python app.py
```

Visit: [http://localhost:5000](http://localhost:5000)

### JSON API Endpoints

#### 1. Get Available Models

```bash
GET /api/models
```

**Response:**

```json
{
  "available_models": ["BTC", "ETH", "LTC", "XPR"],
  "features": ["Open", "High", "Low", "Close", ...],
  "prediction_type": "next_day_close_price"
}
```

#### 2. Make Prediction

```bash
POST /api/predict
```

**Request:**

```json
{
  "cryptocurrency": "BTC",
  "features": {
    "Open": 42000.50,
    "High": 42500.75,
    "Low": 41800.25,
    "Close": 42200.00,
    "RSI": 65.5,
    "Volatility_7": 0.025
  }
}
```

**Response:**

```json
{
  "cryptocurrency": "BTC",
  "prediction": 42450.25,
  "prediction_type": "next_day_close",
  "features": { ... },
  "timestamp": "2024-01-15T14:30:00"
}
```

## Model Details

### Training Approach

- **Target**: `Close.shift(-1)` (tomorrow's closing price)
- **Algorithm**: XGBoost Regressor(Optional Random forest regressot)
- **Features**: 14 technical indicators
- **Data**: Historical cryptocurrency time series data

### Required Features for Prediction

```python
# Minimum required (others auto-calculated)
required = ['Open', 'High', 'Low', 'Close']
```

## Adding New Cryptocurrencies

1. **Train a new model** with the same 14 features
2. **Save the model** as `xgboost_model_{SYMBOL}_joblib`
3. **Place it** in the `Models/` directory
4. **Update** `config.py`:

 ```python
   CRYPTOCURRENCIES = ['BTC', 'ETH', 'LTC', 'XPR', 'NEW_SYMBOL']
   
   MODEL_PATHS = {
       # ... existing models
       'NEW_SYMBOL': MODELS_DIR / "xgboost_model_NEW_SYMBOL_joblib"
   }
   ```

5. **Restart** the application

### Sample Prediction Test

```python
import requests
import json

data = {
    "cryptocurrency": "BTC",
    "features": {
        "Open": 42000.50,
        "High": 42500.75,
        "Low": 41800.25,
        "Close": 42200.00
    }
}

response = requests.post('http://localhost:5000/api/predict', json=data)
print(json.dumps(response.json(), indent=2))
```

## UI Features

1. **Prediction Form**: Clean input form with validation
2. **Sample Data**: Pre-filled data for testing
3. **Auto-calculation**: Daily Return automatically computed
4. **Results Display**: 
   - Predicted price with percentage change
   - Trading insights based on prediction
   - Detailed feature table
   - Visual indicators (up/down arrows)

5. **Responsive Design**: Works on mobile and desktop

## Notes & Limitations

- **Minimum Input**: Open, High, Low, Close are required
- **Feature Order**: Model expects features in specific order
- **Model Format**: Supports `.joblib` format models
- **Auto-calculation**: Technical indicators calculated if not provided
- **Disclaimer**: Predictions are for educational purposes only

## Future Enhancements

1. Real-time market data integration
2. Historical prediction accuracy tracking
3. Multiple prediction horizons (daily, weekly)
4. Model performance comparison dashboard
5. Advanced visualization with charts

## License

MIT License

## Author

**Kenean Dita**

- GitHub: [@KeneanDita](https://github.com/KeneanDita)

Built with using Flask, XGBoost, and Bootstrap. Designed for cryptocurrency price prediction research and education.
