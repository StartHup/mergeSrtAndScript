import csv
import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms.shortest_paths import weighted
import numpy as np
def file_to_list(filename):
    with open(filename, "r") as script:
        return list(csv.reader(script))


def mainly():
    script = file_to_list("bbt/srt-script.csv")
    #2.b
    names = set([line[3] for line in script])
    print (names)
    # 2.c 
    g = nx.MultiDiGraph()
    g.add_nodes_from(names)
    edges = []
    for i in range(len(script) - 1):
        g.add_edge(script[i][3], script[i+1][3], length=1)
    pos = nx.spring_layout(g)
    nx.draw_networkx_nodes(g, pos, with_labels=True)

    pos = nx.spring_layout(g)
    nx.draw(g, pos)
    edge_labels=dict([((u,v,),d['length'])
                for u,v,d in g.edges(data=True)])
    nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels, label_pos=0.3, font_size=7)
    plt.show()

def main():
    script = file_to_list("bbt/srt-script.csv")
    names = list(set([line[3] for line in script]))
    print(names)
    table = np.zeros(((len(names),len(names))), dtype=int)
    for i in range(len(script) -1 ):
        talker = names.index(script[i][3])
        next = names.index(script[i+1][3])
        table[min(talker, next)][max(talker, next)] += 1
    print(table)

if __name__ == "__main__":
    main()