""" Customer """
import random
import statistics

import person


##############################################################################
class Customer(person.Person):
    """ Customer - resource consumer """
    def __init__(self, pub, name, pos):
        super().__init__(pub, name, pos)
        self.demands = {'time': 0, 'amount': 0}
        self.thirst = random.randint(1, 9)
        self.target = None
        self.target_chair = None
        self.chair = None
        self.repr = 'C'
        self.mode = person.CUST_WAIT_FOR_CHAIR
        self.stats = {
            'enter_tick': self.pub.time
            }

    ##########################################################################
    def order(self):
        """ Deliver order to staff """
        self.mode = person.CUST_WAIT_TO_DRINK
        return self.demands['amount']

    ##########################################################################
    def go_to_chair(self):
        """ Find a chair to sit down at """
        if self.blocked > 5:
            self.mode = person.CUST_WAIT_FOR_CHAIR
            self.blocked = 0
            return True
        if not self.move():
            self.mode = person.CUST_WAIT_TO_ORDER
            self.chair = self.target_chair
            self.pos = self.target_chair.pos
            self.chair.sit_down(self)
            print(f"{self} sat down in {self.chair}")
            self.stats['find_seat_tick'] = self.pub.time
            self.stats['time_to_find_seat'] = \
                self.stats['find_seat_tick'] - self.stats['enter_tick']
            self.target = None
        return True

    ##########################################################################
    def stats_dump(self):
        """ Dump out stats """
        print(f"{self}")
        for k, v in self.stats.items():
            if not k.startswith('_'):
                print(f"    {k} {v}")

    ##########################################################################
    def wait_for_chair(self):
        """ Move somewhere and wait for a chair to be free """
        self.target_chair = self.pub.find_empty_chair()
        if self.target_chair is None or self.blocked > 5:
            self.blocked = 0
            if self.target is None:
                self.target = self.pub.map.free_people_loc()
                print(f"{self} Moving to {self.target} waiting for chair")
            self.move()
        else:
            self.target = self.target_chair.pos
            self.mode = person.CUST_GO_CHAIR
        return True

    ##########################################################################
    def wait_to_order(self, tick):
        """ Wait for staff to come and request order """
        if not self.thirst:
            self.mode = person.CUST_GO_HOME
            return True
        stat = f"wait_order_{self.thirst}_tick"
        if stat not in self.stats:
            self.stats[stat] = tick
        self.generate_demand(tick)
        return True

    ##########################################################################
    def generate_stats(self):
        """ Generate useful stats """
        drink = 1
        waits = []
        while f"time_to_drink_order_{drink}" in self.stats:
            waits.append(self.stats[f"time_to_drink_order_{drink}"])
            drink += 1
        self.stats = {
            'time_to_find_seat': self.stats['time_to_find_seat'],
            }
        if waits:
            self.stats['min_order_time'] = min(waits)
            self.stats['max_order_time'] = max(waits)
            self.stats['avg_order_time'] = statistics.mean(waits)
            self.stats['_waits'] = waits

    ##########################################################################
    def drink(self, tick):
        """ Consume """
        if self.thirst:
            wait_stat = f"wait_order_{self.thirst}_tick"
            drink_stat = f"drink_order_{self.thirst}_tick"
            self.stats[drink_stat] = tick
            time_stat = f"time_to_drink_order_{self.thirst}"
            try:
                self.stats[time_stat] = self.stats[drink_stat] - self.stats[wait_stat]
            except KeyError:
                print(f"{self} Failed to have good stats: {self.stats}")
            self.thirst -= 1
            self.mode = person.CUST_WAIT_TO_ORDER
        else:
            self.mode = person.CUST_GO_HOME
        return True

    ##########################################################################
    def go_home(self, tick):
        """ You don't need to go home but you can't stay here """
        self.target = self.pub.door
        if self.chair:
            print(f"{self} got up from {self.chair}")
            self.chair.get_up()
            self.chair = None
        if self.pos == self.pub.door.pos:
            self.stats['left_tick'] = tick
            self.stats['time_at_pub'] = self.stats['left_tick'] - self.stats['enter_tick']
            self.generate_stats()
            self.stats_dump()
            return False
        if self.blocked > 5:
            self.target = self.pub.map.free_people_loc()
        self.move()
        return True

    ##########################################################################
    def turn(self, tick):
        """ Time passing """
        if self.blocked > 7:
            print(f"{1/0}")
        res = True
        if self.mode == person.CUST_GO_CHAIR:
            res = self.go_to_chair()
        elif self.mode == person.CUST_WAIT_TO_ORDER:
            res = self.wait_to_order(tick)
        elif self.mode == person.CUST_WAIT_TO_DRINK:
            pass
        elif self.mode == person.CUST_DRINK:
            res = self.drink(tick)
        elif self.mode == person.CUST_GO_HOME:
            res = self.go_home(tick)
        elif self.mode == person.CUST_WAIT_FOR_CHAIR:
            res = self.wait_for_chair()
        return res

    ##########################################################################
    def generate_demand(self, tick):
        """ So thirsty ... """
        if not self.demands.get('amount', 0) and self.thirst:
            self.demands = {'time': tick, 'amount': random.randint(1, 3)}

    ##########################################################################
    def receive(self, hasamt):
        """ Receive supplies from a server """
        self.mode = person.CUST_DRINK
        grab = min(hasamt, self.demands['amount'])
        self.demands['amount'] -= grab
        return grab

# EOF
