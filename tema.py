import sys


def extract_input_line():
    return map(int, sys.stdin.readline().strip().split())


def print_array(array):
    for elem in array:
        sys.stdout.write(f"{elem}\n")


def transpose_graph(neighbours):
    new_neighbours = [[] for _ in range(len(neighbours))]

    for i, neigh_list in enumerate(neighbours):
        for neigh in neigh_list:
            new_neighbours[neigh].append(i)

    return new_neighbours


def get_dfs_reachable_states(graph_neighbours, starting_states):
    visited = {state: True for state in starting_states}

    stack = starting_states
    while len(stack) != 0:
        top = stack.pop()

        for neigh in graph_neighbours[top]:
            if neigh not in visited:
                stack.append(neigh)
                visited[neigh] = True

    return [key for key in visited]


def solve_accessible(neighbours, starting_states):
    print_array(get_dfs_reachable_states(neighbours, starting_states))


def solve_productive(neighbours, ending_states):
    print_array(get_dfs_reachable_states(transpose_graph(neighbours), ending_states))


def solve_utils(neighbours, starting_states, ending_states):
    accessible_states = get_dfs_reachable_states(neighbours, starting_states)
    productive_states = get_dfs_reachable_states(transpose_graph(neighbours), ending_states)

    intersected_states = [state for state in productive_states if state in set(accessible_states)]
    print_array(intersected_states)


def traverse_sequence(automaton, sequence, starting_state):
    state = starting_state
    for elem in sequence:
        state = automaton[state][elem]
    return state


def find_reachable_states(automaton, states, sequence):
    reachable_states = set()
    for state in states:
        reachable_states.add(traverse_sequence(automaton, sequence, state))

    return reachable_states


def find_two_states(reachable_states):
    states = []
    for key in reachable_states:
        if len(states) < 2:
            states.append(key)
        elif len(states) == 2:
            break

    return sorted(states)


def get_double_state_neighbours(state, neighbours_list, num_symbols):
    neigh = []
    i, j = state

    for sym in range(num_symbols):
        fst_state = neighbours_list[i][sym]
        snd_state = neighbours_list[j][sym]

        if fst_state == snd_state:
            neigh.append(fst_state)
        else:
            found_pair = (fst_state, snd_state) if fst_state < snd_state else (snd_state, fst_state)
            neigh.append(found_pair)

    return neigh


def extract_parents_path(parents, head):
    path = []
    while head != -1:
        head, symbol = parents[head]
        path.append(symbol)
    path.pop()

    return reversed(path)


def find_merging_sequence(starting_pair, neighbours, num_symbols, ending_states):
    visited = {}
    parents = {}
    stack = []

    visited[starting_pair] = True
    stack.append(starting_pair)
    parents[starting_pair] = (-1, -1)

    while len(stack) > 0:
        top = stack.pop()

        neigh_list = neighbours[top] if type(top) is not tuple \
            else get_double_state_neighbours(top, neighbours, num_symbols)

        for i, neigh in enumerate(neigh_list):
            if neigh not in visited:
                parents[neigh] = (top, i)

                if type(neigh) is not tuple and (len(ending_states) == 0 or neigh in ending_states):
                    return extract_parents_path(parents, neigh)

                visited[neigh] = True
                stack.append(neigh)


def solve_synchronize(neighbours, num_symbols, starting_states, ending_states):
    synchronize_sequence = []
    states = [i for i in range(len(neighbours))]
    if len(starting_states) != 0:
        states = starting_states

    currently_reachable_states = find_reachable_states(neighbours, states, synchronize_sequence)

    while len(currently_reachable_states) > 1:
        first_state, second_state = find_two_states(currently_reachable_states)
        merging_sequence = find_merging_sequence((first_state, second_state), neighbours, num_symbols,
                                                 set(ending_states))

        synchronize_sequence += merging_sequence
        currently_reachable_states = find_reachable_states(neighbours, states, synchronize_sequence)

    sys.stdout.write(' '.join([str(elem) for elem in synchronize_sequence]))


def main(argv):
    if len(argv) != 2:
        sys.exit('Running example: \n\tpython3 tema <problem>')

    num_states, num_symbols, num_starting_states, num_ending_states = extract_input_line()

    neighbours = []
    for _ in range(num_states):
        neighbours.append(list(extract_input_line()))

    starting_states = list(extract_input_line()) if num_starting_states != 0 else []
    ending_states = list(extract_input_line()) if num_ending_states != 0 else []

    if argv[1] == 'accessible':
        solve_accessible(neighbours, starting_states)
    elif argv[1] == 'productive':
        solve_productive(neighbours, ending_states)
    elif argv[1] == 'useful':
        solve_utils(neighbours, starting_states, ending_states)
    elif argv[1] == 'synchronize':
        solve_synchronize(neighbours, num_symbols, starting_states, ending_states)


if __name__ == '__main__':
    main(sys.argv)
