import bottle
import os

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

<<<<<<< HEAD

    # TODO: Do things with data
=======
    get_mode(data)
>>>>>>> 0adf26be1f52bb3c750308267983813540dc1a89

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

def get_mode(data):
    if True:
        default(data)
    elif False:
        default(data)


def default(data):
    shia = get_shia_snake(data)
    get_move(shia["coords"][0], [0,0], data)


def get_shia_snake(data):
    for snake in data["snakes"]:
        if snake["id"] == SHIA_ID:
            return snake


def get_move(start, goal, grid):
    

    return {"North"}


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
