import re
from bs4 import BeautifulSoup

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages

import sys
import os
# os.path.dirname(__file__)
algorithm_path = os.path.join(os.getcwd(), '..')
sys.path.append(algorithm_path)

from algorithm import bfs, A_star, func
from shapely.geometry import Point, LineString
from datetime import datetime

# Lấy id của bản đồ trong file html----------------
def get_map_name(path):
    with open(path, "r") as file:
        content = file.read()

    soup = BeautifulSoup(content, "html.parser")

    #Sử dụng biểu thức chính quy để tìm id map
    script_tag = soup.find_all('script')[-1]
    pt = re.compile(r'addTo\(([^\)]*)\)') 
    match = pt.search(script_tag.string)
    return match.group(1)

# Trang ban đầu để chọn 2 điểm 
def homeView(request):
    path = os.path.join(os.getcwd(), 'app', 'templates', 'base', 'map.html')
    context = {
        'map_name': get_map_name(path) 
    }
    return render(request, 'home.html', context)

# Chạy trang tìm kiếm: Tìm đường đi giữa 2 điểm
def searchView(request, searchText):
    t_start = datetime.now()
    x1, y1, x2, y2 = [float(i) for i in searchText.split('_')]
    start = Point(x1, y1)
    target = Point(x2, y2)

    data_file = 'mapTrucBach.geojson'
    data_path = os.path.join(os.getcwd(), '..', 'preprocess_data', 'geojson', data_file)
    html_path = os.path.join(os.getcwd(), 'app', 'templates', 'base', 'map.html')

    gdf = func.get_road_data(data_path)

    # start_route, route, end_route = bfs.search(gdf, start, target)
    start_route, route, end_route = A_star.search(gdf, start, target)
    t_end = datetime.now()
    messages.success(request, f'Tìm kiếm thành công trong {t_end - t_start}')
    context = {
        'start_route': start_route,
        'route':route,
        'end_route':end_route,
        'start': [y1, x1], 
        'target': [y2, x2],
        'map_name': get_map_name(html_path)
    }
    return render(request, 'search.html', context)
