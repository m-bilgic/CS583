from data_utils import load_linqs_data
from classifiers import LocalClassifier
from classifiers import RelationalClassifier
from classifiers import CountAggregator

from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.cross_validation import train_test_split
import numpy as np

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
    
    for t in range(args.num_trials):
        for b in budget:
            train, test ... = train_test_split(..., train_size=b, random_state=t)
            # local classifier fit and test
            local_accuracies[b].append(accuracy)
            # relational classifier fit and test
            relational_accuracies[b].append(accuracy)
    
    #compute the mean
    for b in budget:
        local_mean = np.mean(local_accuracies[b])
    
        
    
    
