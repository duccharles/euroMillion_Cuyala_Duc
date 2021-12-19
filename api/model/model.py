from api.predict import predict
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

def check_duplicates(numbers, star_numbers):
    """
        Checks for duplicates in the numbers and star_numbers
        
        Args:
            numbers: numbers chosen by the user
            star_numbers: star number chosen by the user
            
        Returns
            no_duplicates: boolean return value
    """
    no_duplicates = True
    numbers_duplicates = set(x for x in numbers)
    star_numbers_duplicates = set(x for x in star_numbers)
    if (len(numbers) != len(numbers_duplicates) or len(star_numbers) != len(star_numbers_duplicates)):
        no_duplicates = False
    return (no_duplicates)

def check_numbers_validity(numbers, star_numbers):
    """
        Checks the validity of the numbers
        
        Args:
            numbers: numbers chosen by the user
            star_numbers: star number chosen by the user
            
        Returns
            valid_numbers: boolean return value
    """
    valid_numbers = True
    for n in numbers:
        if (predict.min_number > n or n > predict.max_number):
            valid_numbers = False
    for s_n in star_numbers:
        if (predict.min_star_number > s_n or s_n > predict.max_star_number):
            valid_numbers = False
    return (valid_numbers)

def check_choice_validity(chosen_numbers: predict.Numbers, chosen_star_numbers: predict.StarNumbers):
    """
        Checks the validity of the choice
        
        Args:
            numbers: numbers chosen by the user
            star_numbers: star number chosen by the user
            
        Returns
            valid_choice: boolean return value
    """
    valid_choice = True
    numbers = []
    star_numbers = []
    for n in chosen_numbers:
        numbers.append(n)
    for s_n in chosen_star_numbers:
        star_numbers.append(s_n)
    print(numbers)
    no_duplicates = check_duplicates(numbers, star_numbers)
    valid_numbers = check_numbers_validity(numbers, star_numbers)
    valid_choice = no_duplicates and valid_numbers
    return valid_choice

@router.get("/api/model/")
async def get_technical_informations():
    """
        Returns technical informations about the model
        
        Args:
            
        Returns
            message: string return value
    """
    model = pickle.load(open("datasource/saved_model.pickle","rb"))
    tn, fp, fn, tp = confusion_matrix(model[4],model[5]).ravel()
    acc = accuracy_score(model[4],model[5])
    return {"Algorithm": "RandomForestClassifier",
            "Training setting": "X_train, y_train",
            "Performance critics": {"True negatives": int(tn),
                                    "False negatives": int(fn),
                                    "True positives": int(tp),
                                    "False positives:": int(fp),
                                    "Accuracy score": float(acc)
                                    }
            }

@router.put("/api/model/")
async def add_new_data(draw_data: DrawData):
    """
        Add new data to the csv
        
        Args:
            draw_data: value to be added to the csv
            
        Returns
            message: string return value
    """
    draw_data_chosen_numbers: predict.Numbers = [draw_data.number_1,
                                                 draw_data.number_2,
                                                 draw_data.number_3,
                                                 draw_data.number_4,
                                                 draw_data.number_5]
    draw_data_chosen_star_numbers: predict.Numbers = [draw_data.star_number_1,
                                                      draw_data.star_number_2]
    numbers = []
    star_numbers = []
    for n in draw_data_chosen_numbers:
        numbers.append(n)
    for s_n in draw_data_chosen_star_numbers:
        star_numbers.append(s_n)
    valid_choice = check_choice_validity(numbers,star_numbers)
    if valid_choice:
        draw_values = open('datasource/test_values.csv','a')
        draw_data_dict = draw_data.dict()
        draw_values.write(','.join(map(str,draw_data_dict.values())))
        draw_values.write('\n')
        draw_values.close() 
        return {"message": "New data added"}
    else:
        return {"message": "Invalid input, this data can't be added"}