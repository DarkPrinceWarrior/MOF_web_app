import streamlit
from streamlit_option_menu import option_menu
import requests
import pandas as pd
import numpy as np


def main_action():
    streamlit.title("Предсказание свойств МОК")

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
        response = requests.post("http://127.0.0.1:5000/predict", json=data)
        prediction_table = response.json()
        print()
        # print(prediction_table)
        streamlit.title("Предполагаемые свойства МОК:")
        streamlit.table(pd.DataFrame(prediction_table, index=[0]))


def excel_action():
    streamlit.title("Excel файл базы данных параметров СЭХ для синтеза МОК")
    df = pd.read_excel("../data_00.xlsx")
    streamlit.write(df)


def project_action():
    streamlit.title("Информация по проекту")
    streamlit.markdown("Проект лаборатории нацелен на решение проблем молекулярной диагностики и создания "
                       "предсказательных сервисов в адсорбционных технологиях", unsafe_allow_html=False)
    streamlit.markdown("Задачи лаборатории:\n"
                       "Разработка требований к структуре и методам работы с реляционными базами данных, содержащими "
                       "информацию о MOК, методах их синтеза и их адсорбционных свойствах.\n "
                       "Наполнение баз данных, их масштабирование и вовлечение новых участников в их разработку\n"
                       "Разработка алгоритмов прогнозирования на основе методов машинного обучения с использованием "
                       "сгенерированных баз данных\n "
                       "Разработка прогностических моделей проявления сенсорных свойств MOК на основе численных методов "
                       "молекулярной динамики и квантово-химических методов\n "
                       "Синтез и функционализация MOК с заданными свойствами для задач point-of-care молекулярной "
                       "диагностики \n",unsafe_allow_html=False)


def contact_action():
    streamlit.title("Контакты по проекту")
    streamlit.image("../images/contact_image.jpg")


def run():
    selected = option_menu(
        menu_title="Лаборатория сорбционных методов "
                   "молекулярной диагностики",
        options=["Главная", "Наш проект", "Контакты", "База данных"],
        icons=["house", "list task", "person lines fill", "clipboard data fill"],
        menu_icon="list",
        default_index=0,
        orientation="horizontal"
    )

    if selected == "Главная":
        main_action()

    if selected == "Наш проект":
        project_action()
    if selected == "Контакты":
        contact_action()
    if selected == "База данных":
        excel_action()


if __name__ == '__main__':
    # by default it will run at 8501 port
    # streamlit run app.py
    run()
