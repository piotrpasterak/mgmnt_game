import numpy as np
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


import portfolio as po



root = tk.Tk()   
root.title("Analiza porfela projektów")  


root.counter = 0
krok = 1

COUNT = [0]

def runda_click():
    root.counter += 1
    rundaBut['text'] = 'Runda ' + str(root.counter)
    tabela = po.Projekty(root.counter, krok).wyniki.iloc[:,:-1]

    COUNT.append(root.counter) 
    for i in range(len(tabela)):
        for j in range(len(tabela.columns)):
            # dane w tabeli
            label = tk.Label(projektyRamka, text=tabela.iloc[i,j], borderwidth=5, width=5)
            label.grid(row=i+2, column=j+1, sticky='w', padx=1, pady=1)
    for i in range(9):
        label = tk.Label(projektyRamka, text= ' --- ', borderwidth=5, width=5)
        label.grid(row=i+2, column=7, sticky='w', padx=4, pady=1)
    wynikiBut['state'] = 'disabled'
    zatwierBut['state'] = 'disabled'
    for cbtn in vars:
        cbtn[0].config(state="normal")
        cbtn[1].set(0)

    label = tk.Label(wybraneProjektyRamka, text = '       Koszt =')
    label.grid(row=0, column=1, sticky='e', padx=1, pady=1)
    
    label = tk.Label(wybraneProjektyRamka, text = '       Zysk =')
    label.grid(row=1, column=1, sticky='e', padx=1, pady=1)
    
    label = tk.Label(wybraneProjektyRamka, text = '        Zwrot =')
    label.grid(row=2, column=1, sticky='e', padx=1, pady=1)
    
    label = tk.Label(wybraneProjektyRamka, text = '        Ryzyko =')
    label.grid(row=3, column=1, sticky='e', padx=1, pady=1)    
    for j in range(3):
        label = tk.Label(wybraneProjektyRamka, text = '                ')
        label.grid(row=j, column=0, sticky='w', padx=1, pady=1)    
    
    label = tk.Label(wynikiPor, text = 'Koszt =       ')
    label.grid(row=0, column=0, sticky='w', padx=1, pady=1)

    label = tk.Label(wynikiPor, text = 'Zysk =       ')
    label.grid(row=1, column=0, sticky='w', padx=1, pady=1)

    label = tk.Label(wynikiPor, text = 'Zwrot =       ')
    label.grid(row=2, column=0, sticky='w', padx=1, pady=1)

    label = tk.Label(wynikiPor, text = 'Ryzyko =       ')
    label.grid(row=3, column=0, sticky='w', padx=1, pady=1)
    
    
def oknoProjektu(idx):
    newTop = tk.Toplevel()
    tek = '''s-sprzedaż, k-koszty, z-zysk, p(s<z)-prawdopodobieństwo strat
    p(|z|)-prawdopodobieństwo osiągnięcia zysków w przedziale +/- 10% '''
    display = tk.Label(newTop, text=tek, bg = '#fff9d0', anchor='w', font="Arial 8 italic").pack(fill=tk.X, side=tk.BOTTOM)  
    canvas = FigureCanvasTkAgg(po.Wykresy(root.counter, krok).rys1(idx+1), master=newTop)
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)    

def mapaPortfeli():
    newTop = tk.Toplevel()
    fig, ax = plt.subplots(figsize=(7, 6))
    plt.rc('grid', linestyle="--", lw=0.3, color='black')
    x = po.Portfele(root.counter, krok).tabela().loc[:,'ryzyko']
    y = po.Portfele(root.counter, krok).tabela().loc[:,'zysk']
    ax.grid('on', linestyle='--', lw=.3, c='grey')
    ax.scatter(x, y,  edgecolor='k', facecolors = 'y', alpha=0.7, s = 50, lw =1)
    ax.set_ylim(0, 100)
    ax.set_yticks(np.arange(0, 100, 10))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(1))
    ax.set_facecolor('whitesmoke')
    ax.set_xlim(0, 1)
    ax.set_xticks(np.arange(0, 1.1, 0.1))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.01))
    
    b = idPortfela[-1]
    portfel = '-'.join(['P'+str(e+1) for e in b]).rstrip()
    df = po.Portfele(root.counter, krok).tabela()

    wybrPortfelDane = df.loc[df['portfele'] == portfel]
    x1 = wybrPortfelDane['ryzyko']
    y1 = wybrPortfelDane['zysk']
    ax.scatter(x1, y1, edgecolor='k', facecolors = 'steelblue', alpha=0.7, s = 100, lw =1)

    plt.annotate('Twój portfel\n  '+portfel, xy=(x1, y1), xytext=(50, 50),
            textcoords='offset points', ha='left', va='top',
            bbox=dict(boxstyle='round,pad=0.5', fc='steelblue', alpha=0.3, lw =0.9),
            arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0.2', lw =0.9))
    
    

    fig.text(0.5, 0.05, 'ryzyko portfela', ha='center', va='center', fontsize=11)
    fig.text(0.05, 0.5, 'zysk z portfela', ha='center', va='center', rotation='vertical', fontsize=11)
    fig.patch.set_facecolor('#fff9d0')
    fig. tight_layout(pad=3, w_pad=1, h_pad=1)
    canvas = FigureCanvasTkAgg(fig, master=newTop)
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)  
    
def zatwier_click():
    wynikiBut['state'] = 'normal'
    for cbtn in vars:
        cbtn[0].config(state="disabled")


        
def wyniki_click():

    tabela1 = po.Projekty(root.counter, krok).wyniki
    for i in range(9):
        zysk_rz = tabela1.iloc[i,4]
        label = tk.Label(projektyRamka, text= zysk_rz, borderwidth=5, width=5)
        label.grid(row=i+2, column=7, sticky='w', padx=1, pady=1)
    
    counter = 0
    id = [] #indeksy wbranych projektów
    for i, cbtn in enumerate(vars):
        if cbtn[1].get() == 1:
            counter += 1
            id.append(i)
    

    if tabela1.iloc[id,1].sum()>0:
        koszt = tabela1.iloc[id,0].sum()
        zysk = tabela1.iloc[id,4].sum()
        zwrot = np.round(tabela1.iloc[id,4].sum()/tabela1.iloc[id,0].sum(), 2)
        a = tabela1.iloc[id,0]
        b = tabela1.iloc[id,3]
        ryzyko = np.round(np.average(b, weights=a),2)
    else:
        koszt = '###'
        zysk  = '###'
        zwrot = '###'
        ryzyko = '###'


    label = tk.Label(wynikiPor, text = 'Koszt = '+str(koszt)+ '      ')
    label.grid(row=0, column=0, sticky='w', padx=1, pady=1)

    label = tk.Label(wynikiPor, text = 'Zysk = '+str(zysk)+ '      ')
    label.grid(row=1, column=0, sticky='w', padx=1, pady=1)

    label = tk.Label(wynikiPor, text = 'Zwrot = '+str(zwrot)+ '      ')
    label.grid(row=2, column=0, sticky='w', padx=1, pady=1)

    label = tk.Label(wynikiPor, text = 'Ryzyko = '+str(ryzyko)+ '      ')
    label.grid(row=3, column=0, sticky='w', padx=1, pady=1)

idPortfela =[]

def wybrane_proj():
    counter = 0
    id = [] #indeksy wbranych projektów
    for i, cbtn in enumerate(vars):
        if cbtn[1].get() == 1:
            counter += 1
            id.append(i)
    if counter == 3:
        for cbtn in vars:
            if cbtn[1].get() != 1:
                cbtn[0].config(state="disabled")
        zatwierBut['state'] = 'normal'
        mapaBut['state'] = 'normal'
    else:
        for cbtn in vars:
            cbtn[0].config(state="normal")
        zatwierBut['state'] = 'disabled'
        mapaBut['state'] = 'disabled'
    for j, i in enumerate(np.array(id)):
        label = tk.Label(wybraneProjektyRamka, text = 'Projekt ' +str(i+1))
        label.grid(row=j, column=0, sticky='e', padx=1, pady=1)
    idPortfela.append(id)
    
    tabela = po.Projekty(root.counter, krok).wyniki.iloc[:,:-1]

    if tabela.iloc[id,1].sum()>0:
        koszt = tabela.iloc[id,0].sum()
        zysk = tabela.iloc[id,1].sum()
        zwrot = np.round(tabela.iloc[id,1].sum()/tabela.iloc[id,0].sum(), 2)
        a = tabela.iloc[id,0]
        b = tabela.iloc[id,3]
        ryzyko = np.round(np.average(b, weights=a),2)
    else:
        koszt = '###'
        zysk  = '###'
        zwrot = '###'
        ryzyko = '###'
    
    label = tk.Label(wybraneProjektyRamka, text = '     Koszt = '+str(koszt))
    label.grid(row=0, column=1, sticky='e', padx=1, pady=1)
    
    label = tk.Label(wybraneProjektyRamka, text = '     Zysk = '+str(zysk))
    label.grid(row=1, column=1, sticky='e', padx=1, pady=1)
    
    label = tk.Label(wybraneProjektyRamka, text = '        Zwrot = '+str(zwrot))
    label.grid(row=2, column=1, sticky='e', padx=1, pady=1)
    
    label = tk.Label(wybraneProjektyRamka, text = '       Ryzyko = '+str(ryzyko))
    label.grid(row=3, column=1, sticky='e', padx=1, pady=1)
    

tabControl = ttk.Notebook(root)
tab1 = ttk.Frame(tabControl)
tabControl.add(tab1, text='   Info   ')
tab0 = ttk.Frame(tabControl)
tabControl.add(tab0, text='    Gra   ')
tab2 = ttk.Frame(tabControl)
tabControl.add(tab2, text='    Dane    ')
tab3 = ttk.Frame(tabControl)
tabControl.add(tab3, text='  Wyślij  ')
tabControl.pack(expand=True, fill=tk.BOTH)

#----------Zakładka Info-------------------------------------

cel_gry = '''\n
   Celem  gry jest maksymalizacja  zwrotu z portfela projektów.
Zwrot jest rozumiany jako stosunek zysków do kosztów.
\n\n
   Gra skałda się z rund. W każdej rundzie generowane są losowo 
dane na temat dziewięciu projektów. Zadaniem gracza jest  wybór 
trzech  spośród  dziewęciu  podanych projektów,  które łącznnie 
tworzą portfel. 
\n\n   
   Po zatwierdzeniu portfela generowane są loswo rzeczysiste 
zyski  projektów.  Losowanie  odbywa się zgodnie z  podanymi 
na wykresach rozkładami prawdopodobieństwa ralizacji przychodów 
dla poszczególnych projektów.
\n\n   
   Podgląd  wykresów  jest możliwy  po kliknięciu odpowiedniego 
projektu. Przed  zatwierdzeniem  portfela można zobaczyć wykres 
funkcji zysków wszystkich portfeli względem ryzyka (mapa).
\n\n\n\n\n\n\n\n'''

Info = ttk.Label(tab1, text=cel_gry)
Info.grid(padx=10, pady=15)

#----------Zakładka Gra----------------------------------------

projektyRamka = ttk.LabelFrame(tab0, text='Projekty')
projektyRamka.grid(column=0, row=0, columnspan=4, padx=10, pady=5)
rundaBut = tk.Button(projektyRamka, text='Rozpocznij grę', borderwidth=1, width=20, command=runda_click)
rundaBut.grid(column=1, row=0, columnspan=4, sticky='we', padx=1, pady=1)
label = tk.Label(projektyRamka, text='Wynik', borderwidth=5, width=5)
label.grid(row=1, column=7, sticky='w', padx=4, pady=1)


twojPorfelRamka = ttk.LabelFrame(tab0, text='Twój bieżący portfel:')
twojPorfelRamka.grid(row=1, column=0, columnspan=2, sticky='nw', padx=10, pady=5)
wybraneProjektyRamka = tk.Label(twojPorfelRamka)
wybraneProjektyRamka.grid(row=0, column=0, rowspan=4, columnspan=2, sticky="n", padx=1, pady=1)
mapaBut = tk.Button(twojPorfelRamka, text='Mapa', state='disabled', borderwidth=0.5, width=8, 
                       command=mapaPortfeli)
mapaBut.grid(row=3, column=0, sticky="sw", padx=1, pady=1)

zatwierBut = tk.Button(tab0, text='Zatwierdź portfel !', state='disabled', borderwidth=0.5, width=20,
                       command=zatwier_click)
zatwierBut.grid(row=2, column=0, columnspan=2, sticky="we", padx=10, pady=1)


wynikiRamka = ttk.LabelFrame(tab0, text='Realizacja zysków portfela:')
wynikiRamka.grid(row=1, column=2, columnspan=2, sticky='ne', padx=10, pady=5)
wynikiPor = tk.Label(wynikiRamka)
wynikiPor.grid(row=0, column=0, rowspan=4, sticky="n", padx=1, pady=1)

wynikiBut = tk.Button(tab0, text='Generuj zyski !', state='disabled', borderwidth=0.5, width=20, 
                      command=wyniki_click)
wynikiBut.grid(row=2, column=3, columnspan=2, sticky="we", padx=10, pady=1)

#----------Zakładka Dane----------------------------------------

daneinfo = '''
Tutaj znajdą się dane dotyczące wyników z kolejnych
rund gracza
'''

zakladka_Dane = ttk.Label(tab2, text=daneinfo)
zakladka_Dane.grid(padx=20, pady=15)


#----------Zakładka Wyślij----------------------------------------

wyślijinfo = '''
Tutaj znajdzie się metryczka określjąca wiek, płeć
i doświadczenie zawodowe gracza, a także email
'''

zakladka_Dane = ttk.Label(tab3, text=wyślijinfo)
zakladka_Dane.grid(padx=20, pady=30)




vars = []

for i in range(9):
    var = tk.IntVar()
    cbtn = tk.Checkbutton(projektyRamka, text='P'+str(i+1), state='disabled', 
                          command=wybrane_proj, variable = var)
    vars.append([cbtn, var])
    vars[i][0].grid(row=i+2, column=5, sticky="w", padx=1, pady=1)
    vars[i][0].bind("<Configure>")
    
    button = tk.Button(projektyRamka, text='Projekt '+str(i+1), borderwidth=0.5, width=8,
                      command = lambda idx = i: oknoProjektu(idx))
    button.grid(row=i+2, column=0, sticky='w', padx=1, pady=1)

    for j in range(4):  
        opisy = ['Koszt', 'Zysk', 'Zwrot', 'Ryzyko']
        label = tk.Label(projektyRamka, text=opisy[j], width=5)
        label.grid(row=1, column=j+1, sticky='w', padx=1, pady=1)

        # dane w tabeli wyjściowej (runda 1)

        label = tk.Label(projektyRamka, text= ' --- ',  width=5)
        label.grid(row=i+2, column=j+1, sticky='w', padx=1, pady=1)




#-------------------------------------------------------------- 
root.update() 
root.deiconify() 
root.mainloop() 
