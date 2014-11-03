"""
This module provides an example of how to run LinearRegression from Scikit-Learn
"""
__author__ = 'zoraida'
__version__ = "1.0"
__email__ = "zoraida@tid.es"


from hourlypowerconsumptions import HourlyPowerConsumptions

import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from visualizations import plot_regression


def plot_univariate_regression(regressor, X_train, y_train, X_test, y_test, x_label, y_label):
    """
    Expects X to be of the shape(N,1) were N is the number of observations and only
    one explanatory variable is given
    :param regressor: LinearRegression object to fit and predict
    :param X_train: Explanatory variable for the observations training set
    :param y_train: Target variable for the observations training set
    :param X_test: Explanatory variable for the observations testing set
    :param y_test: Target variable for the observations testing set
    :return: None
    """
    y_pred = evaluate(regressor, X_train, y_train, X_test, y_test)
    plot_regression(X_test, y_test, y_pred, x_label, y_label)


def evaluate(regressor, X_train, y_train, X_test, y_test):
    """
    Given a regressor, it fits the model with X_train and y_train
    and then predicts for X_test. Prints the Variance score. Best possible score is 1.0, lower values are worse.
    :param regressor: the regressor
    :param X_train:
    :param y_train:
    :param X_test:
    :param y_test:
    :return: None
    """

    regressor.fit(X_train, y_train)

    y_pred = regressor.predict(X_test)

    print('Coefficients: \n', regressor.coef_)
    # The mean square error
    print("Residual sum of squares: %.2f"
          % np.mean((y_pred - y_test) ** 2))
    # Explained variance score: 1 is perfect prediction
    print('Variance score: %.2f' % regressor.score(X_test, y_test))

    return y_pred


def plot_curves(x, y_pred, y_test, x_label, y_label, legend):
    """
    It plots to curves, the truth and the predicted
    :param x: 1 dim array for x
    :param y_pred: 1 dim array for predicted curve
    :param y_test: 1 dim array for truth curve
    :param x_label: x label
    :param y_label: y label
    :param legend: legend (expected of size 2)
    :return:
    """
    if not isinstance(y_pred, np.ndarray):
        y_pred = np.asarray(y_pred)

    if not isinstance(y_test, np.ndarray):
        y_test = np.asarray(y_test)

    if not isinstance(x, np.ndarray):
        x = np.asarray(x)

    # Plot outputs
    plt.plot(x, y_pred)
    plt.plot(x, y_test)

    plt.legend(legend, loc='upper left')
    plt.axis([x.min() - 0.2, x.max() + 0.2, y_test.min() - 0.2, y_test.max() + 0.2])
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    plt.show()


if __name__ == "__main__":
    # Should be changed to be pased as parameters
    dir_path = "/Users/mtolos/BoxSyncPrivado/Box Sync/Projecte/all-country-data"
    pattern = "/Hourly_201*month*.xls"
    year = 2013 # year to predict
    country = 'ES' # country to predict

    pc = HourlyPowerConsumptions(dir_path, pattern, skiprows=9,
                                 maxcolumns=26, hourchange='3B:00:00')
    # get data transformed: country | 01-01-2011 | 01-01-2012 | 01-01-2013 |
    # ... | 31-12-2011 | 31-12-2012 | 31-12-2013

    df = pc.historical_daily_aggregates(country, year, num_years=3)

    df = df[df.date != '2012-02-29']

    y_pred_matrix = []
    y_test_matrix = []

    y_train = df[df.year.isin(range(year-3,year))].Consumption.values
    y_test = df[df.year == year].Consumption.values

    X_train = var = df[df.year.isin(
        range(year - 3, year))][['month','year', 'weekday']].values
    X_test = df[df.year == year][['month','year','weekday']].values

    regressor = LinearRegression()

    # Univariate regressions
    X_train_T = X_train.astype(int)
    X_test_T = X_test.astype(int)

    plot_univariate_regression(regressor, X_train_T[:,[0]], y_train,
                               X_test_T[:,[0]], y_test, 'Month', 'Consumption')
    plot_univariate_regression(regressor,
                               X_train_T[:,[1]], y_train, X_test_T[:,[1]],
                               y_test, 'Year', 'Consumption')
    plot_univariate_regression(regressor, X_train_T[:,[2]], y_train,
                               X_test_T[:,[2]], y_test,
                               'Weekday', 'Consumption')

    vec = OneHotEncoder(sparse=False, categorical_features=[0, 2])
    X_train_T = vec.fit_transform(X_train).astype(int)
    X_test_T = vec.transform(X_test).astype(int)

    # Returns prediction of a day consumption for all the countries
    y_pred = evaluate(regressor, X_train_T, y_train, X_test_T, y_test)

    # 2013 no es bisiesto, ojo con eso
    plot_curves(range(1, 366), y_pred, y_test, 'Days of the year',
                country + ' Consumption', ['Predicted', 'Truth'])