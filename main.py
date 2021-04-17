import networkx as nx
from matplotlib import pyplot as plt
import os
from construct import *
from sim import *
from tmr import *


# Main Function
plt.figure(figsize=(100, 550))
if __name__ == '__main__':
    # Input path of file
    file_path = input('\x1b[0;31;49m' + 'Enter the path of the file: ')
    module, inbuf, outbuf, tribuf, ari, cfg, defparam = parser(file_path)
    # Create a directed graph using networkx
    graph = nx.MultiDiGraph()
    # Add nodes
    graph , color = add_node(graph, module, inbuf, outbuf, tribuf, ari, cfg)
    # Add edges
    graph = add_edge(graph, module, inbuf, outbuf, tribuf, ari, cfg)
    # Print the graph (Adj List)
    adj_graph = nx.to_dict_of_lists(graph)
    for x , y in adj_graph.items():
        print('\x1b[0;36;49m' + x + ':' + str(y) + '\x1b[0m' )

    pos = nx.get_node_attributes(graph, 'pos')
    # Drawing the graph along with some specifications
    nx.draw(graph, with_labels=True, pos=pos, node_color=list(color.values()), node_size=30000,
            bbox=dict(facecolor="white", edgecolor='black', boxstyle='round,pad=0.2'))
    # Saving the output image
    plt.savefig('Output/' + os.path.splitext(os.path.basename(file_path))[0] + '.png')
    # # Taking inputs from user
    data = {}
    print('\x1b[0;33;49m' + 'INPUTS :' + '\x1b[0m' )
    for x in module['input']:
        data[x] = input('\x1b[0;33;49m' + f'Enter the value of input {x} : ')

    simulate(data, graph, module, inbuf, outbuf, tribuf, ari, cfg, defparam)
    
    tmr(data, graph, inbuf, outbuf, tribuf, ari, cfg, color, file_path)