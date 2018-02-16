#!/usr/bin/env python
# coding: utf-8

import numpy as np
from sklearn import svm

import utils.get_data as data
import utils.plots as plots

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression

def svm_classifier(config, data):
    X_train, y_train = data["X_train"], data["y_train"]
    C = 1.0  # SVM regularization parameter
    model = svm.SVC(kernel = 'linear',  gamma=0.7, C=C )
    model.fit(X_train, y_train)
    return model

def lda_propscores(n_clusters, X_propscore, X_train):
    X_propscore, y_propscore = data.parse_data_propscore(n_clusters, X_propscore)
    clf = LinearDiscriminantAnalysis(solver='lsqr', shrinkage='auto').fit(X_propscore, y_propscore)
    propscores  = clf.predict_proba(X_train)
    return propscores

def iw2s_logistic(n_clusters, X_propscore, X_train, X_test):
    propscores  = lda_propscores(n_clusters, X_propscore, X_train)
    print(propscores.shape)

def main():
    import utils.get_data as data
    import utils.plots as plots

    np.random.seed(seed=1234)
    root = '/Users/kdgutier/Desktop/cov_shift/'
    #
    #n_train, n_test = 60, 30
    #X_train, y_train, X_test, y_test = data.get_data_sugiyama(n_train, n_test)
    #
    #data = {"X_train": X_train, "y_train": y_train, "X_test": X_test, "y_test": y_test}
    #config = {"n_train": n_train, "n_test": n_test}
    #
    #
    #model = svm_classifier(config, data)
    #plots.graph_data_sugiyama1(config, data, path = root+'images/sugiyama1.png')
    #plots.graph_data_sugiyama2(config, data, model0 = model, path = root+'images/sugiyama2.png')

    np.random.seed(seed=1234)
    root = '/Users/kdgutier/Desktop/cov_shift/'

    n_clusters, r, n_grid = 6, 4, 20
    n_samples = 120
    X, Y, V = data.get_data_experiment(n_samples, n_clusters, r, n_grid)
    plots.graph_data_experiment(n_clusters, X, Y, V, path=(root+'images/experiment2.png') )

    data.save_data_experiment(n_clusters, X, Y, V, path=(root + 'data/'))
    X, Y, V = data.load_data_experiment(n_clusters, path=(root + 'data/'))

    data = data.split_data_experiment(n_clusters, X, Y)

if __name__ == '__main__':
    main()