from sklearn.tree import DecisionTreeClassifier

def abstract():
    import inspect
    caller = inspect.getouterframes(inspect.currentframe())[1][3]
    raise NotImplementedError(caller + ' must be implemented in subclass')

class Aggregator(object):
    
    def __init__(self, directed = False):
        self.directed = directed
    
    def aggregate(self, graph, node, train_indices): 
        # TODO: We need to keep track of predicted labels somewhere or pass them to this function
        # We can create a predicted label variable in the Node class and set it everytime we predict something for it
        abstract()

class Classifier(object):
    '''
    The base classifier object
    '''

    def __init__(self, scikit_classifier_name):
        self.scikit_classifier_name = scikit_classifier_name
    
    
    def fit(self, graph, train_indices):
        '''
        Create a scikit-learn classifier object and fit it using the Nodes of the Graph
        that are referenced in the train_indices
        '''
        abstract()
    
    def predict(self, graph, test_indices):
        '''
        This function should be called only after the fit function is called.
        Predict the labels of test Nodes assuming the labels of the train Nodes are observed.
        '''
        abstract()

class LocalClassifier(Classifier):

    def __init__(self,scikit_classifier_name):
        super(LocalClassifier,self).__init__(scikit_classifier_name)
        self.classifier=DecisionTreeClassifier()

    def fit(self, graph, train_indices):
        '''
        Create a scikit-learn classifier and fit it to the Node attributes
        ''' 
        # abstract()
        X=[graph.node_list[t].feature_vector for t in train_indices]
        y=[graph.node_list[t].label for t in train_indices]
        self.classifier.fit(X,y)


    def predict(self, graph, test_indices):
        '''
        This function should be called only after the fit function is called.
        Predict the labels of test Nodes assuming the labels of the train Nodes are observed.
        Use only the node attributes for prediction.
        '''
        # abstract()
        X=[graph.node_list[t].feature_vector for t in test_indices]
        return self.classifier.predict(X)

class RelationalClassifier(Classifier):
    
    def __init__(self, scikit_classifier_name, aggregator, use_node_attributes = False):
        super(RelationalClassifier, self).__init__(scikit_classifier_name)
        self.aggregator = aggregator
        self.use_node_attributes = use_node_attributes
    
    def fit(self, graph, train_indices):
        '''
        Create a scikit-learn classifier and fit it to relational (+ potentially node) attributes
        ''' 
        abstract()
    
    def predict(self, graph, test_indices):
        '''
        This function should be called only after the fit function is called.
        Predict the labels of test Nodes assuming the labels of the train Nodes are observed.
        Use relational (+ potentially node) attributes for prediction.
        '''
        abstract()

class ICA(Classifier):
    
    def __init__(self, local_classifier, relational_classifier, max_iteration = 10):
        self.local_classifier = local_classifier
        self.relational_classifier = relational_classifier
        self.max_iteration = 10
    
    
    def fit(self, graph, train_indices):
        self.local_classifier.fit(graph, train_indices)
        self.relational_classifier.fit(graph, train_indices)
    
    def predict(self, graph, train_indices, test_indices):
        '''
        This function should be called only after the fit function is called.
        Iteratively, predict the labels of all Nodes that are in the graph but not in train indices.
        '''
        abstract()
    