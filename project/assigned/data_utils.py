from graph import DirectedGraph, Node, Edge

def _load_linqs_graph(data_path):
    '''
    Create a DirectedGraph object and add Nodes and Edges
    This is specific to the data files provided at http://linqs.cs.umd.edu/projects/projects/lbc/index.html
    '''
    raise NotImplementedError('You need to implement this method')

def load_cora(data_path):
    '''
    Load cora data set.
    '''
    return _load_linqs_graph(data_path)

def load_citeseer(data_path):
    '''
    Load citeseer data set
    '''
    return _load_linqs_graph(data_path)