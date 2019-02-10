import sys
import Mahjong
import random
import csv


def main():
    count = 50
    with open('mahjong.csv', 'w') as file:
        writer = csv.writer(file)
        for j in range(count):
            tile_mountain = Mahjong.init()
            random.shuffle(tile_mountain)
            tiles = []
            for i in tile_mountain:
                tiles.append(i.tileType)
            writer.writerow([tiles])
    sys.exit()


main()
