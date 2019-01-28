# Where I learned
https://docs.microsoft.com/en-us/azure/machine-learning/service/

## Dependencies/Installations
Install azure cli
Install conda, then run the following shell commands.

conda create -n myenv -y Python=3.6
conda activate myenv #or: source activate myenv

# Install Jupyter
conda install nb_conda

# Install the base SDK and Jupyter Notebook
pip install azureml-sdk[notebooks]

# Install the base SDK and auto ml components
pip install azureml-sdk[automl]

# Install the base SDK and the model explainability component
pip install azureml-sdk[explain]

# Install the base SDK and experimental components
pip install azureml-sdk[contrib]

conda install -y cython matplotlib scikit-learn pandas numpy


# How this project is done
## OBS: If you already have a trained model saved as a pickle file, move it to a subfolder called output and go to 3 for deployment. Step 1 and 2 are simple examples of data preprocessing and model training.
1. Get the data: I downloaded the data into my directory and called the file train.csv.
Preprocess the data: I use the script called process_data.py for the data preprocessing. This script removes all columns containing nan values and removes all columns not containing numbers. This it splits the training data into a train, test and validation dataset. Each dataset is written to a csv file into a subfolder called data.

2. Train model: I use the create_model.py to create my trained model. First I load the train.csv dataset from the data folder created in 1. I train my model on this data with the target as the SalePrice column. The model is then saved as a pickle file into a subfolder called output.

3. Deploy model as a web service in Azure Machine Learning Service: The script called deploy_model_to_azure.py
will deploy the model in the output folder to Azure. You need to pass in your subscription id as an environment variable when you run the script. This is needed so we know what account on Azure to deploy to. When you do this a webpage might come up where you need to log into your account.
Workspace: First the script sets up a workspace on your azure account. For this you need to have a configuration file called config.json located in a subfolder called aml_config. If this doesn't exist the script will create the config file and then create the workspace. (All of the functions connected to the workspace is in the workspace.py file.)
Load model: Next we will have to register the model from the local pickle file.
Score file: We have to create a score.py file which will be used in the web service call to show how to use the model.
Environment file: We need to create an environment file which specifies all of the dependencies we will need.
Container Instance config file: We need a configuration file which specifies how many CPU and how much memory we will need our container instances to have. You can also add tags to you container here to make it easier to search for in the Azure GUI.
Container Image: Now we are ready to create our container image. We will need the score and the environment file for this.
Deployment: Finally we can deploy the model into the Azure Workspace using the workspace, Container Instance config file, the model and the Container Image. (#TO DO: add the possibility to update the model) Here I used the function deploy_from_model, which also uploads you image to your workspace.

If you like, you can first upload the image separately using Image.create and then deploy you azure container instance using deploy_from_image, here's a good link https://docs.microsoft.com/en-us/azure/machine-learning/service/how-to-troubleshoot-deployment.

IMPORTANT: When you run this script you will get the address to the web server (a uri) printed in your terminal. This you will need in the next step. (Look something like http://999.99.99.999:99/score)

4. Make predictions using the web server: To make predictions use the http_request_to_deployed_model.py. You need to change to your uri in the script which you got in step 3. First we will load the data that we want to make predictions on. Then we send this data as a post using the uri and we get predictions made by the model back. In this case I use the test data from step 1 which I also had the actual values for. I saved both the actual and the predictions to a csv file called prediction_made_on_test in the subdirectory called prediction.

5. Evaluation: Use the eval_pred.py to get a visualization of the prediction and r2 score.

6. Delete the workspace: When you are done you can delete the workspace. Note that this will also delete everything that is created in that workspace. Either in the Azure GUI or using the delete_workspace function in workspace.py.

## Notes
If you have created the workspace config file and then deleted the workspace in azure, you will have to delete the config file locally as well if you want to dun the deployment again. #TO DO: If a workspace config file exists locally but not in azure, create that workspace anyway, without having to delete the config locally.

## Workspace
If you want to deploy your model in azure you need to do this in a workspace.
Start by creating a Workspace and save the workspace as a configuration file.
Then you can load the configuration file whenever you are going to use the workspace.
