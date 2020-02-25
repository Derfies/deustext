import os
import sys
path = r'C:\Users\Jamie Davies\Documents\git\pglib\tests'
if path not in sys.path:
    sys.path.append(path)
import logging

import enum
import networkx as nx

import adventurelib as al
from pglib.graph.const import Direction as OrthDirection, DIRECTION
from ortho import OrthogonalLayouter


logger = logging.getLogger(__name__)
logging.basicConfig()


class Direction(enum.Enum):

    north = 0
    east = 1
    south = 2
    west = 3


class RoomLoader(object):

    def __init__(self, g):
        self.layouter = OrthogonalLayouter(g)
        self.layouter.run()
        self.root_room = self.create_rooms(self.layouter.graphs[0])

    def create_rooms(self, g):
        rooms = {}
        for node in g:
            room = al.Room(str(node))
            rooms[node] = room

        for edge in g.edges(data=True):
            head, tail, data = edge
            src_room = rooms[head]
            tgt_room = rooms[tail]
            forward_dir = data[DIRECTION]
            #reverse_dir = OrthDirection.opposite(forward_dir)

            al_forward_dir = Direction(forward_dir)
            #al_reverse_dir = Direction(reverse_dir)

            #print al_forward_dir.name
            setattr(src_room, al_forward_dir.name, tgt_room)
            #logger.info(src_room, str(al_forward_dir), tgt_room)
            #print edge, al_forward_dir, al_reverse_dir
            #src_room.east = tgt_room

        return rooms[list(g)[0]]


if __name__ == '__main__':
    g = nx.path_graph(4)
    nodes = list(g.nodes())
    g.add_edge(nodes[-1], nodes[0])
    loader = RoomLoader(g)