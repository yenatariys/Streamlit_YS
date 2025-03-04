# -*- coding: utf-8 -*-
"""porto-spoti.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/16Hom18DJ5EZXHYCA9pqhn47HUdU_KDRN
"""

#Import Library
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from datetime import datetime

#Upload dataset
from google.colab import files
uploaded = files.upload()

#Baca dataset
df = pd.read_csv('spotify_history.csv')

#Tampilkan 5 baris pertama
df.head()

#Cek Struktur Data

#info dataset
df.info()

#cek apakah ada data yang hilang
df.isnull().sum()

#Eksplorasi awal data

#statistik dasar untuk kolom numerik
df.describe()

#cek jumlah track unik yang pernah diputar
df['track_name'].nunique()

#cek jumlah artis unik yang pernah diputar
df['artist_name'].nunique()

#Top 10 lagu yang paling sering diputar
df['track_name'].value_counts().head(10)

"""**Top Artist Tahun ini vs Tahun Lalu**"""

#Konversi ts ke Datetime
df['ts'] = pd.to_datetime(df['ts'])

#Tambahkan kolom tahun & bulan untuk analisis
df['year'] = df['ts'].dt.year
df['month'] = df['ts'].dt.month

#Cek apakah konversi berhasil
df[['ts','year', 'month']].head()

#Ganti angka tahun sesuai dataset. Karna di dataset tahunnya 2013-2015, maka:
tahun_ini = 2015 #tahun terbaru
tahun_lalu = 2014 #tahun sebelumnya

df_tahun_ini = df[df['year'] == tahun_ini]
df_tahun_lalu = df[df['year'] == tahun_lalu]

#Cek jumlah data per tahun
print(f"Jumlah data tahun {tahun_ini}: {len(df_tahun_ini)}")
print(f"Jumlah data tahun {tahun_lalu}: {len(df_tahun_lalu)}")
print("Jumlah data tahun 2013:", len(df[df['year'] == 2013]))

"""**Top Artist di 2015**"""

#Hitung jumlah pemutaran per artis di 2015
top_artis_2015 = df_tahun_ini['artist_name'].value_counts().head(10)

#Tampilkan hasil
print("Top 10 Artis di 2015:")
print(top_artis_2015)

#Visualisasi
import matplotlib.pyplot as plt

#Plot bar chart
plt.figure(figsize=(10,5))
top_artis_2015.plot(kind='bar', color='skyblue')

#Tambahkan judul & label
plt.title('Top 10 Artis di 2015 (berdasarkan jumlah pemutaran)')
plt.xlabel('Nama Artis')
plt.ylabel('Jumlah Pemutaran')
plt.xticks(rotation=45) #label diputar agar mudah dibaca
plt.grid(axis="y", linestyle="--", alpha=0.7)

#Tampilkan plot
plt.show()

"""**Top 10 Lagu di 2015**"""

# Hitung jumlah pemutaran per lagu di 2015
top_lagu_2015 = df_tahun_ini['track_name'].value_counts().head(10)

# Tampilkan hasil
print("Top 10 Lagu di 2015:")
print(top_lagu_2015)

#Visualisasi
import matplotlib.pyplot as plt

#Plot bar chart
plt.figure(figsize=(10,5))
top_lagu_2015.plot(kind='bar', color='lightcoral')

#Tambahkan judul & label
plt.title('Top 10 Lagu di 2015 (berdasarkan jumlah pemutaran)')
plt.xlabel('Nama Lagu')
plt.ylabel('Jumlah Pemutaran')
plt.xticks(rotation=45, ha='right') #label diputar agar mudah dibaca
plt.grid(axis="y", linestyle="--", alpha=0.7)

#Tampilkan grafik
plt.show()

"""**Analisis Skip Rate di 2015**"""

#Hitung jumlah total pemutaran dan jummlah lagu yang di-skip
total_play = df_tahun_ini.shape[0]
total_skip = df_tahun_ini[df_tahun_ini['skipped'] == True].shape[0]

#Hitung persentase skip
skip_rate = (total_skip / total_play) * 100

#Tampilkan hasil
print(f"Jumlah total pemutaran: {total_play}")
print(f"Jumlah total skip: {total_skip}")
print(f"Persentase skip: {skip_rate:.2f}%")

"""78.75% lagu di skip--berarti sebagian besar lagu hanya diputar **sebentar** sebelum dilewati ,berarti bisa jadi:
*   Pengguna banyak mencari lagu baru tapi cepat melewatkannya
*   Mereka hanya ingin mendengar bagian tertentu dari lagu (misal intro/chorus)
*   Algoritma shuffle yang tidak sesuai dengan preferensi




"""

#Visualisasi skip rate
skip_data = pd.DataFrame({
    'Status': ['Skip', 'Tidak Skip'],
    'Jumlah': [total_play, total_skip - total_skip]
})

#Plot bar chart
plt.figure(figsize=(8,5))
sns.barplot(x='Status', y='Jumlah', data=skip_data, palette=['lightblue', 'salmon'])

#Tambahkan judul & label
plt.title('Perbandingan Lagu yang Diputar vs Diskip (2015)')
plt.ylabel("Jumlah lagu")
plt.grid(axis="y", linestyle='--', alpha=0.7)

#Tampilkan grafik
plt.show()

"""**Potensi Insight**
*   Pengguna sedang mencari lagu tertentu, jadi banyak yang dilewati
*   Pengguna sering memainkan playlist dengan shuffle, lalu skip lagu yang kurang disukai
* Kalau data ada dari tahun sebelumnya, bisa dibandingkan apakah tingkat skip semakin tinggi atau tetap stabil
"""

# Filter data per tahun
df_2015 = df[df['ts'].dt.year == 2015]
df_2014 = df[df['ts'].dt.year == 2014]
df_2013 = df[df['ts'].dt.year == 2013]

# Hitung jumlah total pemutaran dan skip per tahun
def hitung_skip(df):
    total = len(df)
    skip = df['skipped'].sum()
    return (skip / total) * 100 if total > 0 else 0

percent_skip_2015 = hitung_skip(df_2015)
percent_skip_2014 = hitung_skip(df_2014)
percent_skip_2013 = hitung_skip(df_2013)

# Buat data untuk plotting
years = ['2013', '2014', '2015']
percent_skipped = [percent_skip_2013, percent_skip_2014, percent_skip_2015]

# Plot perbandingan
plt.figure(figsize=(6,4))
sns.barplot(x=years, y=percent_skipped, palette=['gray', 'lightgray', 'royalblue'])

# Tambahkan label
plt.title("Perbandingan Persentase Skip Lagu (2013-2015)")
plt.xlabel("Tahun")
plt.ylabel("Persentase Skip (%)")
plt.ylim(0, 100)

# Tampilkan nilai di atas bar
for i, v in enumerate(percent_skipped):
    plt.text(i, v + 2, f"{v:.2f}%", ha="center", fontsize=12)

plt.show()

"""****Beberapa kemungkinan penyebab****
* Adanya perubahan kebiasaan pengguna seperti lebih picky dan suka skip lagu yang kurang menarik
* Adanya fitur baru di spotify seperti auto-shuffle play, atau rekoemndasi yang kurang sesuai
* Adanya perubahan preferensi genre musik

****Analisis apakah skip lebih banyak terjadi di lagu-lagu baru atau yang sudah sering diputar****

***Kalo lagu yang sering diputar lebih jarang di-skip, berarti mereka cenderung menyukai lagu tsb. Sebaliknya, kalau lagu yang jarang diputar malah lebih sering diskip, bisa jadi itu lagu yang kurang disukai***
"""

import pandas as pd
import matplotlib.pyplot as plt

#Kelompokkan lagu berdasarkan total jumlah pemutarannya
stats_lagu = df_2015.groupby('track_name').agg({
    'skipped': ['sum', 'count']
}).reset_index()

# Rename the columns for better readability
stats_lagu.columns = ['track_name', 'total_skip', 'total_play']  # Rename columns

#Hitung persentase skip
stats_lagu['skip_rate'] = (stats_lagu['total_skip'] / stats_lagu['total_play']) * 100

#Scatterplot untuk jumlah pemutaran vs persentase skip
plt.figure(figsize=(10, 5))
plt.scatter(stats_lagu['total_play'], stats_lagu['skip_rate'], alpha=0.5)
plt.xlabel('Total Pemutaran')
plt.ylabel('Persentase Skip (%)')
plt.title('Hubungan Jumlah Pemutaran vs Persentase Skip (2015)')
plt.xscale('log')  # Gunakan log scale agar lebih jelas
plt.grid(True)
plt.show()

"""* Lagu dengan sedikit pemutaran (di sisi kiri grafik) cenderung punya persentase skip yang sangat tinggi. Ini bisa berarti banyak lagu baru yang dicoba tapi langsung di-skip
* Lagu dengan pemutaran lebih banyak (di sisi kanan grafik) masih ada yang di-skip, tapi beberapa memiliki persentase skip yang lebih rendah. Ini menunjukkan bahwa lagu yang sering diputar kemungkinan lebih disukai
* Ada beberapa titik di bagian atas dengan persentase skip 100*--mungkin itu lagu yang dicoba sekali lalu langsung di-skip setiap kali
"""