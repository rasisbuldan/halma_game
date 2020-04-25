# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 08:04:48 2020

@author: Mursito
"""

import random
import time
from halma_model import HalmaModel

class HalmaPlayer:
    nama = 'Pemain'
    deskripsi = 'Random Strategy'
    type = 'AI'
    nomor = 1    
    index = 0
    papan = []
    teman = None
    
    def __init__(self, nama):
        self.nama = nama
        
    def setNomor(self, nomor):
        self.nomor = nomor
        self.index = nomor-1
    
    def setTeman(self, p):
        self.teman = p
    
    def getTeman(self):
        return self.teman
    
    def getType(self):
        return self.type

    # mengembalikan semua kemungkikan main (geser / loncat) bidak di (x1, y1)
    def bisaMain(self, model, papan, x1, y1):
        geser = []
        loncat = []
        ip = self.index
        dTujuan = model.dalamTujuan(ip, x1, y1)
        for a in model.ARAH:
            x2 = x1 + a[0]
            y2 = y1 + a[1]
            #print((x2, y2), end="")
            if model.dalamPapan(x2, y2):
                if (papan[x2][y2] == 0):
                    if not dTujuan or model.dalamTujuan(ip, x2, y2):
                        geser.append((x2,y2))
                else:
                    x3 = x2 + a[0]
                    y3 = y2 + a[1]
                    #print((x3, y3), end="")
                    if model.dalamPapan(x3, y3):
                        if (papan[x3][y3] == 0):
                            if not dTujuan or model.dalamTujuan(ip, x3, y3):
                                loncat.append((x3,y3))
        return geser, loncat
       
    # Pemain beraksi
    # return [(x2,y2)], (x1,y1), aksi
    # aksi = A_GESER, A_LONCAT, atau A_BERHENTI
    # (x1, y1) = posisi bidak awal
    # [(x2, y2)] = posisi tujuan (array, isi 1 kalau geser, isi banyak kalau loncat)
    def main(self, model):
        random.seed(time.process_time_ns())
        papan = model.getPapan()
        b0 = model.getPosisiBidak(self.index)
        random.shuffle(b0)

        k = 0
        # Dummy algorithms for delay
        for i in range(10000000):
            k += i

        for b in b0:
            g,l = self.bisaMain(model, papan, b[0], b[1])
            
            # Randomize move
            random.shuffle(g)
            random.shuffle(l)

            if g != [] :
                #print('return g',[g[0]],b,model.A_GESER)
                return [g[0]], b, model.A_GESER
            if l != [] :
                #print('return l',[l[0]],b,model.A_LONCAT)
                return [l[0]], b, model.A_LONCAT
        return None, None, model.A_BERHENTI