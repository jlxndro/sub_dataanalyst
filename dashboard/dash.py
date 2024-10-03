import config
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns 
import streamlit as st 
from babel.numbers import format_currency

day_df = pd.read_csv("data/day.csv")
hour_df = pd.read_csv("data/hour.csv")
day_clean_df = pd.read_csv("data/day_cleaned.csv")
hour_clean_df = pd.read_csv("data/hour_cleaned.csv")

datetime_columns = ["dteday"]
day_df.sort_values(by="dteday", inplace=True)
day_df.reset_index(inplace=True)
 
for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])

min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()
 
with st.sidebar:
    count = day_df["casual"].sum()
    st.metric("Total pengguna kasual", value=count)
    count = day_df["registered"].sum()
    st.metric("Total pengguna terdaftar", value=count)
    count = day_df["cnt"].sum()
    st.metric("Total pengguna", value=count)
    

st.title('Analisis Data Pengguna Sepeda')



st.header('Visualisasi Data')
tab1, tab2,tab3,tab4 = st.tabs(["Tipe Hari", "Jam", "Musim", "Cuaca"])
with tab1:
    st.subheader('Perbandingan Working day, Weekend, dan Holiday')
    col1, col2 = st.columns(2)
    with col1:
        day_df["day_type"] = day_df.apply(lambda row: "Holiday" if row["holiday"] == 1 else ("WorkingDay" if row["workingday"] == 1 else "Weekend"), axis=1)
        day_df.groupby("day_type")["cnt"].agg(['sum', 'mean'])
        plt.figure(figsize=(8, 6))
        sns.barplot(x=day_df.groupby("day_type", observed=False)["cnt"].agg(['sum']).index, y=day_df.groupby("day_type", observed=False)["cnt"].agg(['sum'])['sum'])
        plt.title('Total Cyclist by Day Type')
        plt.xlabel('')
        plt.ylabel('Total (Million)')
        st.pyplot(plt)

    with col2:
        day_order = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        day_clean_df['weekday'] = pd.Categorical(day_clean_df['weekday'], categories=day_order, ordered=True)
        plt.figure(figsize=(8, 6))
        sns.barplot(x='weekday', y='sum', data=day_clean_df.groupby("weekday", observed=False)["total"].agg(['sum']))
        plt.title('Total Cyclist per Day')
        plt.xlabel('')
        plt.ylabel('Total')
        st.pyplot(plt)

with tab2:
    st.subheader('Waktu Bersepeda Dalam Sehari')
    plt.figure(figsize=(8, 6))
    sns.barplot(x='hour', y='sum', data=hour_clean_df.groupby("hour")["total"].agg(['sum']))
    plt.title('Total Cyclist per Hour')
    plt.xlabel('Hour')
    plt.ylabel('Total')
    st.pyplot(plt)

with tab3:
    st.subheader('Musim Terbaik Untuk Bersepeda')
    col1, col2 = st.columns([2,1])
    with col1:
        season_order = ['Spring', 'Summer', 'Fall', 'Winter']
        day_clean_df['season'] = pd.Categorical(day_clean_df['season'], categories=season_order, ordered=True)
        plt.figure(figsize=(8, 6))
        sns.barplot(x='season', y='sum', data=day_clean_df.groupby("season", observed=False)["total"].agg(['sum']))
        plt.title('Total Cyclist per Season')
        plt.xlabel('')
        plt.ylabel('Total (Million)')
        st.pyplot(plt)

    with col2:
        plt.figure(figsize=(8, 6))
        sns.barplot(x='season', y='sum', hue='year', data=day_clean_df.groupby(["season", "year"], observed=False)["total"].agg(['sum']))
        plt.title('Total Cyclist per Season')
        plt.xlabel('')
        plt.ylabel('Total (Million)')
        st.pyplot(plt)

        plt.figure(figsize=(8, 6))
        sns.lineplot(x='season', y='sum', hue='year', data=day_clean_df.groupby(["season", "year"], observed=False)["total"].agg(['sum']))
        plt.title('Total Cyclist per Season')
        plt.xlabel('Hour')
        plt.ylabel('Total')
        st.pyplot(plt)

with tab4:
    st.subheader('Pengaruh Cuaca Terhadap Jumlah Pengguna Sepeda')
    col1, col2 = st.columns(2)
    with col1:
        plt.figure(figsize=(8, 6))
        sns.barplot(x='weather', y='sum', data=day_clean_df.groupby("weather", observed=False)["total"].agg(['sum']))
        plt.xlabel('')
        plt.ylabel('Total (Million)')
        st.pyplot(plt)

    with col2:
        correlation = day_df[["temp", "atemp", "hum", "windspeed", "cnt"]].corr()
        plt.figure(figsize=(8, 6))
        sns.heatmap(correlation, annot=True, cmap="coolwarm")
        plt.title("Correlation Heatmap")
        st.pyplot(plt)


