from datetime import datetime

from model.model import Model
import networkx as nx
mymodel=Model()
mymodel.buildGraph(5)

v0=mymodel.getAllNodes()[0]

connessa=list(nx.node_connected_component(mymodel._grafo,v0))

v1= connessa[10]

print(v0,v1)

tic=datetime.now()
bestPath, bestObjFun=mymodel.getCamminoOttimo(v0,v1,4)
print("----------")
print(f"Cammino ottimo tra {v0} e {v1} ha peso = {bestObjFun} \n trovato in {datetime.now()-tic} secondi")
print(*bestPath,sep='\n')
