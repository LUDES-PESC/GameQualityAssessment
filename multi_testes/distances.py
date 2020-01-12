'''
Created on 21/06/2015

@author: mangeli
'''
import numpy as np
import scipy.spatial as sp

v1 = [1, 4]
v2 = [4, 1]

print (sp.distance.cosine(v1, v2))


comp = []
comp.append(v1)
comp.append(v2)

myInput = np.matrix.transpose(np.matrix(comp))
 
print (sp.distance.pdist(myInput, 'cosine') )