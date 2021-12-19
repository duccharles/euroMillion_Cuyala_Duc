from numpy.core.fromnumeric import size
from fastapi import APIRouter
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import random
import pickle

router = APIRouter()

min_number = 1
max_number = 50
min_star_number = 1
max_star_number = 12
total_numbers = 5
total_star_numbers = 2

losing_lines = 5272

test_size = 0.2
random_state = 0

csv_source = "datasource/EuroMillions_numbers.csv"

def make_new_data():
    """
        Creates a randow draw of numbers
        
        Args:
            
        Returns
            tab_numbers: array of int return value
    """
    tab_numbers = []
    for i in range(total_numbers):
        number = random.randint(min_number,max_number)
        all_good = False
        while not all_good:
            all_good = True
            rand = False
            for j in range(len(tab_numbers)):
                if number == tab_numbers[j]:
                    rand = True
            if rand:
                number = random.randint(min_number,max_number)
                all_good = False
        tab_numbers.append(number)
    for i in range(total_star_numbers):
        number = random.randint(min_star_number,max_star_number)
        all_good = False
        while not all_good:
            all_good = True
            rand = False
            for j in range(len(tab_numbers)):
                if number == tab_numbers[j]:
                    rand = True
            if rand:
                number = random.randint(min_star_number,max_star_number)
                all_good = False
        tab_numbers.append(number)
    return tab_numbers

def init_dataframe():
    """
        Initialize the dataframe with the csv file
        
        Args:
            
        Returns
            df: dataframe return value
    """
    df = pd.read_csv(csv_source, sep=";")
    df = df.assign(Winning=True)
    winning_lines = 1318
    for i in range(losing_lines):
        tab_numbers = make_new_data()
        df.loc[winning_lines] = [None, 
                                 tab_numbers[0],
                                 tab_numbers[1],
                                 tab_numbers[2],
                                 tab_numbers[3],
                                 tab_numbers[4],
                                 tab_numbers[5],
                                 tab_numbers[6],
                                 0,
                                 0,
                                 False
                                ]
        winning_lines += 1
    return df

def train_model():
    """
        Train the model
        
        Args:
            
        Returns
            model: string return value about the model
            X_train: training draws  
            X_test: testing draws
            y_train: training results
            y_test: testing results
            performance_metrics: performance_metrics return value
    """
    draw_values_df = init_dataframe()
    data_numbers = draw_values_df[['N1','N2','N3','N4','N5','E1','E2']]
    data_winning = draw_values_df['Winning']
    X_train, X_test, y_train, y_test = train_test_split(data_numbers, data_winning, test_size = test_size, random_state=random_state)
    model = RandomForestClassifier(n_estimators = 10)
    model = model.fit(X_train, y_train)
    performance_metrics = RandomForestClassifier(n_estimators = 10)
    performance_metrics = model.fit(X_train, y_train)
    performance_metrics = performance_metrics.predict(X_test)
    return model, X_train, X_test, y_train, y_test, performance_metrics
    
    
@router.post("/api/model/retrain/")
async def retrain_model():
    """
        Retrain the model
        
        Args:
            
        Returns
            message: string return value
    """
    model = train_model()
    pickle.dump(model,open("datasource/saved_model.pickle","wb"))
    return {"message": "Model has been trained and saved"}