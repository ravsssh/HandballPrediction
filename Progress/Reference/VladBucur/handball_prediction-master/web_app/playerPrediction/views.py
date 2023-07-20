from django.shortcuts import render
import pandas as pd

def predictionView(request):

    try:
        playerName = request.POST['player-name']
        predictionSeason = request.POST['prediction-season']
    except:
        return render(request, 'playerPrediction.html', {"playerName": "", "predictionSeason": "",
                                "predictionModelsList": [], "playerAttributes": [], "recommendedModel":""})

    predictionModelsList = ['Linear Regression', 'Lasso Regressor', 'Ridge Regressor', 'Decision Tree Regressor',
                             'Random Forest Regressor', 'Neural Network', 'Logistic Regression',
                             'Decision Tree Classifier', 'Random Forest Classifier']

    players_raw_df = pd.read_csv('../inputs/raw_data.csv')
    current_player_df = players_raw_df[(players_raw_df['name'] == playerName) & \
                                       (players_raw_df['prediction_season'] == predictionSeason)]

    playerAttributes = []

    player_position = current_player_df['position'].values[0]
    player_height = current_player_df['height'].values[0]
    player_appearances = current_player_df['matches_year2'].values[0]
    player_goals = current_player_df['goals_year2'].values[0]

    playerAttributes.append(player_position)

    if player_height > players_raw_df['height'].quantile(.75):
        playerAttributes.append('tall player')
    elif player_height < players_raw_df['height'].quantile(.25):
        playerAttributes.append('short player')
    else:
        playerAttributes.append('average height')

    if player_appearances > players_raw_df['matches_year2'].quantile(.75):
        playerAttributes.append('often playing')
    elif player_appearances < players_raw_df['matches_year2'].quantile(.25):
        playerAttributes.append('rarely playing')
    else:
        playerAttributes.append('average playing')

    if player_goals > players_raw_df['goals_year2'].quantile(.75):
        playerAttributes.append('high scoring')
    elif player_goals < players_raw_df['goals_year2'].quantile(.25):
        playerAttributes.append('low scoring')
    else:
        playerAttributes.append('average scoring')

    randomForestRegressorScore = 0
    decisionTreeClassifierScore = 0
    randomForestClassifierScore = 0

    if player_position in ['Left Wing', 'Right Back', 'Right Wing', 'Left Back', 'Back']:
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

    return render(request, 'playerPrediction.html', {"playerName": playerName, "predictionSeason": predictionSeason,
                            "predictionModelsList": predictionModelsList, "playerAttributes": playerAttributes,
                            "recommendedModel":recommendedModel})