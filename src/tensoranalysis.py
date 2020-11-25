'''
atributo: receber uma lista com os pesos dos tensores - OK
atributo: receber uma lista com os tensores - OK
ponderar os tensores - OK
fornecer a percepção(norma) do total da qualidade a partir dos tensores - OK
fornecer a percepção(norma) da qualidade de cada tesnor
calcular o produto tensorial - OK
calcular a distância vetorial - OK
'''

import numpy as np
import tensorly as ts
import math
from functools import reduce

class TensorAnalysis():

    def __init__(self, *args):
        self.spqcTensor = ts.tensor(args[0])
        self.spqcWeightedTensor = []
        self.spqcTensorWeights = []
        self.spqc = 0.0
        if args.__len__() > 1:
            self.spqcTensorWeights = args[1]
        else:
            for i in range(self.spqcTensor.__len__()):
                self.spqcTensorWeights.append(float(1))

    def SPQCWeightedTensor(self):
        for i in range(self.spqcTensor.__len__()):
            self.spqcWeightedTensor.append(np.multiply(self.spqcTensorWeights[i], self.spqcTensor[i]))
        return self

    def SPQCCalcute(self):
        if not self.spqcWeightedTensor:
            self.spqc = np.linalg.norm(ts.base.tensor_to_vec(ts.tenalg.kronecker(self.spqcTensor)))
        else:
            self.spqc = np.linalg.norm(ts.base.tensor_to_vec(ts.tenalg.kronecker(self.spqcWeightedTensor)))
        return self

def TensorCossineSim(tensor, SPQCPlaned, SPQCRealized):
    sumSPQCPlaned = list()
    sumSPQCRealized = list()
    powerTPQCPlaned = list()
    powerTPQCRealized = list()
    tensorList = list()

    #tensorList.append(np.asarray(SPQCPlaned))
    #tensorList.append(np.asarray(SPQCRealized))

    tensorList.append(SPQCPlaned)
    tensorList.append(SPQCRealized)




    for i in range(len(SPQCPlaned)):
        dim = np.array([])
        sumSPQCPlanedDim = 0
        dim = SPQCPlaned[0:len(SPQCPlaned)][i]
        sumSPQCPlanedDim += sum(sum(np.asarray(dim)))
        sumSPQCPlaned.append(sumSPQCPlanedDim)
        powerTPQCPlaned.append(sumSPQCPlanedDim**2)

    for i in range(len(SPQCRealized)):
        dim = np.array([])
        sumSPQCRealizedDim = 0
        dim = SPQCRealized[0:len(SPQCRealized)][i]
        sumSPQCRealizedDim += sum(sum(np.asarray(dim)))
        sumSPQCRealized.append(sumSPQCRealizedDim)
        powerTPQCRealized.append(sumSPQCRealizedDim**2)

    numerator = np.linalg.norm(ts.base.tensor_to_vec(ts.tenalg.kronecker(tensor)))


#    numerator = np.dot(np.asarray(SPQCPlaned), np.asarray(SPQCRealized))
    teste = np.reshape(numerator, -1)
    denominator = math.sqrt(sum(powerTPQCPlaned)*sum(powerTPQCRealized))

    if denominator > 0:
        return numerator / denominator
    else:
        return 0


performanceEfficiency = []
performanceEfficiencyARRAY = np.empty((2, 3), int)
performance_efficiency_wheighted = []
security = []
securityARRAY = np.empty((3, 3), int)
security_wheighted = []
quality_tensor_wheigted = []
qualityTensor = list()

quality_tensor_wheigted.append(float(0.4))
quality_tensor_wheigted.append(float(0.7))

performanceEfficiency.append([1, 2, 3])
performanceEfficiency.append([9, 7, 0])

performanceEfficiencyARRAY = np.asarray(performanceEfficiency)

security.append([3, 4, 0])
security.append([3, 5, 7])
security.append([0, 0, 0])

securityARRAY = np.asarray(security)

#qualityTensorTesteARRAY = np.stack((performanceEfficiencyARRAY, securityARRAY))


qualityTensorTeste = list()
qualityTensorARRAY = list()

qualityTensor.append(performanceEfficiency)
qualityTensor.append(security)

qualityTensorARRAY.append(performanceEfficiencyARRAY)
qualityTensorARRAY.append(securityARRAY)

SQPCTensor = ts.tensor(np.asarray(qualityTensor))

print('***********************Imprimindo o tensor SQPCTensor *******************####################')
print(SQPCTensor[..., 0])
print(SQPCTensor[..., 1])

performance_efficiency_wheighted.append(np.multiply(quality_tensor_wheigted[0], performanceEfficiency))
security_wheighted.append(np.multiply(quality_tensor_wheigted[1], security))

qualityTensorTeste.append(performance_efficiency_wheighted)
qualityTensorTeste.append(security_wheighted)


print('\n***********************Imprimindo o produto kronecker SQPCTensor(tensor) *************#############\n')
print(ts.base.tensor_to_vec(ts.tenalg.kronecker(SQPCTensor)))


SPQCnd_array = np.array([]).reshape((0,2))
X1 = ts.tensor(qualityTensorARRAY)
print('\n***********************Imprimindo mode-0 X1 *************#############')
print(ts.unfold(X1, 0))


print('\n***********************Imprimindo mode-1 X1 *************#############')
#print(ts.unfold(X1, 1))


print('\n***********************Imprimindo a similaridade tensores X e Y *************#############')

X = ts.tensor(np.arange(24).reshape((3, 4, 2)))
Y = ts.tensor(np.asarray(qualityTensor))

tensorSQPC = list()
tensorSQPC.append(X)
tensorSQPC.append(Y)



simX_Y = TensorCossineSim(SQPCTensor, X, Y)

print('A similaridade da configuração da qualidade de produto planejada X realizada é de: ' + str(simX_Y))


print('\n*********************Imprimindo a norma do produto dos tensores X e Y *************#############')
print('A norma do tensor X é: ' + str(np.linalg.norm(ts.base.tensor_to_vec(ts.tenalg.kronecker(SQPCTensor)))))


print('\n*********************** Imprimindo a SPQC do tensor ponderado *******************####################')

testeTensor = TensorAnalysis(X1, quality_tensor_wheigted)
testeTensor.SPQCWeightedTensor()
testeTensor.SPQCCalcute()
print(testeTensor.spqc)

print('\n*********************** Imprimindo o tensor X1 SEM ponderaçao *******************####################')

testeTensor1 = TensorAnalysis(X1)
testeTensor1.SPQCCalcute()
print(testeTensor1.spqc)
