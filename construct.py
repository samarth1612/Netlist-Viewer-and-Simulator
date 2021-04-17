import random


# Coloring the nodes
def color_node():
    return random.randint(0, 255)


def parser(file):
    random.seed()
    # Dictionary for input, output, wires, inbufs, outbufs, tribufs, ari, cfg blocks
    module = {
        'input': [],
        'output': [],
        'wire': []
    }
    inbuf = {}
    outbuf = {}
    tribuf = {}
    ari = {}
    cfg = {
        "CFG1": {},
        "CFG2": {},
        "CFG3": {},
        "CFG4": {},
    }
    defparam = {}
    # Counter to keep track till where we have read each block
    count = -1
    # Opening file in read mode
    with open(file, "r") as fp:
        file_data = fp.readlines()
    # Reading each line
    for line in file_data:
        # Incrementing  count and storing it in a temp variable
        count += 1
        temp = count
        # Splitting the lines
        word = line.split()
        # If word length zero then continue
        if len(word) == 0:
            continue
        # If word[0] is any key from module append it to the module[word[0]]
        if word[0] in list(module.keys()):
            module[word[0]].append(word[1])
        # If word[0] is "INBUF" append inbuf[mod_name] to the dictionary and increment the temp (counter)
        elif word[0] == "INBUF":
            mod_name = word[1]
            inbuf[mod_name] = []
            temp += 1
            # Scan for the inputs and outputs
            while file_data[temp].split()[0] != ");":
                x = file_data[temp].replace("(", "( ")
                x = x.replace(")", " )").split()
                inbuf[mod_name].append(x[1])
                temp += 1
        # If word[0] is "OUTBUF" append outbuf[mod_name] to the dictionary and increment the temp (counter)
        elif word[0] == "OUTBUF":
            mod_name = word[1]
            outbuf[mod_name] = []
            temp += 1
            # Scan for the inputs and outputs
            while file_data[temp].split()[0] != ");":
                x = file_data[temp].replace("(", "( ")
                x = x.replace(")", " )").split()
                outbuf[mod_name].append(x[1])
                temp += 1
        # If word[0] is "TRIBUF" append tribuf[mod_name] to the dictionary and increment the temp (counter)
        elif word[0] == "TRIBUFF":
            mod_name = word[1]
            tribuf[mod_name] = []
            temp += 1
            # Scan for the inputs and outputs
            while file_data[temp].split()[0] != ");":
                x = file_data[temp].replace("(", "( ")
                x = x.replace(")", " )").split()
                tribuf[mod_name].append(x[1])
                temp += 1
        # If word[0] is "ARI1" append ari[mod_name] to the dictionary and increment the temp (counter)
        elif word[0] == "ARI1":
            mod_name = word[1]
            ari[mod_name] = []
            temp += 1
            # Scan for the inputs and outputs
            while True:
                x = file_data[temp].replace("(", "( ")
                x = x.replace(".", " . ")
                x = x.replace("=", " = ")
                x = x.replace(";", " ; ")
                x = x.replace(")", " )").split()
                if x[0] == "defparam":
                    defparam[x[1]] = x[5]
                    break
                # Inserting the output at starting indices else place them normally
                if x[1] in ["Y(", "FCO(", "S("]:
                    ari[mod_name].insert(0, x[2])
                elif x[0] + x[1] == ");":
                    temp += 1
                    continue
                else:
                    ari[mod_name].append(x[2])
                temp += 1
        # If word[0] is in list of cfg{}, append cfg[word[0][mod_name]] to the dict and increment the temp (counter)
        elif word[0] in list(cfg.keys()):
            mod_name = word[1]
            cfg[word[0]][mod_name] = []
            temp += 1
            # Scan for the inputs and outputs
            while True:
                x = file_data[temp].replace("(", "( ")
                x = x.replace(".", " . ")
                x = x.replace("=", " = ")
                x = x.replace(";", " ; ")
                x = x.replace(")", " )").split()
                if x[0] == "defparam":
                    defparam[x[1]] = x[5]
                    break
                # Inserting the output at first index  else place them normally
                if x[1] == "Y(":
                    cfg[word[0]][mod_name].insert(0, x[2])
                elif x[0] + x[1] == ");":
                    temp += 1
                    continue
                else:
                    cfg[word[0]][mod_name].append(x[2])
                temp += 1
    return module, inbuf, outbuf, tribuf, ari, cfg, defparam


def add_node(graph, module, inbuf, outbuf, tribuf, ari, cfg):
    # List for storing different colors for nodes
    color = {}

    # Variable to give positions for nodes
    y = 0
    # Adding input nodes
    color_hex = '#%02X%02X%02X' % (color_node(), color_node(), color_node())
    for node in module['input']:
        graph.add_node(node, pos=(10, -y))
        color[node] = color_hex
        y += 10

    y = 0
    # Adding output nodes
    color_hex = '#%02X%02X%02X' % (color_node(), color_node(), color_node())
    for node in module['output']:
        graph.add_node(node, pos=(70, -y))
        color[node] = color_hex
        y += 10

    y = 0
    # Adding inbuf nodes
    color_hex = '#%02X%02X%02X' % (color_node(), color_node(), color_node())
    for in_buf in inbuf.keys():
        graph.add_node(in_buf, pos=(20, -y))
        color[in_buf] = color_hex
        y += 10

    y = 0
    # Adding outbuf nodes
    color_hex = '#%02X%02X%02X' % (color_node(), color_node(), color_node())
    for out_buf in outbuf.keys():
        graph.add_node(out_buf, pos=(60, -y))
        color[out_buf] = color_hex
        y += 10

    y = 0
    # Adding tribuf nodes
    color_hex = '#%02X%02X%02X' % (color_node(), color_node(), color_node())
    for tri_buf in tribuf.keys():
        graph.add_node(tri_buf, pos=(30, -y))
        color[tri_buf] = color_hex
        y += 10

    y = 0
    # Adding ari nodes
    color_hex = '#%02X%02X%02X' % (color_node(), color_node(), color_node())
    for ari_block in ari.keys():
        graph.add_node(ari_block, pos=(50, -y))
        color[ari_block] = color_hex
        y += 10

    y = 0
    # Adding cfg nodes
    color_hex = '#%02X%02X%02X' % (color_node(), color_node(), color_node())
    for i, j in cfg.items():
        for x in j.keys():
            graph.add_node(x, pos=(40, -y))
            color[x] = color_hex
            y += 10
    # Adding VCC nodes
    color_hex = '#%02X%02X%02X' % (color_node(), color_node(), color_node())
    graph.add_node("VCC", pos=(25, 10))
    color["VCC"] = color_hex
    # Adding GND nodes
    color_hex = '#%02X%02X%02X' % (color_node(), color_node(), color_node())
    graph.add_node("GND", pos=(45, 10))
    color["GND"] = color_hex
    return graph, color


def add_edge(graph, module, inbuf, outbuf, tribuf, ari, cfg):
    out = 'y'
    # Adding the edges for each nodes
    # For inbuf
    for x in module['input']:
        if x + "_ibuf" in inbuf.keys():
            graph.add_edge(x, x + "_ibuf", attr = out)
    # For output
    for x in module['output']:
        if x + "_obuf" in outbuf.keys():
            graph.add_edge(x + "_obuf", x, attr = out)
    # For tribuf
    for x, y in tribuf.items():
        graph.add_edge("GND", x, attr = out)
        graph.add_edge(x, y[0], attr = out)
    # For ari block
    for x, y in ari.items():
        for i in range(3, 7):
            if y[i] in ['VCC', 'GND']:
                graph.add_edge(y[i], x, attr = out)
            else:
                node , name = cfg_edge(y[i], cfg, tribuf, inbuf, ari)
                graph.add_edge(node, x, attr = name)
    # For cfg block
    for x, y in cfg.items():
        for i, j in y.items():
            for m in range(1, len(j), 1):
                if j[m] in ['VCC', 'GND']:
                    graph.add_edge(j[m], i, attr = out)
                else:
                    node , name = cfg_edge(j[m], cfg, tribuf, inbuf, ari)
                    graph.add_edge(node, i, attr = name)
    # For outbuf
    for x, y in outbuf.items():
        if y[1] in ['VCC', 'GND']:
            graph.add_edge(y[1], x, attr = out)
        else:
            node , name = cfg_edge(y[1], cfg, tribuf, inbuf, ari)
            graph.add_edge(node, x, attr = name)

    return graph


# Adding edges from cfg blocks to cfg blocks and other blocks
def cfg_edge(in_edge, cfg, tribuf, inbuf, ari):
    # Adding edge between cfg and cfg
    for x, y in cfg.items():
        for i, j in y.items():
            if in_edge == j[0]:
                return i , 'y'
    # Adding edge between tribuf and cfg
    for x, y in tribuf.items():
        if in_edge == y[0]:
            return x , 'y'
    # Adding edge between inbuf and cfg
    for x, y in inbuf.items():
        if in_edge == y[0]:
            return x , 'y'
    # Adding edge between ari and cfg
    for x, y in ari.items():
        if in_edge == y[0]:
            return x , 'y'
        if in_edge == y[1]:
            return x , 's'
        if in_edge == y[2]:
            return x , 'fco'