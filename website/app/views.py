import re
from bs4 import BeautifulSoup

from django.shortcuts import render
from django.http import HttpResponse

import sys
import os
# os.path.dirname(__file__)
algorithm_path = os.path.join(os.getcwd(), '..')
sys.path.append(algorithm_path)

from algorithm import bfs, function
from shapely.geometry import Point, LineString


# Lấy id của bản đồ trong file html----------------
def get_map_name(path):
    with open(path, "r") as file:
        content = file.read()

    soup = BeautifulSoup(content, "html.parser")

    script_tag = soup.find_all('script')[-1]

    pt = re.compile(r'addTo\(([^\)]*)\)')
    match = pt.search(script_tag.string)
    return match.group(1)

# Create your views here.
def mapView(request):
    context = {

    }
    return render(request, 'map.html', context)

# Chạy trang tìm kiếm: Tìm đường đi giữa 2 điểm
def searchView(request, searchText):
    x1, y1, x2, y2 = [float(i) for i in searchText.split('_')]
    start = Point(x1, y1)
    target = Point(x2, y2)

    file_path = path = os.path.join(os.getcwd(), '..', 'preprocess_data', 'geojson', 'export.geojson')
    gdf = function.get_road_data(file_path)
    start_route, route, end_route = bfs.search(gdf, start, target)

    path = os.path.join(os.getcwd(), 'app', 'templates', 'map0.html')
    
    context = {
        'start_route': start_route,
        'route':route,
        'end_route':end_route,
        'start': [y1, x1], 
        'target': [y2, x2],
        # 'text': text,
        'map_name': get_map_name(path)
    }
    return render(request, 'search.html', context)
