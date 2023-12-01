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
    nearest_road = get_nearest_road(gdf, point)
    line = nearest_road['geometry']
    new_start = line.interpolate(line.project(point))

    min_d1 = min_d2 = 10000000
    point1 = point2 = new_start

    for p in line.coords:
        d = new_start.distance(Point(p))
        if min_d1 > d:
            point2 = point1
            point1 = Point(p)
            min_d2 = min_d1
            min_d1 = d
        elif min_d2 > d:
            point2 = Point(p)
            min_d2 = d
    return new_start, point1, point2

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
    new_target, target1, target2 = get_nearest_point(gdf, target)

    fringe = [start1, start2]
    closed = []
    parent = {
        start1: new_start,
        start2: new_start,
    }
    
    while fringe :
        point = fringe.pop(0)
        closed.append(point)
        
        for child in get_children(gdf, point):
            if child in (target1, target2):
                parent[child] = point
                # truy vết lại đường đi --------------------
                route = [[child.y, child.x], [new_target.y, new_target.x], ]
                curr = child
                while curr != new_start:
                    curr = parent[curr]
                    route = [[curr.y, curr.x]] + route
                
                return [[start.y, start.x], [curr.y, curr.x]], route, [[new_target.y, new_target.x],[target.y, target.x]]

            if  child not in closed:
                fringe.append(child)
                parent[child] = point
    return [], [], []





