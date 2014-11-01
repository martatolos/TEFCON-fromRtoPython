"""
This module provides an example of how to run Kmeans from Scikit - Learn
"""
__author__ = 'zoraida'
__version__ = "1.0"
__email__ = "zoraida@tid.es"


from HourlyPowerConsumptions import HourlyPowerConsumptions
from visualizations import plot_barchart
import numpy as np
from sklearn.cluster import KMeans


if __name__ == "__main__":
    # Should be changed to be pased as parameters
    dir_path = "/Users/zoraida/Desktop/TEFCON/all-country-data/hourly"
    pattern = "/Hourly_201*month*.xls"

    pc = HourlyPowerConsumptions(dir_path, pattern, skiprows=9, maxcolumns=26, hourchange='3B:00:00')

    country = "ES"# country to analyse
    df = pc.normalized_hourly_country_data(country)

    kmeans = KMeans(init='k-means++', n_clusters=2, n_init=10)

    labels_ = kmeans.fit_predict(df.iloc[:, 4:28].values)

    df["Cluster"] = labels_

    df = df.reset_index()

    df_cluster1 = df[df.Cluster == 1]
    df_cluster0 = df[df.Cluster == 0]

    print("Cluster 1\n")
    print(df_cluster1.weekday.value_counts())
    print("Cluster 0\n")
    print(df_cluster0.weekday.value_counts())

    # Histogram for weekday
    c1 = df_cluster0.weekday.value_counts(sort=False).values
    c2 = df_cluster1.weekday.value_counts(sort=False).values

    chart_matrix = np.asarray([c1, c2])
    ylabel = 'Observations'
    title = 'Weekday'
    xticklabels = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
    legend = ('Cluster 0', 'Cluster 1')

    #plot_barchart(chart_matrix.T, None, ylabel, title, xticklabels, legend, width=0.35)

    # Histogram for month
    c1 = df_cluster0.month.value_counts(sort=False).values
    c2 = df_cluster1.month.value_counts(sort=False).values

    chart_matrix = np.asarray([c1, c2])
    ylabel = 'Observations'
    title = 'Month'
    xticklabels = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')
    legend = ('Cluster 0', 'Cluster 1')

    plot_barchart(chart_matrix.T, None, ylabel, title, xticklabels, legend, width=0.35)

    # Histogram for year
    c1 = df_cluster0.year.value_counts(sort=False).values
    c2 = df_cluster1.year.value_counts(sort=False).values

    chart_matrix = np.asarray([c1, c2])
    ylabel = 'Observations'
    title = 'Year'
    xticklabels = ('2010', '2011', '2012', '2013')
    legend = ('Cluster 0', 'Cluster 1')

    plot_barchart(chart_matrix.T, None, ylabel, title, xticklabels, legend, width=0.35)
