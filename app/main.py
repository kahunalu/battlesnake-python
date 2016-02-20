import bottle
import os

taunts = ["DO IT! JUST DO IT!", "DON’T LET YOUR DREAMSSSS BE DREAMSSSS.", "JUSSSST DO IT!", "IF YOU’RE TIRED OF SSSSTARTING OVER, SSSSTOP GIVING UP.", "YESSSS YOU CAN. JUST DO IT.", "NOTHING IS IMPOSSIBLE.", "YESSSS YOU CAN.", "NOTHING IS IMPOSSSSSSSSIBLE", "DON'T SSSSTOP!", "SSSSTOP GIVING UP", "YESSSS YOU CAN."]


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


    # TODO: Do things with data

    return {
        'move': 'north',
        'taunt': taunts[(data['turn'] % len(taunts))]
    }


@bottle.post('/end')
def end():
    data = bottle.request.json

    # TODO: Do things with data

    return {
        'taunt': 'battlesnake-python!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))

'''

def a_star(start, goal):
    ClosedSet   = []
    OpenSet     = [start]
    Came_From   = []

    g_score = [-1]
    g_score[start] = 0

    f_score = [-1]
    f_score[start] = heuristic(start, goal)

    while len(OpenSet):
        current := the node in OpenSet having the lowest f_score[] value
        if current = goal
            return reconstruct_path(Came_From, goal)

        OpenSet.Remove(current)
        ClosedSet.Add(current)
        for each neighbor of current
            if neighbor in ClosedSet
                continue		// Ignore the neighbor which is already evaluated.
            tentative_g_score := g_score[current] + dist_between(current,neighbor) // length of this path.
            if neighbor not in OpenSet	// Discover a new node
                OpenSet.Add(neighbor)
            else if tentative_g_score >= g_score[neighbor]
                continue		// This is not a better path.

            // This path is the best until now. Record it!
            Came_From[neighbor] := current
            g_score[neighbor] := tentative_g_score
            f_score[neighbor] := g_score[neighbor] + heuristic_cost_estimate(neighbor, goal)

    return failure

function reconstruct_path(Came_From,current)
    total_path := [current]
    while current in Came_From.Keys:
        current := Came_From[current]
        total_path.append(current)
    return total_path

'''
