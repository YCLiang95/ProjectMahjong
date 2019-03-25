from MahjongCalculator.mahjong.shanten import Shanten
from MahjongCalculator.mahjong.tile import TilesConverter

shanten = Shanten()
tiles = TilesConverter.string_to_34_array(man='12359', pin='123456', sou='443')
result = shanten.calculate_shanten(tiles)

print(result)
