import sys
import Mahjong
import random

tileMountain = []
tileRiver = []


def main():
    global tileMountain
    tileMountain = Mahjong.init()
    random.shuffle(tileMountain)
    for i in tileMountain:
        print(i.tileType)
    sys.exit()


main()
