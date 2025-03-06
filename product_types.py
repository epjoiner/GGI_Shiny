from treelib import Tree

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
