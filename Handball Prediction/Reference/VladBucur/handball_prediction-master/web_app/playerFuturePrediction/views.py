from django.shortcuts import render
import pandas as pd

def futurePredictionView(request):

    def isInt(s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    try:
        playerName = request.POST['player-name']
        playerPosition = request.POST['position']
        playerHeight = request.POST['height']
        matchesYear1 = int(request.POST['matches-year1'])
        goalsYear1 = int(request.POST['goals-year1'])
        matchesYear2 = int(request.POST['matches-year2'])
        goalsYear2 = int(request.POST['goals-year2'])

        if playerName == "" or playerPosition not in ['CENTER','BACK','WING','LINE']:
            raise Exception
    except:
        errorMessage = "Inputs not accepted"  # default

        if request.POST['player-name'] == "":
            errorMessage =  "Invalid player name entered. This should be a non-empty string."
        elif request.POST['position'] is None or request.POST['position'] not in ['CENTER','BACK','WING','LINE']:
            errorMessage = "Invalid player position entered. This should be CENTER/BACK/WING/LINE."
        elif not isInt(request.POST['height']):
            errorMessage = "Invalid player height entered. This should be an integer (cm)."
        elif not isInt(request.POST['matches-year1']):
            errorMessage = "Invalid matches played 2 seasons ago entered. This should be an integer."
        elif not isInt(request.POST['goals-year1']):
            errorMessage = "Invalid goals scored 2 seasons ago entered. This should be an integer."
        elif not isInt(request.POST['matches-year2']):
            errorMessage = "Invalid matches played 1 season ago entered. This should be an integer."
        elif not isInt(request.POST['goals-year2']):
            errorMessage = "Invalid goals scored 1 season ago entered. This should be an integer."

        print(errorMessage)

        return render(request, 'playerFuturePrediction.html', {"playerName": "", "playerPosition": "", "playerHeight": 0,
                                "matchesYear1": 0, "goalsYear1": 0, "matchesYear2": 0, "goalsYear2": 0,
                                "playerAttributes": [], "recommendedModel": "", "predictionModelsList": [],
                                "errorMessage": errorMessage})

    players_raw_df = pd.read_csv('../inputs/raw_data.csv')
    playerAttributes = []

    playerAttributes.append(playerPosition)

    if int(playerHeight) > players_raw_df['height'].quantile(.75):
        playerAttributes.append('tall player')
    elif int(playerHeight) < players_raw_df['height'].quantile(.25):
        playerAttributes.append('short player')
    else:
        playerAttributes.append('average height')

    if int(matchesYear2) > players_raw_df['matches_year2'].quantile(.75):
        playerAttributes.append('often playing')
    elif int(matchesYear2) < players_raw_df['matches_year2'].quantile(.25):
        playerAttributes.append('rarely playing')
    else:
        playerAttributes.append('average playing')

    if int(goalsYear2) > players_raw_df['goals_year2'].quantile(.75):
        playerAttributes.append('high scoring')
    elif int(goalsYear2) < players_raw_df['goals_year2'].quantile(.25):
        playerAttributes.append('low scoring')
    else:
        playerAttributes.append('average scoring')

    randomForestRegressorScore = 0
    decisionTreeClassifierScore = 0
    randomForestClassifierScore = 0

    if playerPosition in ['Left Wing', 'Right Back', 'Right Wing', 'Left Back', 'Back']:
        randomForestRegressorScore = randomForestRegressorScore + 1
    else:
        randomForestClassifierScore = randomForestClassifierScore + 1

    if 'short player' in playerAttributes or 'tall player' in playerAttributes:
        randomForestRegressorScore = randomForestRegressorScore + 1

    if 'rarely playing' in playerAttributes:
        randomForestClassifierScore = randomForestClassifierScore + 1
    elif 'often playing' in playerAttributes:
        randomForestRegressorScore = randomForestRegressorScore + 1

    if 'low scoring' in playerAttributes:
        decisionTreeClassifierScore = decisionTreeClassifierScore + 1
    elif 'high scoring' in playerAttributes:
        randomForestRegressorScore = randomForestRegressorScore + 1

    if (decisionTreeClassifierScore >= randomForestRegressorScore) and \
            (decisionTreeClassifierScore >= randomForestClassifierScore):
        recommendedModel = "Decision Tree Classifier"
    elif randomForestClassifierScore >= randomForestRegressorScore:
        recommendedModel = "Random Forest Classifier"
    else:
        recommendedModel = "Random Forest Regressor"

    predictionModelsList = ['Linear Regression', 'Lasso Regressor', 'Ridge Regressor', 'Decision Tree Regressor',
                            'Random Forest Regressor', 'Neural Network', 'Logistic Regression',
                            'Decision Tree Classifier', 'Random Forest Classifier']

    return render(request, 'playerFuturePrediction.html', {"playerName": playerName, "playerPosition": playerPosition,
                            "playerHeight": playerHeight, "matchesYear1": matchesYear1, "goalsYear1": goalsYear1,
                            "matchesYear2": matchesYear2, "goalsYear2": goalsYear2, "playerAttributes": playerAttributes,
                            "recommendedModel": recommendedModel, "predictionModelsList": predictionModelsList})