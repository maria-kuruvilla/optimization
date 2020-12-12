"""
Create plot of error function and linearized error function
"""

import matplotlib.pyplot as plt
import numpy as np
import math

def frange(start, stop, step):
	i = start
	while i < stop:
		yield i
		i += step

x = []
p=[]
plin = []
qlin = []
q =[]
for i in frange(0,10,0.5):
	x.append(i)
	p.append(1-0.5*(1+math.erf((i-5)/np.sqrt(2))))
	q.append(1-0.5*(1+math.erf((i-4)/np.sqrt(2))))
	if i <=3.5 : 
		plin.append(1)
	if (i < 6.5) and (i > 3.5):
		plin.append(-i/3 + 6.5/3)
	if i >= 6.5 :
		plin.append(0)
	if i <=2.5 : 
		qlin.append(1)
	if (i < 5.5) and (i > 2.5):
		qlin.append(-i/3 + 5.5/3)
	if i >= 5.5 :
		qlin.append(0)


fs=14
plt.close('all') # always start by cleaning up
fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot(111)
ax.plot(x,p, color = 'red', label = 'Threat')
ax.plot(x,q, color = 'blue', label = 'No threat')
#ax.plot(x,plin, color = 'black')
#ax.plot(x,qlin, color = 'black')
plt.xlabel('Threshold', size = 0.9*fs)
plt.ylabel('p or q', size = 0.9*fs)
plt.legend(fontsize=fs, loc='upper right')
plt.grid(True)
plt.show()
out_dir = '../../output/optimization/erf.png'
fig.savefig(out_dir)
