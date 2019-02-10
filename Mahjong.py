class Tile:
    tileType = ""
    order = 0

    def __init__(self, tile, order):
        self.tileType = tile
        self.order = order


class Game:
    def __init__(self):
        pass

    def check_wining(self):
        pass


def init():
    tile_mountain = []
    for i in range(1, 10):
        for j in range(4):
            if i == 5 and j == 3:
                tile_mountain.append(Tile("Ts", 18 + i))
                tile_mountain.append(Tile("Tp", 9 + i))
                tile_mountain.append(Tile("Tm", i))
            else:
                tile_mountain.append(Tile(str(i) + "S", 18 + i))
                tile_mountain.append(Tile(str(i) + "P", 9 + i))
                tile_mountain.append(Tile(str(i) + "M", i))
    for i in range(4):
        tile_mountain.append(Tile("Df", 28))
        tile_mountain.append(Tile("Nf", 29))
        tile_mountain.append(Tile("Xf", 30))
        tile_mountain.append(Tile("Bf", 31))
        tile_mountain.append(Tile("Hz", 32))
        tile_mountain.append(Tile("Fc", 33))
        tile_mountain.append(Tile("Bb", 34))
    return tile_mountain
