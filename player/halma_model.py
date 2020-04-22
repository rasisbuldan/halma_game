# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 07:23:50 2020

Congklak Board Game

@author: Mursito

Layout index:
-------
| 0 1 |
| 3 2 |
-------
"""

import time

# Global variable
N_KOTAK = 10
N_BIDAK_2 = 15
N_BIDAK_4 = 10

# Initial position (4P - 10 pieces)
ASAL_10_10_0=[(0,0),(0,1),(1,0),(0,2),(1,1),(2,0),(0,3),(1,2),(2,1),(3,0)]
ASAL_10_10_1=[(0,9),(0,8),(1,9),(0,7),(1,8),(2,9),(0,6),(1,7),(2,8),(3,9)]
ASAL_10_10_2=[(9,9),(9,8),(8,9),(9,7),(8,8),(7,9),(9,6),(8,7),(7,8),(6,9)]
ASAL_10_10_3=[(9,0),(9,1),(8,0),(9,2),(8,1),(7,0),(9,3),(8,2),(7,1),(6,0)]

# Initial position (2P - 15 pieces)
ASAL_10_15_0=[(0,0),(0,1),(1,0),(0,2),(1,1),(2,0),(0,3),(1,2),(2,1),(3,0),(0,4),(1,3),(2,2),(3,1),(4,0)]
ASAL_10_15_1=[(9,9),(9,8),(8,9),(9,7),(8,8),(7,9),(9,6),(8,7),(7,8),(6,9),(9,5),(8,6),(7,7),(6,8),(5,9)]

class HalmaModel:
    # Action
    A_GESER = 0
    A_LONCAT = 1
    A_BERHENTI = 2

    # Game action status
    S_OK = 0
    S_ILLEGAL = 1
    S_TIMEOUT = 2

    ARAH = [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]

    JATAH_WAKTU = 5.0

    # Private variable
    __papan = []   
    __nkotak = 0
    __npemain = 0
    __pemain= []
    __giliran = 1
    __asal = []
    __tujuan = []
    __waktu = []
    __mulai = 0
    __menang = -1
    __teman = [2,3,0,1]

    # mulai main 2 pemain
    def awal(self, p1, p2, p3=None, p4=None):
        # 2-Player
        if (p3 == None) and (p4 == None):
            self.__npemain = 2
            self.__pemain = [p1, p2]
            self.__nbidak = N_BIDAK_2
            self.__asal = [ASAL_10_15_0, ASAL_10_15_1]
            self.__tujuan = [ASAL_10_15_1, ASAL_10_15_0]
        
        # 4-Player
        else:
            self.__npemain = 4
            self.__pemain = [p1, p2, p3, p4]
            self.__nbidak = N_BIDAK_4
            self.__asal = [ASAL_10_10_0, ASAL_10_10_1, ASAL_10_10_2, ASAL_10_10_3]
            self.__tujuan = [ASAL_10_10_2, ASAL_10_10_3, ASAL_10_10_0, ASAL_10_10_1]

        self.__nkotak = N_KOTAK
        self.__giliran = 0
        self.__papan = [[0]*self.__nkotak for i in range(self.__nkotak)]
        for i in range(self.__npemain):
            self.__pemain[i].setNomor(i+1)
            bp = (i + 1) * 100
            for j in range(self.__nbidak):
                x = self.__asal[i][j][0]
                y = self.__asal[i][j][1]
                self.__papan[x][y] = bp + (j + 1)
        self.__waktu = [0,0,0,0]


    # mengembalikan ukuran (N_KOTAK)
    def getUkuran(self):
        return self.__nkotak
    
    # mengembalikan jumlah pemain
    def getJumlahPemain(self):
        return self.__npemain

    # mengembalikan pemain
    def getPemain(self, ip):
        return self.__pemain[ip]

    # mengembalikan giliran
    def getGiliran(self):
        return self.__giliran

    # mengembalikan bidak di posisi x,y
    def getJumlahBidak(self):
        return self.__nbidak        

    # mengembalikan bidak di posisi x,y
    def getBidak(self, x, y):
        return self.__papan[x][y]        

    # mengembalikan semua bidak pemain tertentu
    # ini lama, jadi sebaiknya jangan dipanggil sering-sering
    def getPosisiBidak(self, p):
        bidak=[]
        bp = p+1
        for x in range(self.__nkotak):
            for y in range(self.__nkotak):
                bxy = self.__papan[x][y] // 100
                if (bxy == bp):
                    bidak.append((x,y))
        return bidak

    # mengembalikan dictionary nomor:posisi bidak pemain tertentu
    # ini lama, jadi sebaiknya jangan dipanggil sering-sering
    def getNomorPosisiBidak(self, p):
        bidak={}
        bp = p+1
        for x in range(self.__nkotak):
            for y in range(self.__nkotak):
                nxy = self.__papan[x][y]
                bxy = nxy // 100
                if (bxy == bp):
                    bidak[nxy] = (x,y)
        return bidak

    def getPapan(self):
        return self.__papan.copy()
    
    def getWaktu(self):
        return time.process_time()

    def getJatahWaktu(self, ip):
        return self.__waktu[ip]

    def getSisaWaktu(self):
        ip = self.__giliran
        return self.__waktu[ip] - (time.process_time()-self.__mulai)
                            
    # return true jika x,y masih dalam papan
    def dalamPapan(self, x2, y2):
        if (x2 < 0) or (x2 >= self.__nkotak):
            return False
        if (y2 < 0) or (y2 >= self.__nkotak):
            return False        
        return True

    # return true jika x,y dalam area tujuan
    def dalamTujuan(self, ip, x, y):
        for xy in self.__tujuan[ip]:
            if (xy[0] == x) and (xy[1]==y):
                return True
        return False
    
    # return true jika boleh geser dr x1,y1 ke x2,y2
    def bolehGeser(self, ip, x1, y1, x2, y2):
        if not self.dalamPapan(x2, y2):
            return False
        if (self.__papan[x2][y2] != 0):
            return False
        dAsal = self.dalamTujuan(ip, x1, y1)
        dTujuan = self.dalamTujuan(ip, x2, y2)
        if (dAsal and not dTujuan):
            return False
        for a in self.ARAH:
            x21 = x1 + a[0]
            y21 = y1 + a[1]
            if (x21==x2) and (y21==y2):
                return True
        return False

    # return true jika boleh loncat dr x1,y1 ke x2,y2
    def bolehLoncat(self, ip, x1, y1, x2, y2):
        if not self.dalamPapan(x2, y2):
            return False
        if (self.__papan[x2][y2] != 0):
            return False
        dAsal = self.dalamTujuan(ip, x1, y1)
        dTujuan = self.dalamTujuan(ip, x2, y2)
        if (dAsal and not dTujuan):
            return False
        for a in self.ARAH:
            x21 = x1 + a[0] + a[0]
            y21 = y1 + a[1] + a[1]
            if (x21==x2) and (y21==y2):
                return True
        return False

    # mulai main, akan dicatat waktunya
    # setelah itu pemain bisa tanya dengan getSisaWaktu
    def mainMulai(self):
        ip = self.__giliran
        self.__mulai = time.process_time()

    # jalan satu geseran
    # return false kalau tak boleh
    def mainGeser(self, x1, y1, x2, y2):
        bnum = self.__papan[x1][y1]
        ip = (bnum // 100) - 1

        if (ip != self.__giliran):
            return self.S_ILLEGAL
        if not self.bolehGeser(ip, x1, y1, x2, y2):
            return self.S_ILLEGAL            
        self.__papan[x2][y2] = self.__papan[x1][y1]
        self.__papan[x1][y1] = 0
        return self.S_OK

    # jalan satu loncatan
    # return false kalau tak boleh
    def mainLoncat(self, x1, y1, x3, y3):
        bnum = self.__papan[x1][y1]
        ip = (bnum // 100) - 1
        if (ip != self.__giliran):
            return self.S_ILLEGAL
        if not self.bolehLoncat(ip, x1, y1, x3, y3):
            return self.S_ILLEGAL
        self.__papan[x3][y3] = self.__papan[x1][y1]
        self.__papan[x1][y1] = 0
        return self.S_OK


    # periksa apakah sudah berakhir
    # return True jika sudah berakhir 
    def akhir(self):
        bp = self.__giliran+1
        for xy in self.__tujuan[self.__giliran]:
            bxy = self.__papan[xy[0]][xy[1]] // 100
            if (bxy != bp):
                return False
        return True
    
    # ganti pemain berikutnya, sambil periksa waktu
    # return True jika pemain lama masih punya jatah waktu
    def ganti(self, selesai):
        self.__waktu[self.__giliran] += self.JATAH_WAKTU - (selesai - self.__mulai)
        print('time stack: ', self.__waktu[self.__giliran])
        if self.__waktu[self.__giliran] < 0:
            return self.S_TIMEOUT
        self.__giliran = (self.__giliran + 1) % self.__npemain
        return self.S_OK

    # periksa apakah regu sudah berakhir
    # return True jika sudah berakhir 
    def akhirBeregu(self):
        bp = self.__giliran+1
        for xy in self.__tujuan[self.__giliran]:
            bxy = self.__papan[xy[0]][xy[1]] // 100
            if (bxy != bp):
                return False

        teman = self.__teman[self.__giliran]
        bp = teman+1
        for xy in self.__tujuan[teman]:
            bxy = self.__papan[xy[0]][xy[1]] // 100
            if (bxy != bp):
                return False
                
        return True
    
    