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
    if True:
        return default(data)
    elif False:
        return default(data)


def default(data):
    shia = get_shia_snake(data)
    return get_move(shia["coords"][0], data["food"][0], data)


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

    print "DEBUG"

    print start
    print coord

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


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
