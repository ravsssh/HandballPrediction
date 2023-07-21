from django.shortcuts import render
from keras.models import model_from_json
import pandas as pd
import pickle

def futurePredictionResultView(request):

    try:
        playerName = request.POST['player-name']
        playerPosition = request.POST['position']
        playerHeight = request.POST['height']
        matchesYear1 = request.POST['matches-year1']
        goalsYear1 = request.POST['goals-year1']
        matchesYear2 = request.POST['matches-year2']
        goalsYear2 = request.POST['goals-year2']
        predictionModel = request.POST['prediction-model']
    except:
        return render(request, 'playerFuturePredictionResult.html', {"playerName": "", "predictionModel": "",
                                                        "predictedValue": "",  "predictionModelDocumentationLink": ""})

    df = pd.DataFrame(columns=['center', 'back', 'wing', 'line', 'height', 'matches_year1', 'goals_year1',
                               'goals_per_match_year1', 'matches_year2', 'goals_year2', 'goals_per_match_year2'])

    center = 0
    back = 0
    wing = 0
    line = 0

    if playerPosition == 'CENTER':
        center = 1
    elif playerPosition == 'BACK':
        back = 1
    elif playerPosition == 'WING':
        wing = 1
    elif playerPosition == 'LINE':
        line = 1

    goals_per_match_year1 = float(goalsYear1) / float(matchesYear1)
    goals_per_match_year2 = float(goalsYear2) / float(matchesYear2)

    df = df.append({'center': center, 'back': back, 'wing': wing, 'line': line, 'height': int(playerHeight),
                    'matches_year1': int(matchesYear1), 'goals_year1': int(goalsYear1),
                    'goals_per_match_year1': goals_per_match_year1, 'matches_year2': int(matchesYear2),
                    'goals_year2': int(goalsYear2), 'goals_per_match_year2': goals_per_match_year2}, ignore_index=True)

    X = df[['center', 'back', 'wing', 'line', 'height', 'matches_year1', 'goals_year1', 'goals_per_match_year1',
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
    else:  # Random Forests Classifier
        pkl_filename = "../models/classification_models/random_forests_classifier_model.pkl"

    if predictionModel in ['Linear Regression', 'Lasso Regressor', 'Ridge Regressor', 'Decision Tree Regressor',
                           'Random Forest Regressor', 'Logistic Regression', 'Decision Tree Classifier',
                           'Random Forest Classifier']:
        model = pickle.load(open(pkl_filename, 'rb'))

    else:  # neural network
        json_file = open('../models/neural_networks/3_layers_NN.json', 'r')
        model_json = json_file.read()
        json_file.close()
        model = model_from_json(model_json)

    # compute predicted value
    predictedValue = model.predict(X)[0]

    # get the predicted value from prediction array of size 1
    if predictionModel in ['Linear Regression', 'Ridge Regressor', 'Neural Network']:
        predictedValue = predictedValue[0]

    # if a classification model is used convert the results to integers (classes)
    elif predictionModel in ['Logistic Regression', 'Decision Tree Classifier', 'Random Forest Classifier']:
        predictedValue = int(predictedValue)

    modelLinks = {}
    modelLinks[
        'Linear Regression'] = 'https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html'
    modelLinks['Lasso Regressor'] = 'https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Lasso.html'
    modelLinks['Ridge Regressor'] = 'https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html'
    modelLinks[
        'Decision Tree Regressor'] = 'https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeRegressor.html'
    modelLinks[
        'Random Forest Regressor'] = 'https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html'
    modelLinks['Neural Network'] = 'https://keras.io/getting-started/sequential-model-guide/'
    modelLinks[
        'Logistic Regression'] = 'https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html'
    modelLinks[
        'Decision Tree Classifier'] = 'https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html'
    modelLinks[
        'Random Forest Classifier'] = 'https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html'

    return render(request, 'playerFuturePredictionResult.html',
                  {"playerName": playerName, "predictionModel": predictionModel,
                   "predictedValue": predictedValue, "predictionModelDocumentationLink": modelLinks[predictionModel]})