import networkx as nx

graph = nx.DiGraph()  # create graph
total_slots = 300


def get_graph(filename):
    """
        Get the adjacency matrix from link_to_port
    """
    # switch_pairs_weight = {(1, 2, 1), (1, 3, 1), (2, 3, 1), (2, 4, 1), (3, 4, 1), (3, 5, 1), (4, 5, 1), (4, 6, 1),
    #                 (5, 6, 1)}  # the connected switches pair
    switch_pairs_weight = []

    with open(filename) as f:
        data = f.readlines()
        for n, line in enumerate(data, 1):
            switch_pairs_weight.append([int(x) for x in line.split(',')])
    # print switch_pairs_weight

    for pair in switch_pairs_weight:
        print pair
        slots_list = total_slots * [0]
        graph.add_edge(pair[0], pair[1], weight=pair[2], spectrum_slots=slots_list)
        graph.add_edge(pair[1], pair[0], weight=pair[2], spectrum_slots=slots_list)
    # print graph.edges(data=True)
    return graph


def get_graph_test():
    switch_pairs = {(1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (3, 5), (4, 5), (4, 6),
                    (5, 6)}  # the connected switches pair
    for pair in switch_pairs:
        slots_list = total_slots * [0]
        graph.add_edge(pair[0], pair[1], weight=1, spectrum_slots=slots_list)
        graph.add_edge(pair[1], pair[0], weight=1, spectrum_slots=slots_list)
    # print graph.edges(data=True)
    return graph