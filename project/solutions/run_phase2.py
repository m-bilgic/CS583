from data_utils import load_linqs_data
from classifiers import LocalClassifier
from classifiers import RelationalClassifier

from classifiers import CountAggregator, ProportionalAggregator, ExistAggregator

from sklearn.metrics import accuracy_score
from sklearn.cross_validation import train_test_split
import numpy as np


from collections import defaultdict

import argparse

def pick_aggregator(agg,domain_labels,directed):
    if agg=='count':
        aggregator=CountAggregator(domain_labels,directed)
    if agg=='prop':
        aggregator=ProportionalAggregator(domain_labels,directed)
    if agg=='exist':
        aggregator=ExistAggregator(domain_labels,directed)
    return aggregator

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-content_file', help='The path to the content file.')
    parser.add_argument('-cites_file', help='The path to the cites file.')    
    parser.add_argument('-classifier', default='sklearn.linear_model.LogisticRegression', help='The underlying classifier.')
    parser.add_argument('-num_trials', type=int, default=10, help='The number of trials.')
    parser.add_argument('-aggregate', choices=['count', 'prop', 'exist'], default='exist', help='The aggreagate function.')
    parser.add_argument('-directed', default=False, action='store_true', help='Use direction of the edges for aggregates.')
    parser.add_argument('-dont_use_node_attributes',default=False,help="Dont use the node attributes in relational classify.")
    args = parser.parse_args()
    
    graph, domain_labels = load_linqs_data(args.content_file, args.cites_file)
    
    budget=[0.1, 0.2, 0.3, 0.4, 0.6, 0.7, 0.8, 0.9]

    n=range(len(graph.node_list))

    local_accuracies = defaultdict(list)
    relational_accuracies = defaultdict(list)


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
            agg=pick_aggregator(args.aggregate,domain_labels,args.directed)
            relational_clf=RelationalClassifier(args.classifier,agg,args.dont_use_node_attributes)
            relational_clf.fit(graph,train)
            relational_y_pred=relational_clf.predict(graph,test)
            relational_accuracy=accuracy_score(y_true,relational_y_pred)
            relational_accuracies[b].append(relational_accuracy)

    
    #compute the mean
    # local_mean=[]
    # relational_mean=[]
    print "budget\tlocal accuracy\trelational accuracy"
    for b in budget:
        print str(b)+'\t\t'+str(np.mean(local_accuracies[b]))+'\t\t'+str(np.mean(relational_accuracies[b]))
        # local_mean.append(np.mean(local_accuracies[b]))
        # print 'local=',local_mean
        # relational_mean.append(np.mean(relational_accuracies[b]))
        # print 'relation=',relation_mean

    # n_groups=len(budget)
    # fig=plt.plot()
    # index=np.arange(n_groups)
    # bar_width=0.35
    #
    # opacity = 0.4
    # rects1 = plt.bar(index, local_mean, bar_width,alpha=opacity, color='b',label='local_mean')
    # rects2 = plt.bar(index + bar_width, relational_mean, bar_width,alpha=opacity,color='r',label='relation_mean')
    #
    # plt.xlabel('Budget')
    # plt.ylabel('Accuracy')
    # plt.title('Accuracy by Budget and different classifiers')
    # plt.xticks(index + bar_width, tuple(budget))
    # plt.ylim(0,1)
    # plt.legend(loc=2)
    #
    # plt.tight_layout()
    # plt.show()

    
        
    
    
