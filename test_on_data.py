import pandas as pd
import random


# importation des données
df = pd.read_csv("EuroMillions_numbers.csv", sep = ';')


# Ajout d'une colonne pour dire que ce sont des tirages gagnant
df = df.assign(Winning=True)
print(df)

# Création de tirage perdant pour entrainer le modéle
len_tot = df.shape[0] / 0.2
print(len_tot)
len_missing = len_tot - df.shape[0]
print(len_missing)

def makeLoosingData():
    tab_numbers = []
    for i in range(5):
        number = random.randint(1,50)
        allgood = False
        while not allgood:
            allgood = True
            rand = False
            for j in range(len(tab_numbers)):
                if number == tab_numbers[j]:
                    rand = True
            if rand:
                number = random.randint(1,50)
                allgood = False
        tab_numbers.append(number)
    for i in range(2):
        number = random.randint(1,12)
        allgood = False
        while not allgood:
            allgood = True
            rand = False
            for j in range(len(tab_numbers)):
                if number == tab_numbers[j]:
                    rand = True
            if rand:
                number = random.randint(1,12)
                allgood = False
        tab_numbers.append(number)
    return tab_numbers

# Ajout des tirages perdant afin d'avoir un 80% perdant 20% gagnant
line = 1318
for i in range(5272):
  tab_numbers = makeLoosingData()
  df.loc[line] = [None, tab_numbers[0],tab_numbers[1],tab_numbers[2], tab_numbers[3],tab_numbers[4],tab_numbers[5],tab_numbers[6],0, 0, False]
  line += 1

print(df)

# On prend les colonnes du dataframe qui nous intéresse
data_numbers = df[['N1','N2','N3','N4','N5','E1','E2']]
data_winning = df['Winner']

# importation des librairies qui nous intéresse
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# split des données
def splitDonnees(test_size):
    X_train, X_test, y_train, y_test = train_test_split(data_numbers, data_winning, test_size=test_size, random_state=0)
    return [X_train, X_test, y_train, y_test]

# Ajout dans variable global des données
test_size = 0.2
donnee = splitDonnees[test_size]
X_train = donnee[0]
X_test = donnee[1]
y_train = donnee[2]
y_test = donnee[3]


# tirage a prédire
tab_numbers = makeLoosingData()
tirage = pd.DataFrame({'N1': tab_numbers[0], 'N2':tab_numbers[1],'N3':tab_numbers[2], 'N4':tab_numbers[3],'N5':tab_numbers[4],'E1':tab_numbers[5],'E2':tab_numbers[6]},index = ['1'])
# modèle Naive Bayes
from sklearn.naive_bayes import GaussianNB
def naiveBaye(tirage):
    model = GaussianNB()
    model = model.fit(X_train, y_train)
    prediction = model.predict(tirage)
    return prediction

# modèle arbre de décision
from sklearn import tree
def arbreDecision(tirage):
    model = tree.DecisionTreeClassifier()
    model = model.fit(X_train, y_train)
    prediction = model.predict(X_test)
    return prediction


# modèle random forest 
from sklearn.ensemble import RandomForestClassifier
def randomTree(tirage):
    model = RandomForestClassifier(n_estimators= 10)
    model = model.fit(X_train, y_train)

    prediction = model.predict(X_test)
    return prediction