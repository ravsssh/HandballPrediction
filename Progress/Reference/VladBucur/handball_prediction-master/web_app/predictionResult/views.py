from django.shortcuts import render
from keras.models import model_from_json
import pandas as pd
import pickle

def predictionResultView(request):

    try:
        playerName = request.POST['player-name']
        predictionSeason = request.POST['prediction-season']
        predictionModel = request.POST['prediction-model']
    except:
        return render(request, 'predictionResult.html', {"playerName": "", "predictionSeason": "",
                                                         "predictionModel": "", "predictedValue": "", "actualValue": "",
                                                         "predictionModelDocumentationLink": ""})

    players_df = pd.read_csv('../inputs/final_processed_data.csv')
    players_df = players_df[players_df['name'] == playerName]

    players_raw_df = pd.read_csv('../inputs/raw_data.csv')
    players_raw_df = players_raw_df[(players_raw_df['name'] == playerName) & \
                                    (players_raw_df['prediction_season'] == predictionSeason)]
    players_raw_df['goals_per_match_year3'] = players_raw_df['goals_year3'] / players_raw_df['matches_year3']

    data = players_df.merge(players_raw_df[['goals_per_match_year3', 'prediction_season']],
                            on='goals_per_match_year3', how='inner')
    data = data.head(1)

    X = data[['center', 'back', 'wing', 'line', 'height', 'matches_year1', 'goals_year1', 'goals_per_match_year1',
              'matches_year2', 'goals_year2', 'goals_per_match_year2']]

    # read model from file
    if predictionModel == 'Linear Regression':
        pkl_filename = "../models/regression_models/linear_regression_model.pkl"
    elif predictionModel == 'Lasso Regressor':
        pkl_filename = "../models/regression_models/lasso_regression_model.pkl"
    elif predictionModel == 'Ridge Regressor':
        pkl_filename = "../models/regression_models/ridge_regression_model.pkl"
    elif predictionModel == 'Decision Tree Regressor':
        pkl_filename = "../models/regression_models/decision_tree_regression_model.pkl"
    elif predictionModel == 'Random Forest Regressor':
        pkl_filename = "../models/regression_models/random_forests_regression_model.pkl"
    elif predictionModel == 'Logistic Regression':
        pkl_filename = "../models/classification_models/logistic_regression_model.pkl"
    elif predictionModel == 'Decision Tree Classifier':
        pkl_filename = "../models/classification_models/decission_tree_classifier_model.pkl"
    else: # Random Forests Classifier
        pkl_filename = "../models/classification_models/random_forests_classifier_model.pkl"

    if predictionModel in ['Linear Regression', 'Lasso Regressor', 'Ridge Regressor', 'Decision Tree Regressor',
                'Random Forest Regressor', 'Logistic Regression','Decision Tree Classifier', 'Random Forest Classifier']:
        model = pickle.load(open(pkl_filename, 'rb'))

    else: # neural network
        json_file = open('../models/neural_networks/3_layers_NN.json', 'r')
        model_json = json_file.read()
        json_file.close()
        model = model_from_json(model_json)

    # compute actual and predicted value
    actualValue = data['goals_per_match_year3'].values[0]
    predictedValue = model.predict(X)[0]

    # get the predicted value from prediction array of size 1
    if predictionModel in ['Linear Regression', 'Ridge Regressor', 'Neural Network']:
        predictedValue = predictedValue[0]

    # if a classification model is used convert the results to integers (classes)
    elif predictionModel in ['Logistic Regression','Decision Tree Classifier', 'Random Forest Classifier']:
        actualValue = int(round(actualValue))
        predictedValue = int(predictedValue)

    modelLinks = {}
    modelLinks['Linear Regression'] = 'https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html'
    modelLinks['Lasso Regressor'] = 'https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Lasso.html'
    modelLinks['Ridge Regressor'] = 'https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html'
    modelLinks['Decision Tree Regressor'] = 'https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeRegressor.html'
    modelLinks['Random Forest Regressor'] = 'https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html'
    modelLinks['Neural Network'] = 'https://keras.io/getting-started/sequential-model-guide/'
    modelLinks['Logistic Regression'] = 'https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html'
    modelLinks['Decision Tree Classifier'] = 'https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html'
    modelLinks['Random Forest Classifier'] = 'https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html'

    return render(request, 'predictionResult.html', {"playerName": playerName, "predictionSeason": predictionSeason,
                            "predictionModel": predictionModel, "predictedValue": str(predictedValue),
                            "actualValue": str(actualValue), "predictionModelDocumentationLink": modelLinks[predictionModel]})
