# -*- coding: UTF-8 -*-

from json import loads, dumps

import numpy as np
# import pandas as pd
# import itertools as itt
# from scipy import stats
# import matplotlib.pyplot as plt
# import matplotlib.ticker as ticker
# from collections import Counter


class Projekty():
    
    def __init__(self, runda=1, krok=1):
        self.runda = runda
        self.krok = krok
        self.r1 = np.random.RandomState(self.runda)
        self.r2 = np.random.RandomState(self.krok)
        
        self.projekty = 9
        self.a_min, self.a_max = 5, 20        # a_max<k_min<k_max<s_min
        self.k_min, self.k_max = 20, 31       # koszty
        self.s_min, self.s_max = 31, 40       # sprzedaż
        self.alfa, self.beta = 5, 5
        
        self.a = self.r1.randint(self.a_min, self.a_max, self.projekty)
        self.koszty = self.r1.randint(self.k_min, self.k_max, self.projekty)
        self.sprz = self.r1.randint(self.s_min, self.s_max, self.projekty)
        self.b = 2*self.sprz-self.a
        
        self.zyski = self.sprz-self.koszty
        self.zwrot = np.round((self.zyski/self.koszty), 2)
        
        self.ryzyko = np.round((self.koszty-self.a)/(self.sprz-self.a+2), 2)
        
        self.columns = ['koszt', 'zysk', 'zwrot', 'ryzyko']
        self.index = ['P'+str(p+1) for p in range(self.projekty)]
        self.data = zip(self.koszty, self.zyski, self.zwrot, self.ryzyko)
        self.dane = pd.DataFrame(self.data, columns=self.columns, index = self.index)
        
        self.c = self.r2.beta(self.alfa, self.beta, self.projekty)
        self.sprz_rz = np.round((self.c*(self.b-self.a)+self.a),0).astype(int)
        self.zysk_rz = (self.sprz_rz - self.koszty)
        self.wyniki = self.dane.assign(wynik = self.zysk_rz)

    def rozk_beta(self): #rozkład zysków
        rozrzut = np.arange(self.a_min-self.k_max, self.a_max+self.k_max, 1)
        y_ZT = []
        for i in range(self.projekty):
            a = self.a[i]-self.koszty[i]
            b = self.b[i]-self.koszty[i]
            y_te = stats.beta.pdf(rozrzut, self.alfa, self.beta, loc=a, scale=b-a)
            y_te = np.round(y_te, 4)
            y_ZT.append(y_te)
        df = pd.DataFrame(y_ZT)
        df = df.transpose()
        df.columns = [Projekty().index]
        df.insert(loc=0, column='zysk', value=rozrzut)
        return df
    
    def ryzyko1(self):
        d = np.round((self.sprz*0.9),0).astype(int)
        g = np.round((self.sprz*1.1),0).astype(int)
        RYZYKO = []
        for i in range(self.projekty):
            yd = stats.beta.cdf(d[i], self.alfa, self.beta, 
                                loc=self.a[i], scale=self.b[i]-self.a[i])
            yg = stats.beta.cdf(g[i], self.alfa, self.beta, 
                                loc=self.a[i], scale=self.b[i]-self.a[i])
            ryzyko = np.round(yg-yd, 2)
            RYZYKO.append(ryzyko)
        index = self.index
        columns = ['a', 'd', 's', 'g', 'b', 'ryzyko']
        dane1 = zip(self.a, d, self.sprz, g, self.b, RYZYKO)
        df = pd.DataFrame(dane1, columns=columns, index=index)
        return df

    def zysk1(self): #średni zysk z projektów w danej rundzie
        SZ = []
        for k in range(self.projekty):
            Z = []
            for i in range(100):
                a = Projekty(self.runda,i).zysk_rz[k]
                Z.append(a)
            sz = np.mean(Z)
            SZ.append(sz)
            K=[]
        df = self.wyniki
        df = df.assign(sr_zysk = np.array(SZ))
        return df


class Baza(object):

    projekty = 9
    a_min = 5
    a_max = 20
    k_min = 20 # koszty
    k_max = 31
    s_min = 31 # sprzedaż
    s_max = 40
    # a_max<k_min<k_max<s_min
    alfa = 5
    beta = 5

    k = 3 # liczba elemntów najmniejszego podzbioru(>0)
    m = 3 # liczba elemntów największego podzbioru ( =< liczba projektów)

    def __init__(self):
        super(Baza, self).__init__()


class Runda(Baza):

    def __init__(self, seed):
        super(Runda, self).__init__()
        self.runda = seed
        self.r1 = np.random.RandomState(self.runda)
        self.obliczenia()
        return

    def obliczenia(self):
        # generowanie danych
        self.a = self.r1.randint(self.a_min, self.a_max, self.projekty)
        self.koszty = self.r1.randint(self.k_min, self.k_max, self.projekty)
        self.sprz = self.r1.randint(self.s_min, self.s_max, self.projekty)
        self.b = 2*self.sprz-self.a
        
        # obliczenia podstawowe
        self.zyski = self.sprz-self.koszty
        self.zwrot = np.round((self.zyski/self.koszty), 2)
        self.ryzyko = np.round((self.koszty-self.a)/(self.sprz-self.a+2), 2)

        # # do tworzenia tabeli
        # self.columns = ['koszt', 'zysk', 'zwrot', 'ryzyko']
        # self.index = ['P'+str(p+1) for p in range(self.projekty)]
        # self.data = zip(self.koszty, self.zyski, self.zwrot, self.ryzyko)
        # self.dane = pd.DataFrame(self.data, columns=self.columns, index = self.index)
        return

    def spakuj_dane(self):
        wynik = {}
        # dane podstawowe
        wynik['projekty'] = self.projekty
        wynik['runda'] = self.runda
        # dane wygenerowane
        wynik['a'] = list(map(int, list(self.a)))
        wynik['koszty'] = list(map(int, list(self.koszty)))
        wynik['sprz'] = list(map(int, list(self.sprz)))
        wynik['b'] = list(map(int, list(self.b)))
        wynik['zyski'] = list(map(int, list(self.zyski)))
        wynik['zwrot'] = list(map(float, list(self.zwrot)))
        wynik['ryzyko'] = list(map(float, list(self.ryzyko)))

        wynik['k'] = self.k
        wynik['m'] = self.m
        return wynik

    def rozpakuj_dane(self, dane):
        if type(dane) is str:
            # jeśli zamiast słownika danych otrzymamy tekst
            dane = loads(dane)

        self.projekty = dane['projekty']
        self.runda = dane['runda']
        self.a = np.array(dane['a'])
        self.koszty = np.array(dane['koszty'])
        self.sprz = np.array(dane['sprz'])
        self.b = np.array(dane['b'])
        self.zyski = np.array(dane['zyski'])
        self.zwrot = np.array(dane['zwrot'])
        self.ryzyko = np.array(dane['ryzyko'])
        return


class Portfele(Projekty):
    
    def __init__(self, runda, krok):
        super().__init__(runda, krok)
    
    def liczba(self):
        # generowanie porfeli projektów (k =< m)
        k = 3  # liczba elemntów najmniejszego podzbioru(>0)
        m = 3 #self.projekty # liczba elemntów największego podzbioru ( =< liczba projektów)
        portfele = []
        if k == m:
            for i in itt.combinations(self.index, k):
                portfele.append(i)
        else:
            for k in range(k, m+1):
                for i in itt.combinations(self.index, k):
                    portfele.append(i)
        return portfele
    
    def tabela(self):
        portfele = Portfele(self.runda, self.krok).liczba()
        ID = [] # indeksy portflei
        PO = [] # zestawienie projektów w portfelach
        KO = [] # zagregowane koszty porojektów w portfelach
        ZY = [] # zagregowane zyski projektów w portfelach
        RY = [] # zagregowane ryzyko projektów w portfelach
        WY = [] # zagregowane wyniki rzeczywste portfeli
        for h in range(len(portfele)):
            danepor = self.wyniki.loc[list(portfele[h])]
            KOszpor = danepor.loc[:, 'koszt'].sum() 
            ZYskpor = danepor.loc[:, 'zysk'].sum()
            a = danepor.loc[:, 'koszt']
            b = danepor.loc[:, 'ryzyko']
            RYzypor = np.round(np.average(b, weights=a),2)
            WYnipor = danepor.loc[:, 'wynik'].sum()
            ID.append(h)
            PO.append('-'.join(portfele[h]))
            KO.append(KOszpor)
            ZY.append(ZYskpor)
            RY.append(RYzypor)
            WY.append(WYnipor)
        opisy = ['ID','portfele', 'koszt', 'zysk', 'ryzyko', 'wynik']
        dane = list(zip(ID, PO, KO, ZY, RY, WY))
        df1 = pd.DataFrame(dane, columns = opisy)
        df1['rank_zysk'] = df1['zysk'].rank(method='max', ascending=False).astype(int)
        df1['rank_ryzyko'] = df1['ryzyko'].rank(method='max', ascending=False).astype(int)
        df1['rank_wynik'] = df1['wynik'].rank(method='max', ascending=False).astype(int)
        df1 = df1[['ID','portfele', 'koszt', 'zysk', 'ryzyko', 'wynik', 'rank_zysk', 'rank_ryzyko', 'rank_wynik']]
        return df1


class Wykresy(Projekty):
    
    def __init__(self, runda, krok):
        super().__init__(runda, krok)
        self.gran_ryzy = Projekty(self.runda, self.krok).ryzyko1()
    
    def rys1(self, projekt=1):
        i = projekt-1
        fig, ax = plt.subplots()
        x = np.arange(0, 2*self.s_max-self.a_min, 1)
        yt = stats.beta.pdf(x, self.alfa, self.beta, 
                            loc=self.a[i], scale=self.b[i]-self.a[i])
        plt.plot(x, yt,'k')
        plt.fill_between(x, yt, color = 'r', where = (x <= self.koszty[i]), alpha=0.9)
        plt.fill_between(x, yt, color = 'r',  where = (x >= self.koszty[i]), alpha=0.5)
        plt.fill_between(x, yt, color = 'w',
                         where = (x >= self.gran_ryzy['d'][i])
                         & (x <= self.gran_ryzy['g'][i]), alpha=0.5)

        yt_max = stats.beta.pdf(self.s_min, self.alfa, self.beta, 
                                loc=self.a_max, scale=2*(self.s_min-self.a_max))

        p_s = 'p(s<k)='+ str(np.round((stats.beta.cdf(
            self.koszty[i], self.alfa, self.beta, 
            loc=self.a[i], scale=self.b[i]-self.a[i])), 3))
        ax.annotate(p_s,xy=(self.a[i]+(self.koszty[i]-self.a[i])*0.8,0.005), 
                    xycoords='data', xytext=(0.05,0.2), textcoords='axes fraction',
                    arrowprops=dict(arrowstyle= '->', lw=0.7), va='center')      
        
        gr = 'p(|z|)='+str(self.gran_ryzy['ryzyko'][i])
        ax.annotate(gr ,xy=(self.sprz[i]+2, 0.01), 
            xycoords='data', xytext=(0.8,0.3), textcoords='axes fraction',
            arrowprops=dict(arrowstyle= '->', lw=0.7), va='center') 
        
        kk = 'k= '+str(self.koszty[i])
        ss = 's= '+str(self.sprz[i])
        zz = 'z=s-k='+str(self.sprz[i]-self.koszty[i])
        
        box = dict(fc='#fff9d0', lw=0)
        ax.text(self.koszty[i], 0.115, kk, ha='right', bbox=box)
        ax.text(self.sprz[i], 0.115, ss, ha='left', bbox= box)
        ax.text(self.sprz[i]+3, 0.1, zz, va='center', ha='left', bbox= box)
        ax.text(60, 0.115, 'Projekt '+str(i+1), weight='bold')

        ax.vlines(self.koszty[i], 0, 0.11, lw =0.7, color='k', fc ='k', ls= '--')
        ax.vlines(self.sprz[i], 0, 0.11, lw =0.7, color='k', fc ='k', ls= '--')
        ax.hlines(0.1, self.koszty[i], self.sprz[i]+5, color='k', fc ='k', lw =0.76)
        ax.scatter([self.koszty[i], self.sprz[i]], [0.1, 0.1], marker='.')

        ax.grid('on', linestyle='--', lw=.3, c='grey')
        ax.set_facecolor('#fff9d0')
        fig.patch.set_facecolor('#fff9d0')

        ax.set_ylim(0, yt_max*1.1)
        ax.set_yticks(np.arange(0, yt_max, 0.01))
        ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.01))   

        ax.set_xlim(0, 2*self.s_max-self.a_min)
        ax.set_xticks(np.arange(0, 2*self.s_max-self.a_min+5, 5))
        ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
        
        fig.text(0.5, 0.05, 'przewidywana sprzedaż', ha='center', va='center', fontsize=11)
        fig.text(0.03, 0.5, 'prawdopodobieństwo', ha='center', va='center', rotation='vertical', fontsize=11)
        fig. tight_layout(pad=3, w_pad=1, h_pad=1)
        return fig


        
    def rys2(self):
        gr_kw = {'left':0.08, 'right': 0.95,'bottom':0.08,
                 'top': 0.93, 'wspace':0, 'hspace':0}
        fig, ax = plt.subplots(nrows=3, ncols=3, sharex=True, sharey=True,
                      gridspec_kw = gr_kw, figsize=(11, 7))
        
        for i, ax in enumerate(ax.flatten()):
            x = np.arange(0, 2*self.s_max-self.a_min, 1)
            yt = stats.beta.pdf(x, self.alfa, self.beta, 
                                loc=self.a[i], scale=self.b[i]-self.a[i])
            ax.plot(x, yt,'k')
            ax.fill_between(x, yt, color = 'r', where = (x <= self.koszty[i]), alpha=0.5)
            ax.fill_between(x, yt, color = 'g',  where = (x >= self.koszty[i]), alpha=0.5)
            ax.fill_between(x, yt, color = 'w',
                 where = (x >= self.gran_ryzy['d'][i])
                 & (x <= self.gran_ryzy['g'][i]), alpha=0.5)

            yt_max = stats.beta.pdf(self.s_min, self.alfa, self.beta, 
                                    loc=self.a_max, scale=2*(self.s_min-self.a_max))

            p_s = 'p='+ str(np.round((stats.beta.cdf(
                self.koszty[i], self.alfa, self.beta, 
                loc=self.a[i], scale=self.b[i]-self.a[i])), 3))

            ax.annotate(p_s,xy=(self.a[i]+(self.koszty[i]-self.a[i])*0.8,0.005), 
                        xycoords='data', xytext=(0.05,0.2), textcoords='axes fraction',
                        arrowprops=dict(arrowstyle= '->', lw=0.7), va='center')
            
            gr = 'p(|z|)='+str(self.gran_ryzy['ryzyko'][i])
            ax.annotate(gr ,xy=(self.sprz[i]+2, 0.01), xycoords='data', 
                        xytext=(0.7,0.4), textcoords='axes fraction',
                        arrowprops=dict(arrowstyle= '->', lw=0.7), va='center') 

            kk = 'k= '+str(self.koszty[i])
            ss = 's= '+str(self.sprz[i])
            zz = 'z='+str(self.sprz[i]-self.koszty[i])
            rr = 'r='+str(self.ryzyko[i])

            box = dict(fc='#fff9d0', lw=0)
            ax.text(self.koszty[i], 0.112, kk, ha='right')
            ax.text(self.sprz[i], 0.112, ss, ha='left')
            ax.text(self.sprz[i]+3, 0.1, zz, va='center', ha='left', bbox= box)
            ax.text(62, 0.1, rr, weight='bold')
            ax.text(62, 0.11, 'P'+str(i+1), weight='bold')

            ax.vlines(self.koszty[i], 0, 0.11, lw =0.7, color='k', fc ='k', ls= '--')
            ax.vlines(self.sprz[i], 0, 0.11, lw =0.7, color='k', fc ='k', ls= '--')
            ax.hlines(0.1, self.koszty[i], self.sprz[i]+5, color='k', fc ='k', lw =0.76)
            ax.scatter([self.koszty[i], self.sprz[i]], [0.1, 0.1], marker='.')

            ax.grid('on', linestyle='--', lw=.3, c='grey')
            ax.set_facecolor('#fff9d0')
            fig.patch.set_facecolor('#fff9d0')

            ax.set_ylim(0, yt_max*1.1)
            ax.set_yticks(np.arange(0, yt_max, 0.02))
            ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.01))   

            ax.set_xlim(0, 2*self.s_max-self.a_min)
            ax.set_xticks(np.arange(0, 2*self.s_max-self.a_min+5, 10))
            ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))

        fig.text(0.5, 0.01, 'przewidywana sprzedaż', ha='center', va='center', fontsize=11)
        fig.text(0.01, 0.5, 'prawdopodobieństwo', ha='center', va='center', rotation='vertical', fontsize=11)
        fig.patch.set_facecolor('#fff9d0')
        return fig
    
    def rys3(self):
        fig, ax = plt.subplots(figsize=(7, 6))
        plt.rc('grid', linestyle="--", lw=0.3, color='black')
        x = Portfele(self.runda, self.krok).tabela().loc[:,'ryzyko']
        y = Portfele(self.runda, self.krok).tabela().loc[:,'wynik']
        ax.grid('on', linestyle='--', lw=.3, c='grey')
        ax.scatter(x, y,  edgecolor='k', facecolors = 'y', alpha=0.7, s = 50, lw =1)
        ax.set_ylim(0, 100)
        ax.set_yticks(np.arange(0, 100, 10))
        ax.yaxis.set_minor_locator(ticker.MultipleLocator(1))
        ax.set_facecolor('whitesmoke')
        ax.set_xlim(0, 1)
        ax.set_xticks(np.arange(0, 1.1, 0.1))
        ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.01))
        
        fig.text(0.5, 0.05, 'zysk z portfela', ha='center', va='center', fontsize=11)
        fig.text(0.05, 0.5, 'ryzyko portfela', ha='center', va='center', rotation='vertical', fontsize=11)
        fig.patch.set_facecolor('#fff9d0')
        fig. tight_layout(pad=3, w_pad=1, h_pad=1)
        return fig
    

