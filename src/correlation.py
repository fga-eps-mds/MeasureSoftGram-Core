import numpy as np
import seaborn as sns
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import tensorly as tl

#Parâmetros do data set


csvDataSetFile = '/Users/Hilmer/PycharmProjects/measuresoftgram/datasetPrototipo/dataset_SQPC1_Parasite_v1.csv'

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



a = np.array(df.values[:,0]).astype(float)
b = np.array(df.values[:,1]).astype(float)
c = np.array(df.values[:,2]).astype(float)
d = a
e = a

f = np.dstack([a,b,c,d,e])

print(f)
print(f.shape)
print(f[:,:,0])

# Cria um tensor 1D (vetor)
x1 = np.array([1, 2, 3])

# Cria uma nova dimensão/eixo a partir do tensor x1. # Logo x2 é um tensor-2D (matriz)
x2 = x1[:, np.newaxis]
# Insere o array [4, 5, 6] como se fosse a última coluna de x1, ou seja,
# os valores são inseridos no novo eixo/dimensão criado. O parâmetro 1
x2 = np.insert(x2, len(x1.shape), np.array([4, 5, 6]), axis=len(x1.shape))

# Cria uma nova dimensão/eixo a partir do tensor x2. # Logo x3 é um tensor-3D
x3 = x2[:, np.newaxis]
x3 = np.insert(x3, len(x2.shape), np.array([7, 8, 9]).reshape(1,3,1), axis=len(x2.shape))

# Cria uma nova dimensão/eixo a partir do tensor x3. # Logo x4 é um tensor-4D
x4 = x3[:, np.newaxis]
x4 = np.insert(x4, len(x3.shape), np.array([10, 11, 12]).reshape(1,3,1,1), axis=len(x3.shape))

# Cria uma nova dimensão/eixo a partir do tensor x4. # Logo x4 é um tensor-5D
x5 = x4[:, np.newaxis]
x5 = np.insert(x5, len(x4.shape), np.array([13, 14, 15]).reshape(1,3,1,1,1), axis=len(x4.shape))

# Insere o array [16, 17, 18, 19, 20] como se fosse a última linha de x5,
# ou seja, cada valor é inserido em sua respectiva dimensão/eixo. Simula
# uma inserção de acresecentar os valores coletados em um dia ao tensor
x6 = np.insert(x5, x5.shape[0], np.array((16, 17, 18, 19, 20)), axis=0)


print(x5.shape)
print(x5)



# Realiza em x5 um slice frontal no eixo/dimensão 0
print(x5[:,:,:,:,0])

# Realiza um slice no eixo/dimensão 0 e realiza a multiplicação por um outro tensor ou escalar
x5[:,:,:,:,0] *= [2]
print(x5[:,:,:,:,0])

T = tl.tensor(x5)

#print(T)

print(x6)
print(x6[:,:,:,:,0])
'''

print(tl.unfold(T, 0))
print(tl.unfold(T, 1))
print(tl.unfold(T, 2))
print(tl.unfold(T, 3))
print(tl.unfold(T, 4))

print( tl.tensor_to_vec(T))
'''

#print(tl.tenalg.mode_dot(T,np.array([2]),0))
print(T.ndim)
#Calculq a norma (todos os eixos) do tensor T com tensorly
print(tl.norm(T))
#Calculq a norma do tensor T em um eixo/dimensão específico. No caso, no 1o. eixo = 1, com tensorly.
# OBS: o 1o eixo possui indice 1
print(tl.norm(T,1))
print(tl.norm(T,2))
print(tl.norm(T,3))
print(tl.norm(T,4))


print(np.linalg.norm([13, 14, 15]))

# Realiza um slice frontal no tensor T no eixo/dimensão 0 (tipo 1a coluna)
q = T[:,:,:,:,0].astype(int)
#q = np.ndarray.take(T,)
w = np.array([2]).astype(int)
#print(tl.prod(q ,w))
# Realiza o produto Kronecher(0)  do sub tensor q com o vetor unitário (escalar que representa o peso),
# utilizando numpy
print(np.tensordot(q, w, 0))
# Realiza o produto Kronecher(0)  do sub tensor q com o vetor unitário (escalar que representa o peso),
# utilizando tensorly
print(tl.kron(q,w))
#
print(np.linalg.norm(T[:,:,:,:,0].astype(int)))
print(np.linalg.norm([1, 2, 3]))
print(np.linalg.norm([4, 5, 6]))
print(np.linalg.norm([7, 8, 9]))
norma_tensorly = tl.base.tensor_to_vec(tl.norm(T,2,0))
norma_tensorly1 = tl.norm(T,2,0)
print(norma_tensorly)
print(tl.norm(T))

# realiza o produto interno do T X T com tensorly, o que produz um escalar. OBS: Não está disponível no tensorly
print(tl.tenalg.inner(T,T))

# realiza o produto externo do T X T com numpy, o que produz um tensor. OBS: Não está disponível no tensorly
print(np.multiply.outer(T,T))
