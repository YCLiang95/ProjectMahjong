import Mahjong
import MahjongWinTable
import NeuralNetwork
import random
import threading

tile_table = Mahjong.tile_table()
dic = Mahjong.tile_dictionary()
win_table = MahjongWinTable.load_table("output.txt")
empty_hand_table = []
games = []


def search(table, string, start_index, end_index):
    start = start_index
    end = end_index - 1
    while start <= end:
        middle = start + round((end - start) / 2)
        if string < table[middle]:
            end = middle - 1
        elif string > table[middle]:
            start = middle + 1
        else:
            return True
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


class TrainingThread(threading.Thread):
    def __init__(self, networks, start_index, end_index):
        threading.Thread.__init__(self)
        self.networks = networks
        self.start_index = start_index
        self.end_index = end_index

    def run(self):
        train(self.networks, self.start_index, self.end_index)


def train(networks, start, end):
    for Network in range(start, end):
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
    pass


def test():
    networks = []
    networks_count = 96
    threads_count = 12
    for i in range(networks_count):
        networks.append(NeuralNetwork.NeuralNetwork([34, 255, 255, 34]))
        networks[i].mutate()
    for i in range(34):
        empty_hand_table.append(0)
    for i in range(50):
        mountain = Mahjong.init()
        random.shuffle(mountain)
        games.append(mountain.copy())

    # do 100 test run
    for Generations in range(100):
        print("Generation:" + str(Generations))
        # _thread.start_new_thread(train, (networks, i * 8, i * 8 + 8))
        threads = []
        for i in range(threads_count):
            threads.append(TrainingThread(networks, i * 8, i * 8 + 8))
            threads[i].start()
        for i in threads:
            i.join()
        networks.sort(reverse=True)
        # 3 of the bad networks were randomly chosen to survive
        new_networks = []
        i = random.randint(0, 15)
        j = random.randint(1, 10)
        k = random.randint(1, 5)
        networks[round(networks_count / 2) - 3] = networks[round(networks_count / 2) - 3 + i]
        networks[round(networks_count / 2) - 2] = networks[round(networks_count / 2) - 2 + i + j]
        networks[round(networks_count / 2) - 1] = networks[round(networks_count / 2) - 1 + i + j + k]
        for i in range(round(networks_count / 2)):
            j = random.randint(0, round(networks_count / 2))
            new_networks += NeuralNetwork.uniform_crossover(networks[i], networks[j])
        networks = new_networks


test()
