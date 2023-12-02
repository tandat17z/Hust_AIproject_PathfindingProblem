import geopandas as gpd
from shapely.geometry import Point, LineString


def get_road_data(file_path):
    df = gpd.read_file(file_path)
    return df

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
            if idx > 0: children.append(list_point[idx-1])
            if idx < len(list_point) - 1: children.append(list_point[idx+1])
    return children
    
def bfs(gdf, start, target):
    # Xử lý vị trí bất kì của start ---> trả ra điểm nằm trên các đường
    new_start, start1, start2 = get_nearest_point(gdf, start)
    print(start1, start2)
    new_target, target1, target2 = get_nearest_point(gdf, target)
    print(target1, target2)

    fringe = [start1, ]
    closed = []
    if start2 != None: fringe.append(start2)

    targets = [target1, ]
    if target2 != None: targets.append(target2)

    parent = {
        start1: new_start,
        start2: new_start,
    }
    
    while fringe :
        point = fringe.pop(0)
        closed.append(point)
        
        for child in get_children(gdf, point):
            if child in targets:
                parent[child] = point
                # truy vết lại đường đi --------------------
                route = [[child.y, child.x], [new_target.y, new_target.x], ]
                curr = child
                while curr != new_start:
                    curr = parent[curr]
                    route = [[curr.y, curr.x]] + route
                
                return [[start.y, start.x], [curr.y, curr.x]], route, [[new_target.y, new_target.x],[target.y, target.x]]

            if  child not in closed + fringe:
                fringe.append(child)
                parent[child] = point
    return [], [], []





