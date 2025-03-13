# precalibated classes snippet 

from product_types import *

# fuels 

# Oil 

class OilSands(Fuel):
    def __init__(self, name = "Canadian Oil Sands", carbon_frac = 0.85, processing: float = 0.312):
        self = Fuel.__init__(self, name, carbon_frac, processing)

class ConventionalCrude(Fuel): 
    def __init__(self, name = "Conventional Crude Oil", carbon_frac = 0.85, processing: float = 0.126):
        self = Fuel.__init__(self, name, carbon_frac, processing)
        
# Coal 
  
class Bituminous(Fuel):
    def __init__(self, name = "Bituminous Coal", carbon_frac = 0.7, processing: float = 0.117):
        self = Fuel.__init__(self, name, carbon_frac, processing)
        
class SubBituminous(Fuel):
    def __init__(self, name = "Sub-Bituminous Coal", carbon_frac = 0.5, processing: float = 0.02):
        self = Fuel.__init__(self, name, carbon_frac, processing)
 
class Lignite(Fuel):
    def __init__(self, name = "Lignite", carbon_frac = 0.41, processing: float = 0.02):
        self = Fuel.__init__(self, name, carbon_frac, processing)
        
class Anthracite(Fuel):
    def __init__(self, name = "Anthracite", carbon_frac = 0.78, processing: float = 0.117):
        self = Fuel.__init__(self, name, carbon_frac, processing)
 
 # Natural Gas
 
class NaturalGas(Fuel): 
    def __init__(self, name = "Natural Gas", carbon_frac = 0.763, processing: float = 0.258):
         self = Fuel.__init__(self, name, carbon_frac, processing)
         
class LNG(Product):
    def __init__(self, NaturalGas: Fuel, name = "LNG", processing: float = 0):
         super().__init__(name, processing)
         self.add_feedstock(NaturalGas, unit_ratio = 1/.9)
         
#lng = LNG(NaturalGas())
#print("GHG intensity (CO2e) of", lng.name, ":", round(lng.ggi_co2e(), 2))

 
 # feedstocks as inputs for BOF steel 
        
class Iron(Fuel): 
    def __init__(self, name = "Iron Ore", carbon_frac = 0, processing: float = .168):
        self = Fuel.__init__(self,name, carbon_frac, processing)
        
class Coal(Fuel): 
    def __init__(self, name = "Coal", carbon_frac = 0.93/1.5, processing: float = 0.034):
        self = Fuel.__init__(self,name, carbon_frac, processing)     
 
class Coke(Product): 
    def __init__(self, Coal: Fuel, name = "Coke", processing: float = 0.496):
        super().__init__(name, processing)
        self.add_feedstock(Coal, unit_ratio = 1.5)
        
class Oxygen(Fuel): 
    def __init__(self, name = "Oxygen", carbon_frac = 0, processing: float = 0.525):
        self = Fuel.__init__(self, name, carbon_frac, processing)

class Limestone(Fuel):
    def __init__(self, name = "Limestone", carbon_frac = 0, processing: float = 0.44):
        self = Fuel.__init__(self, name, carbon_frac, processing)
        
# BOF Steel product 
    
class BOFSteel(Product): 
    def __init__(self, Iron: Fuel, Coke: Product, Oxygen: Fuel, Limestone: Fuel, name = "BOF Steel", 
                 processing: float = 0): 
        super().__init__(name, processing)
        self.add_feedstock(Iron, unit_ratio = 1.6)
        self.add_feedstock(Coke, unit_ratio = 0.65)
        self.add_feedstock(Oxygen, unit_ratio = 0.154)
        self.add_feedstock(Limestone, unit_ratio = 0.25)
        
        
#coke = Coke(Coal())
#bof_steel = BOFSteel(Iron(), coke, Oxygen(), Limestone(), processing = 0)
#print("GHG intensity (CO2e) of", bof_steel.name, ":", bof_steel.ggi_co2e())