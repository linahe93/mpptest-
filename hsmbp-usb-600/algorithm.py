from DisjointedNode import path_computing
from SpectrumAssign import routing_and_spectrum
import networkx as nx


def algorithm(graph, flow, threshold):
    src = flow.src_num
    dst = flow.dst_num
    required_bandwidth = flow.bandwidth

    print "3: path computing"
    shortest_paths = path_computing(graph, src, dst, k=4)
    shortest_paths.sort(key=len)
    print "the result of disjoint paths for src %s and dst %s:" % (src, dst),
    print shortest_paths

    print "4: spectrum assigning"
    paths_occupied_spectrum = routing_and_spectrum(graph, shortest_paths, required_bandwidth, threshold)
    print "all routing path and occupied slots %s" % paths_occupied_spectrum

    if paths_occupied_spectrum is not None:
        flow.paths = paths_occupied_spectrum
        working_path = paths_occupied_spectrum[0][0]
        for i in range(len(working_path) - 1):
            graph[working_path[i]][working_path[i+1]]['flows'].append(flow)
            # print "add flow to working path",
            # print graph[working_path[i]][working_path[i+1]]['flows']

    # print "the graph after the spectrum assignment:"
    # print graph.edges(data=True)
    return paths_occupied_spectrum

