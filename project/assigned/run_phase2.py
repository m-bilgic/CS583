from data_utils import load_linqs_data
from classifiers import LocalClassifier
from classifiers import RelationalClassifier
from classifiers import CountAggregator

from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.cross_validation import train_test_split
import numpy as np
import matplotlib.pyplot as plt

from collections import defaultdict

import argparse

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-content_file', help='The path to the content file.')
    parser.add_argument('-cites_file', help='The path to the cites file.')    
    parser.add_argument('-classifier', default='sklearn.linear_model.LogisticRegression', help='The underlying classifier.')
    parser.add_argument('-num_trials', type=int, default=10, help='The number of trials.')
    parser.add_argument('-aggregate', choices=['count', 'prop', 'exist'], default='count', help='The aggreagate function.')
    parser.add_argument('-directed', default=False, action='store_true', help='Use direction of the edges for aggregates.')
    
    args = parser.parse_args()
    
    graph, domain_labels = load_linqs_data(args.content_file, args.cites_file)
    
    budget=[0.1, 0.2, 0.3, 0.4, 0.6, 0.7, 0.8, 0.9]

    n=range(len(graph.node_list))

    local_accuracies = defaultdict([])
    relational_accuracies = defaultdict([])


    for t in range(args.num_trials):
        for b in budget:
            train, test = train_test_split(n, train_size=b, random_state=t)
            
            # True labels
            y_true=[graph.node_list[t].label for t in test]
            
            # local classifier fit and test
            local_clf=LocalClassifier(args.classifier)
            local_clf.fit(graph,train)
            local_y_pred=local_clf.predict(graph,test)            
            local_accuracy=accuracy_score(y_true, local_y_pred)
            local_accuracies[b].append(local_accuracy)
            
            
            # relational classifier fit and test
            agg=CountAggregator(domain_labels,directed=True)
            relational_clf=RelationalClassifier(args.classifier,agg,use_node_attributes=True)            
            relational_clf.fit(graph,train)
            relational_y_pred=relational_clf.predict(graph,test)
            relational_accuracy=accuracy_score(y_true,relational_y_pred)
            relational_accuracies[b].append(relational_accuracy)

    
    #compute the mean
    local_mean=[]
    relational_mean=[]
    for b in budget:
        local_mean.append(np.mean(local_accuracies[b]))
        # print 'local=',local_mean
        relational_mean.append(np.mean(relational_accuracies[b]))
        # print 'relation=',relation_mean

    n_groups=len(budget)
    fig=plt.plot()
    index=np.arange(n_groups)
    bar_width=0.35

    opacity = 0.4
    rects1 = plt.bar(index, local_mean, bar_width,alpha=opacity, color='b',label='local_mean')
    rects2 = plt.bar(index + bar_width, relational_mean, bar_width,alpha=opacity,color='r',label='relation_mean')

    plt.xlabel('Budget')
    plt.ylabel('Accuracy')
    plt.title('Accuracy by Budget and different classifiers')
    plt.xticks(index + bar_width, tuple(budget))
    plt.ylim(0,1)
    plt.legend(loc=2)

    plt.tight_layout()
    plt.show()

    
        
    
    
