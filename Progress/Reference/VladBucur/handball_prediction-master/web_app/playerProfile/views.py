from django.shortcuts import render
import pandas as pd

def profileView(request):
    try:
        playerName = request.POST['player-name']
    except:
        return render(request, 'playerProfile.html', {"playerName": "", "predictionSeasonList": [], "playerPosition": "",
                                                                        "playerHeight": ""})

    players_df = pd.read_csv('../inputs/final_processed_data.csv')
    players_raw_df = pd.read_csv('../inputs/raw_data.csv')

    player_data = players_df[players_df['name'] == playerName]
    player_raw_data = players_raw_df[players_raw_df['name'] == playerName]

    player_raw_data['goals_per_match_year3'] = player_raw_data['goals_year3'] / player_raw_data['matches_year3']
    data = player_data.merge(player_raw_data[['goals_per_match_year3', 'prediction_season']],
                             on='goals_per_match_year3', how='left')

    predictionSeasonList = list(data['prediction_season'][~data['prediction_season'].isna()].unique())
    predictionSeasonList.sort()

    centre = int(player_data['center'].values[0])
    back = int(player_data['center'].values[0])
    wing = int(player_data['wing'].values[0])
    line = int(player_data['line'].values[0])

    if centre == 1:
        playerPosition = "CENTER"
    elif back == 1:
        playerPosition = "BACK"
    elif wing == 1:
        playerPosition = "WING"
    else:
        playerPosition = "LINE"

    playerHeight = int(player_raw_data['height'].values[0])

    return render(request, 'playerProfile.html', {"playerName": playerName, "predictionSeasonList": predictionSeasonList,
                                                  "playerPosition": playerPosition, "playerHeight": playerHeight})
