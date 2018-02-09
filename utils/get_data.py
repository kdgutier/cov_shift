#!/usr/bin/env python
# coding: utf-8

import numpy as np
import math
from sklearn import mixture
import scipy.stats as st

import matplotlib.pyplot as plt
import matplotlib.collections as mcol
import matplotlib.transforms as mtransforms
from matplotlib.legend_handler import HandlerPathCollection
from matplotlib import cm

def gaussian_mixture(n, means, covs, probs):
    k, d = means.shape[0], means.shape[1]
    assert means.shape[0] == covs.shape[0]

    pops = np.random.choice(range(k), p=probs, size=n)
    samples = np.zeros(shape = (n,d))
    for idx, pop in np.ndenumerate(pops):
        sample = np.random.multivariate_normal(means[pop], covs[pop], 1)
        samples[idx] = sample
    return samples

def conditional_expectation(conditional_func, X):
    y = np.zeros(shape=(X.shape[0]))
    for idx in range(X.shape[0]):
        y[idx] = conditional_func(X[idx,:])
    return y

def toy_class(x):
    p = .5 * (1 + math.tanh(x[0]+min(0, x[1])))
    y = np.random.choice([0, 1], p = [p, 1-p])
    return y

def get_data_sugiyama(n_train, n_test):
    means_train = np.array([[-2, 3], [2, 3]])
    covs_train = np.array([[[1, 0],[0, 2]],[[1, 0],[0, 2]]])
    probs_train = np.array([.5, .5])
    
    means_test = np.array([[0, -1], [4, -1]])
    covs_test = np.array([[[1, 0],[0, 1]],[[1, 0],[0, 1]]])
    probs_test = np.array([.5, .5])
    
    X_train = gaussian_mixture(n_train, means_train, covs_train, probs_train)
    X_test = gaussian_mixture(n_test, means_test, covs_test, probs_test)
    
    y_train = conditional_expectation(toy_class, X_train)
    y_test = conditional_expectation(toy_class, X_test)

    return X_train, y_train, X_test, y_test


def graph_data1(config, data, path):
    X_train, X_test = data["X_train"], data["X_test"]
    
    x0min, x0max = -4, 7
    x1min, x1max = -3, 7

    # Peform the kernel density estimate for X_train
    x0 = X_train[:, 0]
    x1 = X_train[:, 1]
    xx0, xx1 = np.mgrid[x0min:x0max:100j, x1min:x0max:100j]
    positions = np.vstack([xx0.ravel(), xx1.ravel()])
    values = np.vstack([x0, x1])
    kernel = st.gaussian_kde(values)
    f_train = np.reshape(kernel(positions).T, xx0.shape)

    # Peform the kernel density estimate for X_train
    x0 = X_test[:, 0]
    x1 = X_test[:, 1]
    xx0, xx1 = np.mgrid[x0min:x0max:100j, x1min:x0max:100j]
    positions = np.vstack([xx0.ravel(), xx1.ravel()])
    values = np.vstack([x0, x1])
    kernel = st.gaussian_kde(values)
    f_test = np.reshape(kernel(positions).T, xx0.shape)

    fig = plt.figure()
    ax = fig.gca()
    ax.set_xlim(x0min, x0max)
    ax.set_ylim(x1min, x1max)

    # Contour plot, and label
    cset_train = ax.contour(xx0, xx1, f_train, linewidths=.5, colors='k')
    ax.clabel(cset_train, inline=1, fontsize=7)

    # Contour plot, and label
    cset_test = ax.contour(xx0, xx1, f_test, linewidths=.5, colors='k')
    ax.clabel(cset_test, inline=1, fontsize=7)
    
    #plotting model
    aux_x1 = np.arange(0, 8, .1)
    aux_x0 = (0 * aux_x1)
    model_x0, model_x1 = aux_x0, aux_x1
    aux_x0 = np.arange(0, 4, .1)
    aux_x1 = (-1 * aux_x0)
    model_x0 = np.concatenate((model_x0, aux_x0))
    model_x1 = np.concatenate((model_x1, aux_x1))
    plt.plot(model_x0, model_x1, color = 'black', label = 'Conditional Expectation')

    ax.annotate('Negative', xy=(-3, 7), xytext=(-3, 6))
    ax.annotate('Positive', xy=(-3, 7), xytext=(1.5, 6))

    ax.annotate('Training', xy=(-3, 7), xytext=(5, 3))
    ax.annotate('Test', xy=(-3, 7), xytext=(5, -.9))

    plt.savefig(path)
class HandlerMultiPathCollection(HandlerPathCollection):
    """
    Handler for PathCollections, which are used by scatter
    """
    def create_collection(self, orig_handle, sizes, offsets, transOffset):
        p = type(orig_handle)(orig_handle.get_paths(), sizes=sizes,
                              offsets=offsets,
                              transOffset=transOffset,
                              )
        return p

def graph_data2(config, data, path):
    #https://stackoverflow.com/questions/31478077/how-to-make-two-markers-share-the-same-label-in-the-legend-using-matplotlib
    fig, ax = plt.subplots()
    #make some data to plot
    n_train = config["n_train"]
    X_train, y_train, X_test, y_test = data["X_train"], data["y_train"], data["X_test"], data["y_test"]
    x0_train, x1_train, x0_test, x1_test = X_train[:,0], X_train[:,1], X_test[:,0], X_test[:,1]
    x0, x1 = np.concatenate((x0_train, x0_test)), np.concatenate((x1_train, x1_test))
    
    x0min, x0max = -4, 7
    x1min, x1max = -3, 7
    
    #make colors and markers
    #markers_train, markers_test  =  * n_train, [u's'] * n_test
    markers_train = [u'o' if y <=0 else u'x' for y in y_train]
    markers_test = [u's' if y <=0 else u'+' for y in y_test]
    markers = markers_train + markers_test
    colors_train = ["#E99F51" if y <=0 else "#386D9D" for y in y_train] #(233, 159, 81), (56, 109, 157)
    colors_test = ["#E99F51" if y <=0 else "#386D9D" for y in y_test]
    colors = colors_train + colors_test
    ec_colors = ["#F1F0EE"] * len(colors)
    #plot points and lines
    plots = []
    for _x0, _x1, _m, _c, _ec in zip(x0, x1, markers, colors, ec_colors):
        plot = plt.scatter(_x0, _x1, marker=_m, c=_c, edgecolors=_ec)
        plots.append(plot)
    
    #plotting model
    aux_x1 = np.arange(0, 8, .1)
    aux_x0 = (0 * aux_x1)
    model_x0, model_x1 = aux_x0, aux_x1
    aux_x0 = np.arange(0, 4, .1)
    aux_x1 = (-1 * aux_x0)
    model_x0 = np.concatenate((model_x0, aux_x0))
    model_x1 = np.concatenate((model_x1, aux_x1))
    line, = plt.plot(model_x0, model_x1, color = 'black', label = 'Conditional Expectation')
    
    #get attributes
    train1, train0 = np.where( y_train == 1 )[0][0], np.where( y_train == 0 )[0][0]
    test1, test0 = np.where( y_test == 1 )[0][0], np.where( y_test == 0 )[0][0]
    
    ids = list(map(int, [train1, train0]))
    plots_train = [plots[i] for i in ids]
    
    paths_train = []
    sizes_train = []
    facecolors_train = []
    edgecolors_train = []
    for plot in plots_train:
        paths_train.append(plot.get_paths()[0])
        sizes_train.append(plot.get_sizes()[0])
        edgecolors_train.append(plot.get_edgecolors()[0])
        facecolors_train.append(plot.get_facecolors()[0])
    
    ids = list(map(int, [n_train + test1, n_train + test0]))
    plots_test = [plots[i] for i in ids]

    paths_test = []
    sizes_test = []
    facecolors_test = []
    edgecolors_test = []
    for plot in plots_test:
        paths_test.append(plot.get_paths()[0])
        sizes_test.append(plot.get_sizes()[0])
        edgecolors_test.append(plot.get_edgecolors()[0])
        facecolors_test.append(plot.get_facecolors()[0])

    ax.set_xlim(x0min, x0max)
    ax.set_ylim(x1min, x1max)

    #make proxy artist out of a collection of markers
    PC_train = mcol.PathCollection(paths_train, sizes_train, transOffset = ax.transData, facecolors = colors, edgecolors = edgecolors_train)
    PC_train.set_transform(mtransforms.IdentityTransform())
    PC_test = mcol.PathCollection(paths_test, sizes_test, transOffset = ax.transData, facecolors = colors, edgecolors = edgecolors_test)
    PC_test.set_transform(mtransforms.IdentityTransform()) #+paths_test
    plt.legend([PC_train, PC_test, line], ['P & N Train','P & N Test', 'Model'], handler_map = {type(PC_train) : HandlerMultiPathCollection()}, scatterpoints = len(paths_train), scatteryoffsets = [.5], handlelength = len(paths_train))
    plt.savefig(path)


def main():
    np.random.seed(seed=1234)
    root = '/Users/kdgutier/Desktop/cov_shift/'
    
    n_train, n_test = 60, 30
    X_train, y_train, X_test, y_test = get_data_sugiyama(n_train, n_test)

    data = {"X_train": X_train, "y_train": y_train, "X_test": X_test, "y_test": y_test}
    config = {"n_train": n_train, "n_test": n_test}
    
    graph_data1(config, data, path = root+'images/sugiyama1.png')
    graph_data2(config, data, path = root+'images/sugiyama2.png')




if __name__ == '__main__':
    main()

    