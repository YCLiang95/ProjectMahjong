import Mahjong
import NeuralNetwork
import random
import threading
import time
from multiprocessing import Process, Lock,  Manager
from MahjongCalculator.mahjong.shanten import Shanten
from MahjongCalculator.mahjong.tile import TilesConverter

tile_table = Mahjong.tile_table()
dic = Mahjong.tile_dictionary()
# win_table = MahjongWinTable.load_table("output.txt")
win_table = []
shanten = Shanten()

def main():
    test()


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
    suo = ""
    pin = ""
    man = ""
    hornor = ""
    for i in hand:
        if i.order <= 9:
            man += str(i.order)
        elif i.order > 9 and i.order <= 18:
            pin += str(i.order - 9)
        elif i.order > 18 and i.order <= 27:
            suo += str(i.order - 18)
        elif i.order == 28:
            hornor += "1"
        elif i.order == 29:
            hornor += "2"
        elif i.order == 30:
            hornor += "3"
        elif i.order == 31:
            hornor += "4"
        elif i.order == 32:
            hornor += "7"
        elif i.order == 33:
            hornor += "6"
        elif i.order == 34:
            hornor += "5"
    tiles = TilesConverter.string_to_34_array(man=man, pin=pin, sou=suo, honors=hornor)
    result = shanten.calculate_shanten(tiles)
    if result == -1:
        return 1.0
    elif result == 1:
        return 0.1
    elif result == -2:
        return 0.0
    else:
        return 0.0


#def check_wining(hand):
#    t = []
#    for i in hand:
#        t.append(i.order)
#    t.sort()
#    s = ""
#    for i in t:
#        s += tile_table[i]
#    return search(win_table, s, 0, len(win_table))


class TrainingThread(threading.Thread):
    def __init__(self, networks, start_index, end_index):
        threading.Thread.__init__(self)
        self.networks = networks
        self.start_index = start_index
        self.end_index = end_index

    def run(self):
        train(self.networks, self.start_index, self.end_index)


def train(networks, start, end, arr_fitness, games):
    for Network in range(start, end):
        arr_fitness[Network] = 0
        for Rounds in range(len(games)):
            fitness = 0.0
            mountain = games[Rounds].copy()
            river = []
            hand = []
            hand_table = [0 for i in range(34)]
            for i in range(13):
                hand.append(mountain.pop())
                hand_table[hand[i].order - 1] += 1
                river.append(mountain.pop())
                river.append(mountain.pop())
                river.append(mountain.pop())
            while len(mountain) > 10:
                hand.append(mountain.pop())
                hand_table[hand[13].order - 1] += 1
                fitness = max(fitness, check_wining(hand))
                #if check_wining(hand):
                if fitness == 1:
                    arr_fitness[Network] += 1
                    break
                for i in range(34):
                    networks[Network].layers[0][i].value = hand_table[i]
                networks[Network].evaluate()
                min_v = 2
                k = 0
                for i in range(34):
                    if hand_table[i] > 0 and networks[Network].layers[3][i].value < min_v:
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
                    fitness = max(fitness, check_wining(hand))
                    # if check_wining(hand):
                    if fitness == 1:
                        arr_fitness[Network] += 1
                        mountain.clear()
                        break
                    hand_table[hand[13].order - 1] -= 1
                    river.append(hand.pop(13))
            if fitness != 1:
                arr_fitness[Network] += fitness
        #print("Network:" + str(Network) + "  Fitness:" + str(round(arr_fitness[Network], 2)))


def test():
    games = []
    networks = []
    networks_count = 96
    threads_count = 4
    cut_off = 24
    game_count = 10
    for i in range(networks_count):
        networks.append(NeuralNetwork.NeuralNetwork([34, 127, 127, 34]))
        networks[i].mutate()
    for i in range(game_count):
        mountain = Mahjong.init()
        random.shuffle(mountain)
        games.append(mountain.copy())

    # do 100 test run
    for Generations in range(100):
        t = time.time()
        print("Generation:" + str(Generations))
        with Manager() as manager:
            network_fitness = manager.list(range(networks_count))
            threads = []
            for i in range(threads_count):
                threads.append(Process(target=train, args=(networks, i * cut_off, i * cut_off + cut_off, network_fitness, games)))
                threads[i].start()
            for i in threads:
                i.join()
            for i in range(len(networks)):
                networks[i].fitness = network_fitness[i]
        networks.sort(reverse=True)
        average = 0
        for i in range(networks_count):
            average += round(networks[i].fitness, 2)
            #print("Network:" + str(i) + "  Fitness:" + str(round(networks[i].fitness, 2)))
        average = round(average / networks_count, 2)
        print("Average Fitness: " + str(average) + " Time eclipsed:" + str(round(time.time() - t, 1)) + "s")
        # 3 of the bad networks were randomly chosen to survive
        # better networks still have better chance to survive
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


if __name__ == '__main__':
    main()

