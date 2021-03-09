""" Implementation of the Map """

import math
import random
import sys
from astar import AStar
from coord import Coord, OutOfBoundsError


##############################################################################
class MapCollision(Exception):
    """ Something is already in that location """
    pass


##############################################################################
class Map(AStar):
    """ Map definition """
    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        self.data = {
            'BUILDING': {},
            'FURNITURE': {},
            'PEOPLE': {},
        }

    ##########################################################################
    def _random_loc(self):
        """ Return a random location on the map """
        x = random.randrange(0, self.size_x)
        y = random.randrange(0, self.size_y)
        pos = Coord(x, y)
        return pos

    ##########################################################################
    def free_building_loc(self):
        """ Find a free building location in the map """
        tries = 0
        while tries < 100:
            tries += 1
            pos = self._random_loc()
            if pos not in self.data['BUILDING']:
                return pos
        print(f"Couldn't find a free building location in {tries} attempts")
        sys.exit(1)

    ##########################################################################
    def free_furniture_loc(self):
        """ Return a free furniture location """
        tries = 0
        while tries < 100:
            tries += 1
            pos = self._random_loc()
            if pos not in self.data['BUILDING'] and pos not in self.data['FURNITURE']:
                return pos
        print(f"Couldn't find a free furniture location in {tries} attempts")
        sys.exit(1)

    ##########################################################################
    def free_people_loc(self):
        """ Return a free people location """
        tries = 0
        while tries < 100:
            tries += 1
            pos = self._random_loc()
            if pos not in self.data['BUILDING'] and \
               pos not in self.data['FURNITURE'] and pos not in self.data['PEOPLE']:
                return pos
        print(f"Couldn't find a free people location in {tries} attempts")
        sys.exit(1)

    ##########################################################################
    def _is_empty(self, layer, pos):
        """ Return if a location in a layer is empty """
        return pos not in self.data[layer]

    ##########################################################################
    def is_building_empty(self, pos):
        """ Return if building spot is empty """
        return self._is_empty('BUILDING', pos)

    ##########################################################################
    def is_furniture_empty(self, pos):
        """ Return if furniture spot is empty """
        return self._is_empty('BUILDING', pos) and self._is_empty('FURNITURE', pos)

    ##########################################################################
    def is_person_empty(self, pos):
        """ Return if person spot is empty """
        return self._is_empty('BUILDING', pos) and \
            self._is_empty('FURNITURE', pos) and self._is_empty('PERSON', pos)

    ##########################################################################
    def _del_item(self, layer, pos):
        """ Delete an item from the map """
        del self.data[layer][pos]

    ##########################################################################
    def del_building(self, pos):
        """ Delete building element """
        self._del_item('BUILDING', pos)

    ##########################################################################
    def del_furniture(self, pos):
        """ Delete furniture """
        self._del_item('FURNITURE', pos)

    ##########################################################################
    def del_people(self, pos):
        """ Delete people """
        self._del_item('PEOPLE', pos)

    ##########################################################################
    def _add_item(self, layer, pos, obj):
        """ Add an item to the map """
        if pos in self.data[layer]:
            raise MapCollision(f"{layer=} {pos=} {obj=} {self.data[layer][pos]=}")
        self.data[layer][pos] = obj

    ##########################################################################
    def add_building(self, pos, obj):
        """ Add building element """
        self._add_item('BUILDING', pos, obj)

    ##########################################################################
    def add_furniture(self, pos, obj):
        """ Add furniture """
        self._add_item('FURNITURE', pos, obj)

    ##########################################################################
    def add_people(self, pos, obj):
        """ Add people """
        self._add_item('PEOPLE', pos, obj)

    ##########################################################################
    def heuristic_cost_estimate(self, n1, n2):  # pylint: disable=arguments-differ
        """computes the 'direct' distance between two (x,y) tuples"""
        (x1, y1) = n1.x, n1.y
        (x2, y2) = n2.x, n2.y
        hce = math.hypot(x2 - x1, y2 - y1)
        return hce

    ##########################################################################
    def distance_between(self, n1, n2):
        """ This method always returns 1, as two 'neighbors' are always adjacent """
        return 1

    ##########################################################################
    def neighbors(self, node):
        """ for a given coordinate in the world, returns up to 4 adjacent
        (north, east, south, west) nodes that can be reached
        (=any adjacent coordinate that is not a wall)
        """
        nx, ny = node.x, node.y
        ans = []
        for nbx, nby in ((nx, ny-1), (nx+1, ny), (nx, ny+1), (nx-1, ny)):
            try:
                pos = Coord(nbx, nby, self.size_x, self.size_y)
            except OutOfBoundsError:
                continue
            if pos in self.data['BUILDING']:
                if not self.data['BUILDING'][pos].permeable:
                    continue
            if pos in self.data['FURNITURE']:
                if not self.data['FURNITURE'][pos].permeable:
                    continue
            if pos in self.data['PEOPLE']:
                if not self.data['PEOPLE'][pos].permeable:
                    continue
            ans.append(pos)
        return ans

    ##########################################################################
    def find_route(self, src, dest, adjacent=False):
        """ Find a route between two points (or adjacent to dest) """
        # print(f"find_route({src=},{dest=}, {adjacent=})") # DBG
        if hasattr(src, 'pos'):
            srcpos = src.pos
        else:
            srcpos = src
        if hasattr(dest, 'pos'):
            destpos = dest.pos
        else:
            destpos = dest
        if adjacent:
            maxlen = 9999
            shortdest = None
            for delta in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                try:
                    deltapos = Coord(destpos.x + delta[0], destpos.y + delta[1])
                except OutOfBoundsError:
                    continue
                route = self.astar(srcpos, deltapos)
                if route is None:
                    continue
                routelen = len(list(route))
                if routelen < maxlen:
                    maxlen = routelen
                    shortdest = deltapos
            destpos = shortdest
        # print(f"find_route({srcpos=},{destpos=})")    # DBG
        route = self.astar(srcpos, destpos)
        return route

    ##########################################################################
    def repr(self, pos):
        """ Return representation of a location """
        for layer in ('PEOPLE', 'FURNITURE', 'BUILDING'):
            if pos in self.data[layer]:
                return self.data[layer][pos].repr
        return '.'

# EOF
