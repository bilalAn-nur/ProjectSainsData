import pandas as pd

# Membaca data dari file CSV (ganti 'data.csv' dengan nama file Anda)
data = pd.read_csv('data.csv')

# Memilih kolom yang diperlukan
selected_columns = data[['jenis_kelamin', 'jumlah_kasus', 'tahun', 'bps_nama_kecamatan']]

# Mengonversi 'jumlah_kasus' menjadi numerik jika belum
selected_columns['jumlah_kasus'] = pd.to_numeric(selected_columns['jumlah_kasus'], errors='coerce')

# Menghapus baris dengan nilai NaN pada kolom 'jumlah_kasus'
selected_columns = selected_columns.dropna(subset=['jumlah_kasus'])

# Mengelompokkan data berdasarkan 'jenis_kelamin' dan 'bps_nama_kecamatan' lalu menjumlahkan kasus
grouped_data = selected_columns.groupby(['bps_nama_kecamatan', 'jenis_kelamin'], as_index=False).agg({
    'jumlah_kasus': 'sum'
})

# Menyimpan hasil ke file baru
grouped_data.to_csv('output_preprocessed_data.csv', index=False)

# Menampilkan data hasil pengelompokan
print(grouped_data)