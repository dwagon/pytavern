""" Define the world """

import math
import random
import sys
from astar import AStar

from .customer import Customer
from .staff import Staff
from .stool import Stool
from .wall import Wall
from .door import Door
from .supply import Supply
from .location import Location
from .coord import Coord, OutOfBoundsError


##############################################################################
class Tavern(AStar):
    """ World Class definition """
    def __init__(self, **kwargs):
        self.size_x = kwargs.get('size_x', 20)
        self.size_y = kwargs.get('size_y', 20)
        self.locations = {}
        self.supply_types = ['beer', 'food', 'water']
        self.customer_num = 0
        self.num_supplies = kwargs.get('num_supplies', 1)
        self.num_staff = kwargs.get('num_staff', 1)
        self.num_stools = kwargs.get('num_stools', 10)
        self.max_customers = kwargs.get('max_customers', 10)
        self.staff = []
        self.supplies = []
        self.stools = []
        self.customers = []
        self.door = Coord(0, 1)
        self.time = 0
        for x in range(self.size_x):
            for y in range(self.size_y):
                self.locations[Coord(x, y)] = Location()

    ##########################################################################
    def populate(self):
        """ Populate the tavern """
        self.draw_walls()
        self.new_customer()
        self.generate_supplies()
        for i in range(self.num_staff):
            pos = self.free_location('person')
            serv = Staff(tavern=self, name=f"Staff_{i}", pos=pos)
            self.locations[pos].add(serv)
            self.staff.append(serv)
        for i in range(self.num_stools):
            pos = self.free_location('furniture')
            stol = Stool(tavern=self, name=f"Stool_{i}", pos=pos)
            self.locations[pos].add(stol)
            self.stools.append(stol)

    ##########################################################################
    def generate_supplies(self):
        """ Generate the supply stations for all the types of supplies """
        for suppl in self.supply_types:
            for i in range(self.num_supplies):
                pos = self.free_location('installation')
                supply = Supply(tavern=self, name=f"Supply_{suppl}_{i}", pos=pos, supplytype=suppl)
                self.locations[pos].add(supply)
                self.supplies.append(supply)

    ##########################################################################
    def draw_walls(self):
        """ Draw the walls around the place """
        for x in range(self.size_x):
            for y in range(self.size_y):
                pos = Coord(x, y)
                if pos == self.door:
                    self.locations[pos].add(Door(self, "Door", pos))
                elif x == 0 or y == 0 or x == self.size_x - 1 or y == self.size_y - 1:
                    self.locations[pos].add(Wall(self, "Wall", pos))

    ##########################################################################
    def new_customer(self):
        """ Create a new customer """
        if not self.locations[self.door].isempty('person'):
            return
        if len(self.customers) >= self.max_customers:
            return
        cust = Customer(tavern=self, name=f"Customer_{self.customer_num}", pos=self.door)
        self.locations[self.door].add(cust)
        self.customers.append(cust)
        self.customer_num += 1
        print(f"{cust} has arrived")

    ##########################################################################
    def turn(self):
        """ Time passing """
        print(f"Time={self.time}")
        odds = 10 - len(self.customers)
        if random.randrange(1, 100) < odds:
            self.new_customer()
        for cust in self.customers:
            cust.turn()
            if cust.terminate:
                print(f"Customer {cust} has left the tavern")
                self.locations[cust.pos].delete('person')
                self.customers.remove(cust)
        for supply in self.supplies:
            supply.turn()
        for stff in self.staff:
            stff.turn()
        self.time += 1
        if self.time > 5000:
            sys.exit(0)

    ##########################################################################
    def free_location(self, category):
        """ Find a free location in the tavern """
        found = False
        while not found:
            x = random.randrange(0, self.size_x)
            y = random.randrange(0, self.size_y)
            pos = Coord(x, y)
            if self.locations[pos].isempty(category):
                return pos

    ##########################################################################
    def find_route(self, src, dest):
        """ Find a route between two points """
        if hasattr(src, 'pos'):
            srcpos = src.pos
        else:
            srcpos = src
        if hasattr(dest, 'pos'):
            destpos = dest.pos
        else:
            destpos = dest
        route = self.astar(srcpos, destpos)
        return route

    ##########################################################################
    def heuristic_cost_estimate(self, n1, n2):  # pylint: disable=arguments-differ
        """computes the 'direct' distance between two (x,y) tuples"""
        (x1, y1) = n1.x, n1.y
        (x2, y2) = n2.x, n2.y
        hce = math.hypot(x2 - x1, y2 - y1)
        return hce

    ##########################################################################
    def distance_between(self, n1, n2):
        """this method always returns 1, as two 'neighbors' are always adajcent"""
        return 1

    ##########################################################################
    def is_goal_reached(self, current, goal):
        """ Succeed if we are adjacent to the goal """
        nx = current.x
        ny = current.y
        for tmpx, tmpy in [(nx, ny-1), (nx+1, ny), (nx, ny+1), (nx-1, ny)]:
            try:
                tmpgoal = Coord(tmpx, tmpy, self.size_x, self.size_y)
            except OutOfBoundsError:
                continue
            if goal == tmpgoal:
                return True
        return False

    ##########################################################################
    def neighbors(self, node):
        """ for a given coordinate in the maze, returns up to 4 adjacent
        (north, east, south, west) nodes that can be reached
        (=any adjacent coordinate that is not a wall)
        """
        nx, ny = node.x, node.y
        ans = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                nbx = nx + dx
                nby = ny + dy
                try:
                    pos = Coord(nbx, nby, self.size_x, self.size_y)
                except OutOfBoundsError:
                    continue
                if not self.locations[pos].isempty():
                    continue
                ans.append(pos)
        return ans

    ##########################################################################
    def move(self, obj, newloc):
        """ Move an object to a new location """
        self.locations[obj.pos].delete(obj.category)
        self.locations[newloc].add(obj)
        obj.pos = newloc

    ##########################################################################
    def mainloop(self):
        """ Run forever """
        while True:
            self.turn()
            print(self.draw())

    ##########################################################################
    def draw(self, zroute=None):
        """ Return a string representation of the tavern """
        result = ''
        if zroute is None:
            zroute = []
        route_path = list(zroute)
        for y in range(self.size_y):
            for x in range(self.size_x):
                pos = Coord(x, y)
                if pos in self.locations:
                    result += self.locations[pos].repr()
                elif pos in route_path:
                    result += '*'
                else:
                    result += '.'
            if y < len(self.customers):
                result += self.customers[y].description()

            index = y - len(self.customers)
            if index >= 0 and index < len(self.staff):
                stf = self.staff[index]
                result += f" {stf.name}@{stf.pos} Has {stf.supplies}"

            index = y - len(self.customers) - len(self.staff)
            if index >= 0 and index < len(self.supplies):
                result += f" {self.supplies[index].name} {self.supplies[index].amount}"

            result += '\n'
        return result

# EOF
