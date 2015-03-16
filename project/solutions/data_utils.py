from project.assigned.graph import DirectedGraph, Node, Edge


def load_linqs_data(content_file, cites_file):
    '''
    Create a DirectedGraph object and add Nodes and Edges
    This is specific to the data files provided at http://linqs.cs.umd.edu/projects/projects/lbc/index.html
    Return two items 1. graph object, 2. the list of domain labels (e.g., ['AI', 'IR'])
    '''
    linqs_graph=DirectedGraph()
    domain_labels=[]
    
    with open(content_file, 'r') as node_file:
        for line in node_file:
            line_info=line.split('\n')[0].split('\t')
            linqs_graph.add_node(Node(line_info[0],map(float,line_info[1:-1]),line_info[-1]))# id, feature vector, label
            if line_info[-1] not in domain_labels:
                domain_labels.append(line_info[-1])

    with open(cites_file,'r') as edge_file:
        for line in edge_file:
            line_info=line.split('\n')[0].split('\t')
            linqs_graph.add_edge(Edge(line_info[1],line_info[0]))
        
    return linqs_graph,domain_labels

