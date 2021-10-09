from datetime import date
from typing import Tuple
import pandas as pd
import numpy as np
from pandas.core.frame import DataFrame


def predict(data, model, sc):
    df, datetime = __data_preprocessing(pd.DataFrame([data]))

    data_predict = sc.transform(df)
    pred = model.predict(data_predict)
    df['Consumo de cerveja (litros)'] = np.floor(np.exp(pred)).astype(int)

    df_final = pd.concat([df['Consumo de cerveja (litros)'], datetime], axis=1)

    return df_final.to_dict('records')


def __data_preprocessing(df: DataFrame) -> Tuple[DataFrame, date]:
    datetime = df['data']

    df['Date'] = pd.to_datetime(df['data'], format='%Y/%m/%d')
    df['Mes'] = df['Date'].dt.month
    df['Dia'] = df['Date'].dt.day
    df['Semana'] = df['Date'].dt.isocalendar().week
    df['DayName'] = df['Date'].dt.day_name()
    df.drop(columns='Date', inplace=True)

    df['Final de Semana'] = df['final_de_semana'].astype(float)

    df['Temperatura Maxima (C)'] = df['temp_maxima'].astype(float)

    df['Precipitacao (mm)'] = df['precipitacao'].astype(float)

    df['DayName_Sin'] = np.sin(pd.Categorical(
        df['DayName']).codes * (2. * np.pi/7))
    df['Dayname_Cos'] = np.cos(pd.Categorical(
        df['DayName']).codes * (2. * np.pi/7))

    df['logPrecipitacao (mm)'] = df['Precipitacao (mm)'].apply(np.log1p)

    df.drop(columns=[
        'data',
        'DayName',
        'temp_media',
        'temp_minima',
        'temp_maxima',
        'final_de_semana',
        'precipitacao'
    ], inplace=True)

    return df, datetime
