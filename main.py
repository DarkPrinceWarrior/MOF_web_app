import pickle

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import pandas as pd
import numpy as np

app = FastAPI()

# don't need while used streamlit
# app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")

pkl_filename = "app/saved_models/Multi_RegressionModel.pkl"
with open(pkl_filename, 'rb') as file1:
    model = pickle.load(file1)

pkl_filename_2 = "app/saved_models/saved_id2cat.pkl"
with open(pkl_filename_2, 'rb') as file2:
    id2cat = pickle.load(file2)


class Data(BaseModel):
    """adsorbent information according to СЭХ

    Tрег, ᵒС <class 'numpy.int64'>
    W0, см3/г <class 'numpy.float64'>
    E0, кДж/ моль <class 'numpy.float64'>
    х0, нм <class 'numpy.float64'>
    а0, ммоль/г <class 'numpy.float64'>
    E,  кДж/моль <class 'numpy.float64'>
    SБЭТ, м2/г <class 'numpy.float64'>
    Ws, см3/г <class 'numpy.float64'>
    Sme, м2/г <class 'float'>
    Wme, см3/г <class 'numpy.float64'>
    """

    Temp_reg_C: int
    W0_cm3_g: float
    E0_KDG_moll: float
    x0_nm: float
    a0_mmoll_gr: float
    E_kDg_moll: float
    SBAT_m2_gr: float
    Ws_cm3_gr: float
    Sme_m2_gr: float
    Wme_cm3_gr: float


@app.get("/")
async def root(request: Request):
    return "Hello world!!!"
    # return templates.TemplateResponse("index.html",
    #                                   {"request": request})


@app.post("/predict")
def predict(data: Data):
    new_data = np.array([data.Temp_reg_C,
                       data.W0_cm3_g,
                       data.E0_KDG_moll,
                       data.x0_nm,
                       data.a0_mmoll_gr,
                       data.E_kDg_moll,
                       data.SBAT_m2_gr,
                       data.Ws_cm3_gr,
                       data.Sme_m2_gr,
                       data.Wme_cm3_gr]).reshape(1, 10)

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

    prediction = {key:value for key,value in zip(prediction_column_names,result.values[0])}
    # get the correct answer with decoded column values
    return prediction
