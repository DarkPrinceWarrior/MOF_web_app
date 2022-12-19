import base64
import pickle

import numpy as np
import streamlit
from pydantic import BaseModel
from streamlit_option_menu import option_menu
import requests
import pandas as pd
from awesome_table import AwesomeTable

from components.page_contact import contact_action
from components.page_database import excel_action
from components.page_information import project_action
from components.page_plots import plots_action
from components.page_mof_information import mof_inf_action

pkl_filename = "saved_models/Multi_RegressionModel.pkl"
with open(pkl_filename, 'rb') as file1:
    model = pickle.load(file1)

pkl_filename_2 = "saved_models/saved_id2cat.pkl"
with open(pkl_filename_2, 'rb') as file2:
    id2cat = pickle.load(file2)

streamlit.set_page_config(
    layout="wide",
    page_title="Adsorptech",
    initial_sidebar_state="collapsed"
)

with open("static/style.css") as css_file:
    streamlit.markdown('<style>{}</style>'.format(css_file.read()), unsafe_allow_html=True)


@streamlit.experimental_memo
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


img = get_img_as_base64("images/background.jpg")

page_back = f"""
<style>

[data-testid="stAppViewContainer"]{{
background-image: url("data:image/png;base64,{img}");
# background-image: url("../images/background.jpg");
background-size: cover;
}}
</style>
"""

streamlit.markdown(page_back, unsafe_allow_html=True)



def predict(data):
    new_data = np.array([data["Temp_reg_C"],
                         data["W0_cm3_g"],
                         data["E0_KDG_moll"],
                         data["x0_nm"],
                         data["a0_mmoll_gr"],
                         data["E_kDg_moll"],
                         data["SBAT_m2_gr"],
                         data["Ws_cm3_gr"],
                         data["Sme_m2_gr"],
                         data["Wme_cm3_gr"]]).reshape(1, 10)

    data_to_predict = pd.DataFrame(columns=['Tрег, ᵒС', 'W0, см3/г', 'E0, кДж/ моль', 'х0, нм', 'а0, ммоль/г',
                                            'E,  кДж/моль', 'SБЭТ, м2/г', 'Ws, см3/г', 'Sme, м2/г', 'Wme, см3/г'],
                                   data=new_data)
    result = model.predict(data_to_predict)

    list_of_cats = ["Металл", "Лиганд", "Растворитель"]
    prediction_column_names = ['Металл', 'Лиганд', 'Растворитель', 'm (соли), г', 'm(кис-ты), г',
                               'Vсин. (р-ля), мл', 'Т.син., °С', 'Vпр. (р-ля), мл', 'Т суш., °С',
                               'm образца']

    result.columns = prediction_column_names
    for cat in list_of_cats:
        result.loc[:, cat] = result[cat].apply(lambda x: id2cat[cat][round(x)])

    prediction = {key: value for key, value in zip(prediction_column_names, result.values[0])}
    # get the correct answer with decoded column values
    return prediction


def predict_action():
    streamlit.title("Предсказание параметров синтеза МОК")

    page_style = f"""
    <style>
    .css-7mza0f {{
        border:3px solid white;
        padding:10px;
        background-color: white;
    }}
    </style>
    """

    streamlit.markdown(page_style, unsafe_allow_html=True)

    Temp_reg_C = streamlit.number_input("Tрег, ᵒС")
    W0_cm3_g = streamlit.number_input("W0, см3/г")
    E0_KDG_moll = streamlit.number_input("E0, кДж/ моль")
    x0_nm = streamlit.number_input("х0, нм")
    a0_mmoll_gr = streamlit.number_input("а0, ммоль/г")
    E_kDg_moll = streamlit.number_input("E,  кДж/моль")
    SBAT_m2_gr = streamlit.number_input("SБЭТ, м2/г")
    Ws_cm3_gr = streamlit.number_input("Ws, см3/г")
    Sme_m2_gr = streamlit.number_input("Sme, м2/г")
    Wme_cm3_gr = streamlit.number_input("Wme, см3/г")

    data = {
        "Temp_reg_C": Temp_reg_C,
        "W0_cm3_g": W0_cm3_g,
        "E0_KDG_moll": E0_KDG_moll,
        "x0_nm": x0_nm,
        "a0_mmoll_gr": a0_mmoll_gr,
        "E_kDg_moll": E_kDg_moll,
        "SBAT_m2_gr": SBAT_m2_gr,
        "Ws_cm3_gr": Ws_cm3_gr,
        "Sme_m2_gr": Sme_m2_gr,
        "Wme_cm3_gr": Wme_cm3_gr
    }
    if streamlit.button("Предсказать"):
        # response = requests.post("http://127.0.0.1:8000/predict", json=data)
        # prediction_table = response.json()

        prediction_table = predict(data)
        streamlit.title("Сгенерированные ИИ параметры синтеза МОК:")
        streamlit.table(pd.DataFrame(prediction_table, index=[0]))


def run():
    with streamlit.sidebar:
        selected = option_menu(
            menu_title="ИИ синтез адсорбентов",
            options=["Наш проект", "МОК информация", "Получить МОК", "Контакты", "База данных",
                     "Интерактив по МОК"],
            icons=["house", "book", "box fill", "person lines fill",
                   "clipboard data fill", "bar-chart-line-fill"],
            menu_icon="kanban fill",
            default_index=0,
            # orientation="horizontal",
            styles={
                "container": {"padding": "0 % 0 % 0 % 0 %"},
                "icon": {"color": "red", "font-size": "25px"},
                "nav-link": {"font-size": "20px", "text-align": "start", "margin": "0px"},
                "nav-link-selected": {"background-color": "#483D8B"},
            }

        )

    if selected == "Наш проект":
        project_action()
    if selected == "Получить МОК":
        predict_action()
    if selected == "Контакты":
        contact_action()
    if selected == "База данных":
        excel_action()
    if selected == "Интерактив по МОК":
        plots_action()
    if selected == "МОК информация":
        image1 = "images/1page.jpg"
        image2 = "images/2page.jpg"
        mof_inf_action(image1, image2)


if __name__ == '__main__':
    # by default it will run at 8501 port
    # streamlit run app.py
    run()
