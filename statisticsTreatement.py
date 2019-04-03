import numpy as np
from scipy import stats
import pandas as pd

csvDataSetFile_v1 = '/Users/Hilmer/Documents/hilmer/UFRJ/2019.2/dataset_SQPC1_Parasite_v1.csv'
df_v1 = pd.read_csv(csvDataSetFile_v1, sep=';',header=None, names=['T_Effectiveness', 'T_Efficiency', 'T_Satisfaction'])

csvDataSetFile_v2 = '/Users/Hilmer/Documents/hilmer/UFRJ/2019.2/dataset_SQPC1_Parasite_v2.csv'
df_v2 = pd.read_csv(csvDataSetFile_v1, sep=';',header=None, names=['T_Effectiveness', 'T_Efficiency', 'T_Satisfaction'])


'''
print(np.random.random_sample((15,1)))
print(np.random.random_sample((15,1)))
print(np.random.random_sample((15,1)))

'''

dist = np.concatenate((df_v1.values, df_v2.values), axis=0)


k2, normal_Test_Pval = stats.normaltest(np.array(dist).astype(float), axis=None)

if (normal_Test_Pval < 0.055):
    print(" isn't a normal distribution")
    print(stats.kruskal(np.array(df_v1.values).astype(float), np.array(df_v2.values).astype(float)))
else:
    print(" is a Normal distribution")

