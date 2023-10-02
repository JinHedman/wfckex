from random import *
import numpy as np
class Cell:
    def __init__(self, value = [], context = 0):
        self.value = value
        self.context = context

    def __str__(self):
        return str(self.value)

    def size(self):
        return len(self.value)

    def randomchoice(self):
        return random.choice(self.value)

    def bool(self):
        lb = np.array([False] * self.context)
        for i in self.value: lb[i] = True
        return lb

    def collapse(self, probability_list):
        item_prob_list = []
        for item in self.value:
            item_prob_list.append(probability_list[item])

        # chooses depending on weight
        rand = choices(self.value, item_prob_list, k = 1)
        self.value = [rand[0]]

    def add_base_values(self, n):
        self.value = list(range(n))