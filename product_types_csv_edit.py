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

def build_products_from_df(df, fuel_processing_default=0.0):
    
    #GTP iterated function 
    """
    builds ModFuel and ModProduct instances from a single long-format DataFrame.

    arguments from df - 
        df (pd.DataFrame): A dataframe with columns:
            - parent product_name
            - id
            - processing
            - feedstock_name
            - feedstock_type ('Fuel' or 'Product')
            - carbon_frac
            - unit_ratio
        fuel_processing_default (float): Default processing value for fuels (if not provided).

    Returns:
        dict: A dictionary of all products keyed by name.
    """
    fuel_dict = {}
    product_dict = {}
    source_dict = {}

    # Step 1: Build unique fuels
    fuel_rows = df[df["feedstock_type"] == "Fuel"]
    unique_fuels = fuel_rows[["feedstock_name", "carbon_frac"]].drop_duplicates()

    for _, row in unique_fuels.iterrows():
        name = row["feedstock_name"]
        carbon_frac = row["carbon_frac"]
        fuel_dict[name] = ModFuel(name, carbon_frac, fuel_processing_default)
    
    source_dict.update(fuel_dict)  # Initial lookup table

    # Step 2: Build products
    for product_name, group in df.groupby("product_name"):
        processing = group["processing"].iloc[0]
        product = ModProduct(product_name, processing)

        for _, row in group.iterrows():
            source_name = row["feedstock_name"]
            source_type = row["feedstock_type"]
            carbon_frac = row["carbon_frac"]
            unit_ratio = row["unit_ratio"]

            if source_type == "Fuel":
                source = fuel_dict.get(source_name)
            elif source_type == "Product":
                source = product_dict.get(source_name)
                if source is None:
                    raise ValueError(f"Product dependency '{source_name}' not yet created. "
                                     "Ensure input data is in dependency order.")
            else:
                raise ValueError(f"Unknown feedstock_type: {source_type}")

            product.add_feedstock(source, carbon_frac, unit_ratio)

        product_dict[product_name] = product
        source_dict[product_name] = product

    return product_dict