import os
import json
import pandas as pd
import numpy as np
import tensorly as tl
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from numpy.random import rand
from numpy.random import seed
from scipy.stats import spearmanr
import urllib3
from urllib3 import request

# Setando as configs do dataframe
pd.set_option("display.max_rows", None, "display.max_columns", None)


# Informando a chave do projeto no SonarCloud
#chave = 'fga-eps-mds_2020.1-eSaudeUnB-FrontEnd'
chave = 'Guilherme-Aguiar_2020.1-VC_Gestor-BackEnd:packages&branch=master'

# Informando a lista de métricas a serem coletadas
metrics_list = [
    'complexity',
    'functions',
    'files',
    'comment_lines_density',
    'duplicated_lines_density',
    'coverage',
    'sqale_rating',
    'test_success_density',
    'bugs',
    'open_issues',
    'reliability_rating',
    'vulnerabilities',
    'security_rating'
]

#Montando a string da lista de métricas e as URLs das requisições da API
string_metricKeys = ''
for metric in metrics_list:
    string_metricKeys += metric + ','

url = "https://sonarcloud.io/api/measures/component_tree?component="+chave+"&metricKeys="+string_metricKeys+"&ps=500"


# Realizando a requisição das métricas na API do SonarCloud
# Instanciando a conexão¶
http = urllib3.PoolManager()

# Realizando as requisições
data = http.request('GET', url)

# Decodificando os arquivos recebidos
json_repositorio = json.loads(data.data.decode('utf-8'))

back_r1_base_component = pd.DataFrame(json_repositorio['baseComponent']['measures'])


#Salvando os arquivos localmente
#nome_arquivo = 'fga-eps-mds_2020.1-eSaudeUnB-FrontEnd-R2.json'
nome_arquivo = 'fga-eps-mds_2020.1-VC_Gestor-BackEnd-R2.json'

with open(nome_arquivo, 'w') as outfile:
    json.dump(json_repositorio, outfile)

# Separando as métricas do projeto
json_projeto = json_repositorio['baseComponent']

# Gerando a lista de colunas
json_projeto_columns = []
for measure in json_projeto['measures']:
    json_projeto_columns.append(measure['metric'])

# Instanciando o dataframe
df_projeto = pd.DataFrame(columns = json_projeto_columns)

# Populando o dataframe
for measure in json_projeto['measures']:
    df_projeto.at['projeto', measure['metric']] = measure['value']

# Separando apenas os arquivos
json_arquivos = []
for component in json_repositorio['components']:
    if component['qualifier'] == 'FIL':
        json_arquivos.append(component)

# Gerando a lista de colunas
json_arquivos_columns = []
for measure in json_arquivos[0]['measures']:
    json_arquivos_columns.append(measure['metric'])

# Gerando a lista de linhas
json_arquivos_index = []
for file in json_arquivos:
    try:
        if file['language'] == 'js':
            json_arquivos_index.append(file['path'])
    except:
        pass

df_arquivos = pd.DataFrame(columns = json_arquivos_columns, index = json_arquivos_index)

for file in json_arquivos:
    try:
        if file['language'] == 'js':
            for measure in file['measures']:
                df_arquivos.at[file['path'], measure['metric']] = measure['value']
    except:
        pass


print(df_arquivos)


df_arquivos['complexity/functions']=df_arquivos['complexity'].astype(float)/df_arquivos['functions'].astype(float)

x = np.array([0, 5])
y = np.array([1, 0])

ma1 = sum(np.interp(list(df_arquivos['complexity/functions'][(df_arquivos['functions'].astype(float) > 0)]), x, y))/len(df_arquivos)

print(ma1)


x = np.array([0, .25])
y = np.array([1, 0])

ma3 = np.interp((float(back_r1_base_component['value'].iloc[1]))/100, x, y)

print(ma3)


# Cria um tensor 1D (vetor - )
x1 = np.array([ma1])

# Cria uma nova dimensão/eixo a partir do tensor x1. # Logo x2 é um tensor-2D (matriz)
x2 = x1[:, np.newaxis]
# Insere o array [ma3] como se fosse a última coluna de x1, ou seja,
# os valores são inseridos no novo eixo/dimensão criado. O parâmetro 1
x2 = np.insert(x2, len(x1.shape), np.array([ma3]), axis=len(x1.shape))

print(x2.shape)
print(x2)


T = tl.tensor(x2)

print(T)

#print(tl.tenalg.mode_dot(T,np.array([2]),0))
print(T.ndim)
#Calculq a norma (todos os eixos) do tensor T com tensorly
print(tl.norm(T))
#Calculq a norma do tensor T em um eixo/dimensão específico. No caso, no 1o. eixo = 1, com tensorly.
# OBS: o 1o eixo possui indice 1
print(tl.norm(T,1))
print(tl.norm(T,2))


# Realiza um slice frontal no tensor T no eixo/dimensão 0 (tipo 1a coluna)
q = T[:,0].astype(int)
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
print(np.linalg.norm(T[:,0].astype(int)))
norma_tensorly = tl.base.tensor_to_vec(tl.norm(T,2,0))
norma_tensorly1 = tl.norm(T,2,0)
print(norma_tensorly)
print(tl.norm(T))

# realiza o produto interno do T X T com tensorly, o que produz um escalar. OBS: Não está disponível no tensorly
print(tl.tenalg.inner(T,T))

# realiza o produto externo do T X T com numpy, o que produz um tensor. OBS: Não está disponível no tensorly
print(np.multiply.outer(T,T))



'''
k2, normal_Test_Pval = stats.normaltest(T, axis=None)

if(normal_Test_Pval < 0.05):
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
'''

#********************************
