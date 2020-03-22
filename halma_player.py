# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 08:04:48 2020

@author: Mursito
"""

import random
import time
from halma_model import HalmaModel

class HalmaPlayer:
    nama = "Pemain"
    deskripsi = "Random Strategy"
    nomor = 1    
    index = 0
    papan = []
    
    def __init__(self, nama):
        self.nama = nama
        
    def setNomor(self, nomor):
        self.nomor = nomor
        self.index = nomor-1

    # mengembalikan semua kemungkikan main (geser / loncat) bidak di (x1, y1)
    def bisaMain(self, model, papan, x1, y1):
        geser = []
        loncat = []
        ip = self.index;
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
        time_mulai = time.process_time()
        a = 0

        # Dummy algorithm to simulate time
        for i in range(0,1000000):
            a += i
        
        papan = model.getPapan()        
        b0 = model.getPosisiBidak(self.index)
        # Randomize choice
        seed1 = random.sample(range(10,1000), 20)
        random.seed(random.choice(seed1))
        l = []
        g = []
        while l == [] or g == []:
            b = random.choice(b0)
            g,l = self.bisaMain(model, papan, b[0], b[1])
        
        if l != [] :
            print('algorithm time: ', time.process_time()-time_mulai)
            return [l[0]], b, model.A_LONCAT

        if g != [] :
            print('algorithm time: ', time.process_time()-time_mulai)
            return g, b, model.A_GESER
        
        print('algorithm time: ', time.process_time()-time_mulai)
        print('HENTI')
        return None, None, model.A_BERHENTI
    
            
        

