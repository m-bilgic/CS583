from data_utils import load_cora

from sklearn.cross_validation import KFold

from classifiers import LocalClassifier

from sklearn.metrics import accuracy_score

import numpy as np

if __name__ == '__main__':

    content_path="G:/IIT/CS583 TA/project/cora/cora.content"
    cites_path="G:/IIT/CS583 TA/project/cora/cora.cites"
    path = [content_path,cites_path]
    graph = load_cora(path)
    
    kf = KFold(n=len(graph.node_list), n_folds=10, shuffle=True, random_state=42)
    
    classifier_name = "sklearn.linear_model.LogisticRegression"
    
    accuracies = []
    
    for train, test in kf:
        clf = LocalClassifier(classifier_name)
        clf.fit(graph, train)
        y_pred = clf.predict(graph, test)
        y_true = [graph.node_list[t].label for t in test]
        accuracies.append(accuracy_score(y_true, y_pred))

    
    print accuracies
    print "Mean accuracy: %0.4f +- %0.4f" % (np.mean(accuracies), np.std(accuracies))
        
    
    