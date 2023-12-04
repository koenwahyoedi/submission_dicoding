# Dashboard submission
import streamlit as st  
import pandas as pd  
import matplotlib.pyplot as plt    
import seaborn as sns
#import calendar
#from PIL import Image
#from babel.numbers import format_currency
sns.set(style='dark')

# load data
df = pd.read_csv('clean.csv')

# Sidebar
with st.sidebar:
    st.image('bike4.png', caption='Bike Rental Logo', use_column_width=True)

# Konversi kolom 'dteday' menjadi tipe data datetime
df['dteday'] = pd.to_datetime(df['dteday'])

# Tampilkan widget rentang tanggal di sidebar
selected_date_range = st.sidebar.date_input("Pilih Rentang Tanggal", 
                                           min_value=df['dteday'].min(), 
                                           max_value=df['dteday'].max(), 
                                           value=(df['dteday'].min(), df['dteday'].max()),
                                           key="date_range")

# Konversi rentang tanggal ke tipe data datetime64[ns]
start_date = pd.to_datetime(selected_date_range[0])
end_date = pd.to_datetime(selected_date_range[1])

# Filter data berdasarkan rentang tanggal yang dipilih
filtered_data = df[(df['dteday'] >= start_date) & (df['dteday'] <= end_date)]

# Menghitung total data yang sudah di filter
total_data_filter = filtered_data['cnt'].sum()

# Generate DataFrame dengan total penyewaan per bulan
monthly_data = filtered_data.resample('M', on='dteday')['cnt'].sum().reset_index()

# Membuat Tabs untuk tampilan dari masing-masing grafik.    
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(['Bulan','Grafik Chart','Holiday', 'Working Day','Cuaca',
                                              'Casual vs Registered'])

with tab1:
    st.subheader('Monthly Bike Rental')

    if not monthly_data.empty:
        # Membuat bar chart
        fig, ax = plt.subplots()
        bars = ax.bar(monthly_data['dteday'].dt.strftime('%b %y'), monthly_data['cnt'], color='g')
        ax.set_title(f'Total Penyewaan Sepeda {start_date.strftime("%B %Y")} - {end_date.strftime("%B %Y")}: {total_data_filter} \n')
        ax.set_xlabel('\n Bulan')
        ax.set_ylabel('Total Jumlah Penyewa')

        # Menambahkan label pada setiap bar
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 1), ha='center', va='bottom', fontsize=7)

        # Menyesuaikan label bulan agar miring
        plt.xticks(rotation=45, ha='right')

        # Tampilkan grafik di dalam tab pertama
        st.pyplot(fig)
    else:
        st.warning("Tidak ada data untuk bulan yang diminta.")

with tab2:
    st.header('Grafik Chart Penyewaan Sepeda')

    # Membuat chart
    fig, ax = plt.subplots(figsize=(60,25))
    ax.plot(
        df['dteday'],
        df['cnt'],
        marker='o',
        linewidth=2,
        color='red'
    )
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=25)

    ax.set_title('Chart selama 2011 - 2012 \n', fontsize=56)
    ax.set_xlabel('\n Waktu penyewaan sepeda dari Tahun 2011 - 2012', fontsize=42)
    ax.set_ylabel('Total Jumlah Penyewa 2011-2012', fontsize=42)
    # Tampilkan grafik
    st.pyplot(fig)

with tab3:
    st.header('Bar Chart Holiday')
    
    # Membuat DataFrame baru untuk menghitung total penyewaan saat Holiday
    total_sewa_holiday = df.groupby('holiday')['cnt'].sum()

    # Membuat bar chart
    fig, ax = plt.subplots()
    bars = ax.bar(total_sewa_holiday.index, total_sewa_holiday, color='grey')
    ax.set_title('Total Penyewaan Sepeda Saat Holiday 2011-2012\n')
    ax.set_xlabel('\nNot Holiday / Holiday')
    ax.set_ylabel('Total Jumlah Penyewa 2011-2012')

    # Mengganti label pada sumbu x
    ax.set_xticks(total_sewa_holiday.index)
    ax.set_xticklabels(['Not Holiday', 'Holiday'])

    # Menambahkan label pada setiap bar
    plt.bar_label(bars, fmt='%d', label_type='center', fontsize=12)

    # Tampilkan grafik
    st.pyplot(fig)

with tab4:
    st.header('Bar Chart Working Day')
    
    # Membuat DataFrame baru untuk menghitung total penyewaan saat Working Day
    total_sewa_workingday = df.groupby('workingday')['cnt'].sum()

    # Membuat bar chart
    fig, ax = plt.subplots()
    bars = ax.bar(total_sewa_workingday.index, total_sewa_workingday, color='y')
    ax.set_title('Total Penyewaan Sepeda Saat Working Day 2011-2012 \n')
    ax.set_xlabel('\n Not Working Day / Working Day')
    ax.set_ylabel('Total Jumlah Penyewa 2011-2012')

    # Mengganti label pada sumbu x
    ax.set_xticks(total_sewa_workingday.index)
    ax.set_xticklabels(['Not Working Day', 'Working Day'])

    # Menambahkan label pada setiap bar
    plt.bar_label(bars, fmt='%d', label_type='center', fontsize=12)

    # Tampilkan grafik
    st.pyplot(fig)

with tab5:
    st.header('Bar Chart Cuaca')

    # Membuat DataFrame baru untuk menghitung total penyewaan cuaca
    total_sewa_cuaca = df.groupby('weathersit')['cnt'].sum()

    # Membuat bar chart
    fig, ax = plt.subplots()
    bars = ax.bar(total_sewa_cuaca.index, total_sewa_cuaca, color='g')
    ax.set_title('Total Penyewaan Sepeda Saat Cuaca Panas, Berawan, dan Hujan selama 2011-2012 \n')
    ax.set_xlabel('\n Kondisi Cuaca')
    ax.set_ylabel('Total Jumlah Penyewa 2011-2012')

    # Mengganti label pada sumbu x
    ax.set_xticks(total_sewa_cuaca.index)
    ax.set_xticklabels(['Cerah', 'Berawan/Mendung', 'Salju/Hujan Ringan'])

    # Menambahkan label pada setiap bar
    plt.bar_label(bars, fmt='%d', label_type='edge', fontsize=12)

    # Tampilkan grafik
    st.pyplot(fig)    

with tab6:
    st.header('Bar Chart Casual vs Registered')

    total_casual = df['casual'].sum()
    total_registered = df['registered'].sum()
    
    # Menggabungkan total_casual dan total_registered menjadi satu DataFrame
    total_df = pd.DataFrame({'Category': ['Casual', 'Registered'], 'Total': [total_casual, total_registered]})

    # Membuat bar chart
    fig, ax = plt.subplots()

    bars = ax.bar(total_df['Category'], total_df['Total'], color=['c','m'])
    
    ax.set_title('Total Penyewaan Sepeda Casual vs Registered 2011-2012 \n')
    ax.set_xlabel('\n Casual / Registered')
    ax.set_ylabel('Total Jumlah Penyewa 2011-2012')

    # Mengganti label pada sumbu x
    ax.set_xticks(total_sewa_workingday.index)
    ax.set_xticklabels(['Casual', 'Registered'])

    # Menambahkan label pada setiap bar
    plt.bar_label(bars, fmt='%d', label_type='center', fontsize=12)

    # Tampilkan grafik
    st.pyplot(fig)    