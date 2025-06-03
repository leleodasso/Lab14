import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def fillDDStore(self):
        listaStore = self._model.getListaStore()
        for store in listaStore:
            self._view._ddStore.options.append(ft.dropdown.Option(text=store[0], key=store[1]))
        pass


    def handleCreaGrafo(self, e):
        store_id = self._view._ddStore.value
        if store_id == "" or store_id == None:
            print("err")
            self._view.txt_result.clean()
            self._view.txt_result.controls.append(ft.Text("DEVI SELEZIONARE UNO STORE"))
            self._view.update_page()
            return
        num_giorni = self._view._txtIntK.value
        if num_giorni == "" or num_giorni is None or not isinstance(int(num_giorni), int) or int(num_giorni) <= 0:
            print("err")
            print(num_giorni)
            self._view.txt_result.clean()
            self._view.txt_result.controls.append(ft.Text("DEVI DIGITARE IL *NUMERO* DI GIORNI"))
            self._view.update_page()
            return



        self._model.buildGrafo(store_id, num_giorni)
        num_nodi, num_archi = self._model.getGraphDetails()
        self._view.txt_result.clean()
        self._view.txt_result.controls.append(ft.Text("grafo creato correttamente"))
        self._view.txt_result.controls.append(ft.Text(f"Numero Nodi: {num_nodi} "))
        self._view.txt_result.controls.append(ft.Text(f"Numero Archi: {num_archi} "))
        self._view.update_page()

        pass





    def handleCerca(self, e):
        pass

    def handleRicorsione(self, e):
        pass
