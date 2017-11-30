import math
import copy

uni_slot_size = 12.5  # the size of uni slot(GHz)


def routing_and_spectrum(graph, paths, required_bandwidth, threshold):
    metrics, sorted_paths = sort_all_k_shortest_paths(paths, graph)
    print "sorted metrics and paths ",
    print metrics, sorted_paths

    central_frequency_list = []
    paths_occupied_spectrum = []
    working_path = None

    for path in sorted_paths:
        m = get_modulation(path, graph)
        # print "modulation %d" % m
        slots_num = get_slots_num(required_bandwidth, m)
        # print "the number of required slots is %s" % slots_num

        central_frequency, start_localization = assign_spectrum(graph, path, slots_num)
        # print "central frequency %s" % central_frequency
        sorted_paths.remove(path)
        if central_frequency is None:
            continue
        else:
            working_path = path
            working_path_occupied_spectrum = (working_path, start_localization, slots_num)
            paths_occupied_spectrum.append(working_path_occupied_spectrum)
            central_frequency_list.append(central_frequency)
            break
    if working_path is None:
        return None

    _graph = copy.deepcopy(graph)
    inter_graph = modify_backup_path(_graph, working_path)
    backup_paths_occupied_spectrum = []
    if len(sorted_paths) == 1 or required_bandwidth < threshold:
        for path in sorted_paths:
            m = get_modulation(path, graph)
            # print "modulation %d" % m
            slots_num = get_slots_num(required_bandwidth, m)
            # print "the number of required slots is %s" % slots_num

            central_frequency, start_localization = assign_spectrum(inter_graph, path, slots_num, backup=True)
            if central_frequency is None:
                continue
            else:
                backup_path_occupied_spectrum = (path, start_localization, slots_num)
                backup_paths_occupied_spectrum.append(backup_path_occupied_spectrum)
                central_frequency_list.append(central_frequency)
                if len(backup_paths_occupied_spectrum) == 1:
                    break
        print "111111111111111111111111111"
        print backup_paths_occupied_spectrum
    else:
        for path in sorted_paths:
            m = get_modulation(path, graph)
            # print "modulation %d" % m
            slots_num = get_slots_num(required_bandwidth/2, m)
            # print "the slots for the backup %s" % slots_num

            central_frequency, start_localization = assign_spectrum(inter_graph, path, slots_num, backup=True)
            # print "central frequency %s" % central_frequency

            if central_frequency is None:
                continue
            else:
                backup_path_occupied_spectrum = (path, start_localization, slots_num)
                backup_paths_occupied_spectrum.append(backup_path_occupied_spectrum)
                central_frequency_list.append(central_frequency)
                if len(backup_paths_occupied_spectrum) == 2:
                    break

        print "2222222222222222222222222222"
        print backup_paths_occupied_spectrum

        if len(backup_paths_occupied_spectrum) == 1:
            print "3333333333333333333333333333"
            backup_paths_occupied_spectrum = []
            for path in sorted_paths:
                m = get_modulation(path, graph)
                # print "modulation %d" % m
                slots_num = get_slots_num(required_bandwidth, m)
                # print "the number of required slots is %s" % slots_num

                central_frequency, start_localization = assign_spectrum(inter_graph, path, slots_num, backup=True)
                if central_frequency is None:
                    continue
                else:
                    backup_path_occupied_spectrum = (path, start_localization, slots_num)
                    backup_paths_occupied_spectrum.append(backup_path_occupied_spectrum)
                    central_frequency_list.append(central_frequency)
                    if len(backup_paths_occupied_spectrum) == 1:
                        print backup_paths_occupied_spectrum
                        break

    if backup_paths_occupied_spectrum:
        for backup_path_occupied_spectrum in backup_paths_occupied_spectrum:
            paths_occupied_spectrum.append(backup_path_occupied_spectrum)

    if len(paths_occupied_spectrum) < 2:
        print "the number of routing path is %d" % len(paths_occupied_spectrum)
        return None

    set_links_slots(paths_occupied_spectrum, graph)
    return paths_occupied_spectrum


def modify_backup_path(graph, working_path):
    for i in range(len(working_path) - 1):
        if graph[working_path[i]][working_path[i+1]].get('flows'):
            flows = graph[working_path[i]][working_path[i+1]]['flows']
            for flow in flows:
                paths_occupied_spectrum = flow.paths[1:]
                for path_occupied_spectrum in paths_occupied_spectrum:
                    path = path_occupied_spectrum[0]
                    loc = path_occupied_spectrum[1]
                    slots_num = path_occupied_spectrum[2]
                    for j in range(len(path) - 1):
                        for n in range(slots_num):
                            graph[path[j]][path[j+1]]['spectrum_slots'][loc + n] = 1
    return graph


def get_modulation(path, graph):
    # M is 1, 2, 3 and 4 for BPSK, QPSK, 8-QAM and 16-QAM
    # BPSK, QPSK, 8 - QAM, and 16 - QAM signals transmission reach: 9600km, 4800km, 2400km, and 1200km,
    sum_distance = 0

    for i in range(len(path)-1):
        sum_distance = sum_distance + graph[path[i]][path[i+1]]['weight']

    if sum_distance <= 1200:
        m = 4
    elif sum_distance <= 2400:
        m = 3
    elif sum_distance <= 4800:
        m = 2
    else:
        m = 1
    return m


def get_slots_num(required_bandwidth, m):
    """
        Calculate the number of slots for required bandwidth
        the guard band is 1.
    """
    slots_num = math.ceil(required_bandwidth / (m * uni_slot_size)) + 1
    return int(slots_num)


def allocate_slots_for_backup_paths(slots_num):
    total_slot = slots_num - 1
    # print math.ceil(total_slot / 2.0)
    sub_1 = int(math.ceil(total_slot/2.0))
    sub_2 = int(total_slot - sub_1)
    return [sub_1 + 1, sub_2 + 1]


def assign_spectrum(graph, path, slots_num, backup=False):
    path_slots_list = get_spectrum_slots_list(path, graph)

    if backup:
        slot_list = [sum([1 for _ in x if _ == 1]) for x in zip(*path_slots_list)]
        # print "aaaaaaaaaaaa"
        # print slot_list
    else:
        slot_list = [sum(x) for x in zip(*path_slots_list)]

    continous_slots = 0
    localization = 0
    for slot in slot_list:
        localization = localization + 1
        if slot == 0:
            continous_slots = continous_slots + 1
            if continous_slots == slots_num:
                break
        else:
            continous_slots = 0
    if continous_slots != slots_num:
        return None, None

    start_localization = localization - slots_num

    central_frequency = get_central_frequency(start_localization, slots_num)

    return central_frequency, start_localization


def get_central_frequency(localization, slots_num):
    return 193.11 + (localization + slots_num) * 6.25


def set_links_slots(paths_occupied_spectrum, graph):
    backup = False
    for path, localization, slots_num in paths_occupied_spectrum:
        hops = len(path)
        for n in range(slots_num):
            for i in range(hops - 1):
                if backup:
                    if graph[path[i]][path[i + 1]]['spectrum_slots'][localization + n] == 0:
                        graph[path[i]][path[i + 1]]['spectrum_slots'][localization + n] = 2
                    else:
                        graph[path[i]][path[i + 1]]['spectrum_slots'][localization + n] = graph[path[i]][path[i + 1]]['spectrum_slots'][localization + n] + 1
                else:
                    graph[path[i]][path[i + 1]]['spectrum_slots'][localization + n] = 1
        backup = True


def sort_all_k_shortest_paths(shortest_paths, graph):
    """
        Sort k paths
    """
    # print "4.1: sort the shortest path through the metric"
    sorted_metric_paths = []
    sorted_shortest_paths = []
    metrics = []
    for path in shortest_paths:
        metric = get_metric(path, graph)
        metric_path = (metric, path)
        sorted_metric_paths.append(metric_path)
    sorted_metric_paths.sort(key=lambda x: x[0], reverse=True)
    for metric, path in sorted_metric_paths:
        sorted_shortest_paths.append(metric)
        metrics.append(path)
    return sorted_shortest_paths, metrics


def get_metric(path, graph):
    hops = len(path)
    m = get_modulation(path, graph)
    # print("hops %s" %hops)
    free_spectrum = 0
    path_slots_list = get_spectrum_slots_list(path, graph)
    for slots_of_edge in path_slots_list:

        free_spectrum += len(slots_of_edge) - sum([1 for _ in slots_of_edge if _ != 0])

    if free_spectrum is not None:
        return (free_spectrum * m/(hops - 1))
    else:
        print "No free spectrum"


def get_spectrum_slots_list(path, graph):
    path_slots_list = []
    for i in range(len(path) - 1):
        path_slots_list.append(graph[path[i]][path[i+1]]['spectrum_slots'])
    return path_slots_list

