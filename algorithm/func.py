import geopandas as gpd
from shapely.geometry import Point, LineString


def get_road_data(file_path):
    df = gpd.read_file(file_path)
    return df

# đường gần point nhất
def get_nearest_road(gdf, point):
    gdf['distance'] = gdf['geometry'].distance(point)
    nearest_road = gdf.loc[gdf['distance'].idxmin()]
    return nearest_road

def get_nearest_point(gdf, point):
    # Trên đoạn thẳng MN (M, N là mút)
    # H là chân đường vuông góc từ point tới MN
    # Cần tìm 2 điểm A, B thuộc các node trên đường gần H nhất
    # A, B đối xứng qua H
    nearest_road = get_nearest_road(gdf, point)
    line = nearest_road['geometry']
    point_H = line.interpolate(line.project(point))

    min_d1 = 10000000
    point_A = point_H

    coords = line.coords
    i = 0
    for p in coords:
        d = point.distance(Point(p))
        if min_d1 > d:
            k = i
            point_A = Point(p)
            min_d1 = d
        else:
            break
        i += 1
    
    vector_HA = (point_A.x - point_H.x, point_A.y - point_H.y)
    if k < len(coords) -1 : 
        point_B = Point(coords[k + 1])
        vector_HB = (point_B.x - point_H.x, point_B.y - point_H.y)
        if vector_HA[0]*vector_HB[0] + vector_HA[1]*vector_HB[1] > 0 :
            point_B = Point(coords[k - 1]) if k > 0 else None
    elif k > 0:
        point_B = Point(coords[k - 1])
    else:
        point_B = None

    return point_H, point_A, point_B

def get_children(gdf, point):
    gdf['distance'] = gdf['geometry'].distance(point)
    lines = gdf.loc[gdf['distance'] == 0]
    children = []
    if not lines.empty: # Nếu point đang nằm trên 1 đường nào đó
        for row in lines.itertuples(): # duyệt qua các đường chứa point ( có case: point là giao điểm của nhiều đường)
            geometry_value = row.geometry
            coords = geometry_value.coords
            list_point = [Point(coord) for coord in coords]
            idx = list_point.index(point)
            if idx > 0 : 
                children.append(list_point[idx-1])

            if idx < len(list_point) - 1: 
                children.append(list_point[idx+1])
    return children
    