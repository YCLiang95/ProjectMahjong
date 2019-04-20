import Mahjong
from MahjongCalculator.mahjong.shanten import Shanten
from MahjongCalculator.mahjong.tile import TilesConverter
from MahjongCalculator.mahjong.hand_calculating.hand import HandCalculator

tile_table = Mahjong.tile_table()
dic = Mahjong.tile_dictionary()
# win_table = MahjongWinTable.load_table("output.txt")
win_table = []
shanten = Shanten()
calculator = HandCalculator()


def check_wining(hand):
    tiles = [0 for i in range(34)]
    for i in hand:
        tiles[i.order - 1] += 1
    result = shanten.calculate_shanten(tiles)
    if result == -1:
        win_tile = [0 for i in range(34)]
        win_tile[hand[13].order - 1] = 1
        a = TilesConverter.to_136_array(tiles)
        b = TilesConverter.to_136_array(win_tile)[0]
        result = calculator.estimate_hand_value(a, b)
        if result.cost is None:
            return 100
        else:
            return result.cost['main'] + result.cost['additional']
    elif result == -2:
        return 0
    elif result == 0:
        return 100
    elif result == 1:
        return 10
    elif result == 2:
        return 1
    else:
        return 0
        # return round(1 / (result + 2) * 1000, 2)

class Game:

    def __init__(self):
        self.player_hand = [[], [], [], []]
        self.tile_mountain = []
        self.tile_river = [[], [], [], []]

    def draw(self, player):
        pass

    def discard(self, player, tile):
        pass

    def can_chi(self):
        pass

    def can_pon(self):
        pass

    def can_kan(self):
        pass
