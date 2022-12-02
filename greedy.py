import networkx as nx
import numpy as np
from numpy import random
from copy import deepcopy

def NewGreedy(G, N, seed_no, sample_type, p):
    '''
    Sam doesnt share his knowledge.
    :param G:
    :param N:
    :param seed_no:
    :param sample_type:
    :param p:
    :return:
    '''
    seeds = []

    GG = deepcopy(G)

    for e in G.edges():
        if sample_type.lower() == "none":
            rand = p 
        
        elif sample_type.lower() == "uniform":
            rand = np.random.random()
        elif sample_type.lower() == "expo":
           rand = random.exponential(p)
    
        if rand>1:
            rand = 1
    
        GG[e[0]][e[1]]['weight'] = rand


    for s in range(seed_no):
        counter = {}

        for node in G:
            counter[node] = counter.get(node,0)

        for n in range(N):
            newG = deepcopy(GG)
            edge_rem = []

            for e in newG.edges():
                if random.random() < (1-(newG[e[0]][e[1]]['weight'])):
                    edge_rem.append(e)
            
            newG.remove_edges_from(edge_rem)

            # init CCs
            CCs = dict()
            explored = dict(zip(newG.nodes(), [False]*len(newG)))
            c = 0

            #perform BFS to discover CC
            for node in newG:    
                if not explored[node]:
                    c += 1
                    explored[node] = True
                    CCs[c] = [node]
                    component = list(newG[node].keys())
                    for neighbor in component:
                        if not explored[neighbor]:
                            explored[neighbor] = True
                            CCs[c].append(neighbor)
                            component.extend(list(newG[neighbor].keys()))

            for i in CCs:
                check_act = set(CCs[i]).intersection(set(seeds))

                if check_act == set():
                    for j in range(len(CCs[i])):
                        counter[CCs[i][j]] += len(CCs[i])

        seeds.append(max(counter, key=counter.get))
    
    return seeds
            

    


'''
# main():
G = nx.Graph()
G.add_nodes_from([0,1,2,3,4,5,6,7,8,9,10,11])
G.add_edges_from([(0,1),(0,2),(1,2),(1,4),(3,4),(2,5),(4,5),(5,6),(5,7),(7,8),(7,10),(9,10),(10,11)])

for e in G.edges():
    rand = random.exponential(0.2)
    
    if rand>1:
        rand = 1
    
    G[e[0]][e[1]]['weight'] = rand

counter, seeds = NewGreedy(G, 10000,2,"expo",0.3)
print(counter, seeds)
'''
