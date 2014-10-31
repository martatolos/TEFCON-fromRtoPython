__author__ = 'zoraida'
__version__ = "1.0"
__email__ = "zoraida@tid.es"


from HourlyPowerConsumptions import HourlyPowerConsumptions
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans



if __name__ == "__main__":
    dir_path = "/Users/mtolos/BoxSyncPrivado/Box Sync/Projecte/all-country-data"
    pattern = "/Hourly_201*month*.xls"


    pc = HourlyPowerConsumptions(dir_path, pattern, skiprows=9, maxcolumns=26, hourchange='3B:00:00')

    country = "ES"

    df = pc.normalized_hourly_country_data(country)

    kmeans = KMeans(init='k-means++', n_clusters=2, n_init=10)

    labels_ = kmeans.fit_predict(df.iloc[:,4:28].values)

    print labels_

    df["Cluster"] = labels_

    df = df.reset_index()

    df_cluster1 = df[df.Cluster==1]
    df_cluster0 = df[df.Cluster==0]

    print("Cluster 1\n")
    print(df_cluster1.weekday.value_counts())
    print("Cluster 0\n")
    print(df_cluster0.weekday.value_counts())
