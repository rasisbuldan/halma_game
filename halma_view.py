# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 07:23:50 2020

Congklak Board Game

@author: Mursito
"""

from halma_model import HalmaModel
from halma_player import HalmaPlayer

S_AKSI = ["Geser", "Loncat", "Henti"]

class HalmaView:
    indent = ""
    # mulai main 2 pemain
    def tampilAwal(self, model):
        print("HALMA")
        print("Ukuran   :", model.getUkuran())
        print("Bidak    :", model.getJumlahBidak())
        print("Pemain 1 :", model.getPemain(0).nama)
        print("Pemain 2 :", model.getPemain(1).nama)
        print()
        print("Bidak \tAksi \tDari \tKe \tWaktu")

    def tampilMulai(self, model):
        # nothing 
       self.indent = "" 

    def tampilGeser(self, model, x1, y1, x2, y2):
        print(model.getBidak(x2,y2),'\t', S_AKSI[model.A_GESER],'\t',(x1,y1),'\t',(x2,y2))

    def tampilLoncat(self, model, x1, y1, x3, y3):
        print(self.indent,model.getBidak(x3,y3),'\t', S_AKSI[model.A_LONCAT],'\t',(x1,y1),'\t',(x3,y3))
        if (self.indent == ""):
            self.indent = " "
        print(*model.getPapan(), sep='\n')
        
    def tampilHenti(self, model):
        self.indent = ""
        
    def tampilGanti(self, model):
        self.indent = ""

    def tampilAkhir(self, model, status):
        print("SELESAI")
        p = model.getPemain(model.getGiliran())
        if (status == model.S_OK):
            print("Pemenang : ", p.nama)
        elif (status == model.S_ILLEGAL):
            print(p.nama, "KALAH karena salah jalan")
        elif (status == model.S_TIMEOUT):
            print(p.nama, "KALAH karena kehabisan waktu")
    
