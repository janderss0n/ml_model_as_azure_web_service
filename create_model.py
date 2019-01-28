import os
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.externals import joblib


def get_training_data(data_dir, data_filname):
    data = pd.read_csv(data_dir+'/'+data_filname)
    X = data.drop(columns=['SalePrice'])
    y = data.SalePrice
    return X, y


def train_a_ridge_regression(X, y):
    return Ridge().fit(X, y)


def save_model_locally(model, model_dir, model_filename):
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(value=model, filename=model_dir+'/'+model_filename)


if __name__=='__main__':
    data_dir = 'data'
    data_filname = 'train.csv'
    model_dir = 'outputs'
    model_filename = 'test_model.pkl'

    X, y = get_training_data(data_dir, data_filname)
    model = train_a_ridge_regression(X, y)
    save_model_locally(model, model_dir, model_filename)
