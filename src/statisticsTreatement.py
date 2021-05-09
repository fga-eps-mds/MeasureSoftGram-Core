import numpy as np
from scipy import stats
import pandas as pd

import plotly
import plotly.offline as py
import plotly.graph_objs as go
import plotly.express as px

'''
csvDataSetFile_v1 = '/Users/Hilmer/PycharmProjects/measuresoftgram/datasetPrototipo/dataset_SQPC1_Parasite_v1.csv'
df_v1 = pd.read_csv(csvDataSetFile_v1, sep=';',header=None, names=['T_Effectiveness', 'T_Efficiency', 'T_Satisfaction'])

csvDataSetFile_v2 = '/Users/Hilmer/PycharmProjects/measuresoftgram/datasetPrototipo/dataset_SQPC1_Parasite_v1.csv'
df_v2 = pd.read_csv(csvDataSetFile_v1, sep=';',header=None, names=['T_Effectiveness', 'T_Efficiency', 'T_Satisfaction'])
'''

'''
print(np.random.random_sample((15,1)))
print(np.random.random_sample((15,1)))
print(np.random.random_sample((15,1)))

'''

'''
q-rapids-csv-path = '/Users/Hilmer/PycharmProjects/measuresoftgram/datasetPrototipo/dataset_SQPC1_Parasite_v1.csv'
df_qrapids = pd.read_csv(csvDataSetFile_v1, sep=';',header=None, names=['qrapidsUQ'])

measuresoftgram-csv-path = '/Users/Hilmer/PycharmProjects/measuresoftgram/..../dataset-sqc-n.csv'
df_measuresoftgram = pd.read_csv(csvDataSetFile_v1, sep=';',header=None, names=['MeasureSoftGram-SQC_n'])
'''


'''

# H_0     : measuresoftgranSQC = qrapidsUQ (all sample distributions are equal. :D The initial results indicates that MeasuSoftGram is able to provide a multidimensional indicator to observe quality software in Tensor Spaces, with 95% of confidence!)
# H_Null  : measuresoftgranSQC < qrapidsUQ (at least two samples have a different distribution :( he initial results indicates that MeasuSoftGram   )



dist = np.concatenate((df_qrapids.values, df_measuresoftgram.values), axis=0)

k2, normal_Test_Pval = stats.normaltest(np.array(dist).astype(float), axis=None)


if (normal_Test_Pval < 0.05): # alpha value is 0.05 or 5%
    print(" isn't a normal distribution")
    
    # print(stats.kruskal(np.array(df_v1.['qrapidsUQ']).astype(float), np.array(df_v2.values).astype(float)))
    
    # alpha value is 0.05 or 5%
     alpha = 0.05
    
    #Kruskal-Wallis H Test
    kruskalStat, kruskalPval  = stats.kruskal(np.array(df_v1.values).astype(float), np.array(df_v2.values).astype(float))
    print('Statistics=%.3f, p=%.3f' % (kruskalStat, kruskalPval)) 
    
    # interpret 
    if kruskalPval > alpha:    
       print("Fail to reject H_0)")
    else:
      print("Different distributions, reject H_0")
      
    # Mann-Whitney U Test
    
    # compare samples
    mw_stat, mw_pval = mannwhitneyu(df_qrapids, data2)
    print('Statistics=%.3f, p=%.3f' % (mw_stat, mw_pval))
    # interpret
    alpha = 0.05
    if p > alpha:
        print('Same distribution (fail to reject H0)')
    else:
        print('Different distribution (reject H0)')
      
      
      
else:
    print(" is a Normal distribution")


    

'''

# traces with separate domains to form a subplot
trace1 = go.Indicator(mode="gauge+number",    value=400,    domain={'x': [0.0, 0.4], 'y': [0.0, 1]},    title={'text': "Speed 1"})

trace2 = go.Indicator(mode="gauge+number",    value=250,    domain={'x': [0.6, 1.0], 'y': [0., 1.00]},    title={'text': "Speed 2"})

# layout and figure production
layout = go.Layout(height = 600,
                   width = 600,
                   autosize = False,
                   title = 'Side by side gauge diagrams')
fig = go.Figure(data = [trace1, trace2], layout = layout)
fig.show()
