import geopandas as gpd
import json
from shapely.geometry import Point, LineString

def get_road_data(file_path):
    gdf = gpd.read_file(file_path)
    return gdf

# Lấy dữ liệu đường 1 chiều
def get_oneway_id(file_path):
    oneway_id = []
    with open(file_path, 'r', encoding='utf-8' ) as file:
        f = file.read()
        data_geojson = json.loads(f)

        for way in data_geojson['features']:
            if 'properties' in way and 'oneway' in way['properties'] and way['properties']['oneway'] == 'yes':
                oneway_id.append(way['properties']['@id'])

    return oneway_id


# đường gần point nhất
def get_nearest_road(gdf, point):
    gdf['distance'] = gdf['geometry'].distance(point)
    nearest_road = gdf.loc[gdf['distance'].idxmin()]
    return nearest_road

def get_nearest_point(gdf, oneway, point, type):
    # Trên đoạn thẳng MN (M, N là mút)
    # H là chân đường vuông góc từ point tới MN
    # Cần tìm 2 điểm A, B thuộc các node trên đường gần H nhất
    # A, B đối xứng qua H
    nearest_road = get_nearest_road(gdf, point)
    line = nearest_road['geometry']
    point_H = line.interpolate(line.project(point))
    way_id = nearest_road['id']

    min_d1 = 10000000
    point_A = point_H

    coords = line.coords
    i = 0
    for p in coords:
        d = point.distance(Point(p))
        if min_d1 > d:
            k_a = i
            point_A = Point(p)
            min_d1 = d
        else:
            break
        i += 1
    
    vector_HA = (point_A.x - point_H.x, point_A.y - point_H.y)
    if k_a < len(coords) -1 : 
        k_b = k_a + 1
        point_B = Point(coords[k_b])
        vector_HB = (point_B.x - point_H.x, point_B.y - point_H.y)
        if vector_HA[0]*vector_HB[0] + vector_HA[1]*vector_HB[1] > 0 :
            k_b = k_a - 1 if k_a > 0 else -1
            point_B = Point(coords[k_b]) if k_b != -1 else None
    elif k_a > 0:
        k_b = k_a - 1
        point_B = Point(coords[k_b])
        vector_HB = (point_B.x - point_H.x, point_B.y - point_H.y)
        if vector_HA[0]*vector_HB[0] + vector_HA[1]*vector_HB[1] > 0 :
            k_b = -1
            point_B = None
    else:
        k_b = -1
        point_B = None

    # Xử lý trường hợp là đường 1 chiều ( HA, HB không thể đi ngược chiều)
    if way_id in oneway and k_b != -1:
        if type == 'start':
            if k_b > k_a:
                point_A = point_B
            point_B = None
        elif type == "end":
            if k_b < k_a:
                point_A = point_B
            point_B = None

    return point_H, point_A, point_B


def get_children(gdf, point, oneway):
    gdf['distance'] = gdf['geometry'].distance(point)
    lines = gdf.loc[gdf['distance'] == 0]
    children = []
    if not lines.empty: # Nếu point đang nằm trên 1 đường nào đó
        for row in lines.itertuples(): # duyệt qua các đường chứa point ( có case: point là giao điểm của nhiều đường)
            geometry_value = row.geometry
            coords = geometry_value.coords
            list_point = [Point(coord) for coord in coords]
            idx = list_point.index(point)

            if idx > 0 and row.id not in oneway: # Nếu không phải đường 1 chiều
                children.append(list_point[idx-1])

            if idx < len(list_point) - 1: 
                children.append(list_point[idx+1])
    return children
    