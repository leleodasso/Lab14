import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._store = None
        self._selectedNode = None

    def fillDDstore(self):
        listaStore = self._model.getStores()
        for store in listaStore:
            self._view._ddStore.options.append(
                ft.dropdown.Option(text=store.store_name, data=store.store_id, on_click=self.handleStore))

    def handleStore(self, e):
        self._store = e.control.data




    def handleCreaGrafo(self, e):
        if self._store is None:
            self._view.txt_result.clean()
            self._view.txt_result.controls.append(ft.Text("DEVI SELESZIONARE UNO STORE"))
            self._view.update_page()

        giorni =  self._view._txtIntK.value
        try:
            int(giorni)
        except ValueError:
            self._view.txt_result.clean()
            self._view.txt_result.controls.append(ft.Text("DEVI IMPOSTARE NUMERO DI GIORNI"))
            self._view.update_page()

        self._model.buildGraph(self._store, giorni)

        numNodi, numArchi = self._model.getNumeriGrafo()
        self._view.txt_result.clean()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato:"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {numNodi}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {numArchi}"))
        self.fillDDNode()
        self._view.update_page()


    def fillDDNode(self):
        listaNodi = self._model.getNodes()
        for nodo in listaNodi:
            self._view._ddNode.options.append(
                ft.dropdown.Option(text=nodo.order_id, data=nodo, on_click=self.handleDDNodo))

    def handleDDNodo(self, e):
        self._selectedNode = e.control.data

    def handleCerca(self, e):
        if self._selectedNode is None:
            self._view.txt_result.controls.append(ft.Text("DEVI SELESZIONARE UN NODO"))
            self._view.update_page()


        listaNodiLunga = self._model.getCammino(self._selectedNode.order_id)

        self._view.txt_result.clean()
        self._view.txt_result.controls.append(ft.Text(f"Nodo di partenza: {self._selectedNode.order_id}"))
        for el in listaNodiLunga:
            self._view.txt_result.controls.append(ft.Text(f"{el.order_id}"))
        self._view.update_page()



    def handleRicorsione(self, e):
        pass