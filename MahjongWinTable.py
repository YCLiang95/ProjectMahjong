import Mahjong


tilesTable = Mahjong.tile_table()


def load_table(path):
    with open(path, 'r') as file:
        result = file.read().splitlines()
    print("Win table loaded:" + str(len(result)))
    return result


def create_table():
    table = []
    for i in range(35):
        table.append(4)
    return table


def find_3tiles(table, depth, string):
    result = []
    for i in range(1, 35):
        if table[i] >= 3:
            table[i] -= 3
            t = string + [i, i, i]
            if depth == 0:
                result += find_pair(table, t)
            else:
                result += find_flush(table, depth - 1, t) + \
                          find_3tiles(table, depth - 1, t)
            table[i] += 3
    return result


def find_pair(table, string):
    result = []
    for i in range(1, 35):
        if table[i] >= 2:
            result.append(string + [i, i])
    return result


def find_flush(table, depth, string):
    result = []
    for i in range(3):
        for j in range(1, 8):
            if table[i * 9 + j] > 0 and table[i * 9 + j + 1] > 0 and table[i * 9 + j + 2] > 0:
                table[i * 9 + j] -= 1
                table[i * 9 + j + 1] -= 1
                table[i * 9 + j + 1] -= 1
                t = string + [i * 9 + j, i * 9 + j + 1, i * 9 + j + 2]
                if depth == 0:
                    result += find_pair(table, t)
                else:
                    result += find_flush(table, depth - 1, t) + \
                              find_3tiles(table, depth - 1, t)
                table[i * 9 + j] += 1
                table[i * 9 + j + 1] += 1
                table[i * 9 + j + 1] += 1
    return result


def main():
    table = create_table()
    result = find_3tiles(table, 3, []) + find_flush(table, 3, [])
    result2 = set()
    for i in result:
        t = sorted(i)
        string = ""
        for j in t:
            string = string + tilesTable[j]
        result2.add(string)
    with open('output.txt', 'w') as file:
        for i in sorted(result2):
            print(i, file=file)


main()
