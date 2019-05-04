import Mahjong
import NeuralNetwork
import random
import time
import os
import sys
import MahjongGame
import numpy as np


from multiprocessing import Process, Manager
sys.path.append('MahjongCalculator')

tile_table = Mahjong.tile_table()


def train(networks, start, end, arr_fitness, games):
    for Network in range(start, end):
        arr_fitness[Network] = 0
        for Rounds in range(len(games)):
            log = ""
            tracker = MahjongGame.GameTracker()
            tracker.tile_mountain = games[Rounds].copy()
            tracker.initial_draw()
            for i in range(4):
                log += "player " + str(i) + " initial hands "
                for j in range(34):
                    for k in range(4):
                        if (tracker.player_hand[i][j][k]) == 1:
                            log += tile_table[j] + " "
                log += '\n'
            current_player = -1

            ron = False
            while tracker.has_next() and not ron:
                current_player = 0
                if current_player == 4:
                    current_player = 0

                tile = tracker.draw(current_player)
                log += "Player " + str(current_player) + " draw " + tile_table[tile.order] + "\n"
                if tracker.check_number_of_tile(current_player, tile.order) == 4:
                    tracker.close_kan(current_player, tile.order)
                    log += "Player " + str(current_player) + " close Kan " + tile_table[tile.order] + "\n"
                    tile = tracker.draw(current_player)
                    log += "Player " + str(current_player) + " draw " + tile_table[tile.order] + "\n"

                # if check_wining(hand):
                score = tracker.check_win(current_player)
                if score >= 1000:
                    arr_fitness[Network] += score
                    log += "Player " + str(current_player) + " won " + str(score) + "\n"
                    log += "player " + str(current_player) + " Wining hands "
                    for j in range(34):
                        for k in range(4):
                            if (tracker.player_hand[current_player][j][k]) == 1:
                                log += tile_table[j] + " "
                    log += '\n'
                    # print(log)
                    break

                networks[Network].inputLayer = np.asarray(tracker.output_array[current_player], dtype=np.float32)
                networks[Network].evaluate()

                m = 0
                index = -1
                for i in range(34):
                    if tracker.player_hand[current_player][i][0] == 1 and (networks[Network].outputLayer[i] < m or index == -1):
                        m = networks[Network].outputLayer[i]
                        index = i
                tracker.discard(current_player, index)
                log += "Player " + str(current_player) + " discard " + tile_table[index] + "\n"
                for i in range(1, 4):
                    tile = tracker.draw(i)
                    log += "Player " + str(i) + " draw " + tile_table[tile.order] + "\n"
                    tracker.discard(i, tile.order)
                    log += "Player " + str(i) + " discard " + tile_table[tile.order] + "\n"
                    score = tracker.check_win(current_player, check_ron=True)
                    if score >= 1000:
                        arr_fitness[Network] += score
                        ron = True
                        log += "Player " + str(current_player) + " won " + str(score) + "\n"
                        log += "player " + str(current_player) + " Wining hands "
                        for j in range(34):
                            for k in range(4):
                                if (tracker.player_hand[current_player][j][k]) == 1:
                                    log += tile_table[j] + " "
                        log += '\n'
                        # print(log)
                        break
                    if networks[Network].outputLayer[tile.order] > 0:
                        t = tracker.check_number_of_tile(0, tile.order)
                        if t == 4:
                            tracker.kan(0, tile.order)
                            log += "Player " + str(current_player) + "Kan " + tile_table[tile.order] + "\n"
                            break
                        elif t == 3:
                            tracker.pon(0, tile.order)
                            log += "Player " + str(current_player) + "Pon " + tile_table[tile.order] + "\n"
                            break
            if not ron:
                arr_fitness[Network] += tracker.check_win(current_player)
        # print("Network:" + str(Network) + "  Fitness:" + str(round(arr_fitness[Network], 2)))


def test():
    networks = []
    networks_count = 96
    threads_count = 6
    cut_off = 16
    test_per_thread = 10
    game_count = 10
    generation_count = 500
    pre_generation = 0
    for i in range(networks_count):
        nn = NeuralNetwork.NeuralNetwork()
        nn.add_convolutional_layer(shape=(10, 34, 4), filter_shape=(5, 2), height=32)
        nn.add_convolutional_layer(shape=(32, 30, 3), filter_shape=(5, 2), height=32)
        nn.add_convolutional_layer(shape=(32, 26, 2), filter_shape=(5, 2), height=32)
        nn.add_flatten_layer()
        nn.add_multilayer_perceptron(shape=(704, 256, 128, 34))
        networks.append(nn)
    if not os.path.exists("NeuroNet"):
        os.makedirs("NeuroNet")
    if os.path.exists("Networks/"):
        i = 0
        for filename in os.listdir("Networks/"):
            networks[i].load("Networks/" + filename)
            i += 1
            if i >= networks_count:
                break
        print(str(i) + " Networks loaded")

    validation_games = []
    games = []
    mountain = Mahjong.init()
    for i in range(game_count):
        random.shuffle(mountain)
        games.append(mountain.copy())
        random.shuffle(mountain)
        validation_games.append(mountain.copy())

    # do 300 test run
    for Generations in range(generation_count):
        t = time.time()
        print("Generation:" + str(pre_generation + Generations))

        if Generations > 0:
            games = []
            for i in range(game_count):
                mountain = Mahjong.init()
                random.shuffle(mountain)
                games.append(mountain.copy())

        with Manager() as manager:
            network_fitness = manager.list(range(networks_count))
            threads = []
            for i in range(threads_count):
                threads.append(Process(target=train, args=(networks, i * cut_off,
                                                           i * cut_off + cut_off,
                                                           network_fitness, games)))
                threads[i].start()
            for i in threads:
                i.join()
            for i in range(len(networks)):
                networks[i].fitness = network_fitness[i]
            networks.sort(reverse=True)

            if (pre_generation + Generations) % 10 == 0:
                threads = []
                network_fitness = manager.list(range(threads_count * test_per_thread))
                for i in range(threads_count):
                    threads.append(Process(target=train, args=(networks, i * test_per_thread,
                                                               i * test_per_thread + test_per_thread,
                                                               network_fitness, validation_games)))
                    threads[i].start()
                for i in threads:
                    i.join()
                average = 0
                validation_max = 0
                for i in range(threads_count * test_per_thread):
                    if network_fitness[i] > validation_max:
                        validation_max = network_fitness[i]
                    average += network_fitness[i]
                average = average / (threads_count * test_per_thread)
                print("Generation " + str(pre_generation + Generations) + " Validation Average fitness: " + str(round(average, 2)))
                print("Generation " + str(pre_generation + Generations) + " Validation Best: " + str(round(validation_max, 2)))
                if not os.path.exists("NeuroNet/" + str(pre_generation + Generations)):
                    os.makedirs("NeuroNet/" + str(pre_generation + Generations))
                with open("NeuroNet/" + str(pre_generation + Generations) + "/validation.txt", 'w+') as file:
                    file.write("Generation " + str(pre_generation + Generations) + " Validation Average fitness: " + str(round(average, 2)) + '\n')
                    for i in range(threads_count * test_per_thread):
                        file.write("Network: " + str(i) + " " + str(round(network_fitness[i], 2)) + '\n')

        average = 0
        average_ten = 0
        average_one = 0
        average_fifty = 0
        if not os.path.exists("NeuroNet/" + str(pre_generation + Generations)):
            os.makedirs("NeuroNet/" + str(pre_generation + Generations))
        for i in range(networks_count):
            average += round(networks[i].fitness, 2)
            if i <= networks_count / 100:
                average_one += round(networks[i].fitness, 2)
            elif i <= networks_count / 10:
                average_ten += round(networks[i].fitness, 2)
            elif i <= networks_count / 2:
                average_fifty += round(networks[i].fitness, 2)
            if i < networks_count / 10:
                networks[i].save("NeuroNet/" + str(pre_generation + Generations) + "/"+str(i) + ".pkl")
            # print("Network:" + str(i) + "  Fitness:" + str(round(networks[i].fitness, 2)))
        average = round(average / networks_count, 2)
        average_fifty = (average_one + average_ten + average_fifty) / (networks_count / 2)
        average_ten = (average_one + average_ten) / (networks_count / 10)
        average_one = average_one / (networks_count / 100)
        print("Average Fitness: " + str(average) + " Time eclipsed:" + str(round(time.time() - t, 1)) + "s")
        print("One Percentile: " + str(round(average_one, 2)))
        print("Ten Percentile: " + str(round(average_ten, 2)))
        print("Fifty Percentile: " + str(round(average_fifty, 2)))
        with open("NeuroNet/" + str(pre_generation + Generations) + "/log.txt", 'w+') as file:
            file.write("Average Fitness: " + str(average) + " Time eclipsed:" + str(round(time.time() - t, 1)) + "s" + '\n')
            file.write("One Percentile: " + str(round(average_one, 2)) + '\n')
            file.write("Ten Percentile: " + str(round(average_ten, 2)) + '\n')
            file.write("Fifty Percentile: " + str(round(average_fifty, 2)) + '\n')
            for i in range(networks_count):
                file.write("Network " + str(i) + " Fitness: " + str(round(networks[i].fitness, 2)) + '\n')
        file.close()

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
            new_networks += networks[i].uniform_crossover(networks[j])
        new_networks[len(new_networks) - 1] = networks[0]
        networks = new_networks
        for i in range(len(networks) - 1):
            networks[i].mutate()


if __name__ == '__main__':
    test()
