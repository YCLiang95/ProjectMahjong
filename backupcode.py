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

