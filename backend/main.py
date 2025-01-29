from fastapi import FastAPI
import pandas as pd
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
data_dummy = pd.read_csv('static/processed_data.csv')
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
