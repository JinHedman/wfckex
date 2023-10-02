import numpy as np
from Part import *
class Rule_creation:
    def __init__(self):
        pass

    def create_set(self, image, res):
        tiles = []

        (y_size, x_size, k) = image.shape
        print(image.shape)
        x_size = int(x_size / res[0])
        y_size = int(y_size / res[1])

        id_grid = np.zeros((y_size, x_size), dtype=int)

        current_id = 0
        for y in range(y_size):
            for x in range(x_size):
                slice = image[y*res[1]:y*res[1]+res[1],x*res[0]:x*res[0]+res[0]].transpose((1,0,2))

                for i, tile in enumerate(tiles):
                    if (tile.grid == slice).all():
                        id_grid[y][x] = tile.ID
                        break
                    if i == len(tiles) - 1:
                        new_tile = Part(slice, current_id)
                        current_id += 1
                        id_grid[y][x] = new_tile.ID
                        tiles.append(new_tile)
                else:
                    new_tile = Part(slice, current_id)
                    current_id += 1
                    id_grid[y][x] = new_tile.ID
                    tiles.append(new_tile)

        prob_list = self.get_probability_list(id_grid, tiles)

        for y in range(y_size):
            for x in range(x_size):
                current_tile = tiles[id_grid[y][x]]
                if x - 1 >= 0:
                    if id_grid[y][x - 1] not in current_tile.left:
                        current_tile.left.append(id_grid[y][x-1])
                if x + 1 < x_size:
                    if id_grid[y][x + 1] not in current_tile.right:
                        current_tile.right.append(id_grid[y][x+1])
                if y - 1 >= 0:
                    if id_grid[y - 1][x] not in current_tile.top:
                        current_tile.top.append(id_grid[y-1][x])
                if y + 1 < y_size:
                    if id_grid[y+1][x] not in current_tile.bottom:
                        current_tile.bottom.append(id_grid[y+1][x])

        return (tiles, prob_list)

    def get_probability_list(self, id_grid, tiles):
        problist = np.array([0.0] * len(tiles))
        grid_size = id_grid.shape[0] * id_grid.shape[1]
        for row in id_grid:
            for tile_nr in row:
                problist[tile_nr] += 1.0

        return list(problist / grid_size)




