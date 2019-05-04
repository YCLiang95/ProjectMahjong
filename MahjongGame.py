from MahjongCalculator.mahjong.shanten import Shanten
from MahjongCalculator.mahjong.tile import TilesConverter
from MahjongCalculator.mahjong.hand_calculating.hand import HandCalculator
from mahjong.hand_calculating.hand_config import HandConfig
from mahjong.meld import Meld

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
        self.open_set = [[[0 for i in range(4)] for j in range(34)] for k in range(4)]
        self.melds = [[], [], [], []]
        self.tile_mountain = []
        self.bounce = [[0 for i in range(4)] for j in range(34)]
        self.last_discard = None
        self.last_discard_player = None
        self.last_draw = None

        self.output_array = [[], [], [], []]
        for i in range(4):
            self.output_array[i] = [[], [], [], [], [], [], [], [], [], []]
            self.output_array[i][0] = self.player_hand[i]
            for j in range(4):
                self.output_array[i][j + 1] = self.tile_river[i]
            for j in range(4):
                self.output_array[i][j + 5] = self.open_set[i]
            self.output_array[i][9] = self.bounce

    def initial_draw(self):
        for i in range(13):
            for j in range(4):
                self.draw(j)

    def get_output(self, player):
        pass

    def has_next(self):
        return len(self.tile_mountain) > 10

    def draw(self, player):
        tile = self.tile_mountain.pop()
        self.last_draw = tile.order
 #       print("Player: " + str(player) + " draw: " + str(tile.order))
        for i in range(4):
            if self.player_hand[player][tile.order][i] == 0:
                self.player_hand[player][tile.order][i] = 1
                break
        return tile

    def discard(self, player, tile):
        discard = False
#        print("Player: " + str(player) + " discard: " + str(tile))
        for i in range(4):
            if self.player_hand[player][tile][3 - i] == 1:
                self.player_hand[player][tile][3 - i] = 0
                discard = True
                break
        for i in range(4):
            if self.tile_river[player][tile][i] == 0:
                self.tile_river[player][tile][i] = 1
                discard = True
                break
        if not discard:
            print("Faild to discard")
        self.last_discard = tile
        self.last_discard_player = player

    def can_chi(self, player, tile):
        pass

    def check_number_of_tile(self, player, tile):
        result = 0
        for i in range(4):
            result += self.player_hand[player][tile][i]
        return result

    def pon(self, player, tile):
        for i in range(3):
            self.player_hand[player][tile][i] = 0
            self.open_set[player][tile][i] = 1
        for i in range(2):
            if self.tile_river[self.last_discard_player][tile][i] == 1:
                self.tile_river[self.last_discard_player][tile][i] = 0
                break
        tiles = [0 for i in range(34)]
        tiles[tile] = 3
        self.melds[player].append(Meld(meld_type=Meld.PON, tiles=tiles))

    def kan(self, player, tile):
        for i in range(4):
            self.player_hand[player][tile][i] = 0
            self.open_set[player][tile][i] = 1
        self.tile_river[self.last_discard_player][tile][0] = 0
        tiles = [0 for i in range(34)]
        tiles[tile] = 4
        self.melds[player].append(Meld(meld_type=Meld.KAN, tiles=tiles))

    def close_kan(self, player, tile):
        for i in range(4):
            self.player_hand[player][tile][i] = 0
            self.open_set[player][tile][i] = 1
        tiles = [0 for i in range(34)]
        tiles[tile] = 4
        self.melds[player].append(Meld(meld_type=Meld.KAN, tiles=tiles))

    def check_win(self, player, check_ron=False):
        tiles = [0 for i in range(34)]
        for i in range(34):
            for j in range(4):
                tiles[i] += self.player_hand[player][i][j]
                if j != 3:
                    tiles[i] += self.open_set[player][i][j]
        open_sets = []
        for i in range(len(self.melds[player])):
            t = []
            for j in range(34):
                for k in range(self.melds[player][i].tiles[j]):
                    t.append(j)
            open_sets.append(t)

        if check_ron:
            tiles[self.last_discard] += 1

        result = shanten.calculate_shanten(tiles, open_sets)
        if result == -1:
            win_tile = [0 for i in range(34)]
            if check_ron:
                win_tile[self.last_discard] = 1
            else:
                win_tile[self.last_draw] = 1
            a = TilesConverter.to_136_array(tiles)
            b = TilesConverter.to_136_array(win_tile)[0]

            if check_ron:
                result = calculator.estimate_hand_value(a, b, melds=self.melds[player])
            else:
                result = calculator.estimate_hand_value(a, b,  melds=self.melds[player], config=HandConfig(is_tsumo=True))

            if result.cost is None:
                return 100
            else:
                return result.cost['main'] + result.cost['additional']
        elif result == -2:
            print("Faild shanten")
            print(tiles)
            print(open_sets)
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
