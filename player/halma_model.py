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

    JATAH_WAKTU = 10.0

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
    
    def setJatahWaktu(self, ip, delta):
        self.__waktu[ip] += delta

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

    '''
        Added function
    '''

    def is_valid(self, pos):
        return ((0 <= pos[0] < 10) and (0 <= pos[1] < 10))
    

    def is_empty(self, pos):
        return self.__papan[pos[0]][pos[1]] == 0


    def is_board_piece(self, pos):
        return self.__papan[pos[0]][pos[1]] // 100


    # Get all board pieces position of player_id (list of position)
    def get_board_pieces(self, player_id):
        pieces = []

        # Board traversal
        for i in range(0,10):
            for j in range(0,10):
                if self.is_board_piece((i,j)) == player_id:
                    pieces.append((i,j))
        return pieces
    

    def get_loncat_multi(self, pos, player_id):
    
        # Helper
        def get_loncat(pos):
            loncat = []

            # Explore all move direction
            for move in self.ARAH:
                x1 = pos[0] + move[0]
                y1 = pos[1] + move[1]
                x2 = pos[0] + (2 * move[0])
                y2 = pos[1] + (2 * move[1])
                
                # Check if can hop and add to list
                if self.is_valid((x2,y2)):
                    if self.is_board_piece((x1,y1)) and self.is_empty((x2,y2)):
                        loncat.append((x2,y2))
            
            return loncat

        # Main
        hopped = []
        path = []
        path_queue = [[pos]]

        while path_queue != []:
            current_path = path_queue.pop(0)
            current_node = current_path[-1]
            hopped.append(current_node)

            hopping_child = get_loncat(current_node)
            h_num = 0
            for h_child in hopping_child:
                if h_child not in hopped:
                    hopped.append(h_child)
                    path_queue.append(current_path + [h_child])
                    h_num += 1

            if h_num == 0:
                path.append(current_path)

        # return [[(x2,y2),(x3,y3)],[(x2,y2),(x3,y3),(x4,y4)],...]
        return path


    # Get all hop possibilities for each board piece in node object
    def get_all_loncat(self, player_id):
        loncat_all = []
        pieces = self.get_board_pieces(player_id)

        # Explore all pieces
        for piece in pieces:
            # Get hop list for piece
            hop_list = []
            for h in self.get_loncat_multi(piece, player_id):
                for n in range(1,len(h)):
                    h_buf = h[1:n+1]
                    if h_buf not in hop_list:
                        hop_list.append(h_buf)
            
            if hop_list != [[]]:
                loncat_all.append([piece,hop_list])
        
        return loncat_all
    

    # Get all geser possibilities for each board piece in node object
    def get_all_geser(self, player_id):
        geser = []
        pieces = self.get_board_pieces(player_id)
        for piece in pieces:
            geser_buf = []
            for move in self.ARAH:
                x1 = piece[0] + move[0]
                y1 = piece[1] + move[1]
                
                if self.is_valid((x1,y1)) and self.is_empty((x1,y1)):
                    geser_buf.append((x1,y1))

            geser.append([piece,geser_buf])
        
        return geser


    # Get all moves (return list hop,geser)
    def get_all_moves(self, player_id):
        moves = []

        # Hop
        moves_hop = self.get_all_loncat(player_id)
        for piece_hop in range(len(moves_hop)):
            for move in moves_hop[piece_hop][1]:
                moves.append([moves_hop[piece_hop][0]] + move + ['1'])
        
        # Geser
        moves_geser = self.get_all_geser(player_id)
        for piece_geser in range(len(moves_geser)):
            for move in moves_geser[piece_geser][1]:
                moves.append([moves_geser[piece_geser][0]] + [move] + ['0'])
        
        #print('get_all_moves',moves)
        return moves


    # Calculate path from initial to final position using a-star search
    def calc_path_hop(self, initial, final):
        def is_valid(pos):
            return (0 <= pos[0] < 10 and 0 <= pos[1] < 10)

        def is_board_piece(pos):
            return (self.__papan[pos[0]][pos[1]] != 0)

        print('Calculating path from {} to {}...'.format(initial, final))

        # Initial and final node
        initial_node = Node(None, initial)
        initial_node.set_heur(0,0,0)
        final_node = Node(None, final)
        final_node.set_heur(0,0,0)

        # List initialization (visit: to be visited)
        visit = []
        visit.append(initial_node)
        visited = []

        # Search loop (while there is node to be visited)
        while len(visit) > 0:

            # Select node with minimal f value of visit list
            current_node = visit[0]
            current_id = 0
            for index, node in enumerate(visit):
                if node.f < current_node.f:
                    current_node = node
                    current_id = index

            # Add visited current node to visited list
            visit.pop(current_id)
            visited.append(current_node)

            # If current node is final target
            if current_node.equal(final_node):
                path = []
                current = current_node
                
                # Backtracing parent position of node to initial position
                while current is not None:
                    path.append(current.pos)
                    current = current.parent
                
                # Return reversed path (from initial to final)
                return path[::-1]
            
            # Generate node children
            children = []
            move_possibilities = [(0,-1),(0,1),(-1,0),(1,0),(-1,-1),(-1,1),(1,-1),(1,1)]
            for move in move_possibilities:
                
                # Get next node position
                node_next_pos = (current_node.pos[0] + move[0], current_node.pos[1] + move[1])

                # Node position out of board index
                if not is_valid(node_next_pos):
                    continue
                
                # Next node position is board piece
                if is_board_piece(node_next_pos):
                    next2 = (node_next_pos[0] + move[0], node_next_pos[1] + move[1])

                    # Check if hop target is valid index for board
                    if is_valid(next2):

                        # Hop
                        if self.is_empty(next2):
                            node_next_pos = next2
                            
                            # Create new node
                            new_node = Node(current_node, node_next_pos)
                            children.append(new_node)
                    
                        else:
                            continue
                    
                    else:
                        continue
                    
                

            # Loop through node parent's children
            for child in children:

                # Child already on visited
                already = False
                for v in visited:
                    if child.equal(v):
                        already = True
                if already:
                    continue
                
                # Calculate A* parameter values (f,g,h)
                g = current_node.g + 1
                h = ((child.pos[0] - final_node.pos[0]) ** 2) + ((child.pos[1] - final_node.pos[1]) ** 2)
                child.set_heur(g + h, g, h)

                # Child already on visit
                already = False
                for v in visit:
                    if child.equal(v) and child.g > v.g:
                        already = True
                if already:
                    continue
                
                # Add child to visit list
                visit.append(child)

# Supporting Class
class Node():
    parent = 0
    pos = 0

    # Node definition
    def __init__(self, parent=None, pos=None):
        self.parent = parent
        self.pos = pos

        # Heuristic value
        self.f = 0
        self.g = 0
        self.h = 0
    
    # Set heuristic value for node
    def set_heur(self, f, g, h):
        # f = g + h
        self.f = f
        self.g = g
        self.h = h

    # Check node position equality (boolean)
    def equal(self, other):
        return self.pos == other.pos