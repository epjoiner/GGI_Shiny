# precalibated classes snippet 

from product_types import *

# fuels 

class OilSands(Fuel):
    def __init__(self, name = "Canadian Oil Sands", carbon_frac = 0.85, processing = 0.312):
        self = Fuel.__init__(self, name, carbon_frac, processing)
 
 # feedstocks as inputs for BOF steel 
        
class Iron(Fuel): 
    def __init__(self, name = "Iron Ore", carbon_frac = 0, processing = .168):
        self = Fuel.__init__(self,name, carbon_frac, processing)
        
class Coal(Fuel): 
    def __init__(self, name = "Coal", carbon_frac = 0.93/1.5, processing = 0.034):
        self = Fuel.__init__(self,name, carbon_frac, processing)     
 
class Coke(Product): 
    def __init__(self, Coal: Fuel, name = "Coke", processing = 0.496):
        super().__init__(name, processing)
        self.add_feedstock(Coal, unit_ratio = 1.5)
        
class Oxygen(Fuel): 
    def __init__(self, name = "Oxygen", carbon_frac = 0, processing = 0.525):
        self = Fuel.__init__(self, name, carbon_frac, processing)

class Limestone(Fuel):
    def __init__(self, name = "Limestone", carbon_frac = 0, processing = 0.44):
        self = Fuel.__init__(self, name, carbon_frac, processing)
        
# BOF Steel product 
    
class BOFSteel(Product): 
    def __init__(self, Iron: Fuel, Coke: Product, Oxygen: Fuel, Limestone: Fuel, name = "BOF Steel", processing = 0): 
        super().__init__(name, processing)
        self.add_feedstock(Iron, unit_ratio = 1.6)
        self.add_feedstock(Coke, unit_ratio = 0.65)
        self.add_feedstock(Oxygen, unit_ratio = 0.154)
        self.add_feedstock(Limestone, unit_ratio = 0.25)
        
        
coke = Coke(Coal())
bof_steel = BOFSteel(Iron(), coke, Oxygen(), Limestone(), processing = 0)
print(bof_steel.ggi_co2e())