import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
fs = 18
out_dir = '../../output/optimization/project_plan2.png'
plt.close('all') # always start by cleaning up
fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot(111)
x = np.linspace(stats.norm.ppf(0.001,4,1), stats.norm.ppf(0.999,5,1), 100)
ax.plot(x, stats.norm.pdf(x,4,1),'b-', lw=5, alpha=0.6, label='no threat')
ax.fill_between(x, stats.norm.pdf(x,4,1), where=(x>3.5), color='b', alpha=0.5)
ax.plot(x, stats.norm.pdf(x,5,1),'r-', lw=5, alpha=0.6, label='threat')
ax.fill_between(x, stats.norm.pdf(x,5,1), where=(x>3.5), color='r', alpha=0.5)
ax.text(5.25, .3, 'p')
ax.text(3.75, .3, 'q') #, fontsize=18, transform = ax.transAxes, ha='center', bbox=dict(facecolor='w', edgecolor='None', alpha=0.5))
ax.text(3.51, .5, 'Threshold'+r'$\tau$',fontsize=fs)
ax.axvline(x=3.5)
ax.set_xlim(0, 10)
ax.set_ylim(0, 0.6)
plt.xlabel('Score', size = fs)
plt.ylabel('Probability Density', size = fs)
plt.legend()
plt.show()
fig.savefig(out_dir)
