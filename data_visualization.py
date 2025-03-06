import matplotlib.pyplot as plt
import numpy as np
from product_types import *

def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i, y[i] + .1, y[i], ha = 'center')

class Plot:
    def __init__(self, *args: Fuel):
        self.fuels = list(args)

    def add_column(self, fuel: Fuel):
        self.fuels.append(fuel)
    
    def column_plot(self, title: chr = None):
        self.names = []
        self.cols = []
        
        for fuel in self.fuels:
            self.names.append(fuel.name)
            self.cols.append([fuel.carbon_frac*44/12, fuel.processing, fuel.leak_co2e])
        self.cols = np.array(self.cols)
        self.heights = np.sum(self.cols, axis = 1).tolist()

        plt.bar(self.names, self.cols[:,0], label = "Carbon Content")
        plt.bar(self.names, self.cols[:,1], bottom = self.cols[:,0], label = "Processing")
        plt.bar(self.names, self.cols[:,2], bottom = self.cols[:,0] + self.cols[:,1], label = "Leakage")
        addlabels(self.names, [round(x,2) for x in self.heights])
        plt.ylabel('GHG Intensity (tCO2e)')
        plt.title(title)
        plt.margins(y = .5)
        handles, labels = plt.gca().get_legend_handles_labels()
        plt.legend(handles[::-1], labels[::-1])
        plt.show()
