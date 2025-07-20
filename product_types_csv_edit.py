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
    
    @classmethod
    def from_dataframe_row(cls, row):
        fuel = cls(
            name=row['name'],
            carbon_frac=row['carbon_frac'],
            processing=row['processing']
        )
        if 'leak_rate' in row and 'gwp' in row:
            fuel.set_leakage(row['leak_rate'], row['gwp'])
        return fuel
    
    def __repr__(self):
        return f"Fuel('{self.name}')"

    def __str__(self):
        return f"'{self.name}' fuel, carbon fraction = {self.carbon_frac}, processing emissions = {self.processing}, leakage = {self.leak_co2e != 0}"



class ModProduct:
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
    
    # import product processing, feedstock, unit ratio data from df using pandas 
    @classmethod
    def from_dataframe_row(cls, row, fuel_dict, product_dict=None):
        product = cls(name=row['name'], processing=row['processing'])
    
        feedstocks = row['feedstocks']
        if not isinstance(feedstocks, list):
            raise ValueError(f"need tuples: {feedstocks}")
    
        for fs in feedstocks:
            if isinstance(fs, tuple) and len(fs) == 2:
                source_name, ratio = fs
            else:
                raise ValueError(f"wrong feedstock format: {fs}")
        
            if source_name in fuel_dict:
                source = fuel_dict[source_name]
            elif product_dict and source_name in product_dict:
                source = product_dict[source_name]
            else:
                raise ValueError(f"no feedstock source: {source_name}")
        
            product.add_feedstock(source, ratio)
            
        return product

    # @classmethod
    # def from_dataframe_row(cls, row, fuel_dict, product_dict=None):
    #     product = cls(name=row['name'], processing=row['processing'])
    #     feedstocks = row['feedstocks']  
    #     for source_name, unit_ratio in feedstocks:
    #         if source_name in fuel_dict:
    #             source = fuel_dict[source_name]
    #         elif product_dict and source_name in product_dict:
    #             source = product_dict[source_name]
    #         product.add_feedstock(source, unit_ratio)
    #     return product

     
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
                    f"{child['source']}, unit_ratio = {child['ratio']}",
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

def build_products_from_df(df):
    fuel_dict = {}
    product_dict = {}
    
    # Step 1: Create all fuels
    for _, row in df[df['feedstock_type'] == 'Fuel'].iterrows():
        name = row['feedstock_name']
        if name not in fuel_dict:
            fuel_dict[name] = ModFuel(name, row['carbon_frac'], processing=0.0)

    # Step 2: Create all products
    for product_name in df['product_name'].unique():
        product_rows = df[df['product_name'] == product_name]
        processing = product_rows.iloc[0]['processing']
        product = ModProduct(product_name, processing)
        product_dict[product_name] = product

    # Step 3: Add feedstocks to each product
    for product_name, product in product_dict.items():
        product_rows = df[df['product_name'] == product_name]
        for _, row in product_rows.iterrows():
            feedstock_name = row['feedstock_name']
            unit_ratio = row['unit_ratio']
            feedstock_type = row['feedstock_type']

            if feedstock_type == 'Fuel':
                source = fuel_dict[feedstock_name]
            elif feedstock_type == 'Product':
                source = product_dict[feedstock_name]
            else:
                raise ValueError(f"Unknown feedstock type: {feedstock_type}")

            product.add_feedstock(source, unit_ratio)

    return product_dict