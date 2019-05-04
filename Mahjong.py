def tile_table():
    result = []
    for i in range(1, 10):
        result.append(str(i) + "M")
    for i in range(1, 10):
        result.append(str(i) + "P")
    for i in range(1, 10):
        result.append(str(i) + "S")
    result.append("Df")
    result.append("Nf")
    result.append("Xf")
    result.append("Bf")
    result.append("Bb")
    result.append("Fc")
    result.append("Hz")
    return result


def tile_dictionary():
    table = tile_table()
    result = {}
    for i in range(len(table)):
        result[table[i]] = i
    return result


class Tile:
    tileType = ""
    order = 0

    def __init__(self, tile, order):
        self.tileType = tile
        self.order = order


def init():
    tile_mountain = []
    for i in range(9):
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
        tile_mountain.append(Tile("Df", 27))
        tile_mountain.append(Tile("Nf", 28))
        tile_mountain.append(Tile("Xf", 29))
        tile_mountain.append(Tile("Bf", 30))
        tile_mountain.append(Tile("Bb", 31))
        tile_mountain.append(Tile("Fc", 32))
        tile_mountain.append(Tile("Hz", 33))
    return tile_mountain
