from django.shortcuts import render
import pandas as pd

def futurePredictionInputDataView(request):

    try:
        playerName = request.POST['player-name']
        playerPosition = request.POST['position']
        playerHeight = request.POST['height']

    except:
        return render(request, 'playerFuturePredictionInputData.html', {"playerName": "", "playerPosition": "",
                                                                        "playerHeight": 0})

    return render(request, 'playerFuturePredictionInputData.html', {"playerName": playerName, "playerPosition": playerPosition,
                                                                    "playerHeight": playerHeight})