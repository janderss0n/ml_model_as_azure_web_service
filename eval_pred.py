import matplotlib
matplotlib.use('TkAgg')

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

prediction = pd.read_csv('prediction/prediction_made_on_train.csv')

plt.figure()
plt.scatter(prediction.actual_salePrice, prediction.prediction_salePrice)
plt.plot([0,700000],[0,700000], color='black')
plt.show()

print(r2_score(prediction.actual_salePrice, prediction.prediction_salePrice))
