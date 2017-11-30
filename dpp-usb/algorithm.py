from DisjointedNode import path_computing
from SpectrumAssign import routing_and_spectrum
import networkx as nx


def algorithm(graph, flow):
    src = flow.src_num
    dst = flow.dst_num
    required_bandwidth = flow.bandwidth

    print "3: path computing"
    shortest_paths = path_computing(graph, src, dst, k=4)
    shortest_paths.sort(key=len)
    # print "the result of disjoint paths for src %s and dst %s:" % (src, dst),
    print shortest_paths

    print "4: spectrum assigning"
    paths_occupied_spectrum = routing_and_spectrum(graph, shortest_paths, required_bandwidth)
    # print "all routing path and occupied slots %s" % paths_occupied_spectrum
    # print "the graph after the spectrum assignment %s" % graph.edges(data=True)

    return paths_occupied_spectrum

