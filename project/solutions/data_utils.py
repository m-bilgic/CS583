from project.assigned.graph import DirectedGraph, Node, Edge


def load_linqs_data(content_file, cites_file):
    '''
    Create a DirectedGraph object and add Nodes and Edges
    This is specific to the data files provided at http://linqs.cs.umd.edu/projects/projects/lbc/index.html
    Return two items 1. graph object, 2. the list of domain labels (e.g., ['AI', 'IR'])
    '''
    linqs_graph=DirectedGraph()
    domain_labels=[]
    if content_file.split('.')[-1]=='content':  #.content file
        node_file=open(content_file,'r')
        while True:
            line=node_file.readline()    #read line
            if not line:
                break
            line_info=line.split('\n')[0].split('\t')
            linqs_graph.add_node(Node(line_info[0],map(float,line_info[1:-1]),line_info[-1]))# id, feature vector, label
            if line_info[-1] not in domain_labels:
                domain_labels.append(line_info[-1])
        node_file.close()

    if cites_file.split('.')[-1]=='cites':#.cites file
        edge_file=open(cites_file,'r')
        while True:
            line=edge_file.readline()   #read line
            if not line:
                break
            line_info=line.split('\n')[0].split('\t')
            linqs_graph.add_edge(Edge(line_info[0],line_info[1]))# cited -> citing
                                                                # the more out neighbors the more important
        edge_file.close()
    return linqs_graph,domain_labels

