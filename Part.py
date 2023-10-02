import numpy as np

class Part:
    def __init__(self, input, ID):
        self.ID = ID
        self.grid = input
        self.adjecency = {}
        
        self.adjecency["right"]= []
        self.adjecency["left"]= []
        self.adjecency["top"]= []
        self.adjecency["bottom"]= []

        self.left = self.adjecency["left"]
        self.right = self.adjecency["right"]
        self.top = self.adjecency["top"]
        self.bottom = self.adjecency["bottom"]