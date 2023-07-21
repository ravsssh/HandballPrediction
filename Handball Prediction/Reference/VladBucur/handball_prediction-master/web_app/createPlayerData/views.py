from django.shortcuts import render
import pandas as pd

def createPlayerDataView(request):

    return render(request, 'createPlayerData.html', {})