"""
This module provides some functions to visualize the data
"""
__author__ = 'zoraida'
__version__ = "1.0"
__email__ = "zoraida@tid.es"

import numpy as np
import matplotlib.pyplot as plt


def plot_regression(x, y_truth, y_pred, x_label, y_label):
    """
    It plots a linear regression with the observations.
    :param X: Explanatory variables(numpy array of shape (n, m))
    :param y_truth: Response variable(numpy array of shape (n,))(Truth)
    :param y_pred: Predicted response variable(numpy array of shape (n,))
    :return: None
    """
    plt.scatter(x, y_truth,  color='black')
    plt.plot(x, y_pred, color='blue', linewidth=3)
    plt.axis([x.min() - 0.2, x.max() + 0.2, y_truth.min() - 0.2,
              y_truth.max() + 0.2])
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    plt.show()


def plot_barchart(chart_matrix, xlabel, ylabel, title, xticklabels,
                  legend, width=0.35):
    """
    Plots bars chart.
    :param chart_matrix: numpy array of shape(n_feature_categories, n_clusters)
    :param xlabel: label for x axis
    :param ylabel: label for y axis
    :param title: title for the chart
    :param xticklabels: tick labels for x
    :param legend: legend for clusters
    :param width: bar width
    :return: None
    """
    index = np.arange(chart_matrix.shape[0]).astype(int)
    fig, ax = plt.subplots()
    bars = []

    for idx, target in enumerate(chart_matrix.T):
        bars.append(ax.bar(left=index + (width * idx), height=target,
                           width=width, color=np.random.rand(3,1)))

    # add some text for labels, title and axes ticks
    ax.set_ylabel(ylabel)
    if xlabel:
        ax.set_xlabel(xlabel)
    ax.set_title(title)
    ax.set_xticks(index + (width * idx))
    ax.set_xticklabels(xticklabels)

    ax.legend(tuple(bars), legend)
    plt.show()