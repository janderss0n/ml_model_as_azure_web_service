import os
import pickle as pkl
from azureml.core.model import Model
from azureml.core.image import Image
from azureml.core.image import ContainerImage
from azureml.core.webservice import Webservice
from azureml.core.webservice import AciWebservice
from azureml.core.conda_dependencies import CondaDependencies

from workspace import check_if_workspace_config_exists, \
                    create_workspace_and_config_file, \
                    load_workspace_from_config


def azure_register_model_and_deploy_as_web_service(subscription_id,
                                workspace_settings, service_settings,
                                model_settings, score_filename,
                                environment_filename, container_settings):

    ws = get_workspace(subscription_id, workspace_settings)
    model = load_and_register_model_from_local_file(ws, **model_settings)

    aciconfig = create_container_config_file(container_settings)
    create_score_file(score_filename)
    create_env_file(environment_filename)
    image_config = create_container_image(execution_script=score_filename, conda_env_file=environment_filename)

    if service_settings['create_new_service']:
        deploy_new_web_service(ws, service_settings['service_name'], aciconfig, image_config, model)
    else:
        print('TO DO: create a function where you can update the webservice with new image. \
            The from azureml.core.webservice import Webservice class has an update function.')



def get_workspace(subscription_id, workspace_settings):
    if not check_if_workspace_config_exists():
        create_workspace_and_config_file(subscription_id, **workspace_settings)

    return load_workspace_from_config()


def create_score_file(score_filename):
    f = open(score_filename,'w+')
    f.write('''import json
import numpy as np
import os
import pickle
from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression

from azureml.core.model import Model

def init():
    global model
    # retrieve the path to the model file using the model name
    model_path = Model.get_model_path('name_test_model')
    model = joblib.load(model_path)

def run(raw_data):
    data = np.array(json.loads(raw_data)['data'])
    # make prediction
    y_hat = model.predict(data)
    return json.dumps(y_hat.tolist())''')
    f.close()


def create_env_file(environment_filename):
    f = open(environment_filename,'w+')
    f.write('''name: project_environmen
dependencies:
# The python interpreter version.
# Currently Azure ML only supports 3.5.2 and later.
- python=3.6.2

- pip:
    # Required packages for AzureML execution, history, and data preparation.
  - azureml-defaults
  - scikit-learn
  - numpy
  - pandas''')
    f.close()


def create_container_config_file(container_settings):
    return AciWebservice.deploy_configuration(**container_settings)


def create_container_image(execution_script, conda_env_file):
    return ContainerImage.image_configuration(execution_script=execution_script,
                                                      runtime='python',
                                                      conda_file=conda_env_file)


def load_and_register_model_from_local_file(workspace, local_model_path,
                                            azure_model_name):
    return Model.register(model_path=local_model_path,
                        model_name=azure_model_name,
                        workspace=workspace)


def deploy_new_web_service(workspace, service_name, aciconfig, image_config, model):
    service = Webservice.deploy_from_model(workspace=workspace,
                                           name=service_name,
                                           deployment_config=aciconfig,
                                           models=[model],
                                           image_config=image_config)

    service.wait_for_deployment(show_output=True)
    print('The URI to access the web service is: ', service.scoring_uri)


if __name__=='__main__':
    subscription_id = os.getenv('SUBSCRIPTION_ID')
    workspace_settings = {'ws_name': 'myworkspace',
        'ws_resource_group': 'myresourcegroup',
        'ws_location': 'westeurope'
    }
    service_settings = {
        'service_name': 'testdeploy',
        'create_new_service': True
    }
    score_filename = 'score.py'
    environment_filename = 'myenv.yml'
    container_settings = {
        'cpu_cores': 1,
        'memory_gb': 1,
        'tags': {'data': 'SalePrice'},
        'description': 'Describe your container here'
    }
    model_settings = {
        'local_model_path': 'outputs/test_model.pkl',
        'azure_model_name': 'name_test_model'
    }

    azure_register_model_and_deploy_as_web_service(subscription_id,
                                    workspace_settings, service_settings,
                                    model_settings, score_filename,
                                    environment_filename, container_settings)
