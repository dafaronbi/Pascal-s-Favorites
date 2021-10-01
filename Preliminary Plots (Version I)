#Definitely going to need to clean up this section a bunch
#Want to concentrate everything being imported in one place

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy.stats as stats
import math


# In[37]:


# 1. Normal
mu = 0
variance = 1
sigma = math.sqrt(variance)
x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
plt.plot(x, stats.norm.pdf(x, mu, sigma), label = 'normal')
plt.legend()
plt.grid(alpha=.4,linestyle='--')
plt.show


# In[36]:


# 2. Uniform
def uniform(x):
    return x

y = 1
x = np.arange(0, 1)

a = 0
b = 1

plt.hlines(y, xmin = 0, xmax = 1)
plt.hlines(0, xmin = -.5, xmax = a)
plt.hlines(0, xmin = b, xmax = 1.5)
plt.vlines(a, ymin = 0, ymax = y)
plt.vlines(b, ymin = 0, ymax = y)

plt.show


# In[12]:


# 3. Poisson
from scipy.special import factorial

t = np.arange(0, 20, 0.1)
d = np.exp(-5)*np.power(5, t)/factorial(t)

plt.plot(t, d, 'bs')
plt.show()


# In[13]:


# 4. Beta
from scipy.stats import beta

a = 2
b = 2
x = np.arange (-50, 50, 0.1)
y = beta.pdf(x,a,b, scale=100, loc=-50)
plt.plot(x,y)


# In[14]:


# 5. Binomial
from scipy.stats import binom

fig, ax = plt.subplots(1, 1)

n, p = 5, 0.4
mean, var, skew, kurt = binom.stats(n, p, moments='mvsk')

x = np.arange(binom.ppf(0.01, n, p),
              binom.ppf(0.99, n, p))
ax.plot(x, binom.pmf(x, n, p), 'bo', ms=8, label='binom pmf')
ax.vlines(x, 0, binom.pmf(x, n, p), colors='b', lw=5, alpha=0.5)

rv = binom(n, p)
ax.vlines(x, 0, rv.pmf(x), colors='k', linestyles='-', lw=1,
        label='frozen pmf')
ax.legend(loc='best', frameon=False)
plt.show()


# In[15]:


# 6. Burr
from scipy.stats import burr

fig, ax = plt.subplots(1, 1)
c, d = 10.5, 4.3
mean, var, skew, kurt = burr.stats(c, d, moments='mvsk')

x = np.linspace(burr.ppf(0.01, c, d),
                burr.ppf(0.99, c, d), 100)
ax.plot(x, burr.pdf(x, c, d),
       'r-', lw=5, alpha=0.6, label='burr pdf')

vals = burr.ppf([0.001, 0.5, 0.999], c, d)
np.allclose([0.001, 0.5, 0.999], burr.cdf(vals, c, d))

r = burr.rvs(c, d, size=1000)

ax.legend(loc='best', frameon=False)
plt.show()


# In[16]:


# 7. Chi-squared
from scipy.stats import chi2

x = np.arange(0, 20, 0.001)
plt.plot(x, chi2.pdf(x, df=4))


# In[17]:


# 8. Exponential
import scipy.stats as ss

def plot_exponential(x_range, mu=0, sigma=1, cdf=False, **kwargs):
    x = x_range
    if cdf:
        y = ss.expon.cdf(x, mu, sigma)
    else:
        y = ss.expon.pdf(x, mu, sigma)
    plt.plot(x, y, **kwargs)

plot_exponential(x, 0, 1, color='red', lw=2, ls='-', alpha=0.5, label='pdf')
plot_exponential(x, 0, 1, cdf=True, color='blue', lw=2, ls='-', alpha=0.5, label='cdf')
plt.legend();


# In[18]:


# 9. Extreme Value
#NOT SURE IF THIS IS CORRECT
#USING A LEFT-SKEWED GUMBEL DISTRIBUTION
from scipy.stats import gumbel_l

fig, ax = plt.subplots(1, 1)

mean, var, skew, kurt = gumbel_l.stats(moments='mvsk')

x = np.linspace(gumbel_l.ppf(0.01),
                gumbel_l.ppf(0.99), 100)
ax.plot(x, gumbel_l.pdf(x),
       'r-', lw=5, alpha=0.6, label='gumbel_l pdf')

rv = gumbel_l()
ax.plot(x, rv.pdf(x), 'k-', lw=2, label='frozen pdf')

ax.legend(loc='best', frameon=False)
plt.show()


# In[19]:


# 10. F
from scipy.stats import f
fig, ax = plt.subplots(1,1)

dfn, dfd = 29, 18
mean, var, skew, kurt = f.stats(dfn, dfd, moments='mvsk')

x = np.linspace(f.ppf(0.01, dfn, dfd),
                f.ppf(0.99, dfn, dfd), 100)
ax.plot(x, f.pdf(x, dfn, dfd),
       'r-', lw=5, alpha=0.6, label='f pdf')

rv = f(dfn, dfd)
ax.plot(x, rv.pdf(x), 'k-', lw=2, label='frozen pdf')

ax.legend(loc='best', frameon=False)
plt.show()


# In[20]:


# 11. Gamma
from scipy.stats import gamma

fig, ax = plt.subplots(1, 1)

a = 1.99
mean, var, skew, kurt = gamma.stats(a, moments='mvsk')

x = np.linspace(gamma.ppf(0.01, a),
                gamma.ppf(0.99, a), 100)
ax.plot(x, gamma.pdf(x, a),
       'r-', lw=5, alpha=0.6, label='gamma pdf')

rv = gamma(a)
ax.plot(x, rv.pdf(x), 'k-', lw=2, label='frozen pdf')

ax.legend(loc='best', frameon=False)
plt.show()


# In[21]:


# 12. Generalized Extreme Value
from scipy.stats import genextreme

fig, ax = plt.subplots(1,1)

c = -0.1
mean, var, skew, kurt = genextreme.stats(c, moments='mvsk')

x = np.linspace(genextreme.ppf(0.01, c),
                genextreme.ppf(0.99, c), 100)
ax.plot(x, genextreme.pdf(x, c),
       'r-', lw=5, alpha=0.6, label='genextreme pdf')

rv = genextreme(c)
ax.plot(x, rv.pdf(x), 'k-', lw=2, label='frozen pdf')

ax.legend(loc='best', frameon=False)
plt.show()


# In[22]:


# 13. Generalized Pareto
from scipy.stats import genpareto

fig, ax = plt.subplots(1, 1)

c = 0.1
mean, var, skew, kurt = genpareto.stats(c, moments='mvsk')

x = np.linspace(genpareto.ppf(0.01, c),
                genpareto.ppf(0.99, c), 100)
ax.plot(x, genpareto.pdf(x, c),
       'r-', lw=5, alpha=0.6, label='genpareto pdf')

rv = genpareto(c)
ax.plot(x, rv.pdf(x), 'k-', lw=2, label='frozen pdf')

ax.legend(loc='best', frameon=False)
plt.show()


# In[23]:


# 14. Geometric
from scipy.stats import geom

fig, ax = plt.subplots(1, 1)

p = 0.5
mean, var, skew, kurt = geom.stats(p, moments='mvsk')

x = np.arange(geom.ppf(0.01, p),
              geom.ppf(0.99, p))
ax.plot(x, geom.pmf(x, p), 'bo', ms=8, label='geom pmf')
ax.vlines(x, 0, geom.pmf(x, p), colors='b', lw=5, alpha=0.5)

rv = geom(p)
ax.vlines(x, 0, rv.pmf(x), colors='k', linestyles='-', lw=1,
        label='frozen pmf')
ax.legend(loc='best', frameon=False)
plt.show()


# In[24]:


# 15. Half normal
from scipy.stats import halfnorm

fig, ax = plt.subplots(1,1)

mean, var, skew, kurt = halfnorm.stats(moments='mvsk')

x = np.linspace(halfnorm.ppf(0.01),
                halfnorm.ppf(0.99), 100)
ax.plot(x, halfnorm.pdf(x),
       'r-', lw=5, alpha=0.6, label='halfnorm pdf')

rv = halfnorm()
ax.plot(x, rv.pdf(x), 'k-', lw=2, label='frozen pdf')

ax.legend(loc='best', frameon=False)
plt.show()


# In[25]:


# 16. Hypergeometric
from scipy.stats import hypergeom

[M, n, N] = [20, 7, 12]
rv = hypergeom(M, n, N)
x = np.arange(0, n+1)
pmf_dogs = rv.pmf(x)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(x, pmf_dogs, 'bo')
ax.vlines(x, 0, pmf_dogs, lw=2)
ax.set_xlabel('# of dogs in our group of chosen animals')
ax.set_ylabel('hypergeom PMF')
plt.show()


# In[26]:


# 17. Lognormal
from scipy.stats import lognorm

fig, ax = plt.subplots(1, 1)

s = 0.954
mean, var, skew, kurt = lognorm.stats(s, moments='mvsk')

x = np.linspace(lognorm.ppf(0.01, s),
                lognorm.ppf(0.99, s), 100)
ax.plot(x, lognorm.pdf(x, s),
       'r-', lw=5, alpha=0.6, label='lognorm pdf')

rv = lognorm(s)
ax.plot(x, rv.pdf(x), 'k-', lw=2, label='frozen pdf')

ax.legend(loc='best', frameon=False)
plt.show()


# In[27]:


# 18. Negative Binomial
from scipy.stats import nbinom

fig, ax = plt.subplots(1, 1)

n, p = 5, 0.5
mean, var, skew, kurt = nbinom.stats(n, p, moments='mvsk')

x = np.arange(nbinom.ppf(0.01, n, p),
              nbinom.ppf(0.99, n, p))
ax.plot(x, nbinom.pmf(x, n, p), 'bo', ms=8, label='nbinom pmf')
ax.vlines(x, 0, nbinom.pmf(x, n, p), colors='b', lw=5, alpha=0.5)

rv = nbinom(n, p)
ax.vlines(x, 0, rv.pmf(x), colors='k', linestyles='-', lw=1,
        label='frozen pmf')
ax.legend(loc='best', frameon=False)
plt.show()


# In[28]:


# 19. Noncentral F
from scipy import special

x = np.linspace(-1, 8, num=500)
dfn = 3
dfd = 2
ncf_stats = stats.f.cdf(x, dfn, dfd)
ncf_special = special.ncfdtr(dfn, dfd, 0, x)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(x, ncf_stats, 'b-', lw=3)
ax.plot(x, ncf_special, 'r-')
plt.show()


# In[29]:


# 20. Noncentral t
from scipy.stats import t

fig, ax = plt.subplots(1, 1)

df = 2.74
mean, var, skew, kurt = t.stats(df, moments='mvsk')

x = np.linspace(t.ppf(0.01, df),
                t.ppf(0.99, df), 100)
ax.plot(x, t.pdf(x, df),
       'r-', lw=5, alpha=0.6, label='t pdf')

rv = t(df)
ax.plot(x, rv.pdf(x), 'k-', lw=2, label='frozen pdf')

ax.legend(loc='best', frameon=False)
plt.show()


# In[30]:


# 21. Noncentral Chi-squared
from scipy.stats import ncx2

fig, ax = plt.subplots(1, 1)

df, nc = 21, 1.06
mean, var, skew, kurt = ncx2.stats(df, nc, moments='mvsk')

x = np.linspace(ncx2.ppf(0.01, df, nc),
                ncx2.ppf(0.99, df, nc), 100)
ax.plot(x, ncx2.pdf(x, df, nc),
       'r-', lw=5, alpha=0.6, label='ncx2 pdf')

rv = ncx2(df, nc)
ax.plot(x, rv.pdf(x), 'k-', lw=2, label='frozen pdf')

ax.legend(loc='best', frameon=False)
plt.show()


# In[31]:


# 22. Rayleigh
from scipy.stats import rayleigh

fig, ax = plt.subplots(1, 1)

mean, var, skew, kurt = rayleigh.stats(moments='mvsk')

x = np.linspace(rayleigh.ppf(0.01),
                rayleigh.ppf(0.99), 100)
ax.plot(x, rayleigh.pdf(x),
       'r-', lw=5, alpha=0.6, label='rayleigh pdf')

rv = rayleigh()
ax.plot(x, rv.pdf(x), 'k-', lw=2, label='frozen pdf')

ax.legend(loc='best', frameon=False)
plt.show()


# In[32]:


# 23. Stable
from scipy.stats import levy_stable

fig, ax = plt.subplots(1, 1)

alpha, beta = 1.8, -0.5
mean, var, skew, kurt = levy_stable.stats(alpha, beta, moments='mvsk')

x = np.linspace(levy_stable.ppf(0.01, alpha, beta),
                levy_stable.ppf(0.99, alpha, beta), 100)
ax.plot(x, levy_stable.pdf(x, alpha, beta),
       'r-', lw=5, alpha=0.6, label='levy_stable pdf')

rv = levy_stable(alpha, beta)
ax.plot(x, rv.pdf(x), 'k-', lw=2, label='frozen pdf')

ax.legend(loc='best', frameon=False)
plt.show()


# In[33]:


# 24. t
from scipy.stats import t

fig, ax = plt.subplots(1, 1)

df = 2.74
mean, var, skew, kurt = t.stats(df, moments='mvsk')

x = np.linspace(t.ppf(0.01, df),
                t.ppf(0.99, df), 100)
ax.plot(x, t.pdf(x, df),
       'r-', lw=5, alpha=0.6, label='t pdf')

rv = t(df)
ax.plot(x, rv.pdf(x), 'k-', lw=2, label='frozen pdf')

ax.legend(loc='best', frameon=False)
plt.show()


# In[34]:


# 25. Discrete Uniform
from scipy.stats import randint

fig, ax = plt.subplots(1, 1)

low, high = 7, 31
mean, var, skew, kurt = randint.stats(low, high, moments='mvsk')

x = np.arange(randint.ppf(0.01, low, high),
              randint.ppf(0.99, low, high))
ax.plot(x, randint.pmf(x, low, high), 'bo', ms=8, label='randint pmf')
ax.vlines(x, 0, randint.pmf(x, low, high), colors='b', lw=5, alpha=0.5)

rv = randint(low, high)
ax.vlines(x, 0, rv.pmf(x), colors='k', linestyles='-', lw=1,
        label='frozen pmf')
ax.legend(loc='best', frameon=False)
plt.show()


# In[35]:


# 26. Weibull
from scipy.stats import weibull_min

fig, ax = plt.subplots(1, 1)

c = 1.79
mean, var, skew, kurt = weibull_min.stats(c, moments='mvsk')

x = np.linspace(weibull_min.ppf(0.01, c),
                weibull_min.ppf(0.99, c), 100)
ax.plot(x, weibull_min.pdf(x, c),
       'r-', lw=5, alpha=0.6, label='weibull_min pdf')

rv = weibull_min(c)
ax.plot(x, rv.pdf(x), 'k-', lw=2, label='frozen pdf')

ax.legend(loc='best', frameon=False)
plt.show()
