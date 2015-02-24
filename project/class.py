__author__ = 'wolfshjj'

def abstract():
    import inspect
    caller = inspect.getouterframes(inspect.currentframe())[1][3]
    raise NotImplementedError(caller + ' must be implemented in subclass')

class Node(object):
    def __init__(self,iD,features,label):
        self.id=iD
        self.features=features
        self.label = label


class Edge(object):
    def __init__(self,A,B):#A, B: A->B
        self.edge=(A,B)

class Graph(object):
    def __init__(self,content_path):
        self.nodes_dict=self.get_nodes(content_path)

    # def add_node(self,n):
    #     abstract()
    #
    # def add_edge(self,e):
    #     abstract()

    def get_nodes(self,path):
        nodes_dict={}
        if path.split('.')[-1]!='content':
            print 'wrong content file'
        else:
            node_file=open(path,'r')
            while True:
                line=node_file.readline()
                if not line:
                    break
                line_info=line.split('\n')[0].split('\t')
                nodes_dict[line_info[0]]=Node(line_info[0],line_info[1:-1],line_info[-1])
                # self.nodes_list.append(Node(line_info[0],line_info[1:-1],line_info[-1]))
            node_file.close()
        return nodes_dict

    def get_edges(self,path):
        abstract()
        # if path.split('.')[-1]!='cites':
        #     print 'wrong cites file'
        # else:
        #     edge_file=open(path,'r')
        #     while True:
        #         line=edge_file.readline()
        #         if not line:
        #             break
        #         line_info=line.split('\n')[0].split('\t')
        #
        #         self.edges_list.append(Edge(line_info[0],line_info[1]))
        #     edge_file.close()

class Direct_Graph(Graph):
    def __init__(self,content_path,cites_path):
        super(Direct_Graph,self).__init__(content_path)
        # self.nodes_dict=super(Direct_Graph,self).get_nodes(content_path)
        self.edges_list=self.get_edges(cites_path)
        self.outcomes=self.get_outcomes()
        self.incomes=self.get_incomes()

    # def get_nodes(self,path):
    #     nodes_dict={}
    #     if path.split('.')[-1]!='content':
    #         print 'wrong content file'
    #     else:
    #         node_file=open(path,'r')
    #         while True:
    #             line=node_file.readline()
    #             if not line:
    #                 break
    #             line_info=line.split('\n')[0].split('\t')
    #             nodes_dict[line_info[0]]=Node(line_info[0],line_info[1:-1],line_info[-1])
    #             # self.nodes_list.append(Node(line_info[0],line_info[1:-1],line_info[-1]))
    #         node_file.close()
    #     return nodes_dict

    def get_edges(self,path):
        edges_list=[]
        if path.split('.')[-1]!='cites':
            print 'wrong cites file'
        else:
            edge_file=open(path,'r')
            while True:
                line=edge_file.readline()
                if not line:
                    break
                line_info=line.split('\n')[0].split('\t')

                edges_list.append(Edge(line_info[0],line_info[1]))
            edge_file.close()
        return edges_list

    def get_outcomes(self):
        outcomes={}
        for edge in self.edges_list:
            if edge.edge[0] not in outcomes.keys():
                outcomes[edge.edge[0]]=list()
                outcomes[edge.edge[0]].append(self.nodes_dict[edge.edge[1]])
            else:
                outcomes[edge.edge[0]].append(self.nodes_dict[edge.edge[1]])
        return outcomes

    def get_incomes(self):
        incomes={}
        for edge in self.edges_list:
            if edge.edge[1] not in incomes.keys():
                incomes[edge.edge[1]]=list()
                incomes[edge.edge[1]].append(self.nodes_dict[edge.edge[0]])
            else:
                incomes[edge.edge[1]].append(self.nodes_dict[edge.edge[0]])
        return incomes


content_path="G:/IIT/CS583 TA/project/cora/cora.content"
cites_path="G:/IIT/CS583 TA/project/cora/cora.cites"
a=Direct_Graph(content_path,cites_path)

# a.read_nodes("G:/IIT/CS583 TA/project/cora/cora.content")
print(a.outcomes)