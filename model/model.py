import copy

from database.consumo_DAO import ConsumoDAO
from database.impianto_DAO import ImpiantoDAO

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class Model:
    def __init__(self):
        self._impianti = None
        self.load_impianti()

        self.__sequenza_ottima = []
        self.__costo_ottimo = -1

    def load_impianti(self):
        """ Carica tutti gli impianti e li setta nella variabile self._impianti """
        self._impianti = ImpiantoDAO.get_impianti()

    def get_consumo_medio(self, mese:int):
        """
        Calcola, per ogni impianto, il consumo medio giornaliero per il mese selezionato.
        :param mese: Mese selezionato (un intero da 1 a 12)
        :return: lista di tuple --> (nome dell'impianto, media), es. (Impianto A, 123)
        """
        # TODO
        result = []
        for impianti in self._impianti:
            id_impiant = impianti["id"]
            nome = impianti["nome"]
            consumi = ConsumoDAO.get_consumi(id_impianto = id_impiant)
            consumi_mese = [c for c in consumi if c["mese"] == mese]
            if not consumi_mese:
                media = 0
            else:
                somma = sum(c["kwh"] for c in consumi_mese)
                media = somma // len(consumi_mese)
                result.append((nome, media))
        return result

    def get_sequenza_ottima(self, mese:int):
        """
        Calcola la sequenza ottimale di interventi nei primi 7 giorni
        :return: sequenza di nomi impianto ottimale
        :return: costo ottimale (cioè quello minimizzato dalla sequenza scelta)
        """
        self.__sequenza_ottima = []
        self.__costo_ottimo = -1
        consumi_settimana = self.__get_consumi_prima_settimana_mese(mese)

        self.__ricorsione([], 1, None, 0, consumi_settimana)

        # Traduci gli ID in nomi
        id_to_nome = {impianto.id: impianto.nome for impianto in self._impianti}
        sequenza_nomi = [f"Giorno {giorno}: {id_to_nome[i]}" for giorno, i in enumerate(self.__sequenza_ottima, start=1)]
        return sequenza_nomi, self.__costo_ottimo

    def __ricorsione(self, sequenza_parziale, giorno, ultimo_impianto, costo_corrente, consumi_settimana):
        """ Implementa la ricorsione """
        # TODO
        scelta = self._impianti.id
        if len(sequenza_parziale) == 7:
            if costo_corrente < consumi_settimana:
                self.__costo_ottimo = costo_corrente
                self.__sequenza_ottima = sequenza_parziale.copy()
        else:
            for scelt in scelta:
                consumo_giorno = consumi_settimana[scelt][giorno]
                if giorno == 0:
                    costo_giorno = consumo_giorno
                else:
                    if scelta != ultimo_impianto:
                        costo_giorno = costo_corrente + 5
                    else:
                        costo_giorno = costo_corrente

            sequenza_parziale.append(scelta)
            sequenza_parziale.pop()
            self.__ricorsione([], giorno + 1, None, 0, consumi_settimana )

    def __get_consumi_prima_settimana_mese(self, mese: int):
        """
        Restituisce i consumi dei primi 7 giorni del mese selezionato per ciascun impianto.
        :return: un dizionario: {id_impianto: [kwh_giorno1, ..., kwh_giorno7]}
        """
        # TODO
        dizionario = {}
        for impianti in self._impianti:
            id_impiant = impianti["id"]
            consumi = ConsumoDAO.get_consumi(id_impianto = id_impiant)
            consumi_mese = [c for c in consumi if c["mese"] == mese]
            lista_consumi_giorni = consumi_mese[:7]
            dizionario[impianti["nome"]] = lista_consumi_giorni
        return dizionario