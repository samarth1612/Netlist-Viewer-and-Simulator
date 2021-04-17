from matplotlib import pyplot as plt
import networkx as nx
from construct import color_node
import os 

def tmr(data, graph, inbuf, outbuf, tribuf, ari, cfg, color, file_path):
    # Clear the graph that was plotted before
    plt.clf()
    # Take the input nopdes to be duplicated from user
    input_nodes = list(input('\x1b[0;36;49m' + "Enter duplation nodes with space in between : " ).strip().split())
    # get the attributes into pos
    pos = nx.get_node_attributes(graph, 'pos')
    # Inititalize the index for the and and or gates 
    and_index = 0
    or_index = 0
    
    # Loop through all the nodes that can be duplicated
    for node in input_nodes:
        # Check if the node input by user is present in the modules
        if node not in list(inbuf.keys()) + list(outbuf.keys()) + list(tribuf.keys()) + list(ari.keys()) + list(cfg['CFG1'].keys()) + list(cfg['CFG2'].keys()) + list(cfg['CFG3'].keys()) + list(cfg['CFG4'].keys()):
        # If not then raise an error
            raise ValueError('Module not found in the given file')
        # If found then get the in edges and out edges of the node
        else:
            in_data = []
            inward = graph.in_edges(node, data = True)
            # Getting the in_data from in edges
            for src, dst , val in inward:
                in_data.append((src, dst, val))
            # Getting the out_data from out edges
            out_data = []
            outward = graph.out_edges(node, data = True)
            for src, dst , val in outward:
                out_data.append((src, dst, val))
            
            current_pos = pos[node]    
            andgate_0 = 'and' + '_' + str(and_index)
            andgate_1 = 'and' +  '_' + str(and_index + 1)
            andgate_2 = 'and' +  '_' + str(and_index + 2)
            or_gate = 'or' +  '_' + str(or_index)

            # Updating the positions of the nodes that are being duplicated
            for x , y in pos.items(): 
                if current_pos[0] == y[0] and current_pos[1] > y[1]:
                    pos[x] = (y[0], y[1] - 10)
            
            nx.set_node_attributes(graph, pos , 'pos')
            # Remove current node
            graph.remove_node(node)
            color.pop(node)
            # Add the duplicated nodes
            color_hex = '#%02X%02X%02X' % (color_node(), color_node(), color_node())
            graph.add_node(node + '0', pos = (current_pos[0], current_pos[1]))
            color[node + '0'] = color_hex
            graph.add_node(node + '1', pos = (current_pos[0], current_pos[1] - 10))
            color[node + '1'] = color_hex
            graph.add_node(node + '2', pos = (current_pos[0], current_pos[1] - 20))
            color[node + '2'] = color_hex
            
            # Adding the AND and OR gates
            color_hex = '#%02X%02X%02X' % (color_node(), color_node(), color_node())
            graph.add_node(andgate_0, pos = (current_pos[0] + 4, current_pos[1]))
            color[andgate_0] = color_hex
            graph.add_node(andgate_1, pos = (current_pos[0] + 4, current_pos[1] - 10))
            color[andgate_1] = color_hex
            graph.add_node(andgate_2, pos = (current_pos[0] + 4, current_pos[1] - 20))
            color[andgate_2] = color_hex
            color_hex = '#%02X%02X%02X' % (color_node(), color_node(), color_node())
            graph.add_node(or_gate, pos = (current_pos[0] + 6, current_pos[1] - 10))
            color[or_gate] = color_hex

            # Adding the in edges 
            for src, dst, val in in_data:
                graph.add_edge(src, node+'0', weight = val['weight'])
                graph.add_edge(src, node+'1', weight = val['weight'])
                graph.add_edge(src, node+'2', weight = val['weight'])
            # For each out edge
            for src, dst, val in out_data:
                # Pass the node outputs to the AND gates
                graph.add_edge(node+'0', andgate_0, weight = val['weight'])
                graph.add_edge(node+'1', andgate_0, weight = val['weight'])
                graph.add_edge(node+'1', andgate_1, weight = val['weight'])
                graph.add_edge(node+'2', andgate_1, weight = val['weight'])
                graph.add_edge(node+'2', andgate_2, weight = val['weight'])
                graph.add_edge(node+'0', andgate_2, weight = val['weight'])
                # Pass the AND gate outputs to the OR gate
                graph.add_edge(andgate_0, or_gate, weight = val['weight'])
                graph.add_edge(andgate_1, or_gate, weight = val['weight'])
                graph.add_edge(andgate_2, or_gate, weight = val['weight'])
                graph.add_edge(or_gate, dst, weight = val['weight'])
            and_index += 3
            or_index += 1

    # Draw the graph
    pos = nx.get_node_attributes(graph, 'pos')
    # Drawing the graph along with some specifications
    nx.draw(graph, with_labels=True, pos=pos, node_color=list(color.values()), node_size=30000,
            bbox=dict(facecolor="white", edgecolor='black', boxstyle='round,pad=0.2'))
    # Saving the output image
    plt.savefig('Output/' + os.path.splitext(os.path.basename(file_path))[0] + '_tmr.png')