import pandas as pd
import streamlit
import plotly.express as px


def plots_action():
    streamlit.title("Таблица свойств полученных МОК")
    X_test = pd.read_excel("../baseline_X_test.xlsx")
    Y_pred = pd.read_excel("../baseline_results.xlsx")
    streamlit.write(Y_pred)

    # Plots
    streamlit.header('Интерактивный график: как изменяются параметры'
                     'синтеза при изменении параметров МОК')

    # Interactive plots

    col1, col2 = streamlit.columns(2)

    x_axis_val = col1.selectbox('Выбрать параметр X', options=X_test.columns)
    y_axis_val = col2.selectbox('Выбрать параметр Y', options=Y_pred.columns)

    result = pd.concat([X_test, Y_pred], axis=1)

    plot = px.scatter(result, x=x_axis_val, y=y_axis_val)
    streamlit.plotly_chart(plot, use_container_width=True)
