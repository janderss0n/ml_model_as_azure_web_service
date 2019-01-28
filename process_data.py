import os
import pandas as pd
from sklearn.model_selection import train_test_split


data = pd.read_csv('train.csv')
data = data.loc[:,data.isna().sum()==0]
data = data.select_dtypes(['number'])
X = data.drop(columns=['SalePrice'])
y = data.SalePrice

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=223)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=223)

os.makedirs('data', exist_ok=True)
train = X_train.copy()
train['SalePrice'] = y_train
train.to_csv('data/train.csv', index=False)

test = X_test.copy()
test['SalePrice'] = y_test
test.to_csv('data/test.csv', index=False)

val = X_val.copy()
val['SalePrice'] = y_val
val.to_csv('data/val.csv', index=False)
