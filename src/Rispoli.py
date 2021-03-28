import numpy as np
import tensorly as tl

# ============= INICIO-TRATAMENTO (DATASET OBTIDO A PARTIR DE UMA VERSÃO DO PRODUTO) =============
norm_Modificabilidade = np.linalg.norm(tl.base.tensor_to_vec(np.array([(0.093), (0.017), (0.075)])))
norm_Testabilidade = np.linalg.norm(tl.base.tensor_to_vec(np.array([(0.4)])))
norm_DT = np.linalg.norm(tl.base.tensor_to_vec(np.array([(0.25)])))
norm_Maturidade = np.linalg.norm(tl.base.tensor_to_vec(np.array([(0), (0)])))
# ============= FIM-TRATAMENTO (NÃO HÁ TENSOR AINDA) ===================

# ============= INICIO CRIAÇÃO DO TENSOR DE MANUTENIBILIDADE =============
# Cria o tensor T_MANUTENIBILIDADE com a dimensão Modificabilidade
T_MANUTENIBILIDADE = np.array([norm_Modificabilidade])
# Cria a dimensão/eixo  Testabilidade no tensor T_MANUTENIBILIDADE
dimensionalidade_anterior = len(T_MANUTENIBILIDADE.shape)
T_MANUTENIBILIDADE = T_MANUTENIBILIDADE[:, np.newaxis]
# Insere o valor obtido da testabilidade nessa nova dimensão
T_MANUTENIBILIDADE = np.insert(T_MANUTENIBILIDADE, dimensionalidade_anterior, np.array([norm_Testabilidade]), axis=dimensionalidade_anterior)
# Cria a dimensão/eixo  Divida Técnica(DT no tensor T_MANUTENIBILIDADE
dimensionalidade_anterior = len(T_MANUTENIBILIDADE.shape)
T_MANUTENIBILIDADE = T_MANUTENIBILIDADE[:, np.newaxis]
# Insere o valor obtido da testabilidade nessa nova dimensão
T_MANUTENIBILIDADE = np.insert(T_MANUTENIBILIDADE, dimensionalidade_anterior, np.array([norm_DT]), axis=dimensionalidade_anterior)
# ============= FIM CRIAÇÃO DO TENSOR DE MANUTENIBILIDADE =============

print('A dimensionalidade do tenssor de Manutenibilidade é: ' + str(T_MANUTENIBILIDADE.shape))
print(str(T_MANUTENIBILIDADE) + '\n' )

# ============= INICIO CRIAÇÃO DO TENSOR DE CONFIABILIDADE =============
# Cria o tensor T_CONFIABILIDADE com a dimensão Maturidade
T_CONFIABILIDADE = np.array([norm_Maturidade])
# ============= FIM CRIAÇÃO DO TENSOR DE CONFIABILIDADE =============

print('A dimensionalidade do tenssor de Confiabilidade é: ' + str(T_CONFIABILIDADE.shape))
print(T_CONFIABILIDADE)
