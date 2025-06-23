import copy

import networkx as nx
from networkx.classes import neighbors

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo=nx.Graph() #perchè dice semplice, non orientato e pesato
        self._airports=DAO.getAllAirports()
        self._idMapAirports={}
        for a in self._airports:
            self._idMapAirports[a.ID]=a
        self._bestPath = []
        self._bestObjFun = 0


    def getCamminoOttimo(self, v0, v1, t): #t è il numero massimo di tratte
        self._bestPath=[]
        self._bestObjFun=0

        parziale=[v0]

        self._ricorsione(parziale, v1, t)

        return self._bestPath, self._bestObjFun


    def _ricorsione(self, parziale, v1, t):
        #Verificare se parziale è una possibile soluzione
            #verificare se parziale è l'ottimo, quindi meglio del best
            #Esco
        if parziale[-1]== v1 and len(parziale)<t: #coincide con l'aeroporto di termine?Rispetta il vincolo sulle tratte?
            if self.getObjFun(parziale) > self._bestObjFun:
                self._bestObjFun=self.getObjFun(parziale)
                self._bestPath=copy.deepcopy(parziale)
        if len(parziale) >t: #ho superato il numero massimo di tratte:
            return

        #Posso ancora aggiungere nodi
            #Prendo i vicini e aggiungo un nodo alla volta
            #ricorsione
        for n in self._grafo.neighbors(parziale[-1]):
            if n not in parziale:
                parziale.append(n)
                self._ricorsione(parziale,v1,t)
                parziale.pop()





    def getObjFun(self, listOfNodes):
        objVal=0
        for i in range(0,len(listOfNodes)-1):
            objVal+=self._grafo[listOfNodes[i]][listOfNodes[i+1]]["weight"]
        return objVal


    def buildGraph(self,nMin):
        nodes=DAO.getAllNodes(nMin,self._idMapAirports)
        self._grafo.add_nodes_from(nodes)
        self.allArchiV2()
        print("N nodi: ", len(self._grafo.nodes), "N archi: ",self._grafo.number_of_edges())


    def addAllArchiV1(self):
        allEdges=DAO.getAllEdgesV1(self._idMapAirports)
        for e in allEdges:
            if e.aeroportoP in self._grafo and e.aeroportoD in self._grafo:
                if self._grafo.has_edge(e.aeroportoP,e.aeroportoD):
                    self._grafo[e.aeroportoP][e.aeroportoD]["weight"]+=e.peso
                else:
                    self._grafo.add_edge(e.aeroportoP,e.aeroportoD,weight= e.peso)

    def allArchiV2(self):
        allEdges=DAO.getAllEdgesV2(self._idMapAirports)
        for e in allEdges:
            if e.aeroportoP in self._grafo and e.aeroportoD in self._grafo:
                self._grafo.add_edge(e.aeroportoP, e.aeroportoD, weight=e.peso)


    def getGraphDetails(self):
        return self._grafo.number_of_nodes(),self._grafo.number_of_edges()


    def getAllNodes(self):
        nodes= list(self._grafo.nodes)
        nodes.sort(key=lambda x: x.IATA_CODE) #ordiniamo per iata code perchè è quello che visualizziamo nel dropdown (key)
        return nodes


    def getSortedNeighbors(self,node):
        neighbors=self._grafo.neighbors(node) #self._grafo[node] perchè grafo è un dizionario
        neighTuples=[]
        for n in neighbors:
            neighTuples.append((n,self._grafo[node][n]["weight"])) # tuple con nodo e peso dell'arco tra nodo e vicino

        neighTuples.sort(key=lambda x: x[1], reverse=True) #ordino per i pesi
        return neighTuples


    def getPath(self, v0, v1):
        path=nx.dijkstra_path(self._grafo, v0, v1, weight=None) #mettendo weight= None assume che tutti i pesi siano 1 e mi restituisce il cammino minimo
        #path=nx.shortest_path(self._grafo, v0, v1)
        #myDict=dict(nx.bfs_predecessors(self._grafo,v0))
        #path=[v1]
        #while path[0] !=v0:
        #    path.insert(0,myDict[path[0]])
        return path
