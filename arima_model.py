import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

def analyze_arima(data_path: str, kecamatan: str):
    """
    Melakukan analisis ARIMA pada data untuk kecamatan tertentu.
    
    Args:
        data_path (str): Path ke file CSV data.
        kecamatan (str): Nama kecamatan untuk analisis.
    
    Returns:
        dict: Hasil prediksi ARIMA.
    """
    # Membaca data dari file CSV
    df = pd.read_csv(data_path)
    
    # Filter data berdasarkan kecamatan
    df_filtered = df[df['bps_nama_kecamatan'] == kecamatan]
    
    # Pastikan data terurut berdasarkan tahun
    df_filtered = df_filtered.sort_values(by='tahun')
    
    # Data untuk analisis
    cases = df_filtered['jumlah_kasus'].values
    
    # Membuat model ARIMA
    model = ARIMA(cases, order=(1, 1, 1))
    model_fit = model.fit()
    
    # Prediksi 3 tahun ke depan
    forecast = model_fit.forecast(steps=3)
    
    # Hasil prediksi
    return {
        "kecamatan": kecamatan,
        "tahun_prediksi": [2021, 2022, 2023],
        "jumlah_kasus_prediksi": forecast.tolist(),
    }
