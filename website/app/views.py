from django.shortcuts import render
from django.http import HttpResponse

import sys
import os
algorithm_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(algorithm_path)

from algorithm import bfs

# Create your views here.
def mapView(request):
    context = {

    }
    return render(request, 'map.html', context)

def searchView(request, searchText):
    x1, y1, x2, y2 = [float(i) for i in searchText.split('_') if i != '' ]
    text = bfs.search()
    context = {
        'x1': x1,
        'y1': y1,
        'x2': x2,
        'y2': y2,
        'text': text
    }
    return render(request, 'findWay.html', context)
