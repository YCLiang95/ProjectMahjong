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
                tile_mountain.append(Tile("HS" + str(i), 18 + i))
                tile_mountain.append(Tile("HP" + str(i), 9 + i))
                tile_mountain.append(Tile("HM" + str(i), i))
            else:
                tile_mountain.append(Tile("S" + str(i), 18 + i))
                tile_mountain.append(Tile("P" + str(i), 9 + i))
                tile_mountain.append(Tile("M" + str(i), i))
    for i in range(4):
        tile_mountain.append(Tile("D", 28))
        tile_mountain.append(Tile("N", 29))
        tile_mountain.append(Tile("X", 30))
        tile_mountain.append(Tile("B", 31))
        tile_mountain.append(Tile("Z", 32))
        tile_mountain.append(Tile("F", 33))
        tile_mountain.append(Tile("BB", 34))
    return tile_mountain
