'''
Train, test, and extract feature importance for a de
'''

import pandas as pd
import numpy as np
import time

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

import matplotlib.pyplot as plt

CSVs = {
    'role_type': {
        'dan': [
            '../data/role_type/ihd_dan.csv',
            '../data/role_type/melodic_density_duration_dan.csv',
            '../data/role_type/melodic_density_notes_dan.csv',
            '../data/role_type/pitch_dan.csv',
        ],
        'laosheng': [
            '../data/role_type/ihd_laosheng.csv',
            '../data/role_type/melodic_density_duration_laosheng.csv',
            '../data/role_type/melodic_density_notes_laosheng.csv',
            '../data/role_type/pitch_laosheng.csv',
        ]
    },
    'shengqiang': {
        'erhuang': [
            '../data/shengqiang/ihd_erhuang.csv',
            '../data/shengqiang/melodic_density_duration_erhuang.csv',
            '../data/shengqiang/melodic_density_notes_erhuang.csv',
            '../data/shengqiang/pitch_erhuang.csv',
        ],
        'xipi': [
            '../data/shengqiang/ihd_xipi.csv',
            '../data/shengqiang/melodic_density_duration_xipi.csv',
            '../data/shengqiang/melodic_density_notes_xipi.csv',
            '../data/shengqiang/pitch_xipi.csv',
        ]
    },
}


def load_data(CSVs, features):
    '''
    Input: 
        CSVs - [csv_file]
        feaures - role_type, shengqiang, or banshi
    Returns:
        X - features of all the entries in the CSVs
        y - labels 
    '''

    X = []
    y = []

    if not isinstance(CSVs, object):
        # TODO - make this an exception instead of just a print
        print('Error: CSVs must be an object.')
        return
    
    column_names = None # bad code
    
    print(f'features to train on: {features}')
    for subtype in CSVs[features].keys():
        print(f'role type: {subtype}')
        for csv in CSVs[features][subtype]:
            print(f'csv {csv}')

        df_ihd = pd.read_csv(CSVs[features][subtype][0], index_col=0)
        df_mel_den = pd.read_csv(CSVs[features][subtype][1], index_col=0)
        df_mel_notes = pd.read_csv(CSVs[features][subtype][2], index_col=0)
        df_pitch = pd.read_csv(CSVs[features][subtype][3], index_col=0)

        merged_df = pd.merge(df_ihd, df_mel_den, how='inner', left_index=True, right_index=True)
        merged_df = pd.merge(merged_df, df_mel_notes, how='inner', left_index=True, right_index=True)
        merged_df = pd.merge(merged_df, df_pitch, how='inner', left_index=True, right_index=True)

        # Drop NaN rows
        merged_df.dropna(inplace=True)

        column_names = merged_df.columns.to_numpy()

        for index, row in merged_df.iterrows(): 
            X.append(row)
            y.append(subtype)

    X = np.array(X)
    y = np.array(y)
    print(f'Done loading data! \nShape of X: {X.shape} \nShape of y: {y.shape}')
    return X, y, column_names


def train(X_train, y_train, model_name):
    # Initialize
    forest = RandomForestClassifier(random_state=0)
    forest.fit(X_train, y_train)

    # Save model weights to file
    joblib.dump(forest, model_name)

def compute_importances_on_impurity(column_names, model_name):
    forest = joblib.load(model_name)
    # Bad hardcoded labels
    # feature_names = pd.read_csv('../data/ihd_dan.csv').columns[1:]

    # feature_names = [f"feature {i}" for i in range(X.shape[1])]
    start_time = time.time()
    importances = forest.feature_importances_
    std = np.std([tree.feature_importances_ for tree in forest.estimators_], axis=0)
    elapsed_time = time.time() - start_time

    print(f"Elapsed time to compute the importances: {elapsed_time:.3f} seconds")

    forest_importances = pd.Series(importances, index=column_names)

    fig, ax = plt.subplots()
    forest_importances.plot.bar(yerr=std, ax=ax)
    ax.set_title(f"Feature importances using MDI, model: {model_name}")
    ax.set_ylabel("Mean decrease in impurity")
    fig.tight_layout()
    plt.show()

def test(X_test, y_test, model_name):
    # Load from saved model weights file
    forest = joblib.load(model_name)
    y_pred = forest.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    return accuracy
    

if __name__ == '__main__':

    # ----- Role Type Model -----

    # Data loading and preparing
    X, y, column_names = load_data(CSVs, features='role_type')
    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=42)

    # Training the model
    train(X_train, y_train, 'role_type_model.joblib')
    print('Done training role type.')

    # Testing the model
    acc = test(X_test, y_test, 'role_type_model.joblib')
    print(f'Role Type Accuracy: {acc}')

    # Feature importance
    compute_importances_on_impurity(column_names, 'role_type_model.joblib')

    
    # ----- Shengqiang Model -----

    # Data loading and preparing
    X, y, column_names = load_data(CSVs, features='shengqiang')
    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=42)

    # Training the model
    train(X_train, y_train, 'shengqiang_model.joblib')
    print('Done training shengqiang.')

    # Testing the model
    acc = test(X_test, y_test, 'shengqiang_model.joblib')
    print(f'Shengqiang Accuracy: {acc}')

    # Feature importance
    compute_importances_on_impurity(column_names, 'shengqiang_model.joblib')