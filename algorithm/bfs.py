from .func import *

# Chưa fix lại theo chỉnh sửa trong func ----------------------------------------------------------
# get_children + get_nearest_point
# Xử lý liên quan tới đường 1 chiều

def search(gdf, oneway, start, target):
    # Xử lý vị trí bất kì của start ---> trả ra điểm nằm trên các đường
    new_start, start1, start2 = get_nearest_point(gdf, oneway, start, type='start' )
    print(start1, start2)
    new_target, target1, target2 = get_nearest_point(gdf, oneway, target, type='end')
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