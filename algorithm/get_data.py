import geopandas as gpd
from shapely.geometry import Point, LineString


def get_road_data(file_path):
    df = gpd.read_file(file_path)
    return df

def get_nearest_road(gdf, point):
    gdf['distance'] = gdf['geometry'].distance(point)
    nearest_road = gdf.loc[gdf['distance'].idxmin()]
    return nearest_road

def get_children(gdf, point):
    gdf['distance'] = gdf['geometry'].distance(point)
    lines = gdf.loc[gdf['distance'] == 0]
    children = []
    if not lines.empty:
        for row in lines.itertuples():
            geometry_value = row.geometry
            coords = geometry_value.coords
            list_point = [Point(coord) for coord in coords]
            idx = list_point.index(point)
            if idx > 0: children.append(list_point[idx-1])
            if idx < len(list_point) - 1: children.append(list_point[idx+1])
    return children
    
def bfs(gdf, start, targets):
    fringe = [start, ]
    closed = []
    parent = {
        start: start,
    }
    
    while fringe :
        point = fringe.pop(0)
        closed.append(point)
        
        for child in get_children(gdf, point):
            if child == targets:
                parent[child] = point
                # truy vết lại đường đi --------------------
                route = [[targets.y, targets.x],]
                curr = targets
                while curr != start:
                    curr = parent[curr]
                    route = [[curr.y, curr.x]] + route
                return route

            if  child not in closed:
                fringe.append(child)
                parent[child] = point
    return []





