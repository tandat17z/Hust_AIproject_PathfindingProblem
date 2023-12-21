from .func0 import *
import queue

def search(start, target):
    # Xử lý vị trí bất kì của start ---> trả ra điểm nằm trên các đường
    new_start, start1, start2 = get_nearest_point(start, type='start')
    new_target, target1, target2 = get_nearest_point(target, type='end')

    targets = [target1, ]
    if target2 != None: targets.append(target2)

    fringe = [start1, ]
    closed = []
    parent = {
        new_start: start,
        start1: new_start,
    }
    g = {
        start1: start.distance(new_start) + new_start.distance(start1),
    }

    # Khởi tạo hàng đợi ưu tiên
    pq = queue.PriorityQueue() # ban đầu có 2 điểm start1, start2
    pq.put( (g[start1] + target.distance(start1), start1) )
    if start2 != None: 
        fringe.append(start2)
        parent[start2] = new_start
        g[start2] = start.distance(new_start) + new_start.distance(start2)
        pq.put( (g[start2] + target.distance(start2), start2) )

    while pq.empty() == False:
        f, point = pq.get() 
        fringe.remove(point)
        closed.append(point)

        for child in get_children(point,):
            if child in targets:
                parent[child] = point
                # truy vết lại đường đi --------------------
                route = [[child.y, child.x], [new_target.y, new_target.x], ]
                curr = child
                while curr != new_start:
                    curr = parent[curr]
                    route = [[curr.y, curr.x]] + route
                
                return [[start.y, start.x], [curr.y, curr.x]], route, [[new_target.y, new_target.x],[target.y, target.x]]
            
            elif child not in closed:
                if child not in fringe or g[child] > g[point] + point.distance(child):
                    g[child] = g[point] + point.distance(child)
                    pq.put((g[child] + target.distance(child), child))
                    fringe.append(child)
                    parent[child] = point
