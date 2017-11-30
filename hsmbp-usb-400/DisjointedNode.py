import copy
import networkx as nx

"""
Suurballe's algorithm 
"""


def path_computing(graph, src, dst, k):
    _graph = copy.deepcopy(graph)
    shortest_paths = link_disjoint_paths(_graph, src, dst, k)
    return shortest_paths


def link_disjoint_paths(graph, src, dst, k):
    new_graph = copy.deepcopy(graph)
    shortest_path = nx.dijkstra_path(graph, src, dst, 'weight')
    all_shortest_paths = nx.single_source_dijkstra_path(graph, src, 'weight')
    nodes = nx.nodes(graph)
    tree_edges = get_tree_edge(nodes, all_shortest_paths)

    shortest_paths_list = [shortest_path]

    for edge in graph.edges():

        d_src_start = get_weight_sum(graph, edge[0], all_shortest_paths)
        d_src_end = get_weight_sum(graph, edge[1], all_shortest_paths)
        new_graph[edge[0]][edge[1]]['weight'] = graph[edge[0]][edge[1]]['weight'] - d_src_end + d_src_start

    # print "the old weight %s" % graph.edges(data=True)
    # print "the new weight %s" % new_graph.edges(data=True)

    for i in range(k):
        # print "create residual graph"
        residual_graph = create_residual_graph(new_graph, shortest_path)
        # print "residual_graph edges"
        # print residual_graph.edges(data=True)
        try:
            another_shortest_path = nx.dijkstra_path(residual_graph, src, dst, 'weight')
        except nx.NetworkXNoPath:
            print "node %s not reachable from %s" % (src, dst)
            break
        # print "the second shortest path %s" % another_shortest_path
        shortest_paths_list.append(another_shortest_path)
        shortest_path = another_shortest_path

    subgraph = get_subgraph(shortest_paths_list)
    # print subgraph.edges(), src, dst

    generator = nx.all_simple_paths(subgraph, src, dst, 'weight')
    found_paths = []
    generate_paths = []
    for path in generator:
        generate_paths.append(path)
        if check_disjoint(path, found_paths):
            found_paths.append(path)

    # print "the generate path %s" % generate_paths
    # print "the found disjoint path %s" % found_paths
    return found_paths


def check_disjoint(path, found_paths):
    edges = get_edges_of_path(path)
    for found_path in found_paths:
        edges_found_path = get_edges_of_path(found_path)
        for edge in edges:
            for edge_found_path in edges_found_path:
                if edge == edge_found_path:
                    return False
    return True


def get_tree_edge(nodes, all_shortest_paths):
    tree_edges = set()
    for node in nodes:
        path = all_shortest_paths[node]
        for i in range(len(path)-1):
            tree_edges.add((path[i], path[i+1]))
    return tree_edges


def get_weight_sum(graph, node, all_shortest_paths):
    path = all_shortest_paths[node]
    sum = 0
    for i in range(len(path) - 1):
        sum = sum + graph[path[i]][path[i + 1]]['weight']
    return sum


def create_residual_graph(graph, path):
    reverse_edges = get_reverse_edges_of_path(path)
    for edge in reverse_edges:
        if graph.has_edge(edge[0], edge[1]):
            graph.remove_edge(edge[0], edge[1])

    edges = get_edges_of_path(path)
    # print edges
    for edge in edges:
        graph.remove_edge(edge[0], edge[1])
        graph.add_edge(edge[1], edge[0], weight=0)
    return graph


def get_edges_of_path(path):
    edges = []
    for i in range(len(path)-1):
        edges.append((path[i], path[i+1]))
    return edges


def get_reverse_edges_of_path(path):
    edges = []
    for i in range(len(path) - 1):
        edges.append((path[i+1], path[i]))
    return edges


def get_subgraph(paths):
    subgraph = nx.DiGraph()
    overlapping_links = set()
    edges_of_paths = []
    for path in paths:
        edges = get_edges_of_path(path)
        edges_of_paths = edges_of_paths + edges

    for edge in edges_of_paths:
        subgraph.add_edge(edge[0], edge[1], weight=1)
        if subgraph.has_edge(edge[1], edge[0]):
            overlapping_links.add((edge[1], edge[0]))
            overlapping_links.add((edge[0], edge[1]))

    for edge in overlapping_links:
        # print edge[0], edge[1]
        subgraph.remove_edge(edge[0], edge[1])

    return subgraph
