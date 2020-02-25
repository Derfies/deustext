import networkx as nx


import adventurelib as al
from roomloader import RoomLoader


@al.when('north', direction='north')
@al.when('south', direction='south')
@al.when('east', direction='east')
@al.when('west', direction='west')
def go(direction):
    global current_room
    room = current_room.exit(direction)
    if room:
        current_room = room
        al.say('You go {}.'.format(direction))
        look()
    else:
        al.say('You can\'t go {}.'.format(direction))


@al.when('look')
def look():
    al.say(current_room)


    msg = 'Exists are '
    for exit in current_room.exits():
        msg += exit + ' '
    msg += '.'
    al.say(msg)



g = nx.path_graph(4)
nodes = list(g.nodes())
g.add_edge(nodes[-1], nodes[0])
loader = RoomLoader(g)
current_room = loader.root_room


look()
al.start()