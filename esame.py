#########################################
# Corso di studi AIDA
#Università degli studi di Trieste
# Programming Lab
# Traccia https://docs.google.com/document/d/e/2PACX-1vSkUlMTmmHutE6c4q_6SIByt7VEP2n2BmA8r-O7ulbtGuBKtxKQF9cPv36fR0AbGKu538rtM9PzDpJd/pub
# Autore: Nicola Gigante
# Data: 09/02/2022 
#########################################

import datetime

# Example: 1854-2
CSV_DATE_FORMAT = "%Y-%m"


class ExamException(Exception):
    """
    Eccezione lanciata in caso di errore di validazione
    """
    pass


class CSVTimeSeriesFile():
    """
    Legge un file csv e lo inizializza e con get_data fa le varie validazioni
    """

    def __init__(self, name):
        """
        Inizializa classe con filename
        name=name of the csv file
        """

        self.name = name

    def get_data(self):
        """
        return lista di liste
        se il file non esiste o il file non è leggibile alza un eccezione(ExamException)
        se il file non è ordinato o ha duolicati o ha buchi temporali alza un eccezione(ExamException)
        """

        # Se il file non esiste o non e' leggibile lancio Exame ecpetion
        try:
            csv_file = open(self.name, 'r')
        except Exception as e:
            raise ExamException(f"Can't open the file with name {self.name}, Error: {e}")

        if not csv_file.readable():
            raise ExamException(f"Can't read the file with name {self.name}")



        # Array che contiene i risultati
        data = []
        data_str=[]
        chack=False

        # ignoro la prima linea
        csv_file.readline()

        # Leggo linea per linea, strpit e aggiungo data
        for idx, line in enumerate(csv_file):

            line = line.strip()
            element_str = line.split(',')
            
            element_str[1]=float(element_str[1])
            data_str.append(element_str)

            try:
                element = line.split(',')
                date_string = element[0]
                date = datetime.datetime.strptime(date_string, CSV_DATE_FORMAT)
                element[0] = date

                chack=True
            except Exception as e:
                print(f"line `{line}` is not valid")
                continue

            data.append(element)

        # controllo che sia in ordine e senza duplicati
        for i in range(len(data) - 1):
            element = data[i]
            date = element[0]
            next_element = data[i + 1]
            next_date = next_element[0]

            next_month = datetime.datetime(date.year + int(date.month / 12), ((date.month % 12) + 1), 1)

            chack=True

            if next_date != next_month:
                raise ExamException("not consecutive or missing values")
        
        #vado poi ad inserire i dati in formato '1858-02',122 per stamparli come richiesto
        if chack is True:
            element_str[1]=float(element_str[1])
            data_str.append(element_str)

        # Chiudo il file
        csv_file.close()

        return data_str



def compute_avg_monthly_difference(time_series, first_year, last_year):
    """
        calcola la differenza media del numero di passeggeri mensile tra anni consecutivi e fa le varie validazioni sui dati in imput
        """
    # controllo che gli anni siano str
    if not type(first_year) is str:
        raise ExamException('Error, year must be str')

    if not type(last_year) is str:
        raise ExamException('Error, year must be str')

    #controllo che gli anni non siano nulli
    if first_year is None:
        raise ExamException('Error missing value')
    
    if last_year is None:
        raise ExamException('Error missing value')

    #ontrollo che i valori inseriti rispttino i criteri del formato AAAA
    if not len(first_year)==4:
        raise ExamException('Error, format must be "AAAA"')

    if not len(last_year)==4:
        raise ExamException('Error, format must be "AAAA"')

    if int(first_year) > int(last_year):
        raise ExamException(f'{first_year} is smaller than {last_year}')

    chack = True
    try:
    # converto a int
        int(first_year)
        int(last_year)
    except ValueError:
        chack = False
    if chack:
        pass
    else:
        raise ExamException(f'{first_year} or {last_year} are not a integer')

    new_time_series = []

    # Ciclo sulle righe di time_series
    for string_row in time_series:

        # preparo una lista di supporto per salvare i dati
        new_data = []

        # Ciclo su tutti gli elementi della riga con un
        # enumeratore(ottengo gratis l'indice di posizione dell'elemento.
        for i, element in enumerate(string_row):

            if i == 0:
                # splitto sulla barra per escluderla
                dat = element.split('-')

                # unisco i prodotti dello split
                new_data.append(int(dat[0]))
                new_data.append(int(dat[1]))

            else:
                new_data.append(element)

        # salvo sulla lista preparata
        new_time_series.append(new_data)
    # inizializzo delle liste su cui salvarmi i valori
    temporary = []
    y = 0
    avarange = []
    # imposto check di defoult a False (mi servirà in seguito per alzare un'eccezione)
    check = False

    # ciclo sul range dei mesi
    for i in range(1, 13):

        # ciclo sulle righe della lista appena creata
        for string_row in new_time_series:

            # Controllo se il primo carattere della stringa nella riga è compreso tra il primo anno e l'ultimo anno. Se lo è, la riga è considerata valida e il codice passa alla riga successiva.In caso contrario, la riga viene considerata non valida il codice passa alla riga successiva.

            if string_row[0] in range(int(first_year), int(last_year) + 1):

                if string_row[1] == i:
                    # allora l'aggiungo a temporary
                    temporary.append(string_row[2])

                # passato
                check = True

        # altrimenti alzo l'eccezione
        if check == False:
            raise ExamException('Error, year not found')

        # controllo se l'indice corrente è inferiore alla lunghezza dell'elenco.Se lo è stampo il valore dell'indice.
        for i in range(0, len(temporary) - 1):
            # Calcolo la differenza dei passeggeri
            y += temporary[i + 1] - temporary[i]

            #la divido per l'arco temporale per ottenere l’incremento medio
            a=y/(len(temporary)-1)



        
        avarange.append(a)

        #arrotondo
        rounded_avarange=  [round(x,1) for x in avarange] 

    return rounded_avarange


time_series_file = CSVTimeSeriesFile(name='data.csv')
time_series = time_series_file.get_data()
print(time_series)
print('==========================================================')
print('Incrementi medi del periodo')
print('==========================================================')
print(compute_avg_monthly_difference(time_series, '1949', '1951'))
print('==========================================================')
