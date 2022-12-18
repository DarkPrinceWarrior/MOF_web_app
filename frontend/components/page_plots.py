import pandas as pd
import streamlit
import plotly.express as px


def plots_action():
    streamlit.title("Таблица свойств полученных МОК")
    df = pd.read_excel("../baseline_results.xlsx")
    streamlit.write(df)

    # Plots
    streamlit.header('Интерактивный график по параметрам полученных МОК')

    # Interactive plots

    col1, col2 = streamlit.columns(2)

    x_axis_val = col1.selectbox('Выбрать параметр X', options=df.columns)
    y_axis_val = col2.selectbox('Выбрать параметр Y', options=df.columns)

    plot = px.scatter(df, x=x_axis_val, y=y_axis_val)
    streamlit.plotly_chart(plot, use_container_width=True)
