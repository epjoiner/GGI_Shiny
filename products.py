
class Crude:
    def __init__(self, name: str, carbon_frac: float, processing: float):
        self.name = name
        self.carbon_frac = carbon_frac
        self.processing = processing
    
    def ggi(self):
        ggi = 44/12*self.carbon_frac + self.processing
        return ggi
    
    def __repr__(self):
        return f"Crude('{self.name}')"

    def __str__(self):
        return f"'{self.name}' crude product, carbon fraction = {self.carbon_frac}, processing emissions = {self.processing}"

class Derivative:
    def __init__(self, name: str, processing: float):
        self.name = name
        self.processing = processing
        self.feedstocks = []

    def add_feedstock(self, source: Crude, unit_ratio: float):
        self.feedstocks.append({"source":source, "ratio":unit_ratio})

    def ggi(self):
        ggi = self.processing
        for feedstock in self.feedstocks:
            partial_ggi = feedstock["source"].ggi()*feedstock["ratio"]
            ggi += partial_ggi
        return ggi

    def __repr__(self):
        return f"Derivative('{self.name}')"

    def __str__(self):
        return f"'{self.name}' derivative product, processing emissions = {self.processing}"
