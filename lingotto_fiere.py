import csv

#creo le classi dei vari oggetti
class Espositore:
    def __init__(self, codiceE, nomeE, cognomeE):
        self.codiceE = codiceE
        self.nomeE = nomeE
        self.cognomeE = cognomeE

    def __str__(self):
        return f"({self.codiceE}) {self.nomeE} {self.cognomeE}"

class Stand:
    def __init__(self, codiceS, superficie, padiglione, prezzobase):
        self.codiceS = codiceS
        self.superficie = superficie
        self.padiglione = padiglione
        self.prezzobase = prezzobase
        self.espositoreS = None

    def calcolaprezzo(self):
        return self.prezzobase

    def __lt__(self, other):
        return self.calcolaprezzo() < other.calcolaprezzo()

    def __str__(self):
        if self.espositoreS is None:
            stato = "Disponibile"
        else:
            stato = f"Occupato da {self.espositoreS}"
        return f"({self.codiceS}) {self.superficie} mq, padiglione {self.padiglione}, {self.calcolaprezzo():.2f}€ - {stato}"

class StandStandard(Stand):
    def calcolaprezzo(self):
        return self.prezzobase

class StandPrese(Stand):
    def __init__(self, codiceS, superficie, padiglione, prezzobase, prese):
        super().__init__(codiceS, superficie, padiglione, prezzobase)
        self.prese = prese

    def calcolaprezzo(self):
        return self.prezzobase * (1 + 0.07 * self.prese)

    def __str__(self):
        base_str = super().__str__()
        return f"{base_str} - prese elettriche: {self.prese}"

class StandPremium(Stand):
    def __init__(self, codiceS, superficie, padiglione, prezzobase, posizione):
        super().__init__(codiceS, superficie, padiglione, prezzobase)
        self.posizione = posizione

    def calcolaprezzo(self):
        return self.prezzobase * 1.30

    def __str__(self):
        base_str = super().__str__()
        return f"{base_str} - posizione stand: {self.posizione}"

#modifico la classe principale per gestire il programma
class LingottoFiere:
    """Inizializza gli attributi e le strutture dati"""
    def __init__(self, nome):
        self.nome = nome
        self.listaStand = []
        self.listaEspositori = []

    def get_nome(self):
        return self.nome

    def set_nome(self, nuovo_nome):
        self.nome = nuovo_nome

    def carica_file_dati(self, file_path):
        """Carica i dati (stand ed espositori) dal file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as dati:
                reader = csv.reader(dati)
                for riga in reader:
                    if not riga:
                        continue
                    codiceunivoco = riga[0]
                    if codiceunivoco[0:2] == 'ST':
                        codicestand = riga[0]
                        superficie = int(riga[1])
                        padiglione = int(riga[2])
                        prezzobase = int(riga[3])
                        if len(riga) == 4:
                            nuovo_stand = StandStandard(codicestand, superficie, padiglione, prezzobase)
                            self.listaStand.append(nuovo_stand)
                        elif len(riga) == 5:
                            try:
                                valoreprese = int(riga[4])
                                nuovo_stand = StandPrese(codicestand, superficie, padiglione, prezzobase, valoreprese)
                            except ValueError:
                                posizione = riga[4]
                                nuovo_stand = StandPremium(codicestand, superficie, padiglione, prezzobase, posizione)
                            self.listaStand.append(nuovo_stand)
                    if codiceunivoco[0:2] == 'ES':
                        codice = riga[0]
                        nome = riga[1]
                        cognome = riga[2]
                        nuovo_espositore = Espositore(codice, nome, cognome)
                        self.listaEspositori.append(nuovo_espositore)
        except FileNotFoundError:
            raise FileNotFoundError

    def assegna_stand_a_espositore(self, codice_stand, codice_espositore):
        """Associa uno stand a un espositore"""
        stand_trovato = None
        for s in self.listaStand:
            if s.codiceS == codice_stand:
                stand_trovato = s
                break
        espositore_trovato = None
        for e in self.listaEspositori:
            if e.codiceE == codice_espositore:
                espositore_trovato = e
                break
        if stand_trovato is None or espositore_trovato is None:
            raise Exception("Stand o espositore non trovati")
        if stand_trovato.espositoreS is not None:
            raise Exception("Stand già occupato")
        for s in self.listaStand:
            if s.espositoreS == espositore_trovato:
                raise Exception("L'espositore ha già uno stand assegnato")
        stand_trovato.espositoreS = espositore_trovato

    def elenca_espositori(self):
        """Stampa l'elenco degli espositori mostrando, per ognuno, lo stand a cui è associato, quando applicabile """
        for esp in self.listaEspositori:
            stand_associato = None
            for s in self.listaStand:
                if s.espositoreS == esp:
                    stand_associato = s.codiceS
                    break
            if stand_associato:
                print(f"Codice: {esp.codiceE} - Nome completo: {esp.nomeE} {esp.cognomeE} -> stand: {stand_associato}")
            else:
                print(f"Codice: {esp.codiceE} - Nome completo: {esp.nomeE} {esp.cognomeE}")

    def stand_ordinati_per_prezzo(self):
        """Restituisce la lista ordinata degli stand in base al prezzo"""
        return sorted(self.listaStand)