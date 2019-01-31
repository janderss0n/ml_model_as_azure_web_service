import pandas as pd
import requests
import json
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go


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


def generate_table(dataframe, max_rows=10):
    return [
        html.H4(children='Table over a few rows of the data'),
        html.Table(
            [html.Tr(
                [html.Th(col) for col in dataframe.columns]
            )] +
            [html.Tr(
                [html.Td(dataframe.iloc[i][col]) for col in dataframe.columns]
            ) for i in range(min(len(dataframe), max_rows))]
        )
    ]


def generate_pred_actual_plot(df):
    return [
        html.H4(children='Comparison: prediction vs actual'),
        dcc.Graph(
            id='life-exp-vs-gdp',
            figure={
                'data': [
                    go.Scatter(
                        x=df.loc[df.YrSold == i, 'SalePrice'],
                        y=df.loc[df.YrSold == i, 'prediction'],
                        text=str(df.loc[df.YrSold == i, 'YrSold']),
                        mode='markers',
                        opacity=0.7,
                        marker={
                            'size': 15,
                            'line': {'width': 0.5, 'color': 'white'}
                        },
                        name=str(i)
                    ) for i in df.YrSold.unique()
                ],
                'layout': go.Layout(
                    xaxis={'type': 'log', 'title': 'Actual Sale Price'},
                    yaxis={'title': 'Prediction'},
                    margin={'l': 60, 'b': 40, 't': 10, 'r': 10},
                    legend={'x': 0, 'y': 1},
                    hovermode='closest'
                )
            }
        )
    ]


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    dcc.Input(
        id='model-uri',
        value='http://xx.xxx.xxx.xxx:xx/score',
        type='text'
    ),
    dcc.Input(
        id='data-path',
        value='path/filename.csv',
        type='text'
    ),
    html.Div(id = 'table-and-plot')
])


def make_prediction(data, model_uri):
    headers = {'Content-Type':'application/json'}
    X = convert_data_to_json_format(drop_columns(data, columns_to_drop='SalePrice'))
    return filter_resp(make_resquest(model_uri, X, headers))


def generate_table_and_plot(data):
    return (html.Div(generate_table(data)), html.Div(generate_pred_actual_plot(data)))


@app.callback(Output('table-and-plot', 'children'),
    [Input('model-uri', 'value'), Input('data-path', 'value')])
def uppdate_prediction(model_uri, data_path):
    new_data = get_data(data_path)
    new_data['prediction'] = make_prediction(new_data, model_uri)
    return generate_table_and_plot(new_data)


if __name__=='__main__':
    app.run_server(debug=True)
