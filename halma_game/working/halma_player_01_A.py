# -*- coding: utf-8 -*-
"""
Modified by Group 04
Strategi:
    - early game: 8 move awal bikin formasi
    - mid game: cari move dengan delta nilai heuristik terbesar (referensi heuristik 0 di (0,0) sama (9,9))
        - heuristik ini maksudnya fungsi evaluasi?
        - gw blm bikin pake fungsi evaluasi sm strategi minimax gt sih
        - jadi bentuknya lebih kek search
            - search naon??
            - kek A* search gitu, dari initial posititon ke final position (zona awal ke zona akhir)
            - nilai heuristiknya distancenya itu yang f = cost + heuristik
                - ok
        - kl ini udah kelar baru bikin yang versi fungsi evaluasi

    - coba pikirin dim yg bentuk adversarial game nya, gw bingung nentuin fungsi evaluasinya gimana
        - nah itu. karena kita (gw pribadi sih) belum pernah/ jarang bgt main halma
        - makanya tadi gw share link game halma online biar kita tes main dulu wkwk
        - biar dapet sense nya wkwkwk
        
        
        - gw blm pernah main halma samsek wkwk
        - sama wkwk

Fungsi nyoba2 blm kepake di algoritma main:
    - copy_model -> copy model ke local class biar bisa diutak atik (simulasi)
    - calc_path -> A* search buat nyari path dari initial ke final (ga memperhitungkan ada piece)
    - get_pieces_dist -> iseng2 iterasi kombinasi move dari zona awal ke zona akhir
                         paling efisien yang mana (total move nya paling kecil)
                         hasilnya list posisi initial ke final dan brp move buat masing-masing piece


To do:
    - benerin unexpected behavior
        - AI udah mengarah ke target tapi masih bulak balik (lagi nambahin move history biar 
          dia ga balik ke tempat sebelumnya)
    - kalo bidaknya masuk zona akhir dia lgsg berhenti, belom nambahin fungsi buat ngatur2 posisi
      biar bidak yg lain bisa masuk
    
    - oi
    - tes
"""

import random
import time
from halma_player import HalmaPlayer
from halma_model import HalmaModel

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


class HalmaPlayer01(HalmaPlayer):
    # Local class attributes
    local_model = 0
    local_board = 0
    local_piece = 0
    player_id = 0
    n_board = 0
    n_piece = 0

    # Game phase state
    formation = []
    form_i = 0
    state_early = True
    state_mid = False
    state_late = False

    # Move history
    move_history = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

    def __init(self, nama):
        super().__init__(nama)
        self.nomor = 2

    # Copy game state (model) to local (first executed before AI operation)
    def copy_model(self, model):
        self.local_model = model
        self.player_id = self.nomor
        self.local_board = model.getPapan()
        self.local_piece = model.getPosisiBidak(self.player_id)
        self.n_board = model.getUkuran()
        if self.n.board == 10:
            self.n_piece = 5
        else:
            print('Board size other than 10x10 not yet supported')
    
    # Helper to check if (a,b) in triangle zone (currently 10x10 supported)
    # Parameter: row(a), column(b), player_id(p)
    def in_zone(self, a, b, p):
        # Top left
        if p == 1:
            return a in range(0,5) and b in range(0,5 - a)
        elif p == 2:
            return a in range(5,10) and b in range(10 - (a - 4), 10)

    def get_zone(self, p):
        zone_buf = []
        for a in range(0,10):
            for b in range(0,10):
                if self.in_zone(a,b,p):
                    zone_buf.append((a,b))
        #print(zone_buf)
        return zone_buf

    # Calculate manhattan distance from initial to final (tuple)
    # intial = (row,col) 
    # final = (row,col)
    def calc_manhattan(self,initial,final):
        return (abs(final[0] - initial[0]) + abs(final[1] - initial[1]))
    
    # Calculate euclidean distance from initial to final (tuple), without sqroot to minimize computation
    # intial = (row,col) 
    # final = (row,col)
    def calc_euclidean(self, initial, final):
        return (abs(final[0] - initial[0]) ** 2 + abs(final[1] - initial[1]) ** 2)

    # Calculate chebyshev distance (omnidirectional) from initial to final (tuple)
    # intial = (row,col) 
    # final = (row,col)
    def calc_chebyshev(self, initial, final):
        return max(abs(final[0] - initial[0]), abs(final[1] - initial[1]))

    def is_valid(self, pos):
        return (0 <= pos[0] < 10 and 0 <= pos[1] < 10)

    # Calculate path using a-star search
    # Work to do: - Halma move rules
    #             - Board state import (real board piece)
    def calc_path(self, board, initial, final):
        def is_valid(pos):
            return (0 <= pos[0] < 10 and 0 <= pos[1] < 10)

        def is_board_piece(pos):
            return (board[pos[0]][pos[1]] != 0)

        print('Calculating path...')

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
            print('visiting ',current_node.pos)

            # Add visited current node to visited list
            visit.pop(current_id)
            visited.append(current_node)

            # If current node is final target
            if current_node.equal(final_node):
                #print('[final node]')
                path = []
                current = current_node
                
                # Backtracing parent position of node to initial position
                while current is not None:
                    path.append(current.pos)
                    # print('[final path] ',path)
                    current = current.parent
                
                # Return reversed path (from initial to final)
                return path[::-1]
            
            # Generate node children
            children = []
            move_possibilities = [(0,-1), (0,1), (-1,0), (1,0), (-1,-1), (-1,1), (1,-1), (1,1)]
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
                        if board[next2[0]][next2[1]] == 0:
                            node_next_pos = next2
                    
                        else:
                            continue
                    
                    else:
                        continue
                    
                # Create new node
                new_node = Node(current_node, node_next_pos)
                children.append(new_node)

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
                #print('appending ',child.pos)
                visit.append(child)

    # Get potential hop for all pieces in 1 move (modified A* with heuristic reference (0,0) or (9,9))
    # Return: [piece_position, [path]]
    def get_optimal_hop(self, board):
        print('{getting hop}')
        def is_valid(pos):
            return (0 <= pos[0] < 10) and (0 <= pos[1] < 10)
        def get_hop_list(pos, parent):
            
            move_possibilities = [(0,-1), (0,1), (-1,0), (1,0), (-1,-1), (-1,1), (1,-1), (1,1)]
            hop_possibilities = []

            for move in move_possibilities:
                new_pos = (pos[0] + move[0],pos[1] + move[1])
                new_pos2 = (pos[0] + 2*move[0],pos[1] + 2*move[1])
                if is_valid(new_pos): 
                    # Is not a board piece
                    if board[new_pos[0]][new_pos[1]] == 0:
                        continue

                if is_valid(new_pos2):
                    # Next is a board piece and another next is empty
                    if board[new_pos2[0]][new_pos2[1]] == 0:
                        node_hop = Node(parent,new_pos2)
                        node_hop.set_heur(0,0,0)
                        hop_possibilities.append(node_hop)
            
            # Return list of node object which can be hopped from pos
            return hop_possibilities

        def get_all_hop(piece):
            # Initial list
            hopped = []
            hopping = []
            hopping = get_hop_list(piece.pos, piece)

            # Loop for finding possible hop from piece position
            while len(hopping) > 0:
                hh = [h.pos for h in hopping]
                # print('[hopping]',hh)
                current_hop = hopping[0]
                current_id = 0
                
                # Select node with minimum f value
                for idx, nod in enumerate(hopping):
                    if nod.f < current_hop.f:
                        current_hop = nod
                        current_id = idx
                
                # Pop current_hop node out of hopping and add to hopped
                hopping.pop(current_id)
                hopped.append(current_hop)

                # Check search finish condition
                #print('[check cond]')
                finish = False
                k = 0
                for h in hopping:
                    for hd in hopped:
                        if h.equal(hd):
                            k += 1
                
                # Termination
                if k == len(hopping):
                    #print('[terminating]')
                    path = []
                    
                    # Backtracing from final to initial
                    while current_hop is not None:
                        path.append(current_hop.pos)
                        current_hop = current_hop.parent
                    
                    # Return reversed path
                    return path[::-1]
                
                # Check additional hop
                children_hop = get_hop_list(current_hop.pos, current_hop)
                for child in children_hop:
                    #print('[children adding]')

                    # Child already on hopped
                    already = False
                    for h in hopped:
                        if child.equal(h):
                            already = True
                    if already:
                        continue

                    # Calculate A* parameter
                    g = current_hop.g + 1
                    h = self.calc_h(child.pos)
                    
                    # Child already on hopping
                    already = False
                    for h in hopping:
                        if child.equal(h) and child.g > h.g:
                            already = True
                    if already:
                        continue

                    # Add child to hopping list
                    hopping.append(child)
        
        # Get all pieces position
        pieces = []
        player_id = self.nomor
        print('player id: ',player_id)
        for i in range(0,10):
            for j in range(0,10):
                if (board[i][j] // 100) == player_id:
                    node_piece = Node(None,(i,j))
                    node_piece.set_heur(0,0,0)
                    pieces.append(node_piece)
        p = []
        for piece in pieces:
            p.append(piece.pos)
        print(p)

        pieces_path = []
        # Access: piece(row,col)
        for piece in pieces:
            #print('[piece] ',piece.pos)
            path = get_all_hop(piece)
            if path != None:
                h = self.calc_h(path[-1])
                pieces_path.append([piece.pos,path[1:],h])
        return pieces_path

    # (Testing) Optimal total distance for every piece (iteration)
    def get_pieces_dist(self, zone_init, zone_final):
        print('Calculating optimal distance...')
        initial_time = time.time_ns()
        moves_optimal = []
        min_sum = 999
        
        # Get zones
        zone_1 = zone_init.copy()
        zone_2 = zone_final.copy()

        random.seed(time.time_ns())
        for i in range(0,1000):
            sum = 0

            # Get zone
            random.shuffle(zone_1)
            zone_2 = zone_final.copy()
            random.shuffle(zone_2)
            moves = []

            for z in zone_1:
                min_val = 999
                min_pos = (0,0)

                # Calculate minimum distance to final zone from initial
                for zo in zone_2:
                    val = self.calc_chebyshev(z,zo)
                    #print('move ',z,' to ',zo,' at ',val)
                    if val <= min_val:
                        min_val = val
                        min_pos = zo
                moves.append([z,min_pos,min_val])
                sum += min_val
                zone_2.remove(min_pos)
                #print('min: ',min_pos)
                #print('zones_opp: ',zones_opp)
            
            #print('total sum: ',sum)
            if sum < min_sum:
                min_sum = sum
                moves_optimal = moves
                #print('[optimal] sum(',min_sum,'): ',moves)
        print('[time] ', (time.time_ns() - initial_time)/1000000,'ms')
        print('[optimal] sum({}): '.format(min_sum),*moves, sep='\n')

    # Create early game formation (saving time tho) - 8 moves
    def formation_early(self):
        # if player 1
        if self.nomor == 1:
            self.formation = [
                [(4,0),(4,1),'geser'],
                [(3,1),(3,2),'geser'],
                [(1,3),(2,3),'geser'],
                [(0,4),(1,4),'geser'],
                [(3,0),(5,2),'loncat'],
                [(2,1),(4,3),'loncat'],
                [(1,2),(3,4),'loncat'],
                [(0,3),(2,5),'loncat']
            ]
        # if player 2
        elif self.nomor == 2:
            self.formation = [
                [(9,5),(8,5),'geser'],
                [(8,6),(7,6),'geser'],
                [(6,8),(6,7),'geser'],
                [(5,9),(5,8),'geser'],
                [(9,6),(7,4),'loncat'],
                [(8,7),(6,5),'loncat'],
                [(7,8),(5,6),'loncat'],
                [(6,9),(4,7),'loncat']
            ]
    
    # Check if early game formation is achieved
    def check_formation_early(self,board):
        check = True
        for i in range(len(self.formation)):
            if board[self.formation[i][1][0]][self.formation[i][1][1]] == 0:
                check = False
        return check

    # Get geser possibilities (only one move)
    def search_empty_neigh(self,pos,board):
        move_possibilities = [(1,-1),(1,0),(0,-1),(1,1),(-1,-1),(0,1),(-1,0),(-1,1)]
        if self.nomor == 2:
            move_possibilities.reverse()

        i = 0
        new_pos = (pos[0] + move_possibilities[i][0],pos[1] + move_possibilities[i][1])
        while(board[new_pos[0]][new_pos[1]] != 0):
            i += 1
            new_pos = (pos[0] + move_possibilities[i][0],pos[1] + move_possibilities[i][1])

        return new_pos

    # Get geser possibilities
    def get_geser(self,board):
        # Get all pieces position
        pieces = []
        player_id = self.nomor
        #print('player id: ',player_id)
        for i in range(0,10):
            for j in range(0,10):
                if (board[i][j] // 100) == player_id:
                    node_piece = Node(None,(i,j))
                    node_piece.set_heur(0,0,0)
                    pieces.append(node_piece)

        # Traversal for all pieces
        geser_all = []
        for piece in pieces:
            move_possibilities = [(1,-1),(1,0),(0,-1),(1,1),(-1,-1),(0,1),(-1,0),(-1,1)]
            geser_list = []

            # Get move possibilities from initial piece position
            for move in move_possibilities:
                new_pos = (piece.pos[0] + move[0],piece.pos[1] + move[1])
                if self.is_valid(new_pos):
                    if self.nomor == 1:
                        h_val = self.calc_chebyshev(new_pos,(9,9))
                    else:
                        h_val = self.calc_chebyshev(new_pos,(0,0))
                    
                    # If new position doesn't contain board pieces
                    if board[new_pos[0]][new_pos[1]] == 0:
                        geser_list.append([new_pos,h_val])

            geser_all.append([piece.pos,geser_list])
        
        return geser_all
        # geser_all = [[(x,y),[[(i,j),h_val],[(i,j),h_val]]], [(x,y),[[(i,j),h_val],[(i,j),h_val]]]]
    
    def calc_h(self,init):
        if self.nomor == 1:
            h_val = self.calc_chebyshev(init,(9,9))
        else:
            h_val = self.calc_chebyshev(init,(0,0))
        
        return h_val


    def main(self, model):
        board = model.getPapan()

        # Early game (create formation)
        if self.state_early and self.form_i < 8:
            self.formation_early()
            
            # Decompose formation info
            initial = self.formation[self.form_i][0]
            
            final = [self.formation[self.form_i][1]]
            if board[final[0][0]][final[0][1]] != 0:
                final = [self.search_empty_neigh(initial,board)]
            
            a = self.formation[self.form_i][2]
            if a == 'geser':
                action = model.A_GESER
            elif a == 'loncat':
                action = model.A_LONCAT
            else:
                action = model.BERHENTI

            self.form_i += 1

            # Check formation
            if self.form_i == 8:
                self.state_early = False
                self.state_mid = True

        # Mid game (go to target zone)
        elif self.state_mid:
            
            # Get maximum delta from hop
            # Access: move_hop[idx][hop_no]
            move_hop = self.get_optimal_hop(board)
            max_delta_hop = 0
            max_idx_hop = 0
            for i in range(0, len(move_hop)):
                # Check in history
                # in_hist = False
                # print('[move_hop] ',move_hop)
                # if self.move_history != []:
                #     for move_hist in self.move_history:
                #         if move_hist != []:
                #             #print('{move hop check}',move_hop[i][1][len(move_hop[i][1])-1])
                #             #print('{move hist}',move_hist[0][0][-1])
                #             if move_hop[i][1][len(move_hop[i][1])-1] == move_hist[0][0][-1]:
                #                 print('{in hist}')
                #                 in_hist = True
                # if in_hist:
                #     continue
                
                # Get h value of optimal_hop and history
                h_hop = move_hop[i][2]
                piece_id = board[move_hop[i][0][0]][move_hop[i][0][1]] - (100 * self.nomor)
                
                if self.move_history[piece_id - 1] != []:
                    h_hist = self.move_history[piece_id - 1][-1][1]
                else:
                    h_hist = self.calc_h(move_hop[i][0])
                
                # h smaller towards target (+ initial pos not in zone)
                delta = h_hist - h_hop
                if delta > max_delta_hop and not self.in_zone(move_hop[i][0][0], move_hop[i][0][1], 1 + (2 - self.nomor)):
                    max_delta_hop = delta
                    max_idx_hop = i

            # Get maximum delta from geser
            # Access: move_geser[piece][init_pos/geser_list][move_no][pos/h][row/col]
            move_geser = self.get_geser(board)
            max_delta_geser = 0
            max_piece_idx_geser = 0
            max_idx_geser = 0
            for i in range(0, len(move_geser)):
                max_local_delta = 0
                max_local_idx = 0
                for j in range(0, len(move_geser[i][1])):
                    # Check in history
                    # in_hist = False
                    # for move_hist in self.move_history:
                    #     if move_hist != []:
                    #         if move_geser[i][1][j][0] == move_hist[0][0]:
                    #             in_hist = True
                    # if in_hist:
                    #     continue
                    
                    h_geser = move_geser[i][1][j][1]
                    piece_id = board[move_geser[i][0][0]][move_geser[i][0][1]] - (100 * self.nomor)
                    if self.move_history[piece_id - 1] != []:
                        h_hist = self.move_history[piece_id - 1][-1][1]
                    else:
                        h_hist = self.calc_h(move_geser[i][0])

                    delta = h_hist - h_geser
                    if delta > max_delta_geser and not self.in_zone(move_geser[i][0][0], move_geser[i][0][1], 1 + (2 - self.nomor)):
                        max_delta_geser = delta
                        max_piece_idx_geser = i
                        max_idx_geser = j
            
            # Move hop
            if max_delta_hop > max_delta_geser:
                print('{action: hop}')
                action = model.A_LONCAT
                initial = move_hop[max_idx_hop][0]
                final = move_hop[max_idx_hop][1]
            else:
                print('{action: geser}')
                action = model.A_GESER
                initial = move_geser[max_piece_idx_geser][0]
                final = move_geser[max_piece_idx_geser][1][max_idx_geser]


        # Save to move history
        # Access: self.move_history[piece_id][hist_no][init/h][row/col]
        piece_id = board[initial[0]][initial[1]] - (100 * self.nomor) - 1
        print('{piece id} ', piece_id)
        #print('{piece move hist} ', self.move_history[piece_id - 1])
        print('{final} ', final)
        if action == model.A_LONCAT:
            h_val = self.calc_h(final[-1])
        else:
            h_val = self.calc_h(final[0])
        self.move_history[piece_id - 1].append([final,h_val])
        return final, initial, action
                
            
    # Dummy main (for testing purpose without import board)
    def main_local(self):
        # Model simulator
        self.player_id = 2
        #self.get_pieces_optimal_dist()
        #init = [(5,9),(6,8),(6,9),(7,8),(8,6),(8,7),(9,5),(9,6)]
        #final = [(4,7),(5,6),(5,8),(6,5),(6,7),(7,4),(7,6),(8,5)]
        #self.get_pieces_dist(init,final)

        # Search algorithm simulator (A* Search)
        board = [[101, 102, 104, 107, 111,   0,   0,   0,   0,   0],
                 [103, 105, 108, 112,   0,   0,   0,   0,   0,   0],
                 [106, 109, 113,   0,   0,   0,   0,   0,   0,   0],
                 [110, 114,   0,   0, 211,   0, 205,   0,   0,   0],
                 [115,   0,   0,   0,   0, 214,   0,   0,   0,   0],
                 [0,     0,   0,   0,   0,   0, 207,   0, 215, 215],
                 [0,     0,   0,   0,   0,   0,   0, 208,   0, 210],
                 [0,     0,   0,   0,   0,   0,   0, 213, 209, 206],
                 [0,     0,   0,   0,   0,   0, 212,   0,   0, 203],
                 [0,     0,   0,   0,   0,   0,   0, 204, 202, 201]]
        #start = (4,2)
        #target = (8,8)
        #path = self.calc_path(board,start,target)
        #print('Path from {} to {}: '.format(str(start), str(target)), *path, sep=' -> ')
        optimal_hop = self.get_optimal_hop(board)
        print(*optimal_hop, sep='\n')
        

    # Called API for model
    # Return: (selected final position, initial position, action type)
    def main_old(self, model):
        time_mulai = time.process_time()
        
        # Dummy algorithm to simulate time
        a = 0
        for i in range(0,10000000):
            a += i
        
        # Random seed for pseudorandom select
        seed1 = random.sample(range(10,1000), 20)
        random.seed(random.choice(seed1))

        # Pick random move choice
        l = []
        g = []
        papan = model.getPapan()        
        b0 = model.getPosisiBidak(self.index)
        while l == [] or g == []:
            b = random.choice(b0)
            # Calculate move possibilities
            g,l = self.bisaMain(model, papan, b[0], b[1])
        
        print('algorithm time: ', time.process_time()-time_mulai)
        
        # Return move
        # LONCAT
        if l != []:
            return [l[0]], b, model.A_LONCAT

        # GESER
        elif g != []:
            return g, b, model.A_GESER
        
        # If no move left (BERHENTI)
        return None, None, model.A_BERHENTI

# Executed if invoked directly from script
if __name__ == '__main__':
    C = HalmaPlayer01('Bob')
    #C.get_pieces_optimal_dist()
    C.main_local()

# ----------- TRASH -------------- #
"""         
# Mid game (go to target zone)
        elif self.state_mid:
            optimal_hop = self.get_optimal_hop(board)
            h_min = optimal_hop[0][2]
            h_idx = 0
            
            # Get minimum heuristic value from hopping
            # Condition: maximum delta, final not in move_history
            for i in range(1,len(optimal_hop)):
                if optimal_hop[i][2] < h_min and not self.in_zone(optimal_hop[i][0][0], optimal_hop[i][0][1], 1 + (2 - self.nomor)):
                    h_min = optimal_hop[i][2]
                    h_idx = i
            
            initial = optimal_hop[h_idx][0]

            if optimal_hop[h_idx][1] != None:
                action = model.A_LONCAT
                final = optimal_hop[h_idx][1]
            else:
                action = model.A_GESER
                final = [self.search_empty_neighbor(initial,board)] 
"""