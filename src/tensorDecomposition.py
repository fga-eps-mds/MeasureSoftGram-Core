import numpy as np
import tensorly as tl
from tensorly.decomposition import parafac
tensor = tl.tensor([[ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                        [ 0.,  0.,  0.,  0.,  1.,  1.,  1.,  1.,  0.,  0.,  0.,  0.],
                        [ 0.,  0.,  0.,  0.,  1.,  1.,  1.,  1.,  0.,  0.,  0.,  0.],
                        [ 0.,  0.,  0.,  0.,  1.,  1.,  1.,  1.,  0.,  0.,  0.,  0.],
                        [ 0.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  0.],
                        [ 0.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  0.],
                        [ 0.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  0.],
                        [ 0.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  0.],
                        [ 0.,  0.,  0.,  0.,  1.,  1.,  1.,  1.,  0.,  0.,  0.,  0.],
                        [ 0.,  0.,  0.,  0.,  1.,  1.,  1.,  1.,  0.,  0.,  0.,  0.],
                        [ 0.,  0.,  0.,  0.,  1.,  1.,  1.,  1.,  0.,  0.,  0.,  0.],
                        [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.]])

tensor_rank = tensor.ndim

weights, factors = parafac(tensor, rank=2)


print(np.shape(tensor))
print(tensor)

print(len(factors))
print(np.shape(factors))
print(factors)




cp_reconstruction = tl.kruskal_to_tensor((weights, factors))
#print(cp_reconstruction)

X = tl.tensor(np.arange(24).reshape((3, 4, 2)))
X_Rank = X.ndim
print(X)

print(X[..., 0])
print(X[..., 1])

print(tl.unfold(X,0))
print(tl.unfold(X,1))
print(tl.unfold(X,2))


weights_X, factors_X = parafac(X.astype(float), rank=2)
print(len(factors_X))
print(np.shape(factors_X))
print(factors_X)

cp_reconstruction_X = tl.kruskal_to_tensor((weights_X, factors_X))

m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print(m)

t = [[[2], [4], [6]], [[8], [10], [12]], [[14], [16], [18]]]
print(t)

a = np.array([1, 2, 3])
b = np.array([1, 2, 3, 4])
c = np.array([1, 2])

T = np.zeros((a.shape[0], b.shape[0], c.shape[0]))

for i in range(a.shape[0]):
    for j in range(b.shape[0]):
        for k in range(c.shape[0]):
            T[i, j, k] = a[i] * b[j] * c[k]

print(T)


