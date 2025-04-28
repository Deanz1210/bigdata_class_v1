from django.http import JsonResponse
import pandas as pd
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import ast

def load_data_pk():
    df_data_pk = pd.read_csv('app_game_mayor/dataset/pk_game_mayor_election.csv')
    
    global data
    data = {}
    for k, v in zip(df_data_pk['name'], df_data_pk['value']):
        data[k] = ast.literal_eval(v)

    del df_data_pk

load_data_pk()

def home(request):
    return render(request,'app_game_mayor/home.html')

@csrf_exempt
def api_get_game_mayor_data(request):
    return JsonResponse(data)

print('Load app game mayor leaderboard...')
