import pickle

import numpy as np
import pandas as pd


pkl_filename = "saved_models/Multi_RegressionModel.pkl"
with open(pkl_filename, 'rb') as file1:
    model = pickle.load(file1)

pkl_filename_2 = "saved_models/saved_id2cat.pkl"
with open(pkl_filename_2, 'rb') as file2:
    id2cat = pickle.load(file2)


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
