# precalibated classes snippet 

from product_types import *
from copy import deepcopy

# fuels 

oil_sands = Fuel(name = "Canadian Oil Sands", carbon_frac = 0.85, 
                 processing = 0.312)

print(oil_sands)
print("GHG intensity (CO2e):", round(oil_sands.ggi_co2e(), 2))