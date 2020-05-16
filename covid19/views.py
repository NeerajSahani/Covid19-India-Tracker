from django.http import HttpResponse
from django.shortcuts import render
from . import analytics as anl
import pandas as pd

global hits
hits = 0


# def index(request, *args, **kwargs):
#     data = pd.read_json('https://api.covid19india.org/state_district_wise.json')
#     queryset = {}
#     for i, j in data.items():
#         queryset[i] = {k: v for k, v in j['districtData'].items()}
#     return render(request, 'covid19/index.html', {'context': queryset})


def index(request, *args, **kwargs):
    data, df = anl.get_data()
    queryset = {}
    for i, j in data.items():
        queryset[i] = {k: v for k, v in j['districtData'].items()}
    plots = anl.get_pie(df=df)
    context = {
        'context': queryset,
        'gkp': df[df.District == 'Gorakhpur'].iloc[:, 1:6].T,
        'UP': df[df.State == 'Uttar Pradesh'].agg(sum)[1:6].T,
        'india': df.agg(sum).T[1:5],
        'state_pie': anl.get_pie(df),
        'district_bar': anl.get_chart(df, key='District', upto=7),
        'line': anl.get_line_plot(),
        'up_bar': anl.get_chart(df[df.State == 'Uttar Pradesh'], upto=7),
        'map': anl.world_map(),
    }
    global hits
    hits += 1
    return render(request, 'covid19/index.html', context=context)


def get_hits(request):
    global hits
    return HttpResponse("<h1>" + str(hits) + "</h1>")


def plot_map(request):
    return render(request, 'covid19/map.html', {'map': anl.world_map()})
