import Shared
import scipy.stats.kde
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from PIL import Image

def analyze(fig, ax, trade, tradeQuantities):
    m = max(tradeQuantities)
    if(m == 0):
        return
    normalized = [x/m for x in tradeQuantities]
    s = sorted(normalized)
   # c = np.cumsum(s)
    x = [x/(len(tradeQuantities)-1) for x in range(0,len(tradeQuantities))]
    ax.plot(x,s)

    kde = scipy.stats.gaussian_kde(s)
    x = [x/100 for x in range(0,101)]
    y = kde(x).T
    ax.plot(x,y)

    mn = np.median(s)
    sd = np.std(s)
    mnsd = mn + 2 * sd
    if(mnsd < 1):
        crossing = [b for b in s > mnsd].index(True) / len(s)
        xb, xt = ax.get_xlim()
        yb, yt = ax.get_ylim()
        polygonPoints = [[crossing, yt], [crossing, yb], [xt, yb], [xt,yt]]
        polygon = Polygon(polygonPoints, True)
        p = PatchCollection([polygon], alpha=0.3)
        ax.add_collection(p)
    map = recolourMap(normalized, trade)
    fig.savefig('results/trade_' + str(trade) + '.png', bbox_inches='tight')
    if(mnsd < 1):
        return np.argmax(normalized)
    return 0

def recolourMap(values, trade):
    with open("florence-map-small.png", 'rb') as fp:
        fm = Image.open(fp)
        pixels = fm.load()
        for x in range(fm.width):
            for y in range(fm.height):
                px = pixels[x, y]
                for i, n in enumerate(Shared.getNeighbourhoods().keys()):
                    g = int(n / 10)
                    b = n % 10
                    if px[0] == 0 and px[1] == g and px[2] == b:
                        pixels[x, y] = (int(values[i] * 255), 0, 0, 255)
        fm.save("results/trademap_" + str(trade) + ".png")
    return fm

def getMCN(trade, tradesmen, population):
    fig, ax = plt.subplots()
    neighbourhood = [x[trade] for n, x in tradesmen.items()]
    totalTradesmen = sum(neighbourhood)
    if(totalTradesmen > 20):
        perCapita = [n / p for n, p in zip(neighbourhood, population)]
        plt.title(Shared.getTradeName(trade))
        bimodal = analyze(fig, ax, trade, perCapita)
        return bimodal
    return -1

tradesmen, population, tradeWealth = Shared.getCatastoData()
centralized = []
decentralized = []
for trade in range(0,100):
    bimodal = getMCN(trade, tradesmen, population)
    if bimodal:
        centralized.append(Shared.getTradeName(trade))
    else:
        decentralized.append(Shared.getTradeName(trade))
print(centralized)
print(decentralized)