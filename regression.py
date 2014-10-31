_author__ = 'zoraida'
__version__ = "1.0"
__email__ = "zoraida@tid.es"


from HourlyPowerConsumptions import HourlyPowerConsumptions

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction import DictVectorizer


def evaluate (X_train, y_train, X_test, y_test, regressor):

    regressor.fit(X_train, y_train)

    y_pred = regression.predict(X_test)

    print('Coefficients: \n', regression.coef_)
    # The mean square error
    print("Residual sum of squares: %.2f"
          % np.mean((y_pred - y_test) ** 2))
    # Explained variance score: 1 is perfect prediction
    print('Variance score: %.2f' % regression.score(X_test, y_test))

    return y_pred

def plot_curves(x, y_pred, y_test, x_label, y_label, legend):
    # Plot outputs
    plt.plot(x, y_pred)
    plt.plot(x, y_test)

    plt.legend(legend, loc='upper left')
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    plt.show()


if __name__ == "__main__":
    dir_path = "/Users/mtolos/BoxSyncPrivado/Box Sync/Projecte/all-country-data"
    pattern = "/Hourly_201*month*.xls"
    # year to predict
    year = 2013
    country = 'ES'

    pc = HourlyPowerConsumptions(dir_path, pattern, skiprows=9,
                           maxcolumns=26, hourchange='3B:00:00')
    # get data transformed: country | 01-01-2011 | 01-01-2012 | 01-01-2013 |
    # ... | 31-12-2011 | 31-12-2012 | 31-12-2013

    df = pc.historical_daily_aggregates(country, year, num_years = 3)

    df = df[df.date != '2012-02-01']

    y_pred_matrix = []
    y_test_matrix = []
    regression = LinearRegression()



    y_train = df[df.year.isin(range(year-3,year))].Consumption.values
    y_test = df[df.year == year].Consumption.values


    X_train = var = df[df.year.isin(range(year - 3, year))][
        ['month', 'year', 'weekday']].values

    X_test = df[df.year == year][['month','year','weekday']].values

    vec = OneHotEncoder(sparse=False, categorical_features=[0,2])
    X_train_T = vec.fit_transform(X_train).astype(int)
    X_test_T = vec.transform(X_test).astype(int)

    # Returns prediction of a day consumption for all the countries
    y_pred = evaluate(X_train_T, y_train, X_test_T, y_test, regression)

    # 2013 no es bisiesto, ojo con eso
    plot_curves(range(1, 366), y_pred, y_test, 'Days of the year',
                country + ' Consumption', ['Predicted', 'Truth'])
