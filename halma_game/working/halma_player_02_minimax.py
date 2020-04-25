# -*- coding: utf-8 -*-
"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!! WORK ON PROGRESS !!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!

Modified by Group 04

Gen 2:
Progress:
    - Get all hop list
    - Basic function (v)

Ongoing:
    - Optimalization (get move with biggest delta)
    - Evaluation function (current: only chebyshev distance)
    - Game tree breadth minimization (prioritize depth)

"""

import random
import time
from halma_player import HalmaPlayer

class HalmaStateNode:
    def __init__(self, depth, turn, parent=None, current=None, move=None):
        self.depth = depth
        self.turn = turn
        
        self.parent = parent
        self.current = [row[:] for row in current]
        self.move = move
        if move != None:
            self.current[move[-2][0]][move[-2][1]] = self.current[move[0][0]][move[0][1]]
            self.current[move[0][0]][move[0][1]] = 0
        
        if parent != None:
            if self.depth % 2 == 1:
                self.val = self.calc_evaluation() + self.parent.val
            else:
                self.val = self.calc_evaluation() - self.parent.val
        else:
            if self.depth % 2 == 1:
                self.val = self.calc_evaluation()
            else:
                self.val = self.calc_evaluation()

    # ---- Selector ----
    def get_move(self):
        return self.move

    def get_current(self):
        return self.current

    def get_parent(self):
        return self.parent
    
    def get_val(self):
        return self.val

    def get_depth(self):
        return self.depth

    def get_turn(self):
        return self.turn
        
    def get_move(self):
        return self.move

    
    # ---- Operation ----
    def get_board_pieces(self, id):
        pieces = []
        for i in range(0,10):
            for j in range(0,10):
                if (self.current[i][j] // 100) == id:
                    pieces.append((i,j))
        return pieces

    # Calculate chebyshev distance (omnidirectional) from initial to final (tuple)
    def calc_chebyshev(self, initial, final):
        return max(abs(final[0] - initial[0]), abs(final[1] - initial[1]))

    # Calculate current state evaluation function
    # To do add: hop possibilities / vulnerabilities
    def calc_evaluation(self):
        eval_value = 0

        # Player 1
        if self.turn == 1:
            target = (9,9)
        # Player 2
        else:
            target = (0,0)

        # Get board pieces
        pieces = self.get_board_pieces(self.turn)
        pieces_opp = self.get_board_pieces(1 + (2 - self.turn))

        # Chebyshev distance total for all pieces
        for pos in pieces:
            eval_value += self.calc_chebyshev(pos,target)
        
        #print('[eval value]',self.get_move(),' : ', eval_value)
        
        return eval_value


class HalmaPlayer02(HalmaPlayer):
    # Move history
    # Add move history
    move_hist = [0,[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

    # Player 1
    move_dir = (0, [(1,-1),(1,0),(0,-1),(1,1),(-1,-1),(0,1),(-1,0),(-1,1)],     # Player 1
                   [(-1,1),(-1,0),(0,1),(-1,-1),(1,1),(0,-1),(1,0),(1,-1)])     # Player 2

    def __init__(self, nama):
        super().__init__(nama)

    # !!! Idea for late game
    def get_optimized_move(self, node):
        # search traversal to matrix start from target zone and is empty
        # A* with hop moves only
        pass

    # Calculate chebyshev distance (omnidirectional) from initial to final (tuple)
    def calc_chebyshev(self, initial, final):
        return max(abs(final[0] - initial[0]), abs(final[1] - initial[1]))
    
    # Get hop list (multiple hop) from initial pos in board
    def get_loncat_multi(self, board, pos, player):
        # Helper
        def get_loncat(pos):
            loncat = []
            for move in self.move_dir[player]:
                #print('[pos]',pos)
                #print('[move]',move)
                x1 = pos[0] + move[0]
                y1 = pos[1] + move[1]
                x2 = pos[0] + (2 * move[0])
                y2 = pos[1] + (2 * move[1])
                
                if self.valid((x2,y2)):
                    if (board[x1][y1] != 0) and (board[x2][y2] == 0):
                        loncat.append((x2,y2))
        
            return loncat

        # Main
        hopped = []
        path = []
        path_queue = [[pos]]

        while path_queue != []:
            #print('[path queue]',path_queue)
            current_path = path_queue.pop(0)
            current_node = current_path[-1]
            #print('[current path]',current_path)
            #print('[current node]',current_node)
            hopped.append(current_node)

            hopping_child = get_loncat(current_node)
            h_num = 0
            for h_child in hopping_child:
                if h_child not in hopped:
                    hopped.append(h_child)
                    #print('appending ',h_child,' to ',current_path)
                    path_queue.append(current_path + [h_child])
                    h_num += 1

            if h_num == 0:
                path.append(current_path)

        # return [[(x2,y2),(x3,y3)],[(x2,y2),(x3,y3),(x4,y4)],...]
        return path
    
    # Get all loncat possibilities for each board piece in node object
    def get_all_loncat(self, node):
        loncat_all = []
        pieces = node.get_board_pieces(node.get_turn())
        board = node.get_current()

        for piece in pieces:
            hop_list = [h[1:] for h in self.get_loncat_multi(board, piece, node.get_turn())]
            
            hop_list = []
            for h in self.get_loncat_multi(board, piece, node.get_turn()):
                for n in range(1,len(h)):
                    h_buf = h[1:n+1]
                    if h_buf not in hop_list:
                        hop_list.append(h_buf)


            if hop_list != [[]]:
                loncat_all.append([piece,hop_list])
            #print('\n[----- hop list -----]',piece,' -> ',*hop_list, sep='\n')
        
        return loncat_all

    # Index valid
    def valid(self, pos):
        return ((0 <= pos[0] < 10) and (0 <= pos[1] < 10))
    
    def get_geser(self, board, pos, player):
        geser = []
        for move in self.move_dir[player]:
            x2 = pos[0] + move[0]
            y2 = pos[1] + move[1]
            
            if self.valid((x2,y2)) and board[move[0]][move[1]] == 0:
                geser.append((x2,y2))
        return geser

    # Get all loncat possibilities for each board piece in node object
    def get_all_geser(self, node):
        geser = []
        pieces = node.get_board_pieces(node.get_turn())
        for piece in pieces:
            geser_buf = []
            for move in self.move_dir[node.get_turn()]:
                x2 = piece[0] + move[0]
                y2 = piece[1] + move[1]
                
                if self.valid((x2,y2)) and node.get_current()[x2][y2] == 0:
                    geser_buf.append((x2,y2))

            geser.append([piece,geser_buf])
        
        return geser

    # Called API for model
    # Return: (selected final position, initial position, action type)
    def main(self, model):
        # AI parameter
        n_ply = 4
        n_move = 30
        
        # Copy model to local
        board = model.getPapan()[:]

        # Get initial time
        start_time = time.process_time()

        # Initialization
        nodes = []

        # Generate root node
        root_node = HalmaStateNode(0, self.nomor, None, board, None)
        root_node.calc_evaluation()
        base_val = root_node.get_val()
        nodes.append(root_node)

        # To do : add time limit
        for ply in range(0,n_ply):
            moves = []
            nodes_buf = []

            # Explore parent(s)
            for node in nodes:
                # moves_hop[piece_no][initial/path][path_no][path_move_no][x/y]
                #print(*node.get_current(), sep='\n')
                
                # Insert hop moves
                moves_hop = self.get_all_loncat(node)
                for piece_hop in range(len(moves_hop)):
                    for m in moves_hop[piece_hop][1]:
                        moves.append([moves_hop[piece_hop][0]] + m + ['loncat'])
                        #print([moves_hop[piece_hop][0]] + m)
                
                # Insert geser moves
                moves_geser = self.get_all_geser(node)
                #print('[moves_geser initial]',moves_geser)
                for piece_geser in range(len(moves_geser)):
                    for m in moves_geser[piece_geser][1]:
                        moves.append([moves_geser[piece_geser][0]] + [m] + ['geser'])
                        #print('[moves geser]',[moves_geser[piece_geser][0]] + [m])


                
                #print('[---- MOVES ----]')
                #print('[n moves]', len(moves))
                #print(*moves, sep='\n')

                #print('[---- GET CURRENT ----]')
                #print(*node.get_current(), sep='\n')
                
                initial_state = [row[:] for row in node.get_current()]

                # Explore child(s)
                for move in moves:
                    # Run moves
                    #print('\n[move]',move)
                    #print('[---- NEW STATE INITIAL ----]')
                    #print(*initial_state, sep='\n')
                    new_state = [row[:] for row in initial_state]
                    new_state[move[-2][0]][move[-2][1]] = new_state[move[0][0]][move[0][1]]
                    new_state[move[0][0]][move[0][1]] = 0
                    #print('[---- NEW STATE ----]')
                    #print(*new_state, sep='\n')
                    new_node = HalmaStateNode(node.get_depth() + 1, 1 + (2 - node.get_turn()), 
                                              node, new_state, move)
                    nodes_buf.append(new_node)
                
                nodes.remove(node)
            
            print('[nodes_buf len] ',len(nodes_buf))
            # Max layer
            if (ply % 2) == 0:
                # Append n selected child to nodes (max values)
                for i in range(0, min(n_move,len(nodes_buf))):
                    #print('[i max] ',i)
                    max_val = -1
                    max_idx = 0
                    for j in range(len(nodes_buf)):
                        val = nodes_buf[j].get_val()
                        if val > max_val:
                            max_val = val
                            max_idx = j
                    #print('[max layer]',nodes_buf[max_idx].get_move(),' : ',nodes_buf[max_idx].get_val())
                    
                    nodes.append(nodes_buf[max_idx])
                    del nodes_buf[max_idx]
            
            # Min layer
            else:
                # Append n selected child to nodes (max values)
                for i in range(0, min(n_move,len(nodes_buf))):
                    min_val = 999
                    min_idx = 0
                    for j in range(len(nodes_buf)):
                        val = nodes_buf[j].get_val()
                        if val < min_val:
                            min_val = val
                            min_idx = j
                    #print('[min layer]',nodes_buf[min_idx].get_move(),' : ',nodes_buf[min_idx].get_val())
                    
                    nodes.append(nodes_buf[max_idx])
                    del nodes_buf[min_idx]
        
        #for node in nodes:
            #print(node.get_move(),' : ',node.get_val(),' -> ',node.get_parent().get_move())

        node = nodes[0]
        while node.get_parent().get_parent() != None:
            node = node.parent
        
        final = node.get_move()[1:-1]
        initial = node.get_move()[0]
        action = node.get_move()[-1]

        piece_id = board[initial[0]][initial[1]] % (self.nomor * 100)
        print('[-- final]',final[-1])
        print('[-- piece_id]',piece_id)

        # If move already in move history
        i = 0
        while final[-1] in self.move_hist[piece_id] and i < len(nodes):
            node = nodes[i]
            while node.get_parent().get_parent() != None:
                node = node.parent
            
            i += 1
        
            final = node.get_move()[1:-1]
            initial = node.get_move()[0]
            action = node.get_move()[-1]

            piece_id = board[initial[0]][initial[1]] % (self.nomor * 100)

            if i == len(nodes):
                # moves_hop[piece_no][initial/path][path_no][path_move_no][x/y]
                moves_geser = self.get_all_geser(node)
                
                initial = moves_geser[0][0]
                final = moves_geser[0][1][0]
                action = 'geser'

        
        # Add to move history
        self.move_hist[piece_id].append(final[-1])

        print('[final]',final)
        print('[initial]',initial)
        print('[action]',action)


        if action == 'geser':
            return final,initial,model.A_GESER
        elif action == 'loncat':
            return final,initial,model.A_LONCAT
        else:
            return 0,0,model.A_BERHENTI


# ##################################
# ########## CLASS DRIVER ##########
# ##################################
if __name__ == '__main__':
    p = HalmaPlayer02('Bob')

    start_time = time.process_time()

    # Search algorithm simulator (A* Search)
    board = [[101, 102, 104, 107, 111,   0,   0,   0,   0,   0],
             [103, 105,   0, 112,   0,   0,   0,   0,   0,   0],
             [106, 109,   0, 112,   0,   0,   0,   0,   0,   0],
             [110, 114, 111,   0, 211,   0, 205,   0,   0,   0],
             [115,   0,   0,   0,   0, 214,   0,   0,   0,   0],
             [0,     0,   0,   0,   0,   0, 207,   0, 215, 215],
             [0,     0,   0,   0,   0,   0,   0, 208,   0, 210],
             [0,     0,   0,   0,   0,   0,   0, 213, 209, 206],
             [0,     0,   0,   0,   0,   0, 212,   0,   0, 203],
             [0,     0,   0,   0,   0,   0,   0, 204, 202, 201]]
    
    N1 = HalmaStateNode(0,1,None,board,None)
    N2 = HalmaStateNode(0,2,None,board,None)
    
    #print(*p.get_loncat_multi(board, (6,8), 2), sep='\n')
    p1_loncat = p.get_all_loncat(N1)
    p1_geser = p.get_all_geser(N1)
    p2_loncat = p.get_all_loncat(N2)
    p2_geser = p.get_all_geser(N2)
    #print('\n---- Player 1 ----')
    #print('[loncat]')
    #print(*p.get_all_loncat(N1), sep='\n')
    #print('\n[geser]')
    #print(*p.get_all_geser(N1), sep='\n')
    print('\n---- Player 2 ----')
    print('[loncat]')
    print(*p.get_all_loncat(N2), sep='\n')
    print('\n[geser]')
    print(*p.get_all_geser(N2), sep='\n')

    #print(*board, sep='\n')

    #board[p2_geser[0][1][0][0]][p2_geser[0][1][0][1]] = board[p2_geser[0][0][0]][p2_geser[0][0][1]]
    #board[p2_geser[0][0][0]][p2_geser[0][0][1]] = 0

    #print(*board, sep='\n')

    moves = []
    k = 0

    """ # Insert hop moves
    print('[insert loncat]')
    moves_hop = p.get_all_loncat(N2)
    for piece_hop in range(len(moves_hop)):
        for m in moves_hop[piece_hop][1]:
            moves.append([moves_hop[piece_hop][0]] + m)
            #print([moves_hop[piece_hop][0]] + m)
            k += 1 """
    
    """ # Insert geser moves
    print('[insert geser]')
    moves_geser = p.get_all_geser(N2)
    for piece_geser in range(len(moves_geser)):
        for m in moves_geser[piece_geser][1]:
            moves.append([moves_geser[piece_geser][0]] + [m])
            #print([moves_geser[piece_geser][0]] + [m])
            k += 1
    
    print('(',moves[3][-1][0],',',moves[3][-1][1],')') """
    
    print('[move possibilities]: ',k)
    print('algorithm time: ', time.process_time() - start_time)