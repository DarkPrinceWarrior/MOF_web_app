import pandas as pd
import streamlit


def excel_action():
    streamlit.title("Excel файл базы данных параметров СЭХ для синтеза МОК")
    df = pd.read_excel("../data_00.xlsx")
    streamlit.write(df)