import Mahjong
import NeuralNetwork
import random
import time
import os
from multiprocessing import Process, Lock,  Manager
from MahjongCalculator.mahjong.shanten import Shanten

tile_table = Mahjong.tile_table()
dic = Mahjong.tile_dictionary()
# win_table = MahjongWinTable.load_table("output.txt")
win_table = []
shanten = Shanten()


def check_wining(hand):
    tiles = [0 for i in range(34)]
    for i in hand:
        tiles[i.order - 1] += 1
    result = shanten.calculate_shanten(tiles)
    if result == -1:
        return 1.0
    elif result == 1:
        return 0.1
    elif result == -2:
        return 0.0
    else:
        return 0.0


def train(networks, start, end, arr_fitness, games):
    for Network in range(start, end):
        arr_fitness[Network] = 0
        for Rounds in range(len(games)):
            mountain = games[Rounds].copy()
            river = []
            hand = []
            ron = False
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
                # if check_wining(hand):
                if check_wining(hand) == 1:
                    arr_fitness[Network] += 1
                    ron = True
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
                    # if check_wining(hand):
                    if check_wining(hand) == 1:
                        arr_fitness[Network] += 1
                        ron = True
                        break
                    hand_table[hand[13].order - 1] -= 1
                    river.append(hand.pop(13))
                if ron:
                    break
            if not ron:
                arr_fitness[Network] += check_wining(hand)
        #print("Network:" + str(Network) + "  Fitness:" + str(round(arr_fitness[Network], 2)))


def test():
    games = []
    networks = []
    networks_count = 960
    threads_count = 12
    cut_off = 80
    game_count = 10
    generation_count = 100
    for i in range(networks_count):
        networks.append(NeuralNetwork.NeuralNetwork([34, 128, 64, 34]))
        networks[i].mutate()
    for i in range(game_count):
        mountain = Mahjong.init()
        random.shuffle(mountain)
        games.append(mountain.copy())
    if not os.path.exists("NeuroNet"):
        os.makedirs("NeuroNet")

    # do 100 test run
    for Generations in range(generation_count):
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
        if not os.path.exists("NeuroNet/" + str(Generations)):
            os.makedirs("NeuroNet/" + str(Generations))
        for i in range(networks_count):
            average += round(networks[i].fitness, 2)
            networks[i].save("NeuroNet/" + str(Generations) + "/"+str(i) + ".txt")
            # print("Network:" + str(i) + "  Fitness:" + str(round(networks[i].fitness, 2)))
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
    test()

