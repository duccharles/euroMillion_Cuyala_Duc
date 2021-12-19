from fastapi import APIRouter
from pydantic import BaseModel
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
import pickle

router = APIRouter()

class DrawData(BaseModel):
    date: str
    number_1: int
    number_2: int
    number_3: int
    number_4: int
    number_5: int
    star_number_1: int
    star_number_2: int
    winner: int
    gain: int

@router.get("/api/model/")
async def get_technical_informations():
    model = pickle.load(open("datasource/saved_model.pickle","rb"))
    tn, fp, fn, tp = confusion_matrix(model[4],model[5]).ravel()
    print(tn,fp,fn,tp)
    acc = accuracy_score(model[4],model[5])
    print(acc)     
    return {"message": "test"}

@router.put("/api/model/")
async def add_new_data(draw_data: DrawData):
    draw_values = open('datasource/test_values.csv','a')
    draw_data_dict = draw_data.dict()
    draw_values.write(','.join(map(str,draw_data_dict.values())))
    draw_values.write('\n')
    draw_values.close() 
    return {"message": "New data added"}