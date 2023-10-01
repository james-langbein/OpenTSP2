def find_hamiltonians_template():
    # nodes = ['A', 'B', 'C', 'D']
    # edges = ['AB', 'BA', 'BC', 'CB', 'BD', 'DB', 'CD', 'DC', 'DA', 'AD']
    nodes = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    edges = ['AB', 'BA', 'BC', 'CB', 'CE', 'EC', 'CD', 'DC', 'EF', 'FE', 'ED', 'DE', 'DF', 'FD', 'FG', 'GF', 'GA', 'AG']
    # list below is missing edge required to make full hamiltonian circuits, use for testing
    # edges = ['AB', 'BA', 'BC', 'CB', 'CE', 'EC', 'CD', 'DC', 'EF', 'FE', 'DF', 'FD', 'FG', 'GF', 'GA', 'AG']

    paths = []
    extended_paths = []
    hamiltonians = []

    more_hamiltonians = True
    first_node = edges[0][0]
    paths.append(first_node)

    path_extensions = [edge for edge in edges if edge[0] == paths[-1]]
    for edge in path_extensions:
        extended_paths.append([first_node, edge[1]])

    while more_hamiltonians:
        paths, extended_paths = extended_paths, []
        # check for infinite loop where there are no hamiltonian circuits present, hence no paths to extend further
        # in this case, paths will be empty after assignment above
        if len(paths) == 0:
            print('No Hamiltonian circuits present.')
            break
        # for each current path that is being extended, find all extension edges and check suitability
        for path in paths:
            # find all edges that extend the current path
            path_extensions = [edge for edge in edges if edge[0] == path[-1]]
            for edge in path_extensions:
                # circuit completed, but not a full circuit, dead end
                # or a short-circuit, i.e. the extension node is already in the path
                if len(path) < len(nodes) and edge[1] in path:
                    continue  # do nothing, don't want to continue with these paths
                # circuit not completed yet, and no short-circuits, add to paths we want to continue with
                elif len(path) < len(nodes) and edge[1] not in path:
                    path_copy = path[:]
                    path_copy.append(edge[1])
                    extended_paths.append(path_copy)
                # circuit completed and is a Hamiltonian circuit
                # also an implicit denial elif for the case where the extension node is in the path but != first_node
                elif len(path) == len(nodes) and edge[1] == path[0]:
                    path_copy = path[:]
                    path_copy.append(edge[1])
                    hamiltonians.append(path_copy)
        all_hamiltonians_check = [True for path in hamiltonians if len(path) > 2 and path[0] == path[-1]]
        if all_hamiltonians_check:
            more_hamiltonians = False

    # next step is to remove mirror-image circuits
    for circuit in hamiltonians:
        other_circuits = [path for path in hamiltonians if path != circuit]
        for other_circuit in other_circuits:
            flipped = other_circuit[::-1]
            if flipped in hamiltonians:
                hamiltonians.remove(other_circuit)

    if len(hamiltonians) > 0:
        print(hamiltonians)


if __name__ == '__main__':
    find_hamiltonians_template()
