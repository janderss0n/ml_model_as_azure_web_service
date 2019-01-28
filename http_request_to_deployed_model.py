import requests
import json
import pandas as pd
import os

uri = your_web_service_uri_here

data = pd.read_csv('data/test.csv')
X_pred = data.drop(columns=['SalePrice'])
X_pred_list = X_pred.values.tolist()

# send a random row from the test set to score
input_data = '{\"data\": ' + str(X_pred_list) + '}'

headers = {'Content-Type':'application/json'}

# for AKS deployment you'd need to the service key in the header as well
# api_key = service.get_key()
# headers = {'Content-Type':'application/json',  'Authorization':('Bearer '+ api_key)}

resp = requests.post(uri, input_data, headers=headers)
pred_output = eval(eval(resp.text))

print('POST to url', uri)
#print('input data:', input_data)
#print('label:', data.SalePrice)
#print('********')
#print('prediction:', pred_output)

os.makedirs('prediction', exist_ok=True)
prediction = pd.DataFrame()
prediction['actual_salePrice'] = data.SalePrice.copy()
prediction['prediction_salePrice'] = pred_output
prediction.to_csv('prediction/prediction_made_on_test.csv', index=False)
