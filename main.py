import argparse
import numpy as np
import networkx as nx

from degree_discount import degree_discount
from utils import evaluate_seeds # TODO: implement evaluate_seeds

argparser = argparse.ArgumentParser()
argparser.add_argument("--algorithm", choices=["greedy", "degree_discount"], default="degree_discount", help="What algorithm to use, greedy or degree discount?")
argparser.add_argument("--sample_type", choices=["none", "normal", "uniform", "expo"], default="none", help="Sampling p? And if so: how?")
argparser.add_argument("--nr_seeds", default=5, type=int, help="Number of seeds to find.")
args = argparser.parse_args()

np.random.seed(args.seed)

# TODO: Load and prepare network


# TODO: prepare sample parameter
if args.sample_type == 'none':
    sample_param = 0.2
elif args.sample_type == 'normal':
    sample_param = (0.2, 0.1)
elif args.sample_type == 'uniform':
    sample_param = 1
elif args.sample_type == 'expo':
    sample_param = 0.2 # numpy takes 1/lambda, so for a lambda of 5 it wants 0.2


if args.algorithm == 'degree_discount':
    seeds = degree_discount(args.network, args.nr_seeds, args.sample, sample_param)
    influence = evaluate_seeds(network, seeds)

if args.algorithm == 'greedy':
    seeds = greedy(args.network, args.nr_seeds, args.sample, sample_param)
    influence = evaluate_seeds(network, seeds)