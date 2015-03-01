from data_utils import load_linqs_data
from classifiers import LocalClassifier


from sklearn.cross_validation import KFold
from sklearn.metrics import accuracy_score, confusion_matrix
import numpy as np

import argparse

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-content_file', help='The path to the content file.')
    parser.add_argument('-cites_file', help='The path to the cites file.')    
    parser.add_argument('-classifier', default='sklearn.linear_model.LogisticRegression', help='The underlying classifier.')
    parser.add_argument('-num_folds', type=int, default=10, help='The number of folds.')
    
    args = parser.parse_args()
    
    graph, domain_labels = load_linqs_data(args.content_file, args.cites_file)
    
    kf = KFold(n=len(graph.node_list), n_folds=args.num_folds, shuffle=True, random_state=42)    
    
    
    accuracies = []
    
    cm = None
    
    for train, test in kf:
        clf = LocalClassifier(args.classifier)
        clf.fit(graph, train)
        y_pred = clf.predict(graph,train, test)
        y_true = [graph.node_list[t].label for t in test]
        accuracies.append(accuracy_score(y_true, y_pred))
        if cm is None:
            cm = confusion_matrix(y_true, y_pred, labels = domain_labels)
        else:
            cm += confusion_matrix(y_true, y_pred, labels = domain_labels)

    
    print accuracies
    print "Mean accuracy: %0.4f +- %0.4f" % (np.mean(accuracies), np.std(accuracies))
    print cm
        
    
    