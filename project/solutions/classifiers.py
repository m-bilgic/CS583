import numpy as np

def abstract():
    import inspect
    caller = inspect.getouterframes(inspect.currentframe())[1][3]
    raise NotImplementedError(caller + ' must be implemented in subclass')



class Aggregator(object):
    
    def __init__(self, domain_labels, directed = False):
        self.domain_labels = domain_labels # The list of labels in the domain
        self.directed = directed # Whether we should use edge directions for creating the aggregation
    
    def aggregate(self, graph, node, conditional_node_to_label_map):
        ''' Given a node, its graph, and labels to condition on (observed and/or predicted)
        create and return a feature vector for neighbors of this node.
        If a neighbor is not in conditional_node_to_label_map, ignore it.
        If directed = True, create and append two feature vectors;
        one for the out-neighbors and one for the in-neighbors.
        '''
        abstract()

class CountAggregator(Aggregator):
    '''The count aggregate'''
    
    def aggregate(self, graph, node, conditional_node_to_label_map): 
        # raise NotImplementedError('You need to implement this method')
        e=[0.0]
        if self.directed:
            in_neighbors_count=len(self.domain_labels)*e
            out_neighbors_count=len(self.domain_labels)*e
            for out_n in graph.get_out_neighbors(node.node_id):
                if out_n in conditional_node_to_label_map.keys():
                    out_neighbors_count[self.domain_labels.index(conditional_node_to_label_map[out_n])]+=1.0
            for in_n in graph.get_in_neighbors(node.node_id):
                if in_n in conditional_node_to_label_map.keys():
                    in_neighbors_count[self.domain_labels.index(conditional_node_to_label_map[in_n])]+=1.0
            return in_neighbors_count+out_neighbors_count
        else:
            neighbors_count=len(self.domain_labels)*e
            for n in graph.get_neighbors(node.node_id):
                if n in conditional_node_to_label_map.keys():
                    neighbors_count[self.domain_labels.index(conditional_node_to_label_map[n])]+=1.0
            return neighbors_count



class ProportionalAggregator(Aggregator):
    '''The proportional aggregate'''
    
    def aggregate(self, graph, node, conditional_node_to_label_map): 
        # raise NotImplementedError('You need to implement this method')
        count_agg=CountAggregator(self.domain_labels,self.directed)
        relation=count_agg.aggregate(graph,node,conditional_node_to_label_map)
        length=len(self.domain_labels)
        if self.directed:
            in_sum=sum(relation[:length])
            out_sum=sum(relation[length:])
            if in_sum !=0:
                for r in range(0,length):
                    relation[r]/=1.*in_sum
                # relation[:length]/=1.*in_sum
            if out_sum !=0:
                # relation[length:]/=1.*out_sum
                for r in range(length,-1):
                    relation[r]/=1.*out_sum
            return relation
        else:
            tot_sum=sum(relation)
            if tot_sum !=0:
                for r in range(len(relation)):
                    relation[r]/=1.*tot_sum
                # relation[:]=relation[:]/1.*tot_sum
            return relation

class ExistAggregator(Aggregator):
    '''The exist aggregate'''
    
    def aggregate(self, graph, node, conditional_node_to_label_map): 
        # raise NotImplementedError('You need to implement this method')
        count_agg=CountAggregator(self.domain_labels,self.directed)
        relation=count_agg.aggregate(graph,node,conditional_node_to_label_map)
        # length=len(self.domain_labels)
        # if self.directed:
        for r in range(len(relation)):
            if relation[r]>=1:
                relation[r]=1
        return relation


def get_class( kls ):
    parts = kls.split('.')
    module = ".".join(parts[:-1])
    m = __import__( module )
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m

class Classifier(object):
    '''
    The base classifier object
    '''

    def __init__(self, scikit_classifier_name, **classifier_args):        
        classifer_class=get_class(scikit_classifier_name)
        self.clf = classifer_class(**classifier_args)

    
    def fit(self, graph, train_indices, conditional_node_to_label_map = None):
        '''
        Create a scikit-learn classifier object and fit it using the Nodes of the Graph
        that are referenced in the train_indices
        '''
        abstract()
    
    def predict(self, graph, test_indices, conditional_node_to_label_map = None):
        '''
        This function should be called only after the fit function is called.
        Predict the labels of test Nodes conditioning on the labels in conditional_node_to_label_map.
        '''
        abstract()

class LocalClassifier(Classifier):

    def fit(self, graph, train_indices, conditional_node_to_label_map = None):
        '''
        Create a feature list of lists (or matrix) and a label list
        (or array) and then fit using self.clf
        ''' 
        X=[graph.node_list[t].feature_vector for t in train_indices]
        y=[graph.node_list[t].label for t in train_indices]
        self.clf.fit(X,y)

    def predict(self, graph, test_indices, conditional_node_to_label_map = None):
        '''
        This function should be called only after the fit function is called.
        Use only the node attributes for prediction.
        '''
        X=[graph.node_list[t].feature_vector for t in test_indices]
        return self.clf.predict(X)

class RelationalClassifier(Classifier):
    
    def __init__(self, scikit_classifier_name, aggregator, use_node_attributes = True, **classifier_args):
        super(RelationalClassifier, self).__init__(scikit_classifier_name, **classifier_args)
        self.aggregator = aggregator
        self.use_node_attributes = use_node_attributes
        self.conditional_map={}

    def create_map(self,graph,train_indices):
        for i in train_indices:
            self.conditional_map[graph.node_list[i].node_id]=graph.node_list[i].label

    def _combine_feature(self,graph,X,i):
        relation=self.aggregator.aggregate(graph,graph.node_list[i],self.conditional_map)
        record=[]
        if self.use_node_attributes:
            record=list(graph.node_list[i].feature_vector)
            record.extend(relation)
        else:
            record.extend(relation)
        X.append(record)

    def fit(self, graph, train_indices, conditional_node_to_label_map = None):
        '''
        Create a feature list of lists (or matrix) and a label list
        (or array) and then fit using self.clf
        You need to use aggregator to create relational features.
        Note that the aggregator needs to know what to condition on, 
        i.e., conditional_node_to_label_map. This should be created using only the train nodes.
        The features list might or might not include the node features, depending on 
        the value of use_node_attributes.
        ''' 
        # raise NotImplementedError('You need to implement this method')
        if conditional_node_to_label_map==None:
            self.create_map(graph,train_indices)
        else:
            self.conditional_map=conditional_node_to_label_map
        X=[]
        y=[]
        for i in train_indices:
            self._combine_feature(graph,X,i)
            # relation=self.aggregator.aggregate(graph,graph.node_list[i],self.conditional_map)
            # record=[]
            # if self.use_node_attributes:
            #     record=graph.node_list[i].feature_vector
            #     record.extend(relation)
            # else:
            #     record.extend(relation)
            # X.append(record)
            y.append(graph.node_list[i].label)
        self.clf.fit(X,y)

    def predict(self, graph, test_indices, conditional_node_to_label_map = None):
        '''
        This function should be called only after the fit function is called.
        Predict the labels of test Nodes conditioning on the labels in conditional_node_to_label_map.
        conditional_node_to_label_map might include the observed and predicted labels.        
        This method is NOT iterative; it does NOT update conditional_node_to_label_map.
        '''
        # raise NotImplementedError('You need to implement this method')
        X=[]
        for i in test_indices:
            self._combine_feature(graph,X,i)
            # relation=self.aggregator.aggregate(graph,graph.node_list[i],self.conditional_map)
            # record=[]
            # if self.use_node_attributes:
            #     record=graph.node_list[i].feature_vector
            #     record.extend(relation)
            # else:
            #     record.extend(relation)
            # X.append(record)
        return self.clf.predict(X)

class ICA(Classifier):
    
    def __init__(self, local_classifier, relational_classifier, max_iteration = 10):
        self.local_classifier = local_classifier
        self.relational_classifier = relational_classifier
        self.max_iteration = 10
    
    
    def fit(self, graph, train_indices, conditional_node_to_label_map = None):
        self.local_classifier.fit(graph, train_indices)
        self.relational_classifier.fit(graph, train_indices)
    
    def predict(self, graph, test_indices, conditional_node_to_label_map = None):
        '''
        This function should be called only after the fit function is called.
        Implement ICA using the local classifier and the relational classifier.
        '''
        raise NotImplementedError('You need to implement this method')
    