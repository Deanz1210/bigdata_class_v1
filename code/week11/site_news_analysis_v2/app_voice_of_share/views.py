from django.http import JsonResponse
from django.shortcuts import render
import pandas as pd

def load_data_lol():
    # Read data from csv file
    df_data = pd.read_csv('app_voice_of_share/dataset/lol.csv',sep=',')
    global response
    response = dict(list(df_data.values))
    del df_data

# load pk data
load_data_lol()

def home(request):
    return render(request,'app_voice_of_share/home.html', response)

print('app_voice_of_share was loaded!')