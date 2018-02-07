# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 16:18:57 2018

@author: 김용우
"""

#샘플 150개, 피쳐 2개, 중심을 3개로 같는 데이터들을 생성한다.
from sklearn.datasets import make_blobs
X,y = make_blobs(n_samples=150, n_features=2, centers=3,cluster_std=0.5,shuffle=True,random_state=0)

import matplotlib.pyplot as plt
plt.scatter(X[:,0],X[:,1],c='white',marker='o',edgecolor='black', s=50)
plt.grid()
plt.show()



# k-means 알고리즘을 통해 그루핑
from sklearn.cluster import KMeans
km=KMeans(n_clusters=3, init='random',n_init=10 ,max_iter=300,tol=1e-04,random_state=0)
y_km=km.fit_predict(X)

plt.scatter(X[y_km==0,0],X[y_km==0,1],s=50,c='green',marker='s',label='cluster 1')
plt.scatter(X[y_km==1,0],X[y_km==1,1],s=50,c='orange',marker='o',label='cluster 2')
plt.scatter(X[y_km==2,0],X[y_km==2,1],s=50,c='blue',marker='v',label='cluster 3')
plt.scatter(km.cluster_centers_[:,0],km.cluster_centers_[:,1],s=250,marker='*',c='red',label='centroids')
plt.legend()
plt.grid()
plt.show()


#Kmean 모델안의 SSE값
print('Distortion: %.2f' % km.inertia_)

#엘보우는 k=3일때
distortions=[]
for i in range(1,11):
    km=KMeans(n_clusters=i, init='k-means++',n_init=10,max_iter=300,random_state=0)
    km.fit(X)
    distortions.append(km.inertia_)
plt.plot(range(1,11),distortions,marker='o')
plt.xlabel('Number of clusters')
plt.ylabel('Distortion')
plt.show()

#실루엣 계수
km=KMeans(n_clusters=3, init='k-means++', n_init=10, max_iter=300, tol=1e-04,random_state=0)
y_km=km.fit_predict(X)

import numpy as np
from matplotlib import cm
from sklearn.metrics import silhouette_samples
cluster_labels=np.unique(y_km)
n_clusters=cluster_labels.shape[0]
silhouette_vals=silhouette_samples(X,y_km,metric='euclidean')
y_ax_lower, y_ax_upper=0 , 0
yticks=[]
for i, c in enumerate(cluster_labels):
    c_silhouette_vals=silhouette_vals[y_km == c]
    c_silhouette_vals.sort()
    y_ax_upper += len(c_silhouette_vals)
    color = cm.jet(i/n_clusters)
    plt.barh(range(y_ax_lower, y_ax_upper),c_silhouette_vals,height=1.0,edgecolor='none',color=color)
    yticks.append((y_ax_lower + y_ax_upper)/2)
    y_ax_lower += len(c_silhouette_vals)
silhouette_avg=np.mean(silhouette_vals)
plt.axvline(silhouette_avg,color="red",linestyle="--")
plt.yticks(yticks,cluster_labels+1)
plt.ylabel('Cluster')
plt.xlabel('Silhouette coefficient')
plt.show()

#그룹은 3개인데 k를 2로 설정하면
km=KMeans(n_clusters=2, init='k-means++',n_init=10,max_iter=300,tol=1e-04,random_state=0)
y_km=km.fit_predict(X)

plt.scatter(X[y_km==0,0],X[y_km==0,1],s=50,c='lightgreen',marker='s',label='cluster 1')
plt.scatter(X[y_km==1,0],X[y_km==1,1],s=50,c='orange',marker='o',label='cluster 2')
plt.scatter(km.cluster_centers_[:,0],km.cluster_centers_[:,1],s=250,c='red',marker='*',label='centroids')
plt.legend()
plt.grid()
plt.show()

#그때의 실루엣계수
cluster_labels=np.unique(y_km)
n_clusters=cluster_labels.shape[0]
silhouette_vals=silhouette_samples(X,y_km,metric='euclidean')
y_ax_lower,y_ax_upper= 0 , 0
yticks=[]
for i, c in enumerate(cluster_labels):
    c_silhouette_vals=silhouette_vals[y_km == c]
    c_silhouette_vals.sort()
    y_ax_upper += len(c_silhouette_vals)
    color=cm.jet(i/n_clusters)
    plt.barh(range(y_ax_lower,y_ax_upper),c_silhouette_vals,height=1.0,edgecolor='none',color=color)
    yticks.append((y_ax_lower + y_ax_upper)/2)
    y_ax_lower += len(c_silhouette_vals)
silhouette_avg=np.mean(silhouette_vals)
plt.axvline(silhouette_avg,color="red",linestyle="--")
plt.yticks(yticks,cluster_labels +1)
plt.ylabel('Cluster')
plt.xlabel('Silhouette coefficient')
plt.show()

# Example 생성
import pandas as pd
import numpy as np
np.random.seed(123)
variables=['X','Y','Z']
labels=['ID_0','ID_1','ID_2','ID_3','ID_4']
X=np.random.random_sample([5,3])*10
df=pd.DataFrame(X,columns=variables, index=labels)
df


#거리계산
from scipy.spatial.distance import pdist, squareform
row_dist = pd.DataFrame(squareform(pdist(df,metric='euclidean')),columns=labels, index=labels)
row_dist


#표생성
from scipy.cluster.hierarchy import linkage
#row_clusters = linkage(row_dist,method='complete',metric='euclidean')
row_clusters=linkage(pdist(df, metric='euclidean'),method='complete')
row_clusters=linkage(df.values,method='complete',metric='euclidean')

pd.DataFrame(row_clusters, columns=['row label 1','row label 2','distance','no. of items in clust.'],
             index=['cluster %d' %(i+1) for i in range(row_clusters.shape[0])])



#계층도
from scipy.cluster.hierarchy import dendrogram
fow_dendr = dendrogram(row_clusters,labels=labels) 
plt.tight_layout()
plt.ylabel('Euclidean distance')
plt.show()

#열지도 + 계층도
fig=plt.figure(figsize=(8,8))
axd=fig.add_axes([0.09,0.1,0.2,0.6])
row_dendr=dendrogram(row_clusters, orientation= 'left')

df_rowclust= df.ix[row_dendr['leaves'][::-1]]

axm=fig.add_axes([0.23,0.1,0.6,0.6])
cax=axm.matshow(df_rowclust,interpolation='nearest',cmap='hot_r')

axd.set_xticks([])
axd.set_yticks([])
for i in axd.spines.values():
    i.set_visible(False)
fig.colorbar(cax)
axm.set_xticklabels([''] + list(df_rowclust.columns))
axm.set_yticklabels(['']+list(df_rowclust.index))
plt.show()

#사이킷 런에서의 k개의 군집화
from sklearn.cluster import AgglomerativeClustering
ac=AgglomerativeClustering(n_clusters=2, affinity='euclidean',linkage='complete')
labels= ac.fit_predict(X)
print('Cluster labels: %s' % labels)

#달모양 샘플 형성
from sklearn.datasets import make_moons
X, y = make_moons(n_samples=200,noise=0.05,random_state=0)
plt.scatter(X[:,0],X[:,1])
plt.show()

#K-Means 알고리즘, 응집성 알고리즘을 이용한 군집화
f, (ax1,ax2)=plt.subplots(1,2,figsize=(8,3))
km=KMeans(n_clusters=2,random_state=0)
y_km=km.fit_predict(X)
ax1.scatter(X[y_km==0,0],X[y_km==0,1],c='blue',marker='o',s=40,label='cluster 1')
ax1.scatter(X[y_km==1,0],X[y_km==1,1],c='red',marker='s',s=40,label='cluster 2')
ax1.set_title('K-means clustering')
ac=AgglomerativeClustering(n_clusters=2,affinity='euclidean',linkage='complete')
y_ac=ac.fit_predict(X)
ax2.scatter(X[y_ac==0,0],X[y_ac==0,1],c='blue',marker='o',s=40,label='cluster 1')
ax2.scatter(X[y_ac==1,0],X[y_ac==1,1],c='red',marker='s',s=40,label='cluster 2')
ax2.set_title('Agglomerative clustering')
plt.legend()
plt.show()


#DBSCAN을 이용한 군집화
from sklearn.cluster import DBSCAN
db=DBSCAN(eps=0.2,min_samples=5,metric='euclidean')
y_db=db.fit_predict(X)
plt.scatter(X[y_db==0,0],X[y_db==0,1],c='blue',marker='o',s=40,label='cluster 1')
plt.scatter(X[y_db==1,0],X[y_db==1,1],c='red',marker='s',s=40,label='cluster 2')
plt.legend()
plt.show()



