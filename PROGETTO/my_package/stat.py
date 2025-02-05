from pandas import DataFrame
from numpy import sum, outer, mean
import tkinter as tk
from tkinter import simpledialog, messagebox
from scipy.stats import chi2, f

def Chi_Quadro (dati):
    ''' Questa funzione calcola la statistica Chi - Quadro per l'omonimo test 
            Parametri: insieme dei dati come CSV
    '''
    tc = dati.values         #tabella di contingenza
    r_sum = tc.sum(axis = 1) #vettore contenente la somma di ogni riga
    c_sum = tc.sum(axis = 0) #vettore contenente la somma di ogni colonna
    n = tc.sum()             #somma di tutti i valori
    
    prod = outer(r_sum, c_sum)                          #matrice contentente i prodotti tra ri,cj
    chi_quadro = (((tc - prod/n) ** 2) / (prod / n)).sum() #calcolo del valore della statistica
    gl = (len(r_sum)- 1) * (len(c_sum) - 1)                #calcolo gradi di libertà
    
    return chi_quadro, gl

def Chi_Quadro_test(Chi_quadro_output, alpha):
    '''
    Questa funznione confronta la statistica Chi - Quadro con il quantile relativo alla significatività scelta  
        Parametri: Chi_quadro_output (valore ritornato dalla funzione Chi_Quadro), alpha (significatività)
    '''
    quantile = chi2.ppf(1 - alpha, Chi_quadro_output[1])
    
    return Chi_quadro_output[0] > quantile

    
def Fisher(dati):
    ''' 
    Questa funzione calcola la statistica di Fisher per il test di Anova 
        Parametri: insieme dei dati come CSV
    '''
    M = dati.values  # trasformo i dati raccolti nel file.csv in un np array
    
    n, m = M.shape  # ricavo n = righe (osservazioni), m = colonne (gruppi)

    X_i_bar = mean(M, axis=0)   # medie per colonna (gruppi)
    X_bar = mean(M)             # media totale
    SSb = n * sum((X_i_bar - X_bar) ** 2)
    
    SSw = sum((M - X_i_bar) ** 2)
    
    gl1 = m - 1           # gradi di libertà della statistica
    gl2 = m*n - m
  
    Fisher = (SSb /gl1)/( SSw / gl2)   # calcolo della statistica F

    return Fisher, gl1, gl2

def Anova_test (Fisher_output, alpha):
    '''
    Questa funznione confronta la statistica di Fisher con il quantile relativo alla significatività scelta  
        Parametri: Fisher_output (valore ritornato dalla funzione Fisher), alpha (significatività)
    '''
    quantile = f.ppf(1 - alpha, Fisher_output[1], Fisher_output[2])    
   
    return Fisher_output[0] > quantile 

def valore_statistica(file, metodo):   
    '''
    Questa funzione prende le informazioni necessarie per risolvere il test e calcola il valore della statistica
        Parametri: file csv con i dati, metodo scelto
    '''
    if metodo == 'ANOVA':
        S = Fisher(file)
    else :
        S = Chi_Quadro(file)
    return S
          
def test(valore_statistica, alpha):
    '''
    Questa funzione confronta la statistica calcolata con il quantile associato alla significatività
        Parametri: valore_della_statistica (ritornato dalla funzione informazioni test) e alpha (significatività)
    '''
    if len(valore_statistica) == 2:
        risultato_test = Chi_Quadro_test(valore_statistica, alpha)
    else :
        risultato_test = Anova_test(valore_statistica, alpha)
        
    s = alpha*100  
    messagebox.showinfo("RISULTATO TEST" ,f"Sulla base dei dati forniti, si rifiuta l'ipotesi nulla del test con significatività {s}% ")if risultato_test else messagebox.showinfo("RISULTATO TEST" ,f"Sulla base dei dati forniti, si accetta l'ipotesi nulla del test con significatività {s}%")
    


    
  
    
    
        
    
       