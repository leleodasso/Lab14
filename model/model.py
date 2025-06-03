import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._idMap = {}

    def getListaStore(self):
        return DAO.getListaStore()

    def buildGrafo(self, store_id, num_giorni):
        self._idMap.clear()

        listaNodi = DAO.getNodes(store_id)
        self._grafo.add_nodes_from(listaNodi)

        for ordine in listaNodi:
            self._idMap[ordine.order_id] = ordine


        listaArchi = DAO.getAllArchi(store_id, num_giorni)

        for arco in listaArchi:
            self._grafo.add_edge(self._idMap[arco[0]], self._idMap[arco[1]], weight=arco[3])

        return listaArchi

    def getGraphDetails(self):
        return self._grafo.number_of_nodes(), self._grafo.number_of_edges()