import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set_theme(style='dark')

#load data
hour_df = pd.read_csv("https://raw.githubusercontent.com/zahirotul/submission/main/data/hour.csv")
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

st.header('Sebaran Bike Sharing :sparkles:')

# Menghitung jumlah total pengguna
total_users = hour_df['casual'].sum() + hour_df['registered'].sum()
st.metric("Jumlah total pengguna:", total_users)

st.subheader("Pengguna berdasarkan jenis hari")
col1, col2, col3 = st.columns(3)
 
with col1:
# Menghitung jumlah total pengguna berdasarkan kondisi libur (holiday)
    total_users_holiday = hour_df[hour_df['holiday'] == 1]['cnt'].sum()
    st.metric("Pengguna Holiday:", total_users_holiday)
with col2:
# Menghitung jumlah total pengguna berdasarkan hari kerja (weekday)
    total_users_weekday = hour_df[hour_df['weekday'] < 5]['cnt'].sum()
    st.metric("Pengguna Weekday:", total_users_weekday)
with col3:
# Menghitung jumlah total pengguna berdasarkan hari kerja (workingday)
    total_users_workingday = hour_df[hour_df['workingday'] == 1]['cnt'].sum()
    st.metric("Pengguna Workingday:", total_users_workingday)

st.subheader("Sebaran Pengguna Tiap Bulan")
# Mengelompokkan data berdasarkan bulan dan menghitung total peminjaman sepeda untuk setiap bulan
monthly_usage = hour_df.groupby('mnth')['cnt'].sum()
# Membuat diagram garis untuk menampilkan penggunaan pada setiap bulan
fig, ax = plt.subplots()
ax.plot(monthly_usage.index, monthly_usage.values, marker='o', linestyle='-')
# Menambahkan label pada sumbu x
plt.title('Penggunaan Sepeda per Bulan')
plt.xlabel('Bulan')
plt.ylabel('Jumlah Peminjaman Sepeda')
plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.grid(True)
# Menampilkan plot menggunakan st.pyplot()
st.pyplot(fig)

min_date = hour_df["dteday"].min()
max_date = hour_df["dteday"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/zahirotul/Gambar/blob/main/bike.png?raw=true")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

st.subheader("Bagaimana pengaruh cuaca terhadap pola peminjaman sepeda?")
relevant_cols = ['weathersit', 'cnt']
filtered_df = hour_df[relevant_cols]

# Mengelompokkan data berdasarkan kondisi cuaca dan menjumlahkan jumlah pengguna pada setiap kondisi cuaca
usage_by_weather = filtered_df.groupby('weathersit')['cnt'].sum()

# Membuat diagram batang dengan matplotlib
fig, ax = plt.subplots()
ax.bar(usage_by_weather.index, usage_by_weather.values)

# Menambahkan label dan judul
ax.set_xlabel('Kondisi Cuaca')
ax.set_ylabel('Jumlah Pengguna')
ax.set_title('Pengaruh Cuaca terhadap Peminjaman Sepeda')
# Mengganti label sumbu x dengan label yang diinginkan
ax.set_xticks(usage_by_weather.index)
ax.set_xticklabels(['Clear', 'Mist', 'Light Snow/Rain', 'Heavy Rain/Snow'], rotation=45)
# Menampilkan diagram menggunakan st.pyplot()
st.pyplot(fig)

st.subheader("Apakah ada perbedaan dalam pola peminjaman sepeda antara pengguna casual dan pengguna terdaftar?")
# Definisi fungsi untuk menghitung persentase casual dan registered
def calculate_percentage(df):
    total_casual = df['casual'].sum()
    total_registered = df['registered'].sum()
    total_users = total_casual + total_registered
    percent_casual = (total_casual / total_users) * 100
    percent_registered = (total_registered / total_users) * 100
    return percent_casual, percent_registered
# Memanggil fungsi untuk menghitung persentase casual dan registered
percent_casual, percent_registered = calculate_percentage(hour_df)
# Data untuk pie chart
labels = ['Casual', 'Registered']
sizes = [percent_casual, percent_registered]
colors = ['lightblue', 'lightgreen']
# Membuat pie chart
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
ax.set_title('Persentase Kontribusi Pengguna Casual dan Terdaftar')
ax.axis('equal')  # Memastikan pie chart berbentuk lingkaran
# Menampilkan pie chart menggunakan st.pyplot()
st.pyplot(fig)

# Definisi fungsi untuk menghitung persentase casual dan registered
def calculate_percentage(df):
    total_casual = df['casual'].sum()
    total_registered = df['registered'].sum()
    total_users = total_casual + total_registered
    percent_casual = (total_casual / total_users) * 100
    percent_registered = (total_registered / total_users) * 100
    return percent_casual, percent_registered

# Memfilter data untuk hanya mengambil kolom yang relevan
relevant_cols = ['holiday', 'weekday', 'workingday', 'casual', 'registered']
filtered_df = hour_df[relevant_cols]

# Menghitung total peminjaman sepeda untuk setiap kondisi
total_casual = filtered_df['casual'].sum()
total_registered = filtered_df['registered'].sum()

# Menghitung persentase peminjaman sepeda untuk pengguna casual dan terdaftar
percent_casual = (total_casual / (total_casual + total_registered)) * 100
percent_registered = (total_registered / (total_casual + total_registered)) * 100

# Data untuk pie chart casual users
casual_labels = ['Holiday', 'Weekday', 'Workingday']
casual_sizes = filtered_df[['holiday', 'weekday', 'workingday']].sum()
casual_colors = ['lightblue', 'lightgreen', 'lightcoral']

# Data untuk pie chart registered users
registered_labels = ['Holiday', 'Weekday', 'Workingday']
registered_sizes = filtered_df[['holiday', 'weekday', 'workingday']].sum()
registered_colors = ['lightblue', 'lightgreen', 'lightcoral']

col1, col2 = st.columns(2)
with col1:
# Membuat pie chart casual users
    st.subheader('Casual Users')
    st.write(f"Percentage of Casual Users: {percent_casual:.2f}%")
    fig1, ax1 = plt.subplots()
    ax1.pie(casual_sizes, labels=casual_labels, colors=casual_colors, autopct='%1.1f%%', startangle=140)
    ax1.axis('equal')
    st.pyplot(fig1)

with col2:
# Membuat pie chart registered users
    st.subheader('Registered Users')
    st.write(f"Percentage of Registered Users: {percent_registered:.2f}%")
    fig2, ax2 = plt.subplots()
    ax2.pie(registered_sizes, labels=registered_labels, colors=registered_colors, autopct='%1.1f%%', startangle=140)
    ax2.axis('equal')
    st.pyplot(fig2)

# Memfilter data untuk pengguna casual dan terdaftar
casual_data = hour_df[hour_df['casual'] > 0]
registered_data = hour_df[hour_df['registered'] > 0]
# Menghitung jumlah peminjaman sepeda pada setiap jam untuk pengguna casual dan terdaftar
casual_hourly_rentals = casual_data.groupby('hr')['casual'].sum()
registered_hourly_rentals = registered_data.groupby('hr')['registered'].sum()
# Membuat histogram untuk membandingkan pola peminjaman sepeda antara pengguna casual dan terdaftar pada jam-jam tertentu
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(casual_hourly_rentals.index, casual_hourly_rentals.values, alpha=0.5, color='darkgreen', label='Casual')
ax.bar(registered_hourly_rentals.index, registered_hourly_rentals.values, alpha=0.5, color='lightgreen', label='Registered')
# Menambahkan label dan judul plot
plt.xlabel('Jam (24 Jam)')
plt.ylabel('Jumlah Peminjaman Sepeda')
plt.title('Pola Peminjaman Sepeda Antara Pengguna Casual dan Terdaftar pada Jam Tertentu')
plt.legend()
# Menampilkan plot menggunakan st.pyplot()
st.pyplot(fig)