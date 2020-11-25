# -*- coding: utf-8 -*-

##from tensorly.base import unfold, fold
import numpy as np
import tensorly as ts
##from scipy.spatial import distance
'''
###########################################################################
# A tensor is simply a numpy array
tensor = T.tensor(np.arange(32).reshape((4, 4, 2)))
print('* original tensor:\n{}'.format(tensor))

###########################################################################
# Unfolding a tensor is easy
for mode in range(tensor.ndim):
    print('* mode-{} unfolding:\n{}'.format(mode, unfold(tensor, mode)))

###########################################################################
# Re-folding the tensor is as easy:
for mode in range(tensor.ndim):
    unfolding = unfold(tensor, mode)
    folded = fold(unfolding, mode, tensor.shape)
    T.assert_array_equal(folded, tensor)

'''

def cosSim(SPQCPlaned, SPQCRealized):
    numerator = np.tensordot(SPQCPlaned, SPQCRealized, 1)
    denominator  = np.linalg.norm(SPQCPlaned) * np.linalg.norm(SPQCRealized)

    if denominator > 0:
        return numerator / denominator
    else:
        return 0

TMT1 = np.array([[0.207], [0.3]])
print('TMT1 = '+ str(TMT1)  + '\n' )

TC1 = np.array([[0]])
print('TC1 = '+ str(TC1) + '\n' )

print('A ponderação de TMT1 (Produto tensorial) TMT1 (x) 0,7 = ' + '\n' + str(np.tensordot(TMT1, [0.7], 0)) + '\n' )

print('A ponderação de TC1 (Produto tensorial) TC1 (x) 0,3 = ' + '\n' + str(np.tensordot(TC1, [0.3], 0)) + '\n' )

print('A norma de TMT1  = ' + '\n' + str(np.tensordot(TMT1, [0.7], 0)) + '\n' )

print('A ponderação de TC1 (Produto tensorial) TC1 (x) 0,3 = ' + '\n' + str(np.tensordot(TC1, [0.3], 0)) + '\n' )


SPQC1 = (np.tensordot(TMT1, [0.7], 0)) + (np.tensordot(TC1, [0.3], 0))
print('A configuração da qualidade (SPQC1) = (TMT1 (x) 0,7) + (TC1 (x) 0,3) = '+ str(SPQC1) + '\n' )
print('A vetorização de SPQC1 é:  '+ str(ts.base.tensor_to_vec(SPQC1)) + '\n' )

D = np.linalg.norm(ts.base.tensor_to_vec(SPQC1))
print('A norma(Frobenius) de SPQC1 = '+ str(D) + '\n' )


TMT1_Modificabilidade = np.array([(0.093), (0.017), (0.075)])
normTMT1_Modificabilidade = np.linalg.norm(ts.base.tensor_to_vec(TMT1_Modificabilidade))
print('A norma(Frobenius) de TMT1_Modificabilidade = '+ str(normTMT1_Modificabilidade))
print('A dimensionalidade de TMT1_Modificabilidade = '+ str(np.shape(TMT1_Modificabilidade)) + '\n' )

TMT1_Testabilidade = np.array([[0.4]])
normTMT1_Testabilidade = np.linalg.norm(ts.base.tensor_to_vec(TMT1_Testabilidade))
print('A norma(Frobenius) de TMT1_Testabilidade = '+ str(normTMT1_Testabilidade))
print('A dimensionalidade de TMT1_Testabilidade = '+ str(np.shape(TMT1_Testabilidade)) + '\n' )

TMT1_DT = np.array([[0.25]])
normTMT1_DT = np.linalg.norm(ts.base.tensor_to_vec(TMT1_DT))
print('A norma(Frobenius) de TMT1_Divida Técnica = '+ str(normTMT1_DT) + '\n' )
print('A dimensionalidade de TMT1_DT = '+ str(np.shape(TMT1_DT)) + '\n' )

TMT1_SubCarac = np.array([[0.120], [0.4], [0.25]])
normTMT1_SubCarac = np.linalg.norm(ts.base.tensor_to_vec(TMT1_SubCarac))
print('A norma(Frobenius) das subcaracteríticas de Modificabilidade = '+ str(normTMT1_SubCarac) )
print('A dimensionalidade de TMT1_SubCarac = '+ str(np.shape(TMT1_SubCarac)) + '\n' )

TMT1_Carac = np.array([[0.3374]])
normTMT1_Carac = np.linalg.norm(ts.base.tensor_to_vec(TMT1_Carac))
print('A norma(Frobenius) da caracterítica TMT1  = '+ str(normTMT1_Carac) )
print('A dimensionalidade de TMT1_Carac = '+ str(np.shape(TMT1_Carac)) + '\n' )

TC1_Maturidade = np.array([[0], [0]])
normTC1_Maturidade = np.linalg.norm(ts.base.tensor_to_vec(TC1_Maturidade))
print('A norma(Frobenius) das subcaracteríticas de TC1_Maturidade = '+ str(normTC1_Maturidade))
print('A dimensionalidade de TC1_Maturidade = '+ str(np.shape(TC1_Maturidade)) + '\n' )

TC1_Carac = np.array([[0]])
normTC1_Carac = np.linalg.norm(ts.base.tensor_to_vec(TC1_Carac))
print('A norma(Frobenius) da caracteríticas TC1 = '+ str(normTC1_Carac) + '\n' )

SQPC1_QP = np.array([[0.337], [0]])
normSQPC1_QP = np.linalg.norm(ts.base.tensor_to_vec(SQPC1_QP))
print('A norma(Frobenius) da qualidade de produto de SQC1 = '+ str(normSQPC1_QP) + '\n' )

print('A similaridade entre as SPQC1 e SPQC1 = ' + str(cosSim(ts.base.tensor_to_vec(SPQC1),ts.base.tensor_to_vec(SPQC1))))




medianaCC = np.array([42, 25, 18, 17, 13, 10, 8, 6, 5, 2, 1, 1, 0, 0, 0, 0, 0, 0])
print('A mediana de CC do Parasite = '+ str(np.median(medianaCC)) + '\n' )

medianaDT = np.array([0.5, 0.3, 0.3, 0.2, 0.1, 10, 8, 6, 5, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
print('A mediana da Divida Técnica do Parasite = '+ str(np.median(medianaDT)) + '\n' )

mediaDT = np.array([0.5, 0.3, 0.3, 0.2, 0.1, 10, 8, 6, 5, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
print('A média da Divida Técnica do Parasite = '+ str(np.mean(mediaDT)) + '\n' )

xa = ts.base.tensor_to_vec(SPQC1)
xa1 = xa.ravel()
##print('A similaridade entre as SPQC1 e SPQC1 = ' + str(distance.cosine(SQPC1_QP.ravel(), SQPC1_QP.ravel())))









Tensor_Rispoli = ts.tensor(np.arange(40).reshape((4, 2, 1, 1, 5)))
print(Tensor_Rispoli)


