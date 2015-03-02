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
        raise NotImplementedError('You need to implement this method')

class ProportionalAggregator(Aggregator):
    '''The proportional aggregate'''
    
    def aggregate(self, graph, node, conditional_node_to_label_map): 
        raise NotImplementedError('You need to implement this method')

class ExistAggregator(Aggregator):
    '''The exist aggregate'''
    
    def aggregate(self, graph, node, conditional_node_to_label_map): 
        raise NotImplementedError('You need to implement this method')

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
        self.clf = classifer_class(classifier_args)

    
    def fit(self, graph, train_indices):
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

    def fit(self, graph, train_indices):
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
    
    def __init__(self, scikit_classifier_name, aggregator, use_node_attributes = False, **classifier_args):
        super(RelationalClassifier, self).__init__(scikit_classifier_name, **classifier_args)
        self.aggregator = aggregator
        self.use_node_attributes = use_node_attributes
    
    def fit(self, graph, train_indices):
        '''
        Create a feature list of lists (or matrix) and a label list
        (or array) and then fit using self.clf
        You need to use aggregator to create relational features.
        Note that the aggregator needs to know what to condition on, 
        i.e., conditional_node_to_label_map. This should be created using only the train nodes.
        The features list might or might not include the node features, depending on 
        the value of use_node_attributes.
        ''' 
        raise NotImplementedError('You need to implement this method')
    
    def predict(self, graph, test_indices, conditional_node_to_label_map = None):
        '''
        This function should be called only after the fit function is called.
        Predict the labels of test Nodes conditioning on the labels in conditional_node_to_label_map.
        conditional_node_to_label_map might include the observed and predicted labels.        
        This method is NOT iterative; it does NOT update conditional_node_to_label_map.
        '''
        raise NotImplementedError('You need to implement this method')

class ICA(Classifier):
    
    def __init__(self, local_classifier, relational_classifier, max_iteration = 10):
        self.local_classifier = local_classifier
        self.relational_classifier = relational_classifier
        self.max_iteration = 10
    
    
    def fit(self, graph, train_indices):
        self.local_classifier.fit(graph, train_indices)
        self.relational_classifier.fit(graph, train_indices)
    
    def predict(self, graph, test_indices, conditional_node_to_label_map = None):
        '''
        This function should be called only after the fit function is called.
        Implement ICA using the local classifier and the relational classifier.
        '''
        raise NotImplementedError('You need to implement this method')
    