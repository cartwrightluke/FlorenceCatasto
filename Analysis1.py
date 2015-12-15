import Shared
import scipy.stats.kde
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

def analyze(fig, ax, tradeQuantities):
    m = max(tradeQuantities)
    if(m == 0):
        return
    normalized = [x/m for x in tradeQuantities]
    s = sorted(normalized)
   # c = np.cumsum(s)
    x = [x/len(tradeQuantities) for x in range(0,len(tradeQuantities))]
    ax.plot(x,s)
    mn = np.median(s)
    sd = np.std(s)
    mnsd = mn + 2 * sd
    if(mnsd < 1):
        crossing = [b for b in s > mnsd].index(True) / len(s)
        polygonPoints = [[crossing, 1], [crossing, 0], [1, 0], [1,1]]
        polygon = Polygon(polygonPoints, True)
        p = PatchCollection([polygon], alpha=0.3)
        ax.add_collection(p)
  #  kde = scipy.stats.gaussian_kde(s)
  #  x = [x/100 for x in range(0,101)]
  #  y = kde(x).T
  #  plt.plot(x,y)


data = Shared.getCatastoData()

for trade in range(0,100):
    fig, ax = plt.subplots()
    neighbourhood = [x[trade] for n, x in data.items()]
    plt.title(Shared.getTradeName(trade))
    analyze(fig, ax, neighbourhood)
    fig.savefig('results/trade_' + str(trade) + '.png', bbox_inches='tight')
