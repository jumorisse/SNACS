import networkx as nx
import numpy as np


def discounted_degree(network, node, seeds, p):
    '''
    Computes the discounted degree of a node according to Chen et al. (2009).

    :param network: A networkx graph object that is the network for which influence is to be optimized.
    :param node: The node for which to compute the discounted degree.
    :param seeds: The nodes that have been selected as seeds so far.
    :param p: The propagation probability to use in the computation
    :return: A float that serves as a discounted degree score of the node to decide which node to pick as the next seed node.
    '''
    neighborhood = list(network.neighbors(node))
    nr_seed_neighbors = len(set(neighborhood).intersection(seeds))
    not_influenced_prob = pow((1-p), nr_seed_neighbors)
    return not_influenced_prob*(1+(len(neighborhood)-nr_seed_neighbors)*p)


def degree_discount(network, nr_seeds, sample, sample_param):
    '''
    Performs influence maximization using the degree discount heuristic proposed by Chen et al. (2009). Different to the implementation by Chen et al. (2009)
    that uses a constant p for all nodes, this implementation can sample p for each node depending on the value of the sample and sample_param parameter.

    :param network: A networkx graph object that is the network for which influence is to be optimized.
    :param nr_seeds: The number of seeds we want to have.
    :param sample: Indicates whether we want to sample p and if we do how (from a uniform, normal or exponential distribution)
    :param sample_param: Type depends on sample. If sample=='one' it is just p, if sample=='uniform' it is None, if sample=='expo' it is the scale parameter
    and if sample=='normal' it is a tuple (mean, std)
    :return: Returns a list of nodes that are the found seed nodes.
    '''
    seeds = []

    for i in range(nr_seeds):
        best_score = 0
        best_node = 0

        for node in network.nodes:
            if sample.lower() == 'none':
                p = sample_param
            elif sample.lower() == 'uniform':
                p = np.random.random()
            elif sample.lower() == 'expo':
                valid_p = False
                while not valid_p:
                    p = np.random.exponential(sample_param)
                    if p > 0 and p < 1:
                        valid_p = True
            elif sample.lower() == 'normal':
                mean = sample_param[0]
                std = sample_param[0]
                valid_p = False
                while not valid_p:
                    p = np.random.normal(mean, std)
                    if p > 0 and p < 1:
                        valid_p = True

            if node not in seeds:
                score = discounted_degree(network, node, seeds, p)
                if score > best_score:
                    best_score = score
                    best_node = node

        seeds.append(best_node)

    return seeds