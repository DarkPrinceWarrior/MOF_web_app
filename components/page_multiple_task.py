import base64

import numpy as np
import pandas as pd
import streamlit
from st_clickable_images import clickable_images

from components.predict import predict


def task_option_action(task_images):
    streamlit.title("Выбор задачи под МОК")

    page_task_style = f"""
    <style>
    .css-7mza0f {{
        border:3px solid white;
        padding:10px;
        background-color: white;
    }}
    </style>
    """

    streamlit.markdown(page_task_style, unsafe_allow_html=True)

    images = []
    for file in task_images:
        with open(file, "rb") as image:
            encoded = base64.b64encode(image.read()).decode()
            images.append(f"data:image/jpeg;base64,{encoded}")

    clicked = clickable_images(
        images,
        titles=[f"MOF_task #{str(i)}" for i in [1,2,3]],
        div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
        img_style={"margin": "5px", "height": "200px"},
    )

    Temp_reg_C = 0
    W0_cm3_g =0
    E0_KDG_moll =0
    x0_nm =0
    a0_mmoll_gr =0
    E_kDg_moll =0
    SBAT_m2_gr = 0
    Ws_cm3_gr =0
    Sme_m2_gr =0
    Wme_cm3_gr =0

    if clicked == 0:
        Temp_reg_C = streamlit.number_input("Tрег, ᵒС", value=110)
        W0_cm3_g = streamlit.number_input("W0, см3/г",value=0.66)
        E0_KDG_moll = streamlit.number_input("E0, кДж/ моль",value=21.17)
        x0_nm = streamlit.number_input("х0, нм",value=0.57)
        a0_mmoll_gr = streamlit.number_input("а0, ммоль/г",value=18.92)
        E_kDg_moll = streamlit.number_input("E,  кДж/моль",value=6.99)
        SBAT_m2_gr = streamlit.number_input("SБЭТ, м2/г",value=1516)
        Ws_cm3_gr = streamlit.number_input("Ws, см3/г",value=0.65)
        Sme_m2_gr = streamlit.number_input("Sme, м2/г",value=6)
        Wme_cm3_gr = streamlit.number_input("Wme, см3/г",value=0.37)


    if clicked == 1:

        Temp_reg_C = streamlit.number_input("Tрег, ᵒС", value=300)
        W0_cm3_g = streamlit.number_input("W0, см3/г", value=0.180649647)
        E0_KDG_moll = streamlit.number_input("E0, кДж/ моль", value=37.39379277)
        x0_nm = streamlit.number_input("х0, нм", value=0.320908876)
        a0_mmoll_gr = streamlit.number_input("а0, ммоль/г", value=5.21)
        E_kDg_moll = streamlit.number_input("E,  кДж/моль", value=12.34)
        SBAT_m2_gr = streamlit.number_input("SБЭТ, м2/г", value=440)
        Ws_cm3_gr = streamlit.number_input("Ws, см3/г", value=0.192187243)
        Sme_m2_gr = streamlit.number_input("Sme, м2/г", value=40)
        Wme_cm3_gr = streamlit.number_input("Wme, см3/г", value=0.011537596)

    if clicked == 2:

        Temp_reg_C = streamlit.number_input("Tрег, ᵒС", value=230)
        W0_cm3_g = streamlit.number_input("W0, см3/г", value=0.46)
        E0_KDG_moll = streamlit.number_input("E0, кДж/ моль", value=49.92)
        x0_nm = streamlit.number_input("х0, нм", value=0.24)
        a0_mmoll_gr = streamlit.number_input("а0, ммоль/г", value=13.2)
        E_kDg_moll = streamlit.number_input("E,  кДж/моль", value=16.47)
        SBAT_m2_gr = streamlit.number_input("SБЭТ, м2/г", value=1140)
        Ws_cm3_gr = streamlit.number_input("Ws, см3/г", value=0.58)
        Sme_m2_gr = streamlit.number_input("Sme, м2/г", value=52)
        Wme_cm3_gr = streamlit.number_input("Wme, см3/г", value=0.12)


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