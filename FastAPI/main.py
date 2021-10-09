from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from ml import predict
import sklearn
import json
import pickle
import xgboost as xgb


class Growler(BaseModel):
    data: str
    temp_media: float
    temp_minima: float
    temp_maxima: float
    precipitacao: float
    final_de_semana: float


app = FastAPI()
bst = xgb.XGBRegressor()
bst.load_model('./extras/models/final_model.model')  # load data
sc = pickle.load(open('./extras/scaler/std_scaler.pickle', 'rb'))


@app.post("/pred/growler")
async def predict_model(dataset: Growler):
    try:
        prediction = predict.predict(dataset.dict(), bst, sc)
        return {"data": dataset, "prediction": prediction}

    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)
