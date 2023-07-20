from django.shortcuts import render
import pandas as pd

def searchView(request):
    try:
        searchString = request.POST['search-input']
    except:
        return render(request, 'playerSearch.html', {"res":[]})

    players_df = pd.read_csv('../inputs/final_processed_data.csv')
    players_name_list = players_df['name'].unique()

    result_list = []

    for player in players_name_list:
        if searchString.upper() in player.upper():
            result_list.append(player)

    return render(request, 'playerSearch.html', {"res":result_list})