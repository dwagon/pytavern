""" Customer """
import random
import statistics

import colorama

import person


##############################################################################
class Customer(person.Person):
    """ Customer - resource consumer """
    def __init__(self, pub, name, pos):
        super().__init__(pub, name, pos)
        self.demands = {'time': 0, 'amount': 0, 'kind': None}
        self.thirst = random.randint(1, 9)
        self.target = None
        self.target_chair = None
        self.chair = None
        self.mode = person.CUST_WAIT_FOR_CHAIR
        self.stats = {
            'enter_tick': self.pub.time
            }

    ##########################################################################
    def repr(self):
        """ Mutable representation """
        if self.mode == person.CUST_GO_HOME:
            fore = f'{colorama.Fore.RED}'
        elif self.mode == person.CUST_WAIT_TO_ORDER:
            fore = f'{colorama.Fore.GREEN}'
        elif self.mode == person.CUST_WAIT_TO_DRINK:
            fore = f'{colorama.Fore.YELLOW}'
        else:
            fore = f'{colorama.Fore.WHITE}'
        return f'{fore}C'

    ##########################################################################
    def desc_line(self):
        """ Return a description of what customer is doing """
        out = f"{self.name}@{self.pos}"
        if self.mode == person.CUST_GO_CHAIR:
            out += f" Going to chair {self.target_chair}"
        elif self.mode == person.CUST_WAIT_TO_ORDER:
            out += f" Waiting to order {self.demands['kind']}"
        elif self.mode == person.CUST_WAIT_TO_DRINK:
            out += f" Waiting for order of {self.demands['kind']}"
        elif self.mode == person.CUST_DRINK:
            out += f" Drinking {self.demands['kind']} for {self.demands['time_to_drink']}"
        elif self.mode == person.CUST_GO_HOME:
            out += " Going home"
        elif self.mode == person.CUST_WAIT_FOR_CHAIR:
            out += " Waiting for a chair"
        if self.target:
            out += f" -> {self.target}"
        if self.thirst:
            out += f" Thirst: {self.thirst}"
        return out

    ##########################################################################
    def order(self):
        """ Deliver order to staff """
        if self.mode != person.CUST_WAIT_TO_ORDER:
            return {}
        self.mode = person.CUST_WAIT_TO_DRINK
        if not self.pub.active_supplies(self.demands['kind']):
            print(f"{self} Pub is out of {self.demands['kind']}")
            self.mode = person.CUST_GO_HOME
            return {}
        return self.demands

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
        print(f"  {self}")
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
    def wait_to_drink(self):
        """ Wait for staff to deliver order """
        if not self.pub.active_supplies():
            self.mode = person.CUST_GO_HOME
        return True

    ##########################################################################
    def wait_to_order(self, tick):
        """ Wait for staff to come and request order """
        if not self.thirst:
            self.mode = person.CUST_GO_HOME
            return True
        if not self.pub.active_supplies():
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
        drnk = 1
        waits = []
        while f"time_to_drink_order_{drnk}" in self.stats:
            waits.append(self.stats[f"time_to_drink_order_{drnk}"])
            drnk += 1
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
        if self.demands['time_to_drink']:
            self.demands['time_to_drink'] -= 1
            return True
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
        assert self.blocked < 8
        res = True
        if self.mode == person.CUST_GO_CHAIR:
            res = self.go_to_chair()
        elif self.mode == person.CUST_WAIT_TO_ORDER:
            res = self.wait_to_order(tick)
        elif self.mode == person.CUST_WAIT_TO_DRINK:
            res = self.wait_to_drink()
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
            self.demands['kind'] = random.choice(self.pub.supply_types)
            self.demands['time_to_drink'] = self.demands['amount'] * random.randint(1, 20)

    ##########################################################################
    def receive(self, hasamt):
        """ Receive supplies from a server """
        self.mode = person.CUST_DRINK
        grab = min(hasamt, self.demands['amount'])
        self.demands['amount'] -= grab
        return grab

# EOF
