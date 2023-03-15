'''
Try implementing a random forest too. This will give us feature importance.

X will be each of the columns of the CSV
y will be the role-type (dan, laodan, laosheng) which is the name of the file
'''

import pandas as pd
import numpy as np
import time

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

import matplotlib.pyplot as plt



def load_data(CSVs):
    '''
    Input: 
        CSVs - [csv_file]
    Returns:
        X - features of all the entries in the CSVs
        y - labels 
    '''

    X = []
    y = []

    if not isinstance(CSVs, list):
        # TODO - make this an exception instead of just a print
        print('Error: CSVs must be a list.')
        return

    for csv_file in CSVs:
        # read csv
        df = pd.read_csv(csv_file)
        print(f'Length of {csv_file}: {df.shape[0]}')

        label = csv_file[12:-4] # cut out the "idh_" and ".csv"
        # labels = [label] * df.shape[0] # same label for whole CSV file

        # for loop is to preserve shape
        for index, row in df.iterrows(): 
            X.append(row[1:]) # column 0 is ID, not a feature
            y.append(label)

    X = np.array(X)
    y = np.array(y)
    print(f'Done loading data! \nShape of X: {X.shape} \nShape of y: {y.shape}')
    return X, y

def train(X_train, y_train):
    forest = RandomForestClassifier(random_state=0)
    forest.fit(X_train, y_train)
    return forest

def compute_importances_on_impurity(forest, X):
    feature_names = [f"feature {i}" for i in range(X.shape[1])]
    start_time = time.time()
    importances = forest.feature_importances_
    std = np.std([tree.feature_importances_ for tree in forest.estimators_], axis=0)
    elapsed_time = time.time() - start_time

    print(f"Elapsed time to compute the importances: {elapsed_time:.3f} seconds")

    forest_importances = pd.Series(importances, index=feature_names)

    fig, ax = plt.subplots()
    forest_importances.plot.bar(yerr=std, ax=ax)
    ax.set_title("Feature importances using MDI")
    ax.set_ylabel("Mean decrease in impurity")
    fig.tight_layout()
    plt.show()

def test(forest, X_test, y_test):
    y_pred = forest.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    return accuracy
    

if __name__ == '__main__':
    CSVs = [
        '../data/ihd_dan.csv',
        '../data/ihd_laosheng.csv',
    ]
    X, y = load_data(CSVs)
    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=42)

    forest = train(X_train, y_train)
    print('Done training.')

    acc = test(forest, X_test, y_test)
    print(f'Accuracy: {acc}')

    compute_importances_on_impurity(forest, X)