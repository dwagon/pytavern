#!/usr/bin/env python3
""" Define the world """
import math
import random
import sys
from astar import AStar

from customer import Customer
from staff import Staff
from wall import Wall
from furniture import Table, Chair
from supply import Supply
from coord import Coord, OutOfBoundsError


##############################################################################
class Pub(AStar):
    """ World Class definition """
    def __init__(self, size_x=40, size_y=15):
        self.size_x = size_x
        self.size_y = size_y
        self.data = {}
        self.customer_num = 0
        self.num_customers = 1
        self.num_supplies = 2
        self.num_staff = 1
        self.num_tables = 3
        self.num_chairs = 8
        self.tables = []
        self.chairs = []
        self.staff = []
        self.supplies = []
        self.customers = []
        self.time = 0
        self.flags = {
            'new_customers': False
        }

    ##########################################################################
    def populate(self):
        """ Populate the pub """
        self.add_walls()
        self.add_tables()
        self.add_chairs()
        self.new_customer()
        for i in range(self.num_supplies):
            pos = self.free_location()
            supply = Supply(pub=self, name=f"Supply_{i}", pos=pos)
            self.data[pos] = supply
            self.supplies.append(supply)
        for i in range(self.num_staff):
            pos = self.free_location()
            serv = Staff(pub=self, name=f"Staff_{i}", pos=pos)
            self.data[pos] = serv
            self.staff.append(serv)

    ##########################################################################
    def add_chairs(self):
        """ Add in a number of chairs """
        for chrnum in range(self.num_chairs):
            avail = self.table_adjacent()
            if avail:
                pos = random.choice(list(avail))
            else:
                pos = self.free_location()
            chair = Chair(self, f"Chair {chrnum}", pos)
            self.data[pos] = chair
            self.chairs.append(chair)

    ##########################################################################
    def table_adjacent(self):
        """ Return a free position adjacent to a table """
        avail = set()
        for tbl in self.tables:
            for pos in tbl.positions():
                for x in (-1, 0, 1):
                    for y in (-1, 0, 1):
                        if abs(x) + abs(y) in (0, 2):   # No corner cases
                            continue
                        adjacent = Coord(pos.x + x, pos.y + y)
                        if adjacent not in self.data:
                            avail.add(adjacent)
        return avail

    ##########################################################################
    def add_tables(self):
        """ Add in a number of tables """
        for tbl in range(self.num_tables):
            placed = False
            while not placed:
                poslist = self.find_space_for_table()
                if not poslist:
                    continue
                table = Table(self, f"Table {tbl}", poslist[0])
                self.tables.append(table)
                for pos in poslist:
                    table.add_position(pos)
                    self.data[pos] = table
                    placed = True

    ##########################################################################
    def find_space_for_table(self):
        """ Tables are 2x2 - find a free location """
        pos = self.free_location()
        poslist = []
        for bit in ((0, 0), (0, 1), (1, 1), (1, 0)):
            newpos = Coord(pos.x + bit[0], pos.y + bit[1])
            if newpos in self.data:
                return None
            poslist.append(newpos)
        return poslist

    ##########################################################################
    def add_walls(self):
        """ Add in the walls around the perimeter """
        for x in range(self.size_x):
            pos = Coord(x, 0)
            self.data[pos] = Wall(self, pos)
            pos = Coord(x, self.size_y-1)
            self.data[pos] = Wall(self, pos)

        for y in range(self.size_y):
            pos = Coord(0, y)
            self.data[pos] = Wall(self, pos)
            pos = Coord(self.size_x-1, y)
            self.data[pos] = Wall(self, pos)

    ##########################################################################
    def new_customer(self):
        """ Create a new customer """
        pos = Coord(1, 1)
        if pos in self.data:
            return
        cust = Customer(pub=self, name=f"Customer_{self.customer_num}", pos=pos)
        self.data[pos] = cust
        self.customers.append(cust)
        self.customer_num += 1

    ##########################################################################
    def turn(self):
        """ Time passing """
        print(f"Time={self.time}")
        odds = 10 - len(self.customers)
        if self.flags['new_customers'] and random.randrange(1, 100) < odds:
            self.new_customer()
        for cust in self.customers:
            rc = cust.turn(self.time)
            if not rc:
                print(f"Customer {cust} has left the pub")
                del self.data[cust.pos]
                self.customers.remove(cust)
        for supply in self.supplies:
            supply.turn(self.time)
        for stff in self.staff:
            rc = stff.turn(self.time)
            if not rc:
                sys.exit(0)
        self.time += 1

    ##########################################################################
    def find_empty_chair(self):
        """ Find a chair that is currently empty """
        for chair in self.chairs:
            if not chair.occupant:
                return chair
        return None

    ##########################################################################
    def free_location(self):
        """ Find a free location in the pub """
        tries = 0
        while tries < 100:
            tries += 1
            x = random.randrange(0, self.size_x)
            y = random.randrange(0, self.size_y)
            pos = Coord(x, y)
            if pos not in self.data:
                return pos
        print(f"Couldn't find a free location in {tries} attempts")
        sys.exit(1)

    ##########################################################################
    def find_route(self, src, dest, adjacent=False):
        """ Find a route between two points (or adjacent to dest) """
        # print(f"find_route({src=},{dest=}, {adjacent=})")
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
                deltapos = Coord(destpos.x + delta[0], destpos.y + delta[1])
                route = self.astar(srcpos, deltapos)
                if route is None:
                    return route
                routelen = len(list(route))
                if routelen < maxlen:
                    maxlen = routelen
                    shortdest = deltapos
            destpos = shortdest
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
        """ This method always returns 1, as two 'neighbors' are always adjacent """
        return 1

    ##########################################################################
    def x_is_goal_reached(self, current, goal):
        """ Succeed if we have arrived """
        if current == goal:
            return True
        return False

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
            if pos in self.data:
                if not self.data[pos].permeable:
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
        """ Return a string representation of the pub """
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
                result += f"  {cust.name}@{cust.pos} mode={cust.mode}"
                if cust.target:
                    result += f" -> {cust.target}"

            index = y - len(self.customers)
            if index >= 0 and index < len(self.staff):
                stf = self.staff[index]
                result += f"  {stf.name}@{stf.pos} mode={stf.mode}"
                if stf.target:
                    result += f" -> {stf.target}"

            index = y - len(self.customers) - len(self.staff)
            if index >= 0 and index < len(self.supplies):
                result += f"  {self.supplies[index].name} {self.supplies[index].amount}"

            result += '\n'
        return result


##############################################################################
if __name__ == "__main__":
    tavern = Pub()
    tavern.populate()
    tavern.mainloop()
    myroute = tavern.find_route(tavern.staff[0], tavern.customers[0])
    print(tavern.draw(myroute))

# EOF
