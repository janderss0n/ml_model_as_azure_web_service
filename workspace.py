import os
from azureml.core.workspace import Workspace


# def create_workspace_and_config_file(subscription_id,
#         ws_name,
#         ws_resource_group,
#         ws_location):
def create_workspace_and_config_file(subscription_id):
    ws = Workspace.create(subscription_id=subscription_id,
                         name='test',
                         resource_group='rg_test',
                         create_resource_group=True,
                         location='westeurope')
    ws.write_config()


def delete_workspace(ws):
    ws.delete(delete_dependent_resources=True)


def load_workspace_from_config():
    return Workspace.from_config()


def print_workspace_info(ws):
    print('Workspace info \n', ws.get_details())


def check_if_workspace_config_exists():
    ws_config_exists = False
    if os.path.exists('./aml_config/config.json'):
        ws_config_exists = True
    return ws_config_exists
