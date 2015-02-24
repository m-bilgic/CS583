__author__ = 'wolfshjj'

class Node(object):
    def __init__(self,iD,features,label):
        self.id=iD
        self.features=features
        self.label = label


class Edge(object):
    def __init__(self,cited,citing):#A, B: A->B
        self.edge=(cited,citing)

class Graph(object):
    def __init__(self,content_path,cites_path):
        self.nodes_list=[]
        self.edges_list=[]
        self.read_nodes(content_path)
        self.read_edges(cites_path)

    def read_nodes(self,path):
        if path.split('.')[-1]!='content':
            print 'wrong content file'
        else:
            node_file=open(path,'r')
            while True:
                line=node_file.readline()
                if not line:
                    break
                line_info=line.split('\n')[0].split('\t')
                self.nodes_list.append(Node(line_info[0],line_info[1:-1],line_info[-1]))
            node_file.close()

    def read_edges(self,path):
        if path.split('.')[-1]!='cites':
            print 'wrong cites file'
        else:
            edge_file=open(path,'r')
            while True:
                line=edge_file.readline()
                if not line:
                    break
                line_info=line.split('\n')[0].split('\t')

                self.edges_list.append(Edge(line_info[0],line_info[1]))
            edge_file.close()

content_path="G:/IIT/CS583 TA/project/cora/cora.content"
cites_path="G:/IIT/CS583 TA/project/cora/cora.cites"
a=Graph(content_path,cites_path)
# a.read_nodes("G:/IIT/CS583 TA/project/cora/cora.content")
print(a.nodes_list[-1].id)