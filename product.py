
class Product:
    def __init__(self, name: str, carbon_frac: float, processing: float):
        self.name = name
        self.carbon_frac = carbon_frac
        self.processing = processing
    
    def ggi(self):
        ggi = 44/12*self.carbon_frac + self.processing
        return ggi
