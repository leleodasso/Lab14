import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.grafo = nx.DiGraph()
        self._idMap = {}

    def getStores(self):
        return DAO.getStores()

    def buildGraph(self, store, giorni):
        self.grafo.clear()

        # nodi
        listaNodi = DAO.getOrdiniStore(store)
        print(len(listaNodi))
        self.grafo.add_nodes_from(listaNodi)

        # archi
        #for u in listaNodi:
         #   for v in listaNodi:
          #      if u != v:
           #         print(u.order_id, v.order_id, store, giorni)
            #        arcoOrientato = DAO.getQtaOggettiCompratiNegliOrdini(u, v, store, giorni)
             #       if arcoOrientato and arcoOrientato[0] > 0:
              #          self.grafo.add_edge(u, v, weight=arcoOrientato[0])
        #archi
        for nodo in listaNodi:
            self._idMap[nodo.order_id] = nodo
        listaArchi = DAO.getAllEdges(self._idMap, store, giorni)
        for arco in listaArchi:
            self.grafo.add_edge(arco[0], arco[1], weight=arco[2])


    def getNumeriGrafo(self):
        return self.grafo.number_of_nodes(), self.grafo.number_of_edges()

    def getNodes(self):
        return self.grafo.nodes()


    def getBFSNodesFromTree(self, source):
        tree = nx.bfs_tree(self.grafo, self._idMap[int(source)])
        archi = list(tree.edges())
        nodi = list(tree.nodes())
        return nodi[1:]

    def getDFSNodesFromTree(self, source):
        tree = nx.dfs_tree(self.grafo, source)
        nodi = list(tree.nodes())
        return nodi[1:]

    def getCammino(self, sourceStr):

        source = self._idMap[int(sourceStr)]  # Ottengo il nodo sorgente dalla mappa ID → nodo
        cammino_piu_lungo = [] # Lista per salvare il cammino più lungo trovato finora

        tree = nx.dfs_tree(self.grafo, source) # Creo un albero DFS a partire dal nodo sorgente
        nodi = list(tree.nodes()) # Ottengo tutti i nodi raggiungibili da source tramite DFS

        # Per ogni nodo raggiungibile nell’albero DFS...
        for node in nodi:
            cammino_temporaneo = [node] # Inizializzo il cammino temporaneo partendo dal nodo corrente

            # Risalgo dal nodo corrente fino al nodo sorgente seguendo i predecessori
            while cammino_temporaneo[0] != source:
                # nx.predecessor restituisce un dizionario di liste di predecessori,
                # quindi prendiamo il predecessore del nodo corrente cammino_temporaneo[0]
                pred = nx.predecessor(tree, source, cammino_temporaneo[0])
                # pred è una lista, prendo il primo elemento e lo aggiungo al cammino temporaneo poi vado ripeto
                cammino_temporaneo.insert(0, pred[0])

            # Se il cammino temporaneo è più lungo di quello salvato, lo aggiorno
            if len(cammino_temporaneo) > len(cammino_piu_lungo):
                cammino_piu_lungo = copy.deepcopy(cammino_temporaneo)

        # Restituisco il cammino più lungo trovato
        return cammino_piu_lungo





