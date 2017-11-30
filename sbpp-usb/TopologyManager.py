import networkx as nx
from DisjointedNode import path_computing

graph = nx.DiGraph()  # create graph
total_slots = 300

def get_graph(filename):
    """
        Get the adjacency matrix from link_to_port
    """
    # switch_pairs_weight = {(1, 2, 1), (1, 3, 1), (2, 3, 1), (2, 4, 1), (3, 4, 1), (3, 5, 1), (4, 5, 1), (4, 6, 1),
    #                 (5, 6, 1)}  # the connected switches pair
    switch_pairs_weight = []

    # filename = 'nsfnet.txt'
    # filename = 'usbnet.txt'
    with open(filename) as f:
        data = f.readlines()
        for n, line in enumerate(data, 1):

            switch_pairs_weight.append([int(x) for x in line.split(',')])
    # print switch_pairs_weight

    for pair in switch_pairs_weight:
        # print pair
        slots_list = total_slots * [0]
        flows = []
        graph.add_edge(pair[0], pair[1], weight=pair[2], spectrum_slots=slots_list, flows=flows)
        graph.add_edge(pair[1], pair[0], weight=pair[2], spectrum_slots=slots_list, flows=flows)
    print graph.edges(data=True)
    return graph


def get_graph_test():
    switch_pairs = {(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 3), (2, 4), (2, 5), (2, 6),
                    (3, 4), (3, 5), (3, 6), (4, 5), (4, 6), (5, 6)}
    for pair in switch_pairs:
        flows = []
        slots_list = total_slots * [0]
        graph.add_edge(pair[0], pair[1], weight=1, spectrum_slots=slots_list, flows=flows)
        graph.add_edge(pair[1], pair[0], weight=1, spectrum_slots=slots_list, flows=flows)
    print graph.edges(data=True)
    return graph


def get_disjoint_test():
    switch_pairs = {(1, 2, 1), (1, 3, 2), (2, 4, 1), (3, 4, 2), (4, 5, 1), (5, 6, 2), (2, 6, 2)}

    for pair in switch_pairs:
        flows = []
        slots_list = total_slots * [0]
        graph.add_edge(pair[0], pair[1], weight=pair[2], spectrum_slots=slots_list, flows=flows)
        graph.add_edge(pair[1], pair[0], weight=pair[2], spectrum_slots=slots_list, flows=flows)
    print graph.edges(data=True)

    shortest_paths = path_computing(graph, 2, 5, k=1)
    shortest_paths.sort(key=len)
    print "the result of disjoint paths for src %s and dst %s:" % (2, 5),
    print shortest_paths
    return graph

# get_disjoint_test()

