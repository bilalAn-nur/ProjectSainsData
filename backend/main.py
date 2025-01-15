from fastapi import FastAPI, Query
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dummy data
data_dummy = pd.read_csv('processed_data.csv')
dbd_data = pd.DataFrame(data_dummy)

# Endpoint: Get data
@app.get("/data/")
def get_data():
    return dbd_data.to_dict(orient="records")

# Endpoint: Statistik
@app.get("/stats/")
def stats():
    stats = {
        "mean_cases": dbd_data['total_kasus'].mean(),
        "highest_year": dbd_data.loc[dbd_data['total_kasus'].idxmax()]["tahun"],
    }
    return stats

# @app.get("/predict/")
# def predict(kecamatan: str = Query(...), steps: int = Query(12)):
#     # Filter data by kecamatan
#     filtered_df = dbd_data[dbd_data['bps_nama_kecamatan'] == kecamatan].sort_values('tahun')
#     if filtered_df.empty:
#         return {"error": f"No data found for kecamatan: {kecamatan}"}

#     # Train ARIMA model
#     model = ARIMA(filtered_df['total_kasus'], order=(1, 1, 1))
#     result = model.fit()

#     # Generate predictions
#     forecast = result.forecast(steps=steps)
#     predicted_values = forecast.tolist()

#     return {"kecamatan": kecamatan, "predictions": predicted_values}