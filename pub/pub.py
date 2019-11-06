#!/usr/bin/env python3
""" Define the world """
import math
import random
import sys
from astar import AStar

from customer import Customer
from staff import Staff
from supply import Supply


##############################################################################
class Pub(AStar):
    """ World Class definition """
    def __init__(self, size_x=20, size_y=20):
        self.size_x = size_x
        self.size_y = size_y
        self.data = {}
        self.num_customers = 5
        self.num_supplies = 2
        self.num_staff = 1
        self.staff = []
        self.supplies = []
        self.customers = []
        self.time = 0

    ##########################################################################
    def populate(self):
        """ Populate the pub """
        for i in range(self.num_customers):
            x, y = self.free_location()
            cust = Customer(pub=self, name=f"Customer_{i}", x=x, y=y)
            self.data[(x, y)] = cust
            self.customers.append(cust)
        for i in range(self.num_supplies):
            x, y = self.free_location()
            supply = Supply(pub=self, name=f"Supply_{i}", x=x, y=y)
            self.data[(x, y)] = supply
            self.supplies.append(supply)
        for i in range(self.num_staff):
            x, y = self.free_location()
            serv = Staff(pub=self, name=f"Staff_{i}", x=x, y=y)
            self.data[(x, y)] = serv
            self.staff.append(serv)

    ##########################################################################
    def turn(self):
        """ Time passing """
        print(f"Time={self.time}")
        for cust in self.customers:
            rc = cust.turn(self.time)
            if not rc:
                print(f"Customer {cust} has left the pub")
                del self.data[(cust.x, cust.y)]
                self.customers.remove(cust)
        for supply in self.supplies:
            supply.turn(self.time)
        for stff in self.staff:
            rc = stff.turn(self.time)
            if not rc:
                sys.exit(0)
        self.time += 1

    ##########################################################################
    def free_location(self):
        """ Find a free location in the pub """
        found = False
        while not found:
            x = random.randrange(0, self.size_x)
            y = random.randrange(0, self.size_y)
            if (x, y) not in self.data:
                return (x, y)

    ##########################################################################
    def find_route(self, src, dest):
        """ Find a route between two points """
        route = self.astar((src.x, src.y), (dest.x, dest.y))
        return route

    ##########################################################################
    def heuristic_cost_estimate(self, n1, n2):  # pylint: disable=arguments-differ
        """computes the 'direct' distance between two (x,y) tuples"""
        (x1, y1) = n1
        (x2, y2) = n2
        hce = math.hypot(x2 - x1, y2 - y1)
        return hce

    ##########################################################################
    def distance_between(self, n1, n2):
        """this method always returns 1, as two 'neighbors' are always adajcent"""
        return 1

    ##########################################################################
    def is_goal_reached(self, current, goal):
        """ Succeed if we are adjacent to the goal """
        nx = current[0]
        ny = current[1]
        for tmpgoal in ((nx, ny-1), (nx+1, ny), (nx, ny+1), (nx-1, ny)):
            if goal[0] == tmpgoal[0] and goal[1] == tmpgoal[1]:
                return True
        return False

    ##########################################################################
    def neighbors(self, node):
        """ for a given coordinate in the maze, returns up to 4 adjacent
        (north, east, south, west) nodes that can be reached
        (=any adjacent coordinate that is not a wall)
        """
        nx, ny = node
        ans = []
        for nb in ((nx, ny-1), (nx+1, ny), (nx, ny+1), (nx-1, ny)):
            x, y = nb
            if (x, y) in self.data:
                continue
            if x < 0 or y < 0:
                continue
            if x > self.size_x or y > self.size_y:
                continue
            ans.append((x, y))
        return ans

    ##########################################################################
    def move(self, obj, newloc):
        """ Move an object to a new location """
        del self.data[(obj.x, obj.y)]
        self.data[(newloc[0], newloc[1])] = obj

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
                if (x, y) in self.data:
                    result += self.data[(x, y)].repr
                elif (x, y) in route_path:
                    result += '*'
                else:
                    result += '.'
            if y < len(self.customers):
                result += f"  {self.customers[y].name} {self.customers[y].demands['amount']}"

            index = y - len(self.customers)
            if index >= 0 and index < len(self.staff):
                result += f"  {self.staff[index].name} {self.staff[index].supplies}"

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
