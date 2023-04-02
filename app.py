import streamlit as st
import pickle
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components

st.set_page_config(page_title="Breathe Air")

st.subheader("AQI of Mumbai Sub division")
def load_model():
    with open('Hawaman_pred.pkl', 'rb') as file:
        data = pickle.load(file)
    return data


data = load_model()

regressor = data["model"]


def predict_aqi(SO2, NOx, RSPM):
    input1 = np.array([[SO2, NOx, RSPM]]).astype(np.float64)
    print(input1)
    prediction = regressor.predict(input1)
    return float(prediction)


html_temp = """<div style="background:#025246, padding:10px">
                <h2 style="color:white;text-align:center;"> Air Quality Index Prediction </h2></div>"""

st.markdown(html_temp, unsafe_allow_html=True)

SO2 = st.text_input("SO2")
NOx = st.text_input("NOx")
RSPM = st.text_input("RSPM")

safe_html = """<div style="background-color:#80ff80; padding:10px;border-radius:25px >
        <h2 style="color:Black;text-align:center;"> This is satisfactory </h2></div>"""

warn_html = """<div style="background-color:#FFFF00; padding:10px;border-radius:25px>
        <h2 style="color:Black;text-align:center;"> This is moderate </h2></div>"""

danger_html = """<div style="background-color:#ff0000; padding:10px;border-radius:25px>
        <h2 style="color:Black;text-align:center;"> This is poor </h2></div>"""

if st.button("Predict the AQI"):
    output = predict_aqi(SO2, NOx, RSPM)
    st.success('The AQI is {}'.format(output))

    if output < 100:
        st.markdown(safe_html, unsafe_allow_html=True)
    elif output == 100:
        st.markdown(warn_html, unsafe_allow_html=True)
    elif output >= 150:
        st.markdown(danger_html, unsafe_allow_html=True)

# plotting map

st.subheader('Regions having different types of AQI', 'font-size:10px')

data = pd.read_csv('hawaman2.csv')

st.map(data)

# Create a folium map centered on a location
# map = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)

# # Add markers to the map for each data point
# for index, row in data.iterrows():
#     folium.Marker(location=[row['latitude'], row['longitude']],
#                   popup=row['City']).add_to(map)

# # Define a function to color the markers based on a value
# def color_marker(output):
#     if (output) <= 100:
#         return 'green'
#     elif (output) == 100:
#         return 'orange'
#     else:
#         return 'red'


# # Add a layer to the map that colors the markers based on a column in the DataFrame
# folium.map.Marker(
#     [row['latitude'], row['longitude']],
#     icon=folium.Icon(color=color_marker(output))
# ).add_to(map)

# presenting visualization

st.subheader("Data Visualization")

st.sidebar.subheader("Settings")
uploaded_file = st.file_uploader(label="Upload your CSV ",
                                 type=['csv', 'xlsx'])

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
    options=['Scatterplots', 'Lineplots', 'Histogram']
)

# numeric_columns = list(df.select_dtypes(['float', 'int']).columns)
if chart_select == 'Scatterplots':
    st.sidebar.subheader("Scatterplot Settings")
    try:
        x_values = st.sidebar.selectbox('X axis', options=numeric_columns)
        y_values = st.sidebar.selectbox('Y axis', options=numeric_columns)
        plot = px.scatter(data_frame=df, x=x_values, y=y_values)

        st.plotly_chart(plot)
    except Exception as e:
        print(e)

if chart_select == 'Histogram':
    st.sidebar.subheader("Histogram Settings")
    try:
        x_values = st.sidebar.selectbox('X axis', options=numeric_columns)
        y_values = st.sidebar.selectbox('Y axis', options=numeric_columns)
        plot = px.histogram(data_frame=df, x=x_values, y=y_values)

        st.plotly_chart(plot)
    except Exception as e:
        print(e)

if chart_select == 'Lineplots':
    st.sidebar.subheader("Lineplot Settings")
    try:
        # x_values = st.sidebar.selectbox('X axis', options=numeric_columns)
        y_values = st.sidebar.selectbox('Y axis', options=numeric_columns)
        # px.line()
        plot = px.line(data_frame=df, y=y_values)

        st.plotly_chart(plot)
    except Exception as e:
        print(e)
