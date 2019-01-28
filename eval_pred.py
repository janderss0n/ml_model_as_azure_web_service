import matplotlib
matplotlib.use('TkAgg')

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score


def evaluate_result(data):
    print(r2_score(prediction.actual_SalePrice, prediction.prediction_SalePrice))

    plt.figure()
    plt.scatter(prediction.actual_SalePrice, prediction.prediction_SalePrice)
    plt.plot([0,700000],[0,700000], color='black')
    plt.show()



if __name__=='__main__':
    prediction_path = 'prediction'
    prediction_actual_filename = 'prediction_made_on_test.csv'

    prediction = pd.read_csv(prediction_path+'/'+prediction_actual_filename)
    evaluate_result(prediction)
