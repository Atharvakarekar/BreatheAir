import pandas as pd
import plotly.express as px
import streamlit as st

st.title("Data Visualization App")

st.sidebar.subheader("Settings")
uploaded_file = st.file_uploader(label="Upload your CSV ",
                 type=['csv','xlsx'])

global df
if uploaded_file is not None:
    print(uploaded_file)
    print("Error")
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        print(e)
        df = pd.read_excel(uploaded_file)

global numeric_columns
try:
    st.write(df)
    numeric_columns = list(df.select_dtypes(['float', 'int']).columns)
except Exception as e:
    print(e)
    st.write("Please upload files")

chart_select = st.sidebar.selectbox(
    label="Select the chart type",
    options=['Scatterplots', 'Lineplots', 'Histogram', 'Boxplot']
)

# numeric_columns = list(df.select_dtypes(['float', 'int']).columns)
if chart_select == 'Scatterplots' :
    st.sidebar.subheader("Scatterplot Settings")
    try:
        x_values = st.sidebar.selectbox('X axis', options=numeric_columns)
        y_values = st.sidebar.selectbox('Y axis', options=numeric_columns)
        plot = px.scatter(data_frame=df, x=x_values, y=y_values)

        st.plotly_chart(plot)
    except Exception as e:
        print(e)
