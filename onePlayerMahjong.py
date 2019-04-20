import Mahjong
import NeuralNetwork
import random
import time
import os
import sys

from multiprocessing import Process, Manager
sys.path.append('MahjongCalculator')




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
                score = check_wining(hand)
                if score >= 1000:
                    arr_fitness[Network] += score
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
                    score = check_wining(hand)
                    if score >= 1000:
                        arr_fitness[Network] += score
                        ron = True
                        break
                    hand_table[hand[13].order - 1] -= 1
                    river.append(hand.pop(13))
                if ron:
                    break
            if not ron:
                arr_fitness[Network] += check_wining(hand)
        # print("Network:" + str(Network) + "  Fitness:" + str(round(arr_fitness[Network], 2)))


def test():
    networks = []
    networks_count = 960
    threads_count = 4
    cut_off = 80
    test_per_thread = 10
    game_count = 10
    generation_count = 500
    pre_generation = 0
    for i in range(networks_count):
        nn = NeuralNetwork.NeuralNetwork()
        nn.add_convolutional_layer(shape=(2, 34, 4))
        nn.add_convolutional_layer(shape=(2, 32, 3))
        nn.add_convolutional_layer(shape=(2, 30, 2))
        nn.add_multilayer_perceptron()
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
    for i in range(game_count):
        mountain = Mahjong.init()
        random.shuffle(mountain)
        validation_games.append(mountain.copy())
        games.append(mountain.copy())

    # do 300 test run
    for Generations in range(generation_count):
        t = time.time()
        print("Generation:" + str(pre_generation + Generations))

        if Generations >= 100:
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

            if Generations % 10 == 0 and Generations >= 100:
                threads = []
                for i in range(threads_count):
                    threads.append(Process(target=train, args=(networks, i * test_per_thread,
                                                               i * test_per_thread + test_per_thread,
                                                               network_fitness, validation_games)))
                    threads[i].start()
                for i in threads:
                    i.join()
                average = 0
                for i in range(threads_count * test_per_thread):
                    average += network_fitness[i]
                average = average / (threads_count * test_per_thread)
                print("Generation " + str(Generations) + " Validation Average fitness: " + str(round(average, 2)))
                with open("NeuroNet/" + str(pre_generation + Generations) + "/validation.txt", 'w+') as file:
                    file.write("Generation " + str(Generations) + " Validation Average fitness: " + str(round(average, 2)) + '\n')

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
            networks[i].save("NeuroNet/" + str(pre_generation + Generations) + "/"+str(i) + ".txt")
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
            new_networks += NeuralNetwork.uniform_crossover(networks[i], networks[j])
        new_networks[len(new_networks) - 1] = networks[0]
        networks = new_networks


if __name__ == '__main__':
    test()
