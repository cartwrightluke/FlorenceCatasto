import Shared
import scipy.stats.kde
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import scipy.stats
import sklearn.cluster
import networkx as nx

def analyze(t1Data, t2Data):
    m1 = max(t1Data)
    m2 = max(t2Data)
    normalized1 = [x/m1 for x in t1Data]
    normalized2 = [x/m2 for x in t2Data]
    #plt.scatter(normalized1,normalized2)
    #plt.show()
    return scipy.stats.linregress(t1Data,t2Data)[2]


tradesmen, population, tradeWealth = Shared.getCatastoData()

threshold = 20
centralized = []
decentralized = []
cormap = []
validTrades = []
for trade1 in range(1,100):
    t1Data = [x[trade1] for n, x in tradesmen.items()]
    t1Sum = sum(t1Data)
    if(t1Sum > threshold):
        validTrades.append(trade1)
        tmp = []
        for trade2 in range(1,100):
            t2Data = [x[trade2] for n, x in tradesmen.items()]
            t2Sum = sum(t2Data)
            if(t2Sum > threshold):
                perCapita1 = [n / p for n, p in zip(t1Data, population)]
                perCapita2 = [n / p for n, p in zip(t2Data, population)]
                correlation = analyze(perCapita1, perCapita2)
                tmp.append(correlation)
        cormap.append(tmp)

c = np.empty([len(cormap), len(cormap)])
for x in range(0,len(cormap)):
    for y in range(0, len(cormap)):
        c[x, y] = cormap[x][y]




ap = sklearn.cluster.AffinityPropagation(damping = 0.9 , affinity='precomputed')
#ap = sklearn.cluster.KMeans()
wmin = scipy.mean(c)
#ap = sklearn.cluster.MeanShift(bandwidth=100, cluster_all=False)
#ap.fit(c)
labels = ap.fit_predict(c)
print(labels)
tl = []
Gl = []
for label in range(min(labels), max(labels) +1):
    tl.append([])
    Gl.append(nx.Graph())
    for i in range(len(labels)):
        if(labels[i] == label):
            trade = validTrades[i]
            tl[label].append(Shared.getTradeName(trade))
            Gl[label].add_node(Shared.getTradeName(trade))

    weights = []
    for i in range(len(labels)):
        if(labels[i] == label):
            for j in range(len(labels)):
                if(labels[j] == label):
                    for x in range(1,4):
                        highTrade = np.argmax(c[i] == sorted(c[i], reverse = True)[x])
                        w = c[i][highTrade]
                        Gl[label - min(labels)].add_edge(Shared.getTradeName(i),Shared.getTradeName(highTrade),weight=w)
                       # if(highTrade > i):
                       #     weights.append(w)

    for node in Gl[label-min(labels)].nodes():


    print("Group " + str(label))
    nx.draw(Gl[label - min(labels)],width=4,edge_cmap=plt.cm.Blues,with_labels=True)
    plt.show()
print(tl)



#plt.imshow(labels)

fig = plt.figure(figsize=(6, 3.2))
ax = fig.add_subplot(111)
plt.imshow(c)
ax.set_aspect('equal')
plt.colorbar(orientation='vertical')
plt.show()
