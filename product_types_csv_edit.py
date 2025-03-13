from treelib import Tree
import pandas as pd

class Fuel:
    def __init__(self, name: str, carbon_frac: float, processing: float):
        self.name = name
        self.carbon_frac = carbon_frac
        self.processing = processing
        self.leak_co2e = 0
    
    def set_leakage(self, leak_rate: float, gwp : float):
        self.leak_co2e =  leak_rate * gwp
    
    def ggi_co2e(self):
        ggi = 44/12 * self.carbon_frac + self.processing + self.leak_co2e
        return ggi
    
    def __repr__(self):
        return f"Fuel('{self.name}')"

    def __str__(self):
        return f"'{self.name}' fuel, carbon fraction = {self.carbon_frac}, processing emissions = {self.processing}, leakage = {self.leak_co2e != 0}"

class Product:
    def __init__(self, name: str, processing: float):
        self.name = name
        self.processing = processing
        self.feedstocks = []

    def add_feedstock(self, source, unit_ratio: float):
        self.feedstocks.append({"source":source, "ratio":unit_ratio})

    def ggi_co2e(self):
        ggi = self.processing
        for feedstock in self.feedstocks:
            partial_ggi = feedstock["source"].ggi_co2e() * feedstock["ratio"]
            ggi += partial_ggi
        return ggi
    
    class IDGenerator:
        def __init__(self):
            self.counter = 0
        
        def generate(self):
            self.counter += 1
            return f"node_{self.counter}"

    def catalog(self, idgen = IDGenerator()):
    
        tree = Tree()
        node_id = idgen.generate()
    
        tree.create_node(f"{self}", identifier = node_id)
    
        for i in range(len(self.feedstocks)):
    
            child = self.feedstocks[i]
    
            if type(child['source']) is Fuel:
                tree.create_node(
                    f"{child['source']}, ratio = {child['ratio']}",
                    identifier = idgen.generate(),
                    parent = node_id
                )
    
            if type(child['source']) is Product:
                tree.paste(node_id, child['source'].catalog(idgen = idgen))
    
        return tree

    def __repr__(self):
        return f"Product('{self.name}')"

    def __str__(self):
        return f"'{self.name}' product, {len(self.feedstocks)} input(s), processing emissions = {self.processing}"


class ModFuel:
    def __init__(self, name: str, carbon_frac: float, processing: float):
        self.name = name
        self.carbon_frac = carbon_frac
        self.processing = processing
        self.leak_co2e = 0
    
    def set_leakage(self, leak_rate: float, gwp : float):
        self.leak_co2e =  leak_rate * gwp
    
    def ggi_co2e(self):
        ggi = 44/12 * self.carbon_frac + self.processing + self.leak_co2e
        return ggi
    
    def __repr__(self):
        return f"Fuel('{self.name}')"

    def __str__(self):
        return f"'{self.name}' fuel, carbon fraction = {self.carbon_frac}, processing emissions = {self.processing}, leakage = {self.leak_co2e != 0}"


class ModProduct:
    def __init__(self, name: str, processing: float):
        self.name = name
        self.processing = processing
        self.feedstocks = []

    def add_feedstock(self, source, carbon_frac: float, unit_ratio: float):
        self.feedstocks.append({"source":source, "carbon_frac": carbon_frac, "ratio":unit_ratio})

    def ggi_co2e(self):
        ggi = self.processing
        for feedstock in self.feedstocks:
            partial_ggi = feedstock["source"].ggi_co2e() * feedstock["ratio"]
            ggi += partial_ggi
        return ggi
    
    # modifying for user input requires accomodating a carbon fraction again here 
            
    def mod_ggi_co2e(self):
        ggi =  self.processing 
        print(f"Base GGI for {self.name}: {ggi}")  # Debug: Print base GGI

        for feedstock in self.feedstocks:
            
            feedstock_ggi = feedstock["source"].mod_ggi_co2e()
            ratio = feedstock["ratio"]
            carbon_frac = feedstock["carbon_frac"]

            print(f"Feedstock: {feedstock['source'].name}, GGI: {feedstock_ggi}, Processing: {self.processing}, Ratio: {ratio}, Carbon Fraction: {carbon_frac}")  # D
            
            if carbon_frac is not None and not pd.isna(carbon_frac):
                carb_ggi =  44/12 * feedstock["carbon_frac"] 
                
                print(f"Carb GGI for {feedstock['source'].name}: {carb_ggi}")  
                ggi += carb_ggi 
                
            partial_ggi = feedstock_ggi * ratio
            
            print(f"Partial GGI for {feedstock['source'].name}: {partial_ggi}")  
            
            ggi += partial_ggi
                      
        print(f"Total GGI for {self.name}: {ggi}")  
        return ggi
    
    # import product processing, feedstock, unit ratio data from df using pandas 
    
    @classmethod
    def from_dataframe(cls, df: pd.DataFrame):
         
         # requires csv to repeat final product inputs for feedstock columns 
         
         inputs = {} 
         
         for _, row in df.iterrows():
            product_name = row["product"]
            processing = row["processing"]

                # fuels / combined product
            if product_name not in inputs:
                inputs[product_name] = cls(product_name, processing)

                # feedstocks
            if pd.notna(row["feedstock"]) and pd.notna(row["ratio"]):
                feedstock_name = row["feedstock"]
                carbon_frac = row.get("carbon_frac")
                ratio = row["ratio"]
                
                if feedstock_name not in inputs:
                    inputs[feedstock_name] = cls(feedstock_name, 0.0)  

                inputs[product_name].add_feedstock(inputs[feedstock_name], carbon_frac, ratio)

         return inputs
     
    # catalog remains unchanged 
    
    class IDGenerator:
        def __init__(self):
            self.counter = 0
        
        def generate(self):
            self.counter += 1
            return f"node_{self.counter}"

    def catalog(self, idgen = IDGenerator()):
    
        tree = Tree()
        node_id = idgen.generate()
    
        tree.create_node(f"{self}", identifier = node_id)
    
        for i in range(len(self.feedstocks)):
    
            child = self.feedstocks[i]
    
            if type(child['source']) is ModFuel:
                tree.create_node(
                    f"{child['source']}, ratio = {child['ratio']}",
                    identifier = idgen.generate(),
                    parent = node_id
                )
    
            if type(child['source']) is ModProduct:
                tree.paste(node_id, child['source'].catalog(idgen = idgen))
    
        return tree

    def __repr__(self):
        return f"Product('{self.name}')"

    def __str__(self):
        return f"'{self.name}' product, {len(self.feedstocks)} input(s), processing emissions = {self.processing}"
