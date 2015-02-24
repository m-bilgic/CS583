from graph import *

def load_direct_graph(data_path):
    '''
    Create a DirectedGraph object and add Nodes and Edges
    '''
    direct_graph=DirectedGraph()
    for path in data_path:
        if path.split('.')[-1]=='content':  #.content file
            node_file=open(path,'r')
            while True:
                line=node_file.readline()    #read line
                if not line:
                    break
                line_info=line.split('\n')[0].split('\t')
                direct_graph.add_node(Node(line_info[0],line_info[1:-1],line_info[-1]))# id, feature vector, label
            node_file.close()

        elif path.split('.')[-1]=='cites':#.cites file
            edge_file=open(path,'r')
            while True:
                line=edge_file.readline()   #read line
                if not line:
                    break
                line_info=line.split('\n')[0].split('\t')
                direct_graph.add_edge(Edge(line_info[0],line_info[1]))# cited -> citing
                                                                    # the more out neighbors the more important
            edge_file.close()
    return direct_graph

# def load_cora(data_path):
#     '''
#     Create a DirectedGraph object and add Nodes and Edges
#     '''
#     cora=DirectedGraph()
#     for path in data_path:
#         if path.split('.')[-1]=='content':  #.content file
#             node_file=open(path,'r')
#             while True:
#                 line=node_file.readline()    #read line
#                 if not line:
#                     break
#                 line_info=line.split('\n')[0].split('\t')
#                 cora.add_node(Node(line_info[0],line_info[1:-1],line_info[-1]))# id, feature vector, label
#             node_file.close()
#
#         elif path.split('.')[-1]=='cites':#.cites file
#             edge_file=open(path,'r')
#             while True:
#                 line=edge_file.readline()   #read line
#                 if not line:
#                     break
#                 line_info=line.split('\n')[0].split('\t')
#                 cora.add_edge(Edge(line_info[0],line_info[1]))# cited -> citing
#             edge_file.close()
#     return cora


# def load_citeseer(data_path):
#     '''
#     Create a DirectedGraph object and add Nodes and Edges
#     '''
#     citesser=DirectedGraph()
#     for path in data_path:
#         if path.split('.')[-1]=='content':
#             node_file=open(path,'r')
#             while True:
#                 line=node_file.readline()
#                 if not line:
#                     break
#                 line_info=line.split('\n')[0].split('\t')
#                 citesser.add_node(Node(line_info[0],line_info[1:-1],line_info[-1]))
#             node_file.close()
#
#         elif path.split('.')[-1]=='cites':
#             edge_file=open(path,'r')
#             while True:
#                 line=edge_file.readline()
#                 if not line:
#                     break
#                 line_info=line.split('\n')[0].split('\t')
#                 citesser.add_edge(Edge(line_info[0],line_info[1]))
#             edge_file.close()
#     return citesser

# content_path="G:/IIT/CS583 TA/project/cora/cora.content"
# cites_path="G:/IIT/CS583 TA/project/cora/cora.cites"

# content_path="G:/IIT/CS583 TA/project/citeseer/citeseer.content"
# cites_path="G:/IIT/CS583 TA/project/citeseer/citeseer.cites"
#
# citeseer=load_direct_graph([content_path,cites_path])
#
# print
