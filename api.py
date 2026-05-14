from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd
from datetime import datetime
import database

# Initialize DB
database.init_db()

# Load model (Only once when the server starts)
with open("car_price_rf_pipeline.pkl", "rb") as f:
    model = pickle.load(f)

app = FastAPI(title="Car Price Predictor API", description="API for predicting car prices and logging data")

class CarData(BaseModel):
    brand: str
    model: str
    year: int
    km_driven: int
    fuel: str
    transmission: str
    seller_type: str = "Individual"
    owner: str = "First Owner"

@app.post("/predict")
def predict_price(car: CarData):
    # Prepare input for the ML model
    car_age = datetime.now().year - car.year
    km_driven_cap = min(car.km_driven, 500000)

    input_df = pd.DataFrame([{
        "km_driven_cap": km_driven_cap,
        "car_age": car_age,
        "fuel": car.fuel,
        "seller_type": car.seller_type,
        "transmission": car.transmission,
        "owner": car.owner,
        "brand": car.brand,
        "model": car.model
    }])

    # Predict using the loaded Random Forest Pipeline
    prediction = model.predict(input_df)[0]

    # Log to SQLite DB asynchronously or synchronously
    database.log_prediction(
        brand=car.brand,
        model=car.model,
        year=car.year,
        km_driven=car.km_driven,
        fuel=car.fuel,
        transmission=car.transmission,
        predicted_price=float(prediction)
    )

    return {"predicted_price": float(prediction)}

@app.get("/feature_importances")
def get_feature_importances():
    try:
        rf_model = None
        if hasattr(model, 'steps'):
            for name, step in model.steps:
                if hasattr(step, 'feature_importances_'):
                    rf_model = step
                    break
        elif hasattr(model, 'feature_importances_'):
            rf_model = model
            
        if rf_model is not None and hasattr(rf_model, 'feature_importances_'):
            importances = rf_model.feature_importances_.tolist()
            
            feature_names = []
            if hasattr(model, 'named_steps') and 'preprocessor' in model.named_steps:
                try:
                    feature_names = model.named_steps['preprocessor'].get_feature_names_out().tolist()
                except:
                    pass
            
            if not feature_names:
                feature_names = getattr(rf_model, 'feature_names_in_', [f"Feature {i}" for i in range(len(importances))])
                if hasattr(feature_names, 'tolist'):
                    feature_names = feature_names.tolist()
                else:
                    feature_names = list(feature_names)
                    
            return {"features": feature_names, "importances": importances}
    except Exception as e:
        return {"error": str(e)}
    return {"error": "Model does not support feature importances"}

@app.get("/logs")
def get_prediction_logs():
    return database.get_logs()
