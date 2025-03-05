# precalibated classes snippet 

from product_types import *

# fuels 

class OilSands(Fuel):
    def __init__(self, name = "Canadian Oil Sands", carbon_frac = 0.85, processing = 0.312):
        self = Fuel.__init__(self, name, carbon_frac, processing)
