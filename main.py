import copy
import random
from random import *

from Part import *
from DrawFast import *
from Input import *
from WFC import *
from GUI import *
from Draw import *
from Cell import *

import numpy as np

tkinter_inputsize = [3,3]

def main():
    gui = GUI(run_test_wfc)
    gui.run()

def run_test_wfc():
    tiles = get_tiles()
    create_rules(tiles)
    field = get_field((10, 10), tiles)
    main_draw = DrawFast(convert_to_array_advance(field, tiles))
    main_draw.update(convert_to_array_advance(field,tiles))
    wfc = WFC(field, tiles, main_draw)


if __name__ == '__main__':
    main()
