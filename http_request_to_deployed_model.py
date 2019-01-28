import requests
import json
import pandas as pd
import os


def get_data(path_to_prediction_data):
    return pd.read_csv(path_to_prediction_data)


def drop_columns(data, columns_to_drop):
    return data.drop(columns=columns_to_drop)


def convert_data_to_json_format(X):
    X_list = X.values.tolist()
    return '{\"data\": ' + str(X_list) + '}'


def make_resquest(uri, input_data, headers):
    return requests.post(uri, input_data, headers=headers)


def filter_resp(resp):
    return eval(eval(resp.text))


def combine_actual_with_output(target_name, data, model_output, compare_output_to_actual):
    prediction = pd.DataFrame()
    if compare_output_to_actual:
        prediction['actual_'+target_name] = data[target_name].copy()

    prediction['prediction_'+target_name] = model_output
    return prediction


def save_model_output(prediction, folder, filename):
    os.makedirs(folder, exist_ok=True)
    prediction.to_csv(folder+'/'+filename, index=False)


if __name__=='__main__':
    uri = os.getenv('URI')
    compare_output_to_actual = True
    path_to_prediction_data = 'data/test.csv'
    target_name = 'SalePrice'
    columns_to_drop=[target_name]
    headers = {'Content-Type':'application/json'}
    model_output_folder = 'prediction'
    model_output_filename = 'prediction_made_on_test.csv'
    # for AKS deployment you'd need to the service key in the header as well
    # api_key = service.get_key()
    # headers = {'Content-Type':'application/json',  'Authorization':('Bearer '+ api_key)}

    data = get_data(path_to_prediction_data)
    X = drop_columns(data, columns_to_drop)
    input_data = convert_data_to_json_format(X)
    resp = make_resquest(uri, input_data, headers)
    model_output = filter_resp(resp)
    prediction = combine_actual_with_output(target_name, data, model_output, compare_output_to_actual)
    save_model_output(prediction, model_output_folder, model_output_filename)
