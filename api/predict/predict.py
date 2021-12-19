from numpy.core.records import array
from fastapi import APIRouter
from pydantic import BaseModel
from api.model.retrain import retrain
import pickle
import pandas as pd

router = APIRouter()

min_number = 1
max_number = 50
min_star_number = 1
max_star_number = 12
total_numbers = 5
total_star_numbers = 2


class Numbers(BaseModel):
    number_1:int
    number_2:int
    number_3:int
    number_4:int
    number_5:int
    
class StarNumbers(BaseModel):
    star_number_1: int
    star_number_2: int
    

def check_duplicates(numbers, star_numbers):
    no_duplicates = True
    numbers_duplicates = set(x[1] for x in numbers)
    star_numbers_duplicates = set(x[1] for x in star_numbers)
    if (len(numbers) != len(numbers_duplicates) or len(star_numbers) != len(star_numbers_duplicates)):
        no_duplicates = False
    return (no_duplicates)

def check_numbers_validity(numbers, star_numbers):
    valid_numbers = True
    for n in numbers:
        if (min_number > n[1] or n[1] > max_number):
            valid_numbers = False
    for s_n in star_numbers:
        if (min_star_number > s_n[1] or s_n[1] > max_star_number):
            valid_numbers = False
    return (valid_numbers)

def check_choice_validity(chosen_numbers: Numbers, chosen_star_numbers: StarNumbers):
    valid_choice = True
    numbers = []
    star_numbers = []
    for n in chosen_numbers:
        numbers.append(n)
    for s_n in chosen_star_numbers:
        star_numbers.append(s_n)
    no_duplicates = check_duplicates(numbers, star_numbers)
    valid_numbers = check_numbers_validity(numbers, star_numbers)
    valid_choice = no_duplicates and valid_numbers
    return valid_choice

@router.post("/api/predict/")
async def check_if_winning_numbers(chosen_numbers: Numbers, chosen_star_numbers: StarNumbers):
    valid_choice = check_choice_validity(chosen_numbers, chosen_star_numbers)
    print(chosen_numbers)
    print(chosen_star_numbers)
    if valid_choice:
        chosen_draw = pd.DataFrame(columns=['N1','N2','N3','N4','N5','E1','E2'])
        chosen_draw = chosen_draw.append({"N1":chosen_numbers.number_1,
                                          "N2":chosen_numbers.number_2,
                                          "N3":chosen_numbers.number_3,
                                          "N4":chosen_numbers.number_4,
                                          "N5":chosen_numbers.number_5,
                                          "E1":chosen_star_numbers.star_number_1,
                                          "E2":chosen_star_numbers.star_number_2,},ignore_index=True)  
        model = pickle.load(open("datasource/saved_model.pickle","rb"))
        test = model[0].predict_proba(chosen_draw)
        return {"Message": test[0][1]}
    else:
        return {"Invalid Numbers"}
    

@router.get("/api/predict/")
async def get_winning_numbers():
    not_good_enough = True
    while not_good_enough:
        random_draw = pd.DataFrame(columns=['N1','N2','N3','N4','N5','E1','E2'])
        new_draw = retrain.make_new_data()
        random_draw = random_draw.append({"N1":new_draw[0],
                                          "N2":new_draw[1],
                                          "N3":new_draw[2],
                                          "N4":new_draw[3],
                                          "N5":new_draw[4],
                                          "E1":new_draw[5],
                                          "E2":new_draw[6],},ignore_index=True)
        model = pickle.load(open("datasource/saved_model.pickle","rb"))
        test = model[0].predict_proba(random_draw)
        if test[0][1] >= 0.3:
            not_good_enough = False
    return {"message": test[0][1]}