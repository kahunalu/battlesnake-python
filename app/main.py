import os
import heapq
import bottle

taunts = ["DO IT! JUST DO IT!", "DON'T LET YOUR DREAMSSSS BE DREAMSSSS.", "JUSSSST DO IT!", "IF YOU'RE TIRED OF SSSSTARTING OVER, SSSSTOP GIVING UP.", "YESSSS YOU CAN. JUST DO IT.", "NOTHING IS IMPOSSIBLE.", "YESSSS YOU CAN.", "NOTHING IS IMPOSSSSSSSSIBLE", "DON'T SSSSTOP!", "SSSSTOP GIVING UP", "YESSSS YOU CAN."]

SHIA_ID = "6b1d5489-e9db-4673-bbce-0b65ee729519"

@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.get('/')
def index():
    head_url = '%s://%s/static/shia-labite.jpg' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    return {
        'color': '#5da36f',
        'head': head_url
    }


@bottle.post('/start')
def start():
    data = bottle.request.json

    # TODO: Do things with data
    print(taunts[data['turn']])

    return {
        'taunt': taunts[0]
    }


@bottle.post('/move')
def move():
    data = bottle.request.json

    if "walls" not in data:
        data["walls"] = []

    '''
    # TODO: Do things with data

    # Remove dead snakes
    for snake in data["snakes"]
        if snake["status"] == "dead":
            data["snakes"].remove(snake)

    get_mode(data)
    '''


    print "Start"

    print "MOVE"
    move = get_mode(data)

    return {
        'move': move,
        'taunt': taunts[(data['turn'] % len(taunts))]
    }


@bottle.post('/end')
def end():
    data = bottle.request.json

    # TODO: Do things with data

    return {
        'taunt': 'battlesnake-python!'
    }

def get_mode(data):
    shia = get_shia_snake(data)
    if shia["health"] < 40:
        return hungry(data)
    else:
        return defualt(data)

def hungry(data):

    shia = get_shia_snake(data)
    heat_map = make_heat_map(data)

    if not len(data["food"]):
        return defualt(data)

    food = food_eval(heat_map, data["food"], shia["coords"][0])

    return get_move(shia["coords"][0], food, data)


def defualt(data):
    shia = get_shia_snake(data)
    heat_map = make_heat_map(data)
    goal, value = evaluate(shia["coords"][0], heat_map, 0)

    print "THIS IS THE GOAL AND VALUE"
    print goal
    print value

    return get_move(shia["coords"][0], goal, data)

def evaluate(coord, heatMap, level):
    value = 0

    if level == 3:
        return coord, value

    heatMap[coord[1]][coord[0]] = 4

    level = level + 1

    north_coord, north_val = evaluate([coord[0],coord[1]-1], heatMap, level)
    south_coord, south_val = evaluate([coord[0],coord[1]+1], heatMap, level)
    east_coord, east_val = evaluate([coord[0]+1,coord[1]], heatMap, level)
    west_coord, west_val = evaluate([coord[0]-1,coord[1]], heatMap, level)

    if coord[1] == 0:
        north = 100
    else:
        north = heatMap[coord[1]-1][coord[0]] + north_val

    if coord[1] == (len(heatMap)-1):
        south = 100
    else:
        south = heatMap[coord[1]+1][coord[0]] + south_val

    if coord[0] == (len(heatMap[0])-1):
        east = 100
    else:
        east = heatMap[coord[1]][coord[0]+1] + east_val

    if coord[0] == 0:
        west = 100
    else:
        west = heatMap[coord[1]][coord[0]-1] + west_val

    values = [north, south, east, west]

    minimum = min(values)

    if north == minimum:
        return north_coord, north

    if south == minimum:
        return south_coord, south

    if east == minimum:
        return east_coord, east

    if west == minimum:
        return west_coord, west

def get_shia_snake(data):
    for snake in data["snakes"]:
        if snake["id"] == SHIA_ID:
            return snake

def get_move(start, goal, data):
    wall_coords     = []
    start           = tuple(start)
    goal            = tuple(goal)

    for snake in data["snakes"]:
        if snake["id"] == SHIA_ID:
            for body in snake["coords"][1:]:
                wall_coords.append(tuple(body))
        else:
            for body in snake["coords"]:
                wall_coords.append(tuple(body))

    for wall in data["walls"]:
        wall_coords.append(tuple(wall))

    print "WALL COORDS"
    print wall_coords

    a = AStar()

    a.init_grid(data["height"],data["width"],wall_coords,start,goal)

    solution = a.solve()

    print solution

    if solution:
        return convert_direction(start, solution[1])

    return None


def convert_direction(start, coord):

    if start[0] > coord[0]:
        print "west"
        return "west"
    elif start[0] < coord[0]:
        print "east"
        return "east"

    if start[1] > coord[1]:
        print "north"
        return "north"

    print "south"
    return "south"


def make_heat_map(data):
    wall_coords = []
    heatMap = []

    for y in range(data["height"]):
        row = []
        for j in range(data["width"]):
            row.append(0)
        heatMap.append(row)


    for snake in data["snakes"]:
        if snake["id"] == SHIA_ID:
            for body in snake["coords"][1:]:
                wall_coords.append(body)
        else:
            for body in snake["coords"]:
                wall_coords.append(body)

    for wall in data["walls"]:
        wall_coords.append(wall)


    for wall in wall_coords:
        y = wall[0]
        x = wall[1]

        heatMap[y][x] = 4

        if y != 0:
            heatMap[y-1][x] += 1

        if y != (data["height"]-1):
            heatMap[y+1][x] += 1

        if x != 0:
            heatMap[y][x-1] += 1

        if x != (data["width"]-1):
            heatMap[y][x+1] += 1

    for y in range(data["height"]):
        for x in range(data["width"]):
            if x == 0 or x == (data["width"]-1):
                heatMap[y][x] += 1
            if y == 0 or y == (data["height"]-1):
                heatMap[y][x] += 1

    return heatMap

'''
Thanks to Laurent Luce for supplying A*
https://github.com/laurentluce/python-algorithms/
'''

class Cell(object):
    def __init__(self, x, y, reachable):
        """Initialize new cell.
        @param reachable is cell reachable? not a wall?
        @param x cell x coordinate
        @param y cell y coordinate
        @param g cost to move from the starting cell to this cell.
        @param h estimation of the cost to move from this cell
                 to the ending cell.
        @param f f = g + h
        """
        self.reachable = reachable
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0


class AStar(object):
    def __init__(self):
        # open list
        self.opened = []
        heapq.heapify(self.opened)
        # visited cells list
        self.closed = set()
        # grid cells
        self.cells = []
        self.grid_height = None
        self.grid_width = None

    def init_grid(self, width, height, walls, start, end):
        """Prepare grid cells, walls.
        @param width grid's width.
        @param height grid's height.
        @param walls list of wall x,y tuples.
        @param start grid starting point x,y tuple.
        @param end grid ending point x,y tuple.
        """
        self.grid_height = height
        self.grid_width = width
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if (x, y) in walls:
                    reachable = False
                else:
                    reachable = True
                self.cells.append(Cell(x, y, reachable))
        self.start = self.get_cell(*start)
        self.end = self.get_cell(*end)

    def get_heuristic(self, cell):
        """Compute the heuristic value H for a cell.
        Distance between this cell and the ending cell multiply by 10.
        @returns heuristic value H
        """
        return 10 * (abs(cell.x - self.end.x) + abs(cell.y - self.end.y))

    def get_cell(self, x, y):
        """Returns a cell from the cells list.
        @param x cell x coordinate
        @param y cell y coordinate
        @returns cell
        """
        return self.cells[x * self.grid_height + y]

    def get_adjacent_cells(self, cell):
        """Returns adjacent cells to a cell.
        Clockwise starting from the one on the right.
        @param cell get adjacent cells for this cell
        @returns adjacent cells list.
        """
        cells = []
        if cell.x < self.grid_width-1:
            cells.append(self.get_cell(cell.x+1, cell.y))
        if cell.y > 0:
            cells.append(self.get_cell(cell.x, cell.y-1))
        if cell.x > 0:
            cells.append(self.get_cell(cell.x-1, cell.y))
        if cell.y < self.grid_height-1:
            cells.append(self.get_cell(cell.x, cell.y+1))
        return cells

    def get_path(self):
        cell = self.end
        path = [(cell.x, cell.y)]
        while cell.parent is not self.start:
            cell = cell.parent
            path.append((cell.x, cell.y))

        path.append((self.start.x, self.start.y))
        path.reverse()
        return path

    def update_cell(self, adj, cell):
        """Update adjacent cell.
        @param adj adjacent cell to current cell
        @param cell current cell being processed
        """
        adj.g = cell.g + 10
        adj.h = self.get_heuristic(adj)
        adj.parent = cell
        adj.f = adj.h + adj.g

    def solve(self):
        """Solve maze, find path to ending cell.
        @returns path or None if not found.
        """
        # add starting cell to open heap queue
        heapq.heappush(self.opened, (self.start.f, self.start))
        while len(self.opened):
            # pop cell from heap queue
            f, cell = heapq.heappop(self.opened)
            # add cell to closed list so we don't process it twice
            self.closed.add(cell)
            # if ending cell, return found path
            if cell is self.end:
                return self.get_path()
            # get adjacent cells for cell
            adj_cells = self.get_adjacent_cells(cell)
            for adj_cell in adj_cells:
                if adj_cell.reachable and adj_cell not in self.closed:
                    if (adj_cell.f, adj_cell) in self.opened:
                        # if adj cell in open list, check if current path is
                        # better than the one previously found
                        # for this adj cell.
                        if adj_cell.g > cell.g + 10:
                            self.update_cell(adj_cell, cell)
                    else:
                        self.update_cell(adj_cell, cell)
                        # add adj cell to open list
                        heapq.heappush(self.opened, (adj_cell.f, adj_cell))


def food_eval(heat_map, data_food, our_head):
        food_distance = []
        for food in data_food:
            food_distance.append(get_distance(our_head, food))
        sorted(food_distance)
        for food in food_distance:
            print food
            if(is_food_safe(food[1], 0, heat_map)):
                return food[1]
        for food in food_distance:
            print food
            if(is_food_safe(food[1], 1, heat_map)):
                return food[1]
        for food in food_distance:
            print food
            if(is_food_safe(food[1], 2, heat_map)):
                return food[1]
        for food in food_distance:
            print food
            if(is_food_safe(food[1], 3, heat_map)):
                return food[1]
        for food in food_distance:
            print food
            if(is_food_safe(food[1], 4, heat_map)):
                return food[1]

def get_distance(our_head, food_coords):
    x_distance = abs(our_head[0] - food_coords[0])
    y_distance = abs(our_head[1] - food_coords[1])
    return [ x_distance + y_distance , food_coords]

def is_food_safe(food_coords, threshold, heat_map):
    return heat_map[food_coords[0]][food_coords[1]] <= threshold

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
