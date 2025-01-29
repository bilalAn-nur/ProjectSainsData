import pandas as pd

# Memuat dataset (ganti 'data.csv' dengan path file Anda)
data = pd.read_csv('data.csv')

# Memilih kolom yang diperlukan
selected_columns = data[[
    'bps_nama_kecamatan', 'jenis_kelamin', 'jumlah_kasus', 'tahun'
]]

# Menghapus baris dengan nilai NaN pada kolom penting
selected_columns = selected_columns.dropna(subset=['bps_kode_kabupaten_kota','bps_nama_kecamatan', 'jenis_kelamin', 'jumlah_kasus', 'tahun'])

# Pastikan data pada kolom jumlah_kasus adalah numerik
selected_columns['jumlah_kasus'] = pd.to_numeric(selected_columns['jumlah_kasus'], errors='coerce')

# Menghapus data yang tidak valid setelah konversi
selected_columns = selected_columns.dropna(subset=['jumlah_kasus'])

# Menjumlahkan jumlah kasus berdasarkan kecamatan, tahun, dan jenis kelamin
aggregated_data = (
    selected_columns.groupby(['bps_nama_kecamatan', 'tahun', 'jenis_kelamin'])
    .agg({'jumlah_kasus': 'sum'})
    .reset_index()
)

# Pivot data untuk memisahkan jumlah kasus laki-laki dan perempuan
pivoted_data = aggregated_data.pivot_table(
    index=['bps_nama_kecamatan', 'tahun'],
    columns='jenis_kelamin',
    values='jumlah_kasus',
    fill_value=0
).reset_index()

# Menambahkan kolom total jumlah kasus (Laki-Laki + Perempuan)
pivoted_data['total_kasus'] = pivoted_data.get('LAKI LAKI', 0) + pivoted_data.get('PEREMPUAN', 0)

# Simpan hasil preprocessing ke file baru
pivoted_data.to_csv('processeds_data.csv', index=False)

# Menampilkan hasil akhir
print(pivoted_data.head())