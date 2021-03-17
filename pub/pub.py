#!/usr/bin/env python3
""" Define the world """
import random
import statistics

from customer import Customer
from map import Map
from staff import Staff
from wall import Wall
from door import Door
from furniture import Table, Chair
from supply import Supply
from coord import Coord


##############################################################################
class Pub():
    """ World Class definition """
    def __init__(self, size_x=40, size_y=15):
        self.size_x = size_x
        self.size_y = size_y
        self.map = Map(size_x, size_y)
        self.customer_num = 0
        self.num_customers = 1
        self.num_supplies = 2
        self.num_staff = 2
        self.num_tables = 3
        self.num_chairs = 8
        self.tables = []
        self.door = None
        self.chairs = []
        self.staff = []
        self.supplies = []
        self.old_customers = []
        self.customers = []
        self.time = 0
        self.flags = {
            'new_customers': True,
            'terminate': False
        }

    ##########################################################################
    def populate(self):
        """ Populate the pub """
        self.door = Door(self, Coord(0, 1))
        self.map.add_building(self.door.pos, self.door)
        self.add_walls()
        self.add_tables()
        self.add_chairs()
        self.new_customer()
        for i in range(self.num_supplies):
            pos = self.map.free_furniture_loc()
            supply = Supply(pub=self, name=f"Supply_{i}", pos=pos)
            self.map.add_furniture(pos, supply)
            self.supplies.append(supply)
        for i in range(self.num_staff):
            pos = self.map.free_people_loc()
            serv = Staff(pub=self, name=f"Staff_{i}", pos=pos)
            self.map.add_people(pos, serv)
            self.staff.append(serv)

    ##########################################################################
    def add_chairs(self):
        """ Add in a number of chairs """
        for chrnum in range(self.num_chairs):
            avail = self.table_adjacent()
            if avail:
                pos = random.choice(list(avail))
            else:
                pos = self.map.free_furniture_loc()
            chair = Chair(self, f"Chair {chrnum}", pos)
            self.map.add_furniture(pos, chair)
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
                        if self.map.is_furniture_empty(adjacent):
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
                    self.map.add_furniture(pos, table)
                    placed = True

    ##########################################################################
    def find_space_for_table(self):
        """ Tables are 2x2 - find a free location that is not too close to
            another table or the door
        """
        bad = True
        while bad:
            pos = self.map.free_furniture_loc()
            if pos.dist(self.door.pos) < 5:
                continue
            bad = False
            for tbl in self.tables:
                if pos.dist(tbl.pos) < 5:
                    bad = True
                    continue
        poslist = []
        for bit in ((0, 0), (0, 1), (1, 1), (1, 0)):
            newpos = Coord(pos.x + bit[0], pos.y + bit[1])
            if not self.map.is_furniture_empty(newpos):
                return None
            poslist.append(newpos)
        return poslist

    ##########################################################################
    def add_walls(self):
        """ Add in the walls around the perimeter """
        for x in range(self.size_x):
            pos = Coord(x, 0)
            if self.map.is_building_empty(pos):
                self.map.add_building(pos, Wall(self, pos))

            pos = Coord(x, self.size_y-1)
            if self.map.is_building_empty(pos):
                self.map.add_building(pos, Wall(self, pos))

        for y in range(self.size_y):
            pos = Coord(0, y)
            if self.map.is_building_empty(pos):
                self.map.add_building(pos, Wall(self, pos))

            pos = Coord(self.size_x-1, y)
            if self.map.is_building_empty(pos):
                self.map.add_building(pos, Wall(self, pos))

    ##########################################################################
    def new_customer(self):
        """ Create a new customer """
        pos = self.door.pos
        if self.map.is_person_empty(pos):
            cust = Customer(pub=self, name=f"Customer_{self.customer_num}", pos=pos)
            self.map.add_people(pos, cust)
            self.customers.append(cust)
            self.customer_num += 1
        else:
            print("Door is not empty")

    ##########################################################################
    def turn(self):
        """ Time passing """
        print(f"Time={self.time}")
        odds = 10 - len(self.customers)
        if self.flags['new_customers'] and random.randrange(1, 500) < odds:
            self.new_customer()
        for cust in self.customers:
            rc = cust.turn(self.time)
            if not rc:
                print(f"Customer {cust} has left the pub")
                self.old_customers.append(cust)
                self.map.del_people(cust.pos)
                self.customers.remove(cust)
        if not self.customers:
            self.flags['terminate'] = True
        for supply in self.supplies:
            supply.turn(self.time)
        for stff in self.staff:
            stff.turn(self.time)
        self.time += 1
        self.validate()

    ##########################################################################
    def active_supplies(self):
        """ List of supplies that still have contents """
        return [_ for _ in self.supplies if not _.is_empty()]

    ##########################################################################
    def validate(self):
        """ Ensure data integrity """
        for cust in self.customers:
            if self.map.data['PEOPLE'].get(cust.pos) != cust:
                for pos in self.map.data['PEOPLE']:
                    print(f"{pos=} {self.map.data['PEOPLE'][pos]}")
                raise AssertionError(f"{cust=} not in place")

        for staff in self.staff:
            if self.map.data['PEOPLE'].get(staff.pos) != staff:
                for pos in self.map.data['PEOPLE']:
                    print(f"{pos=} {self.map.data['PEOPLE'][pos]}")
                raise AssertionError(f"{staff=} not in place")

        for chair in self.chairs:
            if self.map.data['FURNITURE'].get(chair.pos) != chair:
                for pos in self.map.data['FURNITURE']:
                    print(f"{pos=} {self.map.data['FURNITURE'][pos]}")
                raise AssertionError(f"{chair=} not in place")

        for table in self.tables:
            if self.map.data['FURNITURE'].get(table.pos) != table:
                for pos in self.map.data['FURNITURE']:
                    print(f"{pos=} {self.map.data['FURNITURE'][pos]}")
                raise AssertionError(f"{table=} not in place")

    ##########################################################################
    def find_empty_chair(self):
        """ Find a chair that is currently empty """
        chairs = [_ for _ in self.chairs if not _.occupant]
        if chairs:
            return random.choice(chairs)
        return None

    ##########################################################################
    def move(self, obj, newloc):
        """ Move an object to a new location """
        self.map.del_people(obj.pos)
        self.map.add_people(newloc, obj)

    ##########################################################################
    def find_route(self, src, dest, adjacent=False):
        """ Find a route between two points (or adjacent to dest) """
        return self.map.find_route(src, dest, adjacent)

    ##########################################################################
    def mainloop(self):
        """ Run forever """
        while not self.flags['terminate']:
            try:
                self.turn()
                print(self.draw())
            except KeyboardInterrupt:
                self.stats_dump()
                return
        self.stats_dump()

    ##########################################################################
    def stats_dump(self):
        """ Dump statistics """
        waits = []
        if self.old_customers:
            print("\nOld Customers:")
            for cust in self.old_customers:
                waits.extend(cust.stats.get('_waits', []))
                cust.stats_dump()

        if self.customers:
            print("\nExisting Customers:")
            for cust in self.customers:
                waits.extend(cust.stats.get('_waits', []))
                cust.stats_dump()

        if waits:
            print("\nStat summary:")
            print(f"Min: {min(waits)}")
            print(f"Avg: {statistics.mean(waits)}")
            print(f"Max: {max(waits)}")

    ##########################################################################
    def draw(self):
        """ Return a string representation of the pub """
        result = ''
        for y in range(self.size_y):
            for x in range(self.size_x):
                pos = Coord(x, y)
                result += self.map.repr(pos)
            if y < len(self.customers):
                cust = self.customers[y]
                result += f"  {cust.desc_line()}"

            index = y - len(self.customers)
            if index >= 0 and index < len(self.staff):
                stf = self.staff[index]
                result += f"  {stf.desc_line()}"

            index = y - len(self.customers) - len(self.staff)
            if index >= 0 and index < len(self.supplies):
                supl = self.supplies[index]
                result += f"  {supl.desc_line()}"

            result += '\n'
        return result


##############################################################################
if __name__ == "__main__":
    tavern = Pub()
    tavern.populate()
    tavern.mainloop()

# EOF
