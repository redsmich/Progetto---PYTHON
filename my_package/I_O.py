from pandas import read_csv
import matplotlib.pyplot as plt
from numpy import linspace
from scipy.stats import chi2,f
import tkinter as tk
from tkinter import simpledialog, messagebox


def leggi_csv(nomefile):
    '''
    Questa funzione legge un file in formato CSV e ritorna il contenuto del file come un DataFrame pandas
    Parametri: 
        nomefile : Nome del file CSV da leggere.   
    Ritorno: 
        pandas.DataFrame: Dati contenuti nel file CSV. 
    '''
    dati = read_csv(nomefile)
    return dati



def stampa_chi_quadro(valore, gl, a):
    '''
    Questa funzione plotta la distribuzione chi-quadro con gl gradi di libertà, il valore della statistica prodotta dall' omonimo test e il quantile associato al valore alpha
    Parametri:
        valore : valore della statistica prodotto dal test del Chi - Quadro
        gl : gradi di libertà della statistica generati a partire dal test
        a : significatività del test
    '''
    x_max = chi2.ppf(0.999, gl)    #considero il dominio della chi-quadro fino al valore di x associato a 0.999
    x = linspace(0, x_max, 2000)   #divido l'intervallo [0, x_max] in 2000 parti per avere maggiore precisione del plot
    y = chi2.pdf(x, gl)            #calcolo il valore della chi-quadro e ottengo i punti del grafico

    quantile = chi2.ppf(1 - a, gl) #calcolo il valore del quantile associato alla significatività del problema
    
    fig = plt.figure(figsize=(8, 5)) #salvo il plot dell'immagine su una variabile; tutte le modifiche effettuate al grafico vengono salvate su fig (così da poterla esportare come png o pdf )
    
    
    plt.plot(x, y, label=f"Gradi di Libertà={gl}", color="blue") #produce il grafico della statistica e crea un'etichetta con il numero di gradi di libertà 

    #sovrascrivo su x e y (per evitare di creare altre vriabili) l'area che rappresenta la regione di rifiuto
    x = linspace(quantile, x_max, 2000)   
    y = chi2.pdf(x, gl)
    plt.fill_between(x, y, alpha=0.3, color='blue', label=f"Regione di rifiuto")


    #creo la Linea verticale tratteggiata per il quantile e una verticale continua per il valore assunto dalla statistica
    plt.axvline(quantile, color='red', linestyle="--", label=f'Quantile {100*(1-a)}% \nValore del quantile = {quantile: .2f}')
    plt.axvline(valore, color='green', linestyle="-", label=f'Valore della Statistica={valore: .2f}')
    plt.xlabel("Valori della statistica")
    plt.ylabel("Densità di probabilità")
    chi_quadro = "χ²"
    plt.title(f"Distribuzione {chi_quadro} con {gl} gradi di libertà")
    
    
    plt.legend()
    plt.grid()
    plt.show()
    salva_come(fig)
    
    
    
def stampa_fisher(valore, gl1, gl2, a):
    '''
    Questa funzione plotta la distribuzione di Fisher con gl1 e gl2 gradi di libertà, il valore della statistica prodotta dal test di ANOVA e il quantile associato al valore alpha
    Parametri:
        valore : valore della statistica prodotto dal test ANOVA
        gl1, gl2 : gradi di libertà della statistica generati a partire dal test
        a : significatività del test
    '''
    x_max = f.ppf(0.999, gl1, gl2)  
    x = linspace(0, x_max, 2000)  
    y = f.pdf(x, gl1, gl2)

    quantile = f.ppf(1 - a, gl1, gl2)

    fig = plt.figure(figsize=(8, 5))
    
    
    plt.plot(x, y, label=f"F({gl1}, {gl2})", color="blue")

    x = linspace(quantile, x_max, 2000) 
    y = f.pdf(x, gl1, gl2)
    plt.fill_between(x, y, alpha=0.3, color='blue', label=f"Regione di rifiuto")


  
    plt.axvline(quantile, color='red', linestyle="--", label=f'Quantile {100*(1-a)}% \nValore del quantile = {quantile: .2f}')
    plt.axvline(valore, color='green', linestyle="-", label=f'Valore della Statistica={valore: .2f}')
    plt.xlabel("Valori della statistica")
    plt.ylabel("Densità di probabilità")
    plt.title("Distribuzione di Fisher")
    
    plt.legend()
    plt.grid()
    plt.show()
    print(type(fig))
    salva_come(fig)


    
def stampa_statistica(valore_statistica, a):
    '''
    Questa funzione si occupa di stampare la statistica in base al test che si esegue
    Parametri:
        valore_statistica : output prodotto dalla funazione relativa al test scelto
        a : significatività del test
    '''
    if len(valore_statistica) == 2: #se la tupla ritornata ha lunghezza 2 si è scelto il test del chi quadro
        stampa_chi_quadro(valore_statistica[0], valore_statistica[1], a)
    else :
        stampa_fisher(valore_statistica[0], valore_statistica[1],valore_statistica[2], a)
    
    
def scegli_metodo():
    """
    L'esecuzione di questa consente di scegliere quale test effettuare
        valore di ritorno: metodo scelto cioè il nome del test
    """
    def set_metodo(metodo_scelto):    #definisco questa funzione interna per aggiornare lo stato della variabile metodo che                                        è settata come non locale per essere acceduta anche da set_metodo. 
        '''
        Questa funzione, quando viene invocata, modifica lo stato della variabie "metodo" settandolo in base al metodo scelto tramite pulsante
        Parametri:
            metodo_scelto : in questo caso si hanno due possibili scelte, ANOVA o Chi-Quadro
        '''
        nonlocal metodo
        metodo = metodo_scelto
        popup.destroy()   #chiusura della finestra popup aperta dopo aver scelto tra le opzioni
        
        
    metodo = None #setto metodo a un valore di default --> None
    popup = tk.Toplevel() #creo una nuova finestra popup separata dalla finestra principale
    
    #calcolo altezza e larghezza della finestra che si crea
    larghezza = popup.winfo_width()
    altezza = popup.winfo_height()
    #setto le coordinata per centrare la finestra
    x = (popup.winfo_screenwidth() // 2) - (larghezza // 2)
    y = (popup.winfo_screenheight() // 2) - (altezza // 2)
    popup.geometry(f"+{x}+{y}")  #posizionamento della finestra


    tk.Label(popup, text="Scegli il metodo statistico:").pack(pady=20) #etichetta per la finestra pop up della scelta metodo
    #pulsanti per scegliere che metodo usare emtrambi separati da uno spazio di 5 pixel
    #la funzione anonima lambda chiama set_metodo con l'argomento e setta il metodo in base al pulsante cliccato
    tk.Button(popup, text="ANOVA", command=lambda: set_metodo("ANOVA")).pack(pady=5)
    tk.Button(popup, text="Chi-quadro", command=lambda: set_metodo("Chi-quadro")).pack(pady=5)
    tk.Button(popup, text="Annulla", command=lambda: set_metodo(None)).pack(pady=5)
    


    popup.wait_window()  #metto in pausa l'esecuzione del codice finché la finestra pop-up non viene chiusa
    return metodo

def menu_popup():
    '''
    Questa funzione consente l'apertura si un menu pop up per scegliere il test
    '''
    finestra = tk.Tk() #genero manualmente e memorizzo su 'finestra'  la finestra principale vuota che si genererebbe                               automaticamente all'invocazione di una qualsiasi funzione del tipo show per nasconderla all'utente
    finestra.withdraw()  #nascondo la finestra
    
    
    metodo = scegli_metodo() #richiamo la funzione scegli metodo per scegliere il metodo
    if metodo==None:         #se non è stato scelto alcun metodo o se si è scelto annulla, la variabile associata rimane al valore di default e si genera un messaggio di avviso
        messagebox.showwarning("Attenzione", "Nessun metodo selezionato")
        return None, None, None

    
    messagebox.showinfo("REMIND" ,"Ricordarsi di inserire il file CSV nella cartella del progetto.") #messaggio per ricordare di icludere il file nella cartella del progetto

    nome_file = None  #setto nome file a none 
    nome_file = simpledialog.askstring("Input", "Inserisci il nome del file CSV :") #
   
    while nome_file=="": #se non inserisco il nome file l'input preso è una stringa vuota
        messagebox.showwarning("Errore", "Inserire un nome valido") #se il nome non è valido genera un messaggio di errore
        nome_file = simpledialog.askstring("Input", "Inserisci il nome del file CSV:") #chiede di nuovo l'input
        
    if nome_file == 'None' : #se si sceglie annulla
            return None, None, None
    
    
    if not nome_file.endswith(".csv"): #aggiungo l' estensione perchè probabilmente l'utente non la scriverà
        nome_file = nome_file+".csv"

    #set di istruzioni per settare la significatività del test
    alpha = None   
    alpha = simpledialog.askfloat("Inserisci il valore della significatività", "Inserisci il valore della significatività  del test (0 < α < 1):")

    
    if alpha is None:   #se l'utente preme annulla o chiude la finestra, interrompe la funzione
            return None  
        
    while not  (0 < alpha < 1): #se il valore non è valido, mostra un messaggio di errore e chiede di nuovo
        messagebox.showwarning("Valore non valido", "Il valore di α deve essere compreso tra 0 e 1.")
        alpha = simpledialog.askfloat("Inserisci il valore di α", "Inserisci il valore della significatività  del test (0 < α < 1):")

    file = leggi_csv(nome_file)

    return file, metodo, alpha


def scegli_formato():
    '''
    Questa funzione mostra una finestra con due pulsanti, PDF e  PNG e consente  di scegliere in che formato salvare il file
    è analoga alla funzione scegli metodo
    '''
    def set_formato(formato_scelto): #definisco questa funzione interna per aggiornare lo stato della variabile formato che                                        è settata come non locale per essere acceduta anche da set_formato. 
        
        '''
        Questa funzione, quando viene invocata, modifica lo stato della variabie "formato" settandolo in base al formato in cui si vuole salvare l'mmagine scelto tramite pulsante
        Parametri:
            formato_scelto : in questo caso si hanno due possibili scelte, PDF o PNG
        '''
        nonlocal formato
        formato = formato_scelto
        popup.destroy() #chiusura della finestra popup aperta dopo aver scelto tra le opzioni
        
        
    formato = None  #setto formato a un valore di default --> None
    popup = tk.Toplevel() #creo una nuova finestra popup separata dalla finestra principale
    popup.title("Scelta formato")
    #calcolo altezza e larghezza della finestra che si crea
    larghezza = popup.winfo_width()
    altezza = popup.winfo_height()
    #setto le coordinata per centrare la finestra
    x = (popup.winfo_screenwidth() // 2) - (larghezza // 2)
    y = (popup.winfo_screenheight() // 2) - (altezza // 2)
    popup.geometry(f"+{x}+{y}")  #posizionamento della finestra

    tk.Label(popup, text="Scegli il formato:").pack(pady=20) #etichetta per la finestra pop up della scelta metodo
    #pulsanti per scegliere in che formato salvare, emtrambi separati da uno spazio di 5 pixel
    #la funzione anonima lambda chiama set_metodo con l'argomento e setta il metodo in base al pulsante cliccato
    tk.Button(popup, text="PDF", command=lambda: set_formato("PDF")).pack(pady=5)
    tk.Button(popup, text="PNG", command=lambda: set_formato("PNG")).pack(pady=5)
    tk.Button(popup, text="Annulla", command=lambda: set_formato(None)).pack(pady=5)
    
    popup.wait_window()  #metto in pausa l'esecuzione del codice finché la finestra pop-up non viene chiusa
    
    return formato

def salva_come(figura):
    '''
    Questa funzione consente di salvare come immagine una figura
        Parametri: figura che è di tipo classe Figure di matplotlib
    '''
    
    formato = None  #setto la varibile formato a un valore di default
    finestra = tk.Tk()#genero manualmente e memorizzo su 'finestra'  la finestra principale vuota che si genererebbe                               automaticamente all'invocazione di una qualsiasi funzione del tipo show per nasconderla all'utente
    finestra.withdraw()  #nascondo la finestra
    
    risposta = messagebox.askyesno("Salvataggio", "Vuoi salvare il grafico?")
    
    if not risposta : #se la risposta è no termina la funzione
        return
    
    
    formato = scegli_formato()  #scelta del formato
    if not formato: #se scelgo annulla o chiudo la finestra avverte che non è stato selezionato alcun formato
        messagebox.showwarning("Errore", "Nessun formato selezionato!")
        return
    
    
    if formato: #se è stato scelto un formato chiedo il nome con cui salvare il file
        nome_file = simpledialog.askstring("Nome file", "Inserisci il nome del file (senza estensione):")
        
        if nome_file: #se è stato inserito un nome valido salvo con tale nome
            figura.savefig(f"{nome_file}.{formato}")
            messagebox.showinfo("Successo", f"Grafico salvato come {nome_file}.{formato}")
        else:
            messagebox.showwarning("Errore", "Il nome del file non può essere vuoto.")
