def tile_table():
    result = [" "]
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
    result.append("Hz")
    result.append("Fc")
    result.append("Bb")
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
