from objects import *
import numpy as np


def get_stats(num_tests, n):
    """From Obsidian:
    One thing that would be interesting is to experiment on solved instances and find the statistical upper bound
    for edge lengths in comparison to eccentricity.
    This is a good test in the sense that eccentricity is predicated on the edge length range in a problem.
    I need to map the eccentricity range to 0-100 to represent percentages of eccentricity, and then track the upper
    bound against percentiles.
    My hypothesis is that the upper bound will follow a curve, and that the shape of the curve will be different
    depending on the amount of nodes in a problem.
    A nice thing to track would actually be the full range of values for each percentile, graphing the density of values
    by opacity of colour in the range.
    The eccentricity percentile should go on the *x* axis, and the edge length percentage of max on the *y* axis."""
    stats_arr = np.zeros(100)

    for test in range(num_tests):
        inst = Generator.new_instance(n)
        inst.solve()
        max_edge_length = max(inst.n_edge_lengths(all_lengths=True))

        for key, node in enumerate(inst.nodes.values()):
            node.eccentricity = max([edge.length for edge in inst.edges_from_node(node=key+1).values()])

        pass


if __name__ == '__main__':
    get_stats(1000, n=4)
