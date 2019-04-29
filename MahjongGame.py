from MahjongCalculator.mahjong.shanten import Shanten
from MahjongCalculator.mahjong.tile import TilesConverter
from MahjongCalculator.mahjong.hand_calculating.hand import HandCalculator

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
        win_tile[hand[13].order] = 1
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


class GameTracker:

    def __init__(self):
        self.player_hand = [[[0 for i in range(4)] for j in range(34)] for k in range(4)]
        self.tile_river = [[[0 for i in range(4)] for j in range(34)] for k in range(4)]
        self.tile_mountain = []
        self.bounce = [[0 for i in range(4)] for j in range(34)]
        self.output_array = [[], [], [], []]
        for i in range(4):
            self.output_array[i] = [[], [], [], [], [], []]
            self.output_array[i][0] = self.player_hand[i]
            for j in range(4):
                self.output_array[i][j + 1] = self.tile_river[i]
            self.output_array[i][5] = self.bounce

    def initial_draw(self):
        for i in range(13):
            for j in range(4):
                self.draw(j)

    def get_output(self, player):
        pass

    def draw(self, player):
        tile = self.tile_mountain.pop()
        for i in range(4):
            if self.player_hand[player][tile.order][i] == 0:
                self.player_hand[player][tile.order][i] = 1
                break

    def discard(self, player, tile):
        for i in range(4):
            if self.player_hand[player][tile.order][3 - i] == 1:
                self.player_hand[player][tile.order][3 - i] = 0
                break
        for i in range(4):
            if self.tile_river[player][tile.order][i] == 0:
                self.tile_river[player][tile.order][i] = 1
                break

    def can_chi(self):
        pass

    def can_pon(self):
        pass

    def can_kan(self):
        pass

    def check_win(self):
        pass
