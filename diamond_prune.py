from objects import Generator, Node, Edge
from helpers import angle, inner_soddy_center2
from matplotlib import path, pyplot as plt
from collections import deque
from math import ceil
from itertools import islice


def dp_v6(instance, show_work=True):
    """
    Diamond Prune V6
    Given an instance, it runs the dp_v6 algorithm to assign a fitness to the edges.
    This version will take easy route in terms of curvy solution boundaries, and make the 'safe' zone inside
    the potential curves (I'm pretty sure the curves go out from the ISC, not in).
    """
    # instance = Generator.new_instance(4, relative_edges=True)
    if show_work:
        _xs, _ys = [instance.x_values], [instance.y_values]
        plt.xlim(left=0, right=100)
        plt.ylim(bottom=0, top=100)
        plt.scatter(_xs, _ys, color='blue')
        plt.show()
        plt.clf()

    # populate the edge angles
    for edge in instance.edges.values():
        edge.angle = angle(edge.node_one, instance.average_node, edge.node_two)

    # populate the edge lengths (should change this behaviour at some point)
    for edge in instance.edges.values():
        temp = edge.length_  # edge lengths weren't being calculated, need this to force calc

    # for each node, prune the edges for which it is the origin
    for node in instance.nodes.values():

        # get all edges where this node is the origin
        edges_from = [_edge for _edge in instance.edges.values() if _edge.node_one == node]
        # sort the edges by angle > -180 to +180
        edges_from.sort(key=lambda x: x.angle)

        if show_work:
            _xs, _ys = [instance.x_values], [instance.y_values]
            curr_node_x, curr_node_y = node.x, node.y
            plt.xlim(left=0, right=100)
            plt.ylim(bottom=0, top=100)
            plt.scatter(_xs, _ys, color='blue')
            plt.scatter(curr_node_x, curr_node_y, color='red')
            for _edge in edges_from:
                _edge.plot()
            plt.show()
            plt.clf()

        # print(edges_from)

        # prune the list, using a 'sliding window' over ordered triples of edges
        # define the current index 0 for the window, and the stop condition
        # the implementation below will be a naive version for the sliding window
        start_index = 0
        _continue = True
        # while _continue, iterate the windows and mark edges as applicable
        while _continue:
            # get the current ordered triple, t is short for triple to make lines shorter
            t = edges_from[start_index:start_index+3]

            # print the current node and edges being considered
            if show_work:
                _xs, _ys = [instance.x_values], [instance.y_values]
                curr_node_x, curr_node_y = node.x, node.y
                plt.xlim(left=0, right=100)
                plt.ylim(bottom=0, top=100)
                plt.scatter(_xs, _ys, color='blue')
                plt.scatter(curr_node_x, curr_node_y, color='red')
                for _edge in t:
                    _edge.plot(color='red')
                plt.clf()

            # (fast exit check) if the middle edge is longer than the outer two then mark as bad
            if t[1].length > t[0].length and t[1].length > t[2].length:
                t[1].fitness = 'bad'
            # else check if the middle edge's endpoint is a member of the 'good' zone
            else:
                # find the Inner Soddy Center
                isc = inner_soddy_center2(t[1].node_one, t[0].node_two, t[2].node_two)
                # define the 'good zone'
                p = [(t[1].node_one.x, t[1].node_one.y)
                     , (t[0].node_two.x, t[0].node_two.y)
                     , isc
                     , (t[2].node_two.x, t[2].node_two.y)
                     , (t[1].node_one.x, t[1].node_one.y)]
                good_zone = path.Path(p)
                # check if middle edge endpoint is in the 'good zone'
                if good_zone.contains_point(t[1].node_two):
                    # technically unnecessary as edges are good by default, but will keep for clarity
                    t[1].fitness = 'good'
                else:
                    # not in 'good zone', mark as bad
                    t[1].fitness = 'bad'
            # check for current position of window, if start index is 3rd edge from left, then exit
            # (might be able to mark last edge as bad if second-to-last edge is good, opposite would be true
            #  for marking first edge as bad if second edge is good)
            if start_index == len(edges_from)-3:
                _continue = False

            # increase the start_index value
            start_index += 1


def dp_v7(instance, max_angle=180, show_work=False):
    """
    Diamond Prune V7
    Given an instance, it runs the dp_v6 algorithm to assign a fitness to the edges.
    This version will take easy route in terms of curvy solution boundaries, and make the 'safe' zone inside
    the potential curves (I'm pretty sure the curves go out from the ISC, not in).
    In this version I'm also trying to implement a non-naive version of the sliding window for pruning. I'll also not be
    limiting triples to the ordered range -180 to +180, I'll consider all triples as long as the two outer edges are
    within 180 degrees.
    """
    _xs, _ys = [instance.x_values], [instance.y_values]
    plt.xlim(left=0, right=100)
    plt.ylim(bottom=0, top=100)

    # define minimum possible number of edges from node after pruning
    # minimum possible number is related to 360/max_angle
    # so for instance, if max_angle is 120 then the minimum number of edges is 360/120 = 3
    # if fraction result is decimal then round up
    min_queue_count = ceil(360/max_angle)

    if show_work:
        plt.xlim(left=0, right=100)
        plt.ylim(bottom=0, top=100)
        plt.scatter(_xs, _ys, color='blue')
        plt.show()
        plt.clf()

    # populate the edge angles
    for edge in instance.edges.values():
        edge.angle = angle(edge.node_one, instance.average_node, edge.node_two)

    # populate the edge lengths (should change this behaviour at some point)
    for edge in instance.edges.values():
        temp = edge.length_  # edge lengths weren't being calculated, need this to force calc

    # for each node, prune the edges for which it is the origin
    for node in instance.nodes.values():
        curr_node_x, curr_node_y = node.x, node.y  # for plotting

        # get all edges where this node is the origin
        edges_from = [_edge for _edge in instance.edges.values() if _edge.node_one == node]
        # sort the edges by angle > -180 to +180
        edges_from.sort(key=lambda x: x.angle)
        # create a deque (specifically for rotation behaviour, and this is like a 'deepcopy' so modifications don't
        # affect edges_from)
        dq_edges_from = deque(edges_from)

        if show_work:
            # show all edges from current node
            plt.scatter(_xs, _ys, color='blue')
            plt.scatter(curr_node_x, curr_node_y, color='red')
            for _edge in dq_edges_from:
                _edge.plot()
            plt.show()
            plt.clf()

        # prune the list, using a 'sliding window' over ordered triples of edges
        _continue = True
        # while _continue, iterate the windows and mark edges as applicable
        while _continue:
            # get the current ordered triple, t is short for triple
            t = list(islice(dq_edges_from, 0, 3))
            # t = dq_edges_from[0:3]

            if show_work:
                # show currently considered triple
                plt.scatter(_xs, _ys, color='blue')
                plt.scatter(curr_node_x, curr_node_y, color='red')
                for _edge in t:
                    _edge.plot(color='red')
                plt.show()
                plt.clf()

            # (fast exit check) if the middle edge is longer than the outer two then mark as bad
            if t[1].length > t[0].length and t[1].length > t[2].length:
                t[1].fitness = 'bad'
                dq_edges_from.remove(t[1])
            else:
                # check if outer angle less than max angle, check middle edge suitability if so
                if max([t[0].angle, t[2].angle]) - min([t[0].angle, t[2].angle]) < max_angle:
                    # find the Inner Soddy Center
                    isc = inner_soddy_center2(t[1].node_one, t[0].node_two, t[2].node_two)
                    # define the 'good zone'
                    p = [(t[1].node_one.x, t[1].node_one.y)
                         , (t[0].node_two.x, t[0].node_two.y)
                         , isc
                         , (t[2].node_two.x, t[2].node_two.y)
                         , (t[1].node_one.x, t[1].node_one.y)]
                    good_zone = path.Path(p)

                    if show_work:
                        # show good zone and considered edges
                        plt.scatter(_xs, _ys, color='blue')
                        plt.scatter(curr_node_x, curr_node_y, color='red')
                        for _edge in t:
                            _edge.plot(color='red')
                        plt.show()
                        plt.clf()

                    # check if middle edge endpoint is in the 'good zone'
                    # edge either marked good or it is deleted from dq_edges_from
                    if good_zone.contains_point(t[1].node_two):
                        # edge currently good, keep it
                        t[1].fitness = 'good'  # technically not needed but keeping for clarity
                        # rotate dq_edges_from by 1 to the left to get next triple in order on next loop
                        dq_edges_from.rotate(-1)
                    else:
                        # edge not good, remove
                        t[1].fitness = 'bad'  # technically not needed but keeping for clarity also
                        dq_edges_from.remove(t[1])
                        # the same index can then be used again to check the next triple from the same start point
                else:  # gap more than 180 degrees, so we need to consider next triple
                    # gap > max angle, so rotate list by one to the right to consider next triple
                    dq_edges_from.rotate(1)

            # check number of elements left in dq_edges_from, if equal to minimum possible number, then exit
            if len(dq_edges_from) == min_queue_count:
                _continue = False

    # print('Show good edges here.')
    if show_work:
        # show currently considered triple
        plt.scatter(_xs, _ys, color='blue')
        for _edge in instance:
            if _edge.fitness == 'good':
                _edge.plot(color='red')
        plt.show()
        plt.clf()


def dp_v8(instance, max_angle=180, show_work=False):
    """
    Diamond Prune V8

    Given an instance, it runs the dp_v8 algorithm to prune unfit edges.
    In this version I'll limit the ordered triples to the range -180 to +180 and won't wrap around as in V7.
    I'm still not sure about the minimum queue count, need to run in debug mode and fully check the behaviour.
    """

    _xs, _ys = [instance.x_values], [instance.y_values]
    plt.xlim(left=0, right=100)
    plt.ylim(bottom=0, top=100)

    # define minimum possible number of edges from node after pruning
    # minimum possible number is related to 360/max_angle
    # so for instance, if max_angle is 120 then the minimum number of edges is 360/120 = 3
    # if fraction result is decimal then round up
    min_queue_count = ceil(360 / max_angle)

    if show_work:
        plt.xlim(left=0, right=100)
        plt.ylim(bottom=0, top=100)
        plt.scatter(_xs, _ys, color='blue')
        plt.show()
        plt.clf()

    # populate the edge angles
    for edge in instance.edges.values():
        edge.angle = angle(edge.node_one, instance.average_node, edge.node_two)

    # populate the edge lengths (should change this behaviour at some point)
    for edge in instance.edges.values():
        temp = edge.length_  # edge lengths weren't being calculated, need this to force calc

    # for each node, prune the edges for which it is the origin
    for node in instance.nodes.values():
        curr_node_x, curr_node_y = node.x, node.y  # for plotting

        # get all edges where this node is the origin
        edges_from = [_edge for _edge in instance.edges.values() if _edge.node_one == node]
        # sort the edges by angle > -180 to +180
        edges_from.sort(key=lambda x: x.angle)

        if show_work:
            # show all edges from current node
            plt.scatter(_xs, _ys, color='blue')
            plt.scatter(curr_node_x, curr_node_y, color='red')
            for _edge in edges_from:
                _edge.plot()
            plt.show()
            plt.clf()

        # prune the list, using a 'sliding window' over ordered triples of edges
        _continue = True
        start = 0
        # while _continue, iterate the windows and mark edges as applicable
        while _continue:
            # if end_index goes past end of edge list, break
            # this implicitly breaks when there are only 2 edges remaining
            # if start+3 > len(edges_from):
            #     break

            # get the current ordered triple, t is short for triple
            t = edges_from[start:start+3]

            if show_work:
                print(f'Total angle: {t[2].angle - t[0].angle}')
                # show currently considered triple
                plt.scatter(_xs, _ys, color='blue')
                plt.scatter(curr_node_x, curr_node_y, color='red')
                for _edge in t:
                    _edge.plot(color='red')
                plt.show()
                plt.clf()

            # (fast exit check) if the middle edge is longer than the outer two then mark as bad
            if t[1].length > t[0].length and t[1].length > t[2].length:
                # edge bad so remove it and maintain index to get 'next' triple
                t[1].fitness = 'bad'
                edges_from.remove(t[1])
            else:
                if show_work:
                    print(f'Angles: 0 > {t[0].angle}, 1 > {t[1].angle}, 2 > {t[2].angle}')
                # check if outer angle less than max angle, check middle edge suitability if so
                if max([t[0].angle, t[2].angle]) - min([t[0].angle, t[2].angle]) < max_angle:
                    # find the Inner Soddy Center
                    isc = inner_soddy_center2(t[1].node_one, t[0].node_two, t[2].node_two)
                    # define the 'good zone'
                    p = [(t[1].node_one.x, t[1].node_one.y)
                         , (t[0].node_two.x, t[0].node_two.y)
                         , isc
                         , (t[2].node_two.x, t[2].node_two.y)
                         , (t[1].node_one.x, t[1].node_one.y)]
                    good_zone = path.Path(p)

                    if show_work:
                        edge_one = Edge(t[0].node_one, t[0].node_two)
                        edge_two = Edge(t[0].node_two, Node(isc[0], isc[1]))
                        edge_three = Edge(Node(isc[0], isc[1]), t[2].node_two)
                        edge_four = Edge(t[2].node_two, t[2].node_one)
                        good_zone_edges = [edge_one, edge_two, edge_three, edge_four]
                        # show good zone and considered edges
                        plt.scatter(_xs, _ys, color='blue')
                        plt.scatter(curr_node_x, curr_node_y, color='red')
                        for _edge in t:
                            _edge.plot(color='black', edge_width=1, zorder=1)
                        for _edge in good_zone_edges:
                            _edge.plot(color='green', edge_width=1, zorder=2)
                        for _edge in instance.solution.edges:
                            _edge.plot(color='magenta', edge_width=4, zorder=-2)
                        plt.show()
                        plt.clf()

                    # check if middle edge endpoint is in the 'good zone'
                    # edge either marked good or it is deleted from edges_from
                    if good_zone.contains_point(t[1].node_two):
                        # edge currently good, keep it, and move triple one index forwards
                        t[1].fitness = 'good'  # technically not needed but keeping for clarity
                        start += 1
                    else:
                        # edge not good, remove
                        t[1].fitness = 'bad'  # technically not needed but keeping for clarity also
                        edges_from.remove(t[1])
                        # the same index can then be used again to check the next triple from the same start point
                # gap more than max angle, so we need to consider next triple
                else:
                    start += 1
            if start+3 > len(edges_from):
                break


def test_dp_v8():
    # generate an instance
    inst = Generator.new_instance(9, relative_edges=True, solve=True)

    # run dp on the instance
    dp_v8(inst, max_angle=150, show_work=False)

    # plot the results
    xs = [inst.x_values]
    ys = [inst.y_values]
    plt.xlim(left=0, right=100)
    plt.ylim(bottom=0, top=100)
    plt.scatter(xs, ys, color='blue')
    for _edge in inst.edges.values():
        if _edge.fitness == 'good':
            _edge.plot(color='blue', edge_width=1, zorder=-1)
    for _edge in inst.solution.edges:
        _edge.plot(color='magenta', edge_width=4, zorder=-2)
    plt.show()


if __name__ == '__main__':
    test_dp_v8()
