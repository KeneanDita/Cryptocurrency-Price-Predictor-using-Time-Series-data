# Cryptocurrency Price Prediction

A lightweight Flask web application that predicts cryptocurrency prices using pre-trained **XGBoost** models. Although the project contains trained Random Forest Regressors for each crypto. Supports BTC, ETH, LTC, and XPR models stored in the `/Models` directory.

##  Features

- Clean and responsive Flask UI  
- Predicts cryptocurrency prices using loaded XGBoost models  
- AJAX-based `/predict` API  
- Easy-to-extend architecture  
- Auto-loads all XGBoost `.joblib` models on startup  
- Modular Flask blueprint structure  

##  Project Structure

```

CRYPTOCURRENCY-PRICE-PREDICTION/
│
├── app/
│   ├── **init**.py
│   ├── routes.py
│   ├── models_loader.py
│   ├── static/
│   │   └── css/style.css
│   └── templates/
│       ├── layout.html
│       └── index.html
│
├── Models/
│   ├── xgboost_model_BTC.joblib
│   ├── xgboost_model_ETH.joblib
│   ├── xgboost_model_LTC.joblib
│   └── xgboost_model_XPR.joblib
│
├── run.py
├── requirements.txt
└── README.md

```

## How It Works

1. `models_loader.py` loads all XGBoost models from `/Models`
2. The user selects a crypto symbol + enters features
3. The frontend sends a JSON request to `/predict`
4. The model generates a price prediction  
5. The result is displayed instantly on the page

## Installation

### 1. Clone the repository

```p
git clone https://github.com/KeneanDita/Cryptocurrency-Price-Predictor-using-Time-Series-data
cd Cryptocurrency-Price-Predictor-using-Time-Series-data
```

### 2. Install dependencies

```p
pip install -r requirements.txt

```

### 3. Run the Flask app

```p
python run.py
```

The app will run at:

[http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## Prediction API

### **POST** `/predict`

#### Sample Request
```json
{
  "symbol": "BTC",
  "features": [43000, 0.97, 120000000]
}
````

#### Sample Response

```json
{
  "symbol": "BTC",
  "prediction": 43521.9912
}
```

---

##  Adding New Models

To add a new crypto:

1. Train an XGBoost model
2. Save it as:

```
xgboost_model_<SYMBOL>.joblib
```

3. Place it in the `/Models` folder
4. Restart the Flask server

The app will detect it automatically.

---

##  Notes

* Ensure feature ordering matches your training dataset.
* Models must accept a single sample shaped as `[[f1, f2, ...]]`.
* API input is strictly numerical and comma-separated from the UI.

---

##  License

MIT License.

### Author: [Kenean Dita](<https://github.com/keneandita>)

Built with Flask, XGBoost, and a lot of enthusiasm for ML + crypto.
