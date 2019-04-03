import numpy as np
import seaborn as sns
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

#Parâmetros do data set


csvDataSetFile = '/Users/Hilmer/Documents/hilmer/UFRJ/2019.2/dataset_SQPC1_Parasite_v1.csv'
df = pd.read_csv(csvDataSetFile, sep=';',header=None, names=['T_Effectiveness', 'T_Efficiency', 'T_Satisfaction'])


k2, normal_Test_Pval = stats.normaltest(np.array(df.values).astype(float), axis=None)

if(normal_Test_Pval < 0.055):
    cm = df.corr(method='spearman')
else:
    cm = df.corr(method='pearson')

#cm = df.corr(method='spearman')
mask = np.zeros_like(cm)
mask[np.triu_indices_from(mask)] = True
with sns.axes_style("white"):
    sns.heatmap(cm, cmap="YlGnBu", annot=True, mask=mask, square=True)
plt.yticks(rotation=0)
plt.xticks(rotation=90)
plt.show()



