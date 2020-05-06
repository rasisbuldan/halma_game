import time
import _pickle as cPickle
import random
import gc
import math
from halma_game.halma_player import HalmaPlayer

# based on pr4
class HalmaPlayer02A(HalmaPlayer):
    nama = "Pemain 4 Player"
    deskripsi = "Kelompok 2 (13316017 - 13316079 - 13316087)"
    nomor = 2
    index = 0
    teman = None
    papan = []

# 1. FUNGSI INIT --------------------------------------------------------------
    def __init__(self, nama):
        self.nama = nama

        self._ply = 2
        self._childMax = 100
        self.pilihan = []

        self.moveCount = 0
        self.stage = 0
        self.lastScore = 0
        self.lastScore2 = 0

        self.setup = True
        self.nkotak = 0
        self.nbidak = 0

    def setNomor(self, nomor):
        self.nomor = nomor
        self.index = nomor - 1
        self.Iteman = (self.index + 2)%4

    def setTeman(self, p1):
        self.teman = p1

    # To copy a class ~1.6x faster than copy.deepcopy()
    # https://stackoverflow.com/questions/24756712/deepcopy-is-extremely-slow/29385667#29385667
    def deepcopy(self, model):
        return cPickle.loads(cPickle.dumps(model, -1))

# 2. FUNGSI CARI CABANG -------------------------------------------------------
    # Mencari cabang suatu node
    def cariCabang(self, model, index, ketat, n):
        # inisialisasi
        cabang = []
        papan = model.getPapan()
        # index = self.index if maxPlayer else 1 - self.index
        x = self.getTarget(index)
        b0 = model.getPosisiBidak(index)

        # ubah urutan b0 berdasar stage sekarang
        if self.stage == 0:  # stage nol dari depan dulu
            b0 = sorted(b0, key=lambda b: math.sqrt((x[0] - b[0])**2 + (x[1] - b[1])**2))
            # if index == 0:
            #     b0.reverse()
        elif self.stage < 4: # stage 1-3 mulai dari belakang
            b0 = sorted(b0, key=lambda b: math.sqrt((x[0] - b[0])**2 + (x[1] - b[1])**2),  reverse=True)
        else:  # stage 4 pilih acak
            random.shuffle(b0)

        # cari cabang dari b0
        for b in b0:
            # stage 0 usahakan semua telah keluar dari daerah asal dulu
            if self.stage == 0:
                if ketat and not model.dalamTujuan(self.Iteman, b[0], b[1]):
                    continue

            # dapatkan langkah geser dan loncat yang mungkin
            g, l = self.bisaMain(model, papan, index, b[0], b[1])
            asal = b

            # periksa langkah lompatan
            for i in range(len(l)):
                node = self.deepcopy(model)
                aksi = model.A_LONCAT
                tujuan = l[i] if type(l[i]) != tuple else [l[i]]

                # aturan tambahan
                if ketat:
                    # jangan balik ke kandang
                    if self.stage > 0:
                        if model.dalamTujuan(self.Iteman, tujuan[-1][0], tujuan[-1][1]):
                            continue

                    # dahulukan kalau dari luar daerah tujuan bisa masuk ke daerah tujuan
                    # kalau gabisa asal perpindahannya masih di dalem oke2 aja
                    if not model.dalamTujuan(index, asal[0], asal[1]):
                        if model.dalamTujuan(index, tujuan[-1][0], tujuan[-1][1]):
                            pass
                    else:
                        # kalau stage awal jangan ambil yang asalnya dari daerah tujuan
                        # isi dulu daerah target
                        if self.stage < 3:
                            continue
                        else:
                            # kalau pindahnya keluar daerah tujuan maka jangan diambil
                            if not model.dalamTujuan(index, tujuan[-1][0], tujuan[-1][1]):
                                continue

                    # kalau stage akhir kalau asalnya dari dalam daerah tujuan jgn diambil
                    if self.stage == 4:
                        if model.dalamTujuan(index, asal[0], asal[1]):
                            continue

                    # ambil gerakan yang pasti mengurangi Euclidian distance
                    asalCent = math.sqrt((x[0] - asal[0])**2 + (x[1] - asal[1])**2)
                    tujuanCent = math.sqrt((x[0] - tujuan[-1][0])**2 + (x[1] - tujuan[-1][1])**2)
                    if asalCent > tujuanCent:
                        pass
                    else:
                        continue

                    # jadikan cabang yang lolos filter
                    nextNode = self.nextStep(node, tujuan, asal, aksi, index)
                    cabang.append((nextNode, tujuan, asal, aksi))
                else: # aturan versi rileks
                    # kalau pindah dari daerah tujuan ke daerah luar jangan diambil
                    if model.dalamTujuan(index, asal[0], asal[1]) and not model.dalamTujuan(index, tujuan[-1][0], tujuan[-1][1]):
                        continue
                    nextNode = self.nextStep(node, tujuan, asal, aksi, index)
                    cabang.append((nextNode, tujuan, asal, aksi))

            # periksa langkah geser
            for i in range(len(g)):
                node = self.deepcopy(model)
                aksi = model.A_GESER
                tujuan = g[i]

                # aturan tambahan
                if ketat:
                    # jangan balik ke kandang
                    if self.stage > 0:
                        if model.dalamTujuan(self.Iteman, tujuan[0], tujuan[1]):
                            continue

                    # dahulukan kalau dari luar daerah tujuan bisa masuk ke daerah tujuan
                    # kalau gabisa asal perpindahannya masih di dalem oke2 aja
                    if not model.dalamTujuan(index, asal[0], asal[1]):
                        if model.dalamTujuan(index, tujuan[0], tujuan[1]):
                            pass
                    else:
                        # kalau stage awal jangan ambil yang asalnya dari daerah tujuan
                        # isi dulu daerah target
                        if self.stage < 3:
                            continue
                        else:
                            # kalau pindahnya keluar daerah tujuan maka jangan diambil
                            if not model.dalamTujuan(index, tujuan[0], tujuan[1]):
                                continue

                    # kalau stage akhir kalau asalnya dari dalam daerah tujuan jgn diambil
                    if self.stage == 4:
                        if model.dalamTujuan(index, asal[0], asal[1]):
                            continue

                    # ambil gerakan yang pasti mengurangi Euclidian distance
                    asalCent = math.sqrt((x[0] - asal[0])**2 + (x[1] - asal[1])**2)
                    tujuanCent = math.sqrt((x[0] - tujuan[0])**2 + (x[1] - tujuan[1])**2)
                    if asalCent > tujuanCent:
                        pass
                    else:
                        continue

                    # jadikan cabang yang lolos filter
                    nextNode = self.nextStep(node, tujuan, asal, aksi, index)
                    cabang.append((nextNode, tujuan, asal, aksi))
                else: # aturan versi rileks
                    # kalau pindah dari daerah tujuan ke daerah luar jangan diambil
                    if model.dalamTujuan(index, asal[0], asal[1]) and not model.dalamTujuan(index, tujuan[0], tujuan[1]):
                        continue
                    nextNode = self.nextStep(node, tujuan, asal, aksi, index)
                    cabang.append((nextNode, tujuan, asal, aksi))

        if self.lastScore == self.nbidak:
            return []

        # kalau ternyata ga dapat cabang, longgarkan aturan
        if cabang == [] and n<1:
            cabang = self.cariCabang(model, index, False, n+1)

        return cabang

    # mengembalikan semua kemungkikan main (geser / loncat) bidak di (x1, y1)
    def bisaMain(self, model, papan, ip, x1, y1):
        geser = []
        loncat = {}
        baris = 0
        kolom = 0

        dTujuan = model.dalamTujuan(ip, x1, y1)
        for a in model.ARAH:
            x2 = x1 + a[0]
            y2 = y1 + a[1]
            #print((x2, y2), end="")
            if model.dalamPapan(x2, y2):
                if (papan[x2][y2] == 0):
                    if not dTujuan or model.dalamTujuan(ip, x2, y2):
                        geser.append((x2, y2))
                else:
                    x3 = x2 + a[0]
                    y3 = y2 + a[1]
                    #print((x3, y3), end="")
                    if model.dalamPapan(x3, y3):
                        if (papan[x3][y3] == 0):
                            if not dTujuan or model.dalamTujuan(ip, x3, y3):
                                try:
                                    loncat[baris].update(
                                        {kolom: {"xy": (x3, y3)}})
                                except:
                                    loncat[baris] = {kolom: {"xy": (x3, y3), "parent":(x1,y1)}}
                                kolom += 1

        loncat = self.loncatanPlus(model, papan, loncat, ip)

        # done getting the dictionary i wanted, now i need to sort it
        # to match the format specified
        loncat2 = self.sortLoncat(loncat)
        loncat2 = sorted(loncat2, key=lambda l: len(l), reverse=True)

        # print("GESER", geser)
        # print("LONCAT", loncat2)

        return geser, loncat2

    # Mencari loncatan lanjutan
    def loncatanPlus(self, model, papan, loncat, ip):
        loncat_buffer = []
        baris = 1
        stopCheck = False
        memory = []

        baris = 0
        while stopCheck == False:
            try:
                kolom = 0
                # untuk semua elemen dalam satu baris
                for i in range(len(loncat[baris])):
                    x1 = loncat[baris][i]["xy"][0]
                    y1 = loncat[baris][i]["xy"][1]
                    dTujuan = model.dalamTujuan(ip, x1, y1)
                    memory.append( loncat[baris][i]["parent"])
                    for a in model.ARAH:
                        x2 = x1 + a[0]
                        y2 = y1 + a[1]
                        #print((x2, y2), end="")
                        if model.dalamPapan(x2, y2):
                            # print("xy", x2, y2, papan[x2][y2])
                            if (papan[x2][y2] == 0):
                                pass
                            else:
                                x3 = x2 + a[0]
                                y3 = y2 + a[1]
                                # print("xy3", x3, y3, papan[x3][y3])
                                if model.dalamPapan(x3, y3) and (x3, y3) not in memory:
                                    if (papan[x3][y3] == 0):
                                        if not dTujuan or model.dalamTujuan(ip, x3, y3):
                                            # print("BLAST")
                                            try:
                                                # print("BLAST2")
                                                loncat[baris + 1].update(
                                                    {kolom: {"xy": (x3, y3), "parent": (x1, y1)}})
                                            except:
                                                # print("BLAST3")
                                                loncat[baris + 1] = {
                                                    kolom: {"xy": (x3, y3), "parent": (x1, y1)}}
                                            # print(baris, kolom)
                                            kolom += 1
                                            # gc.disable()
                                            memory.append((x1, y1))
                baris += 1
            except:
                stopCheck = True

        return loncat

    # Sort Loncatan yang telah didapat
    def sortLoncat(self, loncat):
        buffer = []
        loncat2 = []
        no = 0
        baris = len(loncat) - 1 if len(loncat) > 0 else None  # baris terakhir
        if baris != None:
            # untuk semua kolom dalam baris terakhir
            for kolom in range(len(loncat[baris])):
                if baris > 0:
                    # tambahkan xy tersebut dan parentnya
                    buffer = [loncat[baris][kolom]["xy"],
                              loncat[baris][kolom]["parent"]]
                    # cari ke atas, kalau xy itu ada di buffer = tambahkan parentnya ke buffer
                    for i in reversed(range(len(loncat) - 1)):
                        for j in range(len(loncat[i])):
                            if (loncat[i][j]["xy"] in buffer):
                                if("parent" in loncat[i][j].keys()):
                                    buffer.append(loncat[i][j]["parent"])
                            else:
                                if (i == 0):
                                    loncat2.append(loncat[i][j]["xy"])

                    buffer2 = buffer[::-1]

                    loncat2.append(buffer2)

                    for i in range(1, len(buffer2)):
                        buffer3 = buffer2[:i]
                        loncat2.append(buffer3)
                else:
                    loncat2.append(loncat[baris][kolom]["xy"])

        return loncat2

    # mensimulasikan next step kalo disi)ilakukan aksi tertentu thd papan
    def nextStep(self, model2, tujuan, asal, aksi, index):
        # sesuaikan giliran
        while model2.getGiliran() != index:
            model2.ganti(0)

        if (aksi == model2.A_LONCAT):
            for xy in tujuan:
                valid = model2.mainLoncat(asal[0], asal[1], xy[0], xy[1])
                if (valid == model2.S_OK):
                    asal = xy
        elif (aksi == model2.A_GESER):
            valid = model2.mainGeser(asal[0], asal[1], tujuan[0], tujuan[1])
            if (valid == model2.S_OK):
                pass
        else:
            pass

        return model2

# 3. FUNGSI STATIC EVALUATION -------------------------------------------------
    # Menghitung Fungsi Evaluasi berdasar kondisi node (Mirip A*)
    def evalFunc(self, node):
        # inisialisasi
        score = 0

        # bobot
        w0 = -0.5
        w1 = 20

        # A* = h + g
        score += w0 * self.evalEuclidian(node, self.index)
        score += w0 * self.evalEuclidian(node, self.Iteman)
        score += w1 * (self.evalFuncTarget(node, self.index) - self.lastScore)
        score += w1 * (self.evalFuncTarget(node, self.Iteman) - self.lastScore2)

        return score

    # Fungsi Evaluasi Euclidian Distance (Heuristik)
    def evalEuclidian(self, node, giliran):
        b0 = node.getPosisiBidak(giliran)
        c = 0

        # Target Euclidian adalah ujung kotak tempat tujuan
        x = self.getTarget(giliran)

        # Kalau stage lanjutan, maka target Euclidian diganti jadi salah satu kotak kosong
        if self.stage > 2 and self.cariKosong(node, giliran) != []:
            x = self.cariKosong(node, giliran)

        for b in b0:
            if node.dalamTujuan(giliran, b[0],b[1]):
                c += 0
            else:
                c += math.sqrt((x[0] - b[0])**2 + (x[1] - b[1])**2)

        return c

    # Fungsi Evaluasi jumlah bidak yang berada di daerah tujuan
    def evalFuncTarget(self, node, giliran):
        score = 0
        papan = node.getPapan()

        for i in range(len(papan)):
            for j in range(len(papan[i])):
                if node.dalamTujuan(giliran, i, j) and papan[i][j] // 100 == (giliran + 1):
                    score += 1

        return score

    # Fungsi untuk mencari kotak yang kosong di daerah tujuan
    def cariKosong(self, node, index):
        # index = self.index
        papan = self.papanBiner(node, index, 1, 0)
        kosong = []
        if index == 1:
            for i in range(len(papan)):
                for j in range(len(papan[i])):
                    if node.dalamTujuan(index, i, j) and papan[i][j] == 0:
                        kosong = (i, j)
                        break
        else:
            for i in reversed(range(len(papan))):
                for j in reversed(range(len(papan[i]))):
                    if node.dalamTujuan(index, i, j) and papan[i][j] == 0:
                        kosong = (i, j)
                        break

        return kosong

    # Untuk dapat ujung daerah tujuan
    def getTarget(self, index):
        if index == 0:
            x = (self.nkotak-1, self.nkotak-1)
        elif index == 1:
            x = (self.nkotak-1, 0)
        elif index == 2:
            x = (0, 0)
        elif index == 3:
            x = (0, self.nkotak-1)
        return x

    # Mengonversi papan menjadi biner 1 / 0 sehingga mudah diolah
    def papanBiner(self, node, giliran, a, b):
        papan = node.getPapan()
        papan_biner = self.deepcopy(papan)

        for i in range(len(papan)):
            for j in range(len(papan)):
                if int(str(papan[i][j])[:1]) == giliran + 1:
                    papan_biner[i][j] = a
                # elif int(str(papan[i][j])[:1]) == 1 - giliran + 1:
                #     papan_biner[i][j] = b
                else:
                    papan_biner[i][j] = b
        return papan_biner

# 4. FUNGSI MINIMAX + PRUNING -------------------------------------------------
    # Minimax with alpha-beta pruning
    # https://www.youtube.com/watch?v=l-hh51ncgDI
    def minimax(self, position, depth, alpha, beta, maxPlayer):
        if depth == 0 or position.akhir():
            return self.evalFunc(position)

        if maxPlayer:
            maxEval = -9999
            cabang = self.cariCabang(position, abs(self._ply-depth+self.index)%4, True,0)
            childCount = 0
            for child in cabang:
                if childCount < self._childMax:
                    eval = self.minimax(
                        child[0], depth - 1, alpha, beta, False)
                    # these two lines is somehow the problem
                    if depth == self._ply and eval >= maxEval:
                        gc.disable()
                        self.pilihan.append((child[1], child[2], child[3]))

                    maxEval = max(maxEval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
                childCount += 1
            return maxEval
        else:
            minEval = 9999
            cabang = self.cariCabang(position, abs(self._ply-depth+self.index)%4, True,0)
            childCount = 0
            for child in cabang:
                if childCount < self._childMax:
                    eval = self.minimax(child[0], depth - 1, alpha, beta, True)
                    minEval = min(minEval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
                childCount += 1
            return minEval

# 0. MAIN CALL ----------------------------------------------------------------
    # Main Function
    def main(self, model):
        # setup to run once
        if self.setup:
            self.nkotak = model.getUkuran()
            self.nbidak = model.getJumlahBidak()
            self.Iteman = (self.index + 2)%4
            self.setup = False

        # indicate stages based on number of moves so far
        if self.moveCount > 20:
            self.stage += 1
            self.moveCount = 0
            if self.stage > 4:
                self.stage = 4

        time_start = time.process_time()

        # initialization
        self.pilihan = []
        initPos = self.deepcopy(model)

        # minimax + pruning
        evalScore = self.minimax(initPos, self._ply, -9999, 9999, True)

        # closing statements
        print("time taken:", time.process_time() - time_start)
        self.moveCount += 1

        # return statements
        if len(self.pilihan) > 0:
            pilih = random.randint(0, len(self.pilihan) - 1)

            # update last score
            self.lastScore = self.evalFuncTarget(self.nextStep(
                initPos, self.pilihan[pilih][0], self.pilihan[pilih][1], self.pilihan[pilih][2], self.index), self.index)
            self.lastScore2 = self.evalFuncTarget(self.nextStep(
                initPos, self.pilihan[pilih][0], self.pilihan[pilih][1], self.pilihan[pilih][2], self.index), self.Iteman)

            if self.lastScore >= self.nbidak / 2 or self.lastScore2 >= self.nbidak / 2:
                self.stage = 4

            # return stuffs
            if self.pilihan[pilih][2] == model.A_LONCAT:
                return (self.pilihan[pilih][0], self.pilihan[pilih][1], self.pilihan[pilih][2]) if type(self.pilihan[pilih][0]) != tuple else ([self.pilihan[pilih][0]], self.pilihan[pilih][1], self.pilihan[pilih][2])
            else:
                return [self.pilihan[pilih][0]], self.pilihan[pilih][1], self.pilihan[pilih][2]
        else:
            print("MANDEG", self.index)
            return None, None, model.A_BERHENTI
