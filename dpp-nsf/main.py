import networkx as nx
from TopologyManager import get_graph, get_graph_test
from simulation import Simulation
from algorithm import algorithm


def main(arrive_rate):
    total_time = 200
    reciprocal_lambda = 0.1
    max_bandwidth = 800
    min_bandwidth = 10
    ave_block_rate = 0
    ave_spec_utilization = 0
    ave_fragmentation_rate = 0
    times = 5
    for i in range(times):
        print "1: create graph"
        # graph = get_graph_test()
        filename = 'nsfnet.txt'
        # filename = 'usbnet.txt'
        graph = get_graph(filename)

        print "2: begin simulation"
        sim = Simulation(algorithm, graph, total_time, arrive_rate, reciprocal_lambda, min_bandwidth,max_bandwidth)
        block_rate, spectrum_utilization, fragmentation_rate = sim.run()
        print block_rate, spectrum_utilization, fragmentation_rate
        ave_block_rate = ave_block_rate + block_rate
        ave_spec_utilization = ave_spec_utilization + spectrum_utilization
        ave_fragmentation_rate = ave_fragmentation_rate + fragmentation_rate

    ave_block_rate = ave_block_rate/times
    ave_spec_utilization = ave_spec_utilization/times
    ave_fragmentation_rate = ave_fragmentation_rate/times

    with open("dpp_nsf_800.txt", "a") as f:
        f.write(str(ave_block_rate) + ',' + str(ave_spec_utilization) + ',' + str(ave_fragmentation_rate) + '\n')


if __name__ == "__main__":
    open('dpp_nsf_800.txt', 'w').close()
    for arrive_rate in xrange(1, 61, 2):
        main(arrive_rate)