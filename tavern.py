#!/usr/bin/env python3
""" Top level for tavern """
from tavern.tavern import Tavern

tavern = Tavern(num_stools=1, num_supplies=1, size_x=10, size_y=10, max_customers=1)
tavern.populate()
tavern.mainloop()
