from networkx.algorithms.dag import dag_longest_path_length as long_path_len

# Simulate function 
def simulate(data, graph, module, inbuf, outbuf, tribuf, ari, cfg, defparam):
    # Finding the length of longest path in the graph 
    longest_length = long_path_len(graph)
    # Going through all the modules of inputs, gnd and vcc and getting the attribute weight for those nodes
    try:
        for x in module['input']:
            graph[x][x + '_ibuf'][0]['weight'] = data[x]
            for src, dst, val in graph.out_edges(x + '_ibuf', data=True):
                val['weight'] = data[x]
    except:
        pass
    for src, dst, val in graph.out_edges('GND', data=True):
        val['weight'] = '0'
    for src, dst, val in graph.out_edges('VCC', data=True):
        val['weight'] = '1'
        
    tri_out = []
    for x in tribuf.keys():
        for src, dst, val in graph.in_edges(x, data=True):
            tri_out.append(val['weight'])
        for src, dst, val in graph.out_edges(x, data=True):
            val['weight'] = tri_out[-1]

    # Looping till we reach the end of the graph 
    while (longest_length):
        # Getting the value from the modules after computation
        for x, y in defparam.items():
            value = y.replace('\'h', ' \'h ').split()
            # If it is an ari block
            if value[0] == '20':
                # Converting the hex value to binary
                val = bin(int(value[2][0], 16))[2:].zfill(4)
                bit_015 = bin(int(value[2][1:], 16))[2:].zfill(16)[::-1]
                bit_1716 = val[:2]
                bit_1918 = val[2:]
                adcb = ""
                # Collecting all the input weights that the module has received and storing it in adcb
                try:
                    for src, dst, val in graph.in_edges(x, data=True):
                        adcb += val['weight']
                except:
                    continue
                # Reversing the string 
                adcb = adcb[::-1]
                # Splitting and assigning the defparam hex init value to required variables 
                bit_07 = bit_015[:8]
                bit_815 = bit_015[8:]

                # Getting the value of Y
                out_y = bit_015[int(adcb[1:],2)]
                # Getting the value of F0 and F1
                f0 = bit_07[int(adcb[2:],2)]
                f1 = bit_815[int(adcb[2:],2)]

                # Getting value of S
                out_s = int(out_y) ^ int(adcb[0])
                
                # Calculating the value of g using the truth table 
                if bit_1716 == '00':
                    g = '0'
                elif bit_1716 == '01':
                    g = f0
                elif bit_1716 == '10':
                    g = '1'
                else:
                    g = f1

                # Calculating the value of p using the truth table
                if bit_1918 == '00':
                    p = '0'
                elif bit_1918 == '01':
                    p = out_y
                else:
                    p = '1'

                # Calculating the value of FCO using the truth table
                if p == '0':
                    out_fco = g
                else:
                    out_fco = adcb[0]

                # Finally assiging the weights to all the out edges from the modules (node)
                for src, dst, val in graph.out_edges(x, data=True):
                    if val['attr'] == 'y':
                        val['weight'] = out_y
                    if val['attr'] == 's':
                        val['weight'] = out_s
                    if val['attr'] == 'fco':
                        val['weight'] = out_fco

            # If it is block other than ari block
            else:
                # Converting the hex value to binary and reversing it 
                bit = bin(int(value[2], 16))[2:].zfill(int(value[0]))[::-1]
                index = ""
                # Collecting all the input weights that the module has received and storing it in index
                try:
                    for src, dst, val in graph.in_edges(x, data=True):
                        index += val['weight']
                except:
                    continue
                # Reverse the string
                index = index[::-1]
                # For each out edge from the module (node) assign the corresponding output 
                for src, dst, val in graph.out_edges(x, data=True):
                    val['weight'] = bit[int(index, 2)]
        # Decrement the longest path length
        longest_length -= 1
    
    # Creating an empty list to store the output 
    final_out = []
    # For every outbuf append the attribute weight associated with it to the final_output
    for x in outbuf.keys():
        for src, dst, val in graph.in_edges(x, data=True):
            final_out.append(val['weight'])
        for src, dst, val in graph.out_edges(x, data=True):
            val['weight'] = final_out[-1]
    if not final_out:
        for x in module['output']:
            for src, dst, val in graph.in_edges(x, data=True):
                final_out.append(val['weight'])
    print('\x1b[0;32;49m' + 'OUTPUTS : ' + '\x1b[0m' )
    for i in range(len(final_out)):
        print('\x1b[0;32;49m' + module['output'][i] + ' : ' + final_out[i] + '\x1b[0m' )