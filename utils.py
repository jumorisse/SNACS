import numpy as np
import networkx as nx


def simulate_cascade(network, start, already_influenced):
    '''
    Simulates the influence spread from a start node. Returns the number of nodes influenced starting from the start node.
    Uses recursion: Starts by counting the number of neighbors that will be influenced. Recursively applied to each of the newly
    influenced neighbors. Base case is reached when none of the neighbors will be influenced due to lack of influence spread or
    because all of them are already influenced.

    :param network: A networkx graph object.
    :param start: The node from which to start the cascade computation.
    :param already_influenced: A set of nodes that already have been influenced.
    :return: A list of nodes that were influenced in the current cascade.
    '''
    cascade_influence = []
    # compute neighbors of start node
    neighbors = network.neighbors(start)
    # simulate which neighbors (that are not in current_influence) are influenced
    influenced_neighbors = []
    for neighbor in neighbors:
        if neighbor not in already_influenced:
            prop_prob = network.get_edge_data(start, neighbor)['weight']
            if np.random.random() < prop_prob:
                cascade_influence.append(neighbor)
                influenced_neighbors.append(neighbor)

    # if no neighbor is additionally influenced, the recursion base case is reached and an empty list returned
    if len(influenced_neighbors) == 0:
        return []
    # run simulate cascade for each node that is newly influenced (with already_influenced updated after each call)
    for influenced_neighbor in influenced_neighbors:
        cascade_influence = cascade_influence + simulate_cascade(network, influenced_neighbor, already_influenced+cascade_influence)

    return cascade_influence


def evaluate_seeds(network, seeds, nr_simulations=1000):
    '''
    Computes the average nr of nodes influenced by the seeds across nr_simulations simulations of influence spread.

    :param network: A networkx graph object with weighted edges (the weights correspond to propagation probabilities)
    :param seeds: A list of seeds that is to be evaluated
    :param nr_simulations: How many times is the influence spread simulated before taking the average.
    :return: The number of nodes that were on average influenced by the given seed.
    '''

    influences = []
    for simulation in range(nr_simulations):
        current_influence = seeds
        for seed in seeds:
            seed_influence = simulate_cascade(network, seed, current_influence)
            current_influence.append(seed_influence)
        influences.append(len(current_influence))

    return np.mean(np.array(influences))