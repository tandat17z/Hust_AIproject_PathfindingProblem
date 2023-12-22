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

from algorithm import A_star
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
    x1, y1, x2, y2 = [float(i) for i in searchText.split('_')]
    start = Point(x1, y1)
    target = Point(x2, y2)

    t_start = datetime.now()
    start_route, route, end_route = A_star.search(start, target)
    t_end = datetime.now()

    time_search = round(t_end.timestamp() - t_start.timestamp(), 5)
    messages.success(request, f'Tìm kiếm thành công trong {time_search} s')
    context = {
        'start_route': start_route,
        'route':route,
        'end_route':end_route,
        'start': [y1, x1], 
        'target': [y2, x2],
        'time_search': time_search,
        'map_name': get_map_name(os.path.join(os.getcwd(), 'app', 'templates', 'base', 'map.html'))
    }
    return render(request, 'search.html', context)
