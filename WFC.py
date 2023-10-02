import numpy as np
import copy

from Cell import *
from Part import *

def WFC(field, tiles, draw):
    field_copy = copy.deepcopy(field)
    while True:
        field_copy = copy.deepcopy(field)
        while not check(field_copy):
            field_copy = collapse(field_copy)
            draw.update(convert_to_array_advance(field_copy, tiles))
            field_copy = propagate(field_copy, tiles)
            if (field_copy == np.array([0])).all():
                print("restart")
                break
        else:
            draw.wait()
    return field_copy


def collapse(field):
    min = get_min(field)
    field[min[0]][min[1]].collapse()
    return field


def propagate(grid, tiles):
    nx = grid.shape[0]
    ny = grid.shape[1]

    C = True

    # while something changes
    while C == True:
        C = False
        for y in range(ny):
            for x in range(nx):

                if grid[x][y].size() == 1:
                    continue

                current = grid[x][y].bool()
                allowed_l = [get_bool([],tiles), get_bool([],tiles), get_bool([],tiles), get_bool([],tiles)]
                allowed = [True] * len(tiles)

                if x - 1 >= 0:
                    for i in grid[x - 1, y].value:
                        allowed_l[0] = conc_or(get_bool(tiles[i].right,tiles), allowed_l[0])
                else:
                    allowed_l[0] = [True] * len(tiles)

                if x + 1 < nx:
                    for i in grid[x + 1,y].value:
                        allowed_l[1] = conc_or(get_bool(tiles[i].left,tiles), allowed_l[1])
                else:
                    allowed_l[1] = [True] * len(tiles)

                if y - 1 >= 0:
                    for i in grid[x, y-1].value:
                        allowed_l[2] = conc_or(get_bool(tiles[i].bottom,tiles), allowed_l[2])
                else:
                    allowed_l[2] = [True] * len(tiles)

                if y + 1 < ny:
                    for i in grid[x, y + 1].value:
                        allowed_l[3] = conc_or(get_bool(tiles[i].top,tiles), allowed_l[3])
                else:
                    allowed_l[3] = [True] * len(tiles)

                for i in range(4):
                    allowed = conc_and(allowed_l[i], allowed)

                if not (current == allowed).all():
                    C = True

                grid[x, y] = get_list(conc_and(current, allowed))

                if grid[x,y].size() == 0:
                    return np.array([0])

    return grid

def check(field):
    for row in field:
        for cell in row:
            if len(cell.value) > 1:
                return False
    return True

def conc_or(l1, l2):
  return [a or b for a, b in zip(l1, l2)]

def conc_and(l1, l2):
  return [a and b for a, b in zip(l1, l2)]

def get_bool(lst, tiles):
  lb = np.array( [False] * len(tiles))
  for i in lst: lb[i] = True
  return lb

def get_list(bool_list):
  lst = []
  for i, el in enumerate(bool_list):
    if el:
      lst.append(i)
  a = Cell([], len(bool_list))
  a.value = lst
  return a

def get_min(arr):
    min = 100
    min_list = []
    for x, el_out in enumerate(arr):
        for y, el in enumerate(el_out):
            if el.size() < min and el.size() != 1:
                min = el.size()
                min_list = [(x, y)]
            elif el.size() == min and el.size() != 1:
                min_list.append((x, y))
    if len(min_list) > 1:
        return choice(min_list)
    return min_list[0]

def create_rules(p):
    for el in p:
        cur = el.grid.T[0, :]
        for el2 in p:
            if (cur == el2.grid.T[el2.grid.T.shape[1] - 1, :]).all():
                el.top.append(el2.ID)

        cur = el.grid.T[el.grid.T.shape[1] - 1, :]
        for el2 in p:
            if (cur == el2.grid.T[0, :]).all():
                el.bottom.append(el2.ID)

        cur = el.grid.T[:, 0]
        for el2 in p:
            if (cur == el2.grid.T[:, el2.grid.T.shape[0] - 1]).all():
                el.left.append(el2.ID)

        cur = el.grid.T[:, el.grid.T.shape[1] - 1]
        for el2 in p:
            if (cur == el2.grid.T[:, 0]).all():
                el.right.append(el2.ID)

def convert_to_array_advance(field, tiles):
    array = np.array([-1])

    tile_x = tiles[0].grid.shape[0]
    tile_y = tiles[1].grid.shape[1]

    for y in range(field.shape[1]):
        temp = np.array([-1])
        for x in range(field.shape[0]):
            tile = np.zeros((tile_x,tile_y))
            for val in field[x, y].value:
                tile = tile + tiles[val].grid
            tile = tile / len(field[x,y].value)

            if not (temp == np.array([-1])).all():
                temp = np.concatenate((temp, tile), axis=0)
            else:
                temp = tile

        if not (array == np.array([-1])).all():
            array = np.concatenate((array, temp), axis=1)
        else:
            array = temp

    return array

def get_tiles():
    return (Part(np.array([[0, 1, 0],
                           [0, 1, 0],
                           [0, 1, 0]]).T, 0),
            Part(np.array([[0, 1, 0],
                           [0, 1, 1],
                           [0, 1, 0]]).T, 1),
            Part(np.array([[0, 1, 0],
                           [1, 1, 0],
                           [0, 1, 0]]).T, 2),
            Part(np.array([[0, 1, 0],
                           [1, 1, 0],
                           [0, 0, 0]]).T, 3),
            Part(np.array([[0, 0, 0],
                           [0, 1, 1],
                           [0, 1, 0]]).T, 4),
            Part(np.array([[0, 0, 0],
                           [1, 1, 1],
                           [0, 0, 0]]).T, 5),
            Part(np.array([[0, 1, 0],
                           [1, 1, 1],
                           [0, 0, 0]]).T, 6),
            Part(np.array([[0, 0, 0],
                           [1, 1, 0],
                           [0, 1, 0]]).T, 7),
            Part(np.array([[0, 0, 0],
                           [0, 0, 0],
                           [0, 0, 0]]).T, 8),
            Part(np.array([[1, 1, 1],
                           [1, 1, 1],
                           [1, 1, 1]]).T, 9),
            Part(np.array([[1, 1, 1],
                           [0, 1, 0],
                           [0, 1, 0]]).T, 10),
            Part(np.array([[0, 1, 0],
                           [0, 1, 0],
                           [1, 1, 1]]).T, 11),
            Part(np.array([[1, 1, 0],
                           [1, 1, 0],
                           [1, 1, 1]]).T, 12),
            Part(np.array([[0, 1, 1],
                           [0, 1, 1],
                           [0, 1, 1]]).T, 13),
            Part(np.array([[0, 0, 0],
                           [0, 0, 0],
                           [1, 1, 1]]).T, 14),
            Part(np.array([[0, 0, 0],
                           [0, 0, 0],
                           [1, 0, 0]]).T, 15),
            Part(np.array([[0, 0, 0],
                           [0, 0, 0],
                           [0, 0, 1]]).T, 16),
            Part(np.array([[0, 0, 1],
                           [0, 0, 0],
                           [0, 0, 0]]).T, 17)
            )
def get_field(size, tiles):
    field = np.array([9999])

    for y in range(size[1]):
        for x in range(size[0]):
            if not (field == np.array([9999])).all():
                a = Cell([], len(tiles))
                a.add_base_values(len(tiles))
                field = np.concatenate((field, [a]), axis=0)

            else:
                a = Cell([], len(tiles))
                a.add_base_values(len(tiles))
                field = [a]
    return field.reshape(size)

def get_test_field():
    return np.array([[Cell([0,3,1], 3), Cell([0,3,3], 3), Cell([0,3,1], 3)],
                     [Cell([0,3,1], 3), Cell([0,3,1], 3), Cell([0,3], 3)]]).T

def printm(field):
    print("___________________")
    field = field.T
    for y, el_out in enumerate(field):
        for x, el in enumerate(el_out):
            print('{:30}'.format(str(field[y, x])), end='')
        print()
        print()
    print("___________________")
