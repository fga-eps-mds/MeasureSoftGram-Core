from scipy.interpolate import interp1d
import numpy as np
import matplotlib.pyplot as plt
x = np.array([10., 20., np.nan, 40., 50., np.nan, 30.])
not_nan = np.logical_not(np.isnan(x))
indices = np.arange(len(x))
interp = interp1d(indices[not_nan], x[not_nan])
print(interp(indices))

x = np.array([0.13, 0.16,0.21])
y = np.array([1, 0.5, 0])
print(np.interp(0.175, x, y))
print('**********************')


x = np.array([0, 10])
y = np.array([1, 0])
print(np.interp(6, x, y))

x = np.array([1, 3])
y = np.array([1, 0])
print(np.interp(2, x, y))

x = np.array([0, 0.09])
y = np.array([1, 0])
print(np.interp(0, x, y))

print("********")

print(np.interp(1.04, x, y))
print(np.interp(3.6, x, y))
print(np.interp(1.13, x, y))
print(np.interp(3.25, x, y))
print(np.interp(2.5, x, y))
print(np.interp(1.33, x, y))
print(np.interp(2, x, y))
print(np.interp(1, x, y))
print(np.interp(0, x, y))

#plt.plot(x, y, 'o')
#plt.show()
