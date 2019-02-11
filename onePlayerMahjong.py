import Mahjong
import MahjongWinTable
import NeuralNetwork
import random

tile_table = Mahjong.tile_table()
dic = Mahjong.tile_dictionary()
win_table = MahjongWinTable.load_table("output.txt")


def search(table, string, start, end):
    if string == table[(end - start) / 2]:
        return True
    else:
        if string < table[(end - start) / 2] and (end - start) / 2 - 1 > start:
            return search(table, string, start, (end - start) / 2 - 1)
        if string > table[(end - start) / 2] and (end - start) / 2 + 1 < end:
            return search(table, string, (end - start) / 2 + 1, end)
    return False


def check_wining(hand):
    t = []
    for i in hand:
        t.append(i.order)
    t.sort()
    s = ""
    for i in t:
        s += tile_table[i]
    return search(win_table, s, 0, len(win_table))


def main():
    pass


def threading(networks, start, end):
    pass


def test():
    networks = []
    for i in range(100):
        networks.append(NeuralNetwork.NeuralNetwork([34, 255, 255, 34]))
        networks[i].mutate()
    empty_hand_table = []
    for i in range(34):
        empty_hand_table.append(0)
    games = []
    for i in range(50):
        mountain = Mahjong.init()
        random.shuffle(mountain)
        games.append(mountain.copy())
    # do 100 test run
    for Generations in range(100):
        print("Generation:" + str(Generations))
        for Network in range(100):
            networks[Network].fitness = 0
            for Rounds in range(50):
                mountain = games[Rounds].copy()
                river = []
                hand = []
                hand_table = empty_hand_table.copy()
                for i in range(13):
                    hand.append(mountain.pop())
                    hand_table[hand[i].order - 1] += 1
                    river.append(mountain.pop())
                    river.append(mountain.pop())
                    river.append(mountain.pop())
                while len(mountain) > 10:
                    hand.append(mountain.pop())
                    hand_table[hand[13].order - 1] += 1
                    if check_wining(hand):
                        networks[Network].fitness += 1
                        break
                    for i in range(34):
                        networks[Network].layers[0][i].value = hand_table[i]
                    networks[Network].evaluate()
                    min_v = 2
                    k = 0
                    for i in range(34):
                        if networks[Network].layers[3][i].value < min_v:
                            min_v = networks[Network].layers[3][i].value
                            k = i
                    hand_table[k] -= 1
                    for i in range(len(hand)):
                        if hand[i].order == k + 1:
                            river.append(hand.pop(i))
                            break
                    for i in range(3):
                        hand.append(mountain.pop())
                        hand_table[hand[13].order - 1] += 1
                        if check_wining(hand):
                            networks[Network].fitness += 1
                            mountain.clear()
                            break
                        hand_table[hand[13].order - 1] -= 1
                        river.append(hand.pop(13))
            print("Network:" + str(Network) + "  Fitness:" + str(networks[Network].fitness))
        networks.sort(reverse=True)
        # 3 of the bad networks were randomly chosen to survive
        new_networks = []
        i = random.randint(0, 15)
        j = random.randint(1, 10)
        k = random.randint(1, 5)
        networks[47] = networks[47 + i]
        networks[48] = networks[47 + i + j]
        networks[49] = networks[47 + i + j + k]
        for i in range(50):
            j = random.randint(0, 50)
            new_networks += NeuralNetwork.uniform_crossover(networks[i], networks[j])
        networks = new_networks


test()
