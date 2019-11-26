#!/usr/bin/env python3
""" Define the world """
import math
import random
import sys
from astar import AStar

from .customer import Customer
from .staff import Staff
from .stool import Stool
from .supply import Supply
from .coord import Coord, OutOfBoundsError


##############################################################################
class Tavern(AStar):
    """ World Class definition """
    def __init__(self, size_x=20, size_y=20):
        self.size_x = size_x
        self.size_y = size_y
        self.data = {}
        self.customer_num = 0
        self.num_customers = 5
        self.num_supplies = 2
        self.num_staff = 1
        self.num_stools = 10
        self.staff = []
        self.supplies = []
        self.stools = []
        self.customers = []
        self.time = 0

    ##########################################################################
    def populate(self):
        """ Populate the tavern """
        self.new_customer()
        for i in range(self.num_supplies):
            pos = self.free_location()
            supply = Supply(tavern=self, name=f"Supply_{i}", pos=pos)
            self.data[pos] = supply
            self.supplies.append(supply)
        for i in range(self.num_staff):
            pos = self.free_location()
            serv = Staff(tavern=self, name=f"Staff_{i}", pos=pos)
            self.data[pos] = serv
            self.staff.append(serv)
        for i in range(self.num_stools):
            pos = self.free_location()
            stol = Stool(tavern=self, name=f"Stool_{i}", pos=pos)
            self.data[pos] = stol
            self.stools.append(stol)

    ##########################################################################
    def new_customer(self):
        """ Create a new customer """
        pos = Coord(0, 0)
        if pos in self.data:
            return
        cust = Customer(tavern=self, name=f"Customer_{self.customer_num}", pos=pos)
        self.data[pos] = cust
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
            rc = cust.turn()
            if not rc:
                print(f"Customer {cust} has left the tavern")
                del self.data[cust.pos]
                self.customers.remove(cust)
        for supply in self.supplies:
            supply.turn()
        for stff in self.staff:
            stff.turn()
        self.time += 1
        if self.time > 5000:
            sys.exit(0)

    ##########################################################################
    def free_location(self):
        """ Find a free location in the tavern """
        found = False
        while not found:
            x = random.randrange(0, self.size_x)
            y = random.randrange(0, self.size_y)
            pos = Coord(x, y)
            if pos not in self.data:
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
        for nbx, nby in ((nx, ny-1), (nx+1, ny), (nx, ny+1), (nx-1, ny)):
            try:
                pos = Coord(nbx, nby, self.size_x, self.size_y)
            except OutOfBoundsError:
                continue
            if pos in self.data:
                continue
            ans.append(pos)
        return ans

    ##########################################################################
    def move(self, obj, newloc):
        """ Move an object to a new location """
        del self.data[obj.pos]
        self.data[newloc] = obj

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
                if pos in self.data:
                    result += self.data[pos].repr
                elif pos in route_path:
                    result += '*'
                else:
                    result += '.'
            if y < len(self.customers):
                cust = self.customers[y]
                result += f"  {cust.name}@{cust.pos}"
                if cust.target:
                    result += f" -> {cust.target}"
                if cust.demands['amount']:
                    result += f" Demands: {cust.demands['amount']}"

            index = y - len(self.customers)
            if index >= 0 and index < len(self.staff):
                stf = self.staff[index]
                result += f"  {stf.name}@{stf.pos} Has {stf.supplies}"

            index = y - len(self.customers) - len(self.staff)
            if index >= 0 and index < len(self.supplies):
                result += f"  {self.supplies[index].name} {self.supplies[index].amount}"

            result += '\n'
        return result


##############################################################################
if __name__ == "__main__":
    tavern = Tavern()
    tavern.populate()
    tavern.mainloop()

# EOF
