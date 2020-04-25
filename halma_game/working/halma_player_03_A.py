# -*- coding: utf-8 -*-
"""

!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!! WORK ON PROGRESS !!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!

Modified by Group 04

Gen 3:
Recursive minimax with alpha-beta pruning
Evaluation function: Total chebyshev distance to reference point (0,0) or (9,9)

To do:
    - Evaluation function tuning
"""

import random
import time
from halma_player import HalmaPlayer


class HalmaStateNode:
    val = 0

    def __init__(self, turn, parent=None, current=None, move=None):
        # Store attributes value
        self.parent = parent
        self.current = [row[:] for row in current]      # 2-D array deepcopy
        self.move = move
        self.turn = turn

        # Run move [(x0,y0),(x1,y1),1]
        if self.move != None:
            #print('~~! [run move]')
            self.current[move[1][0]][move[1][1]] = self.current[move[0][0]][move[0][1]]
            self.current[move[0][0]][move[0][1]] = 0

    # ---- Selector ----
    def get_move(self):
        return self.move

    def get_current(self):
        return [row[:] for row in self.current]

    def get_parent(self):
        return self.parent
    
    def get_val(self):
        return self.val
    
    def get_turn(self):
        return self.turn

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


    # Calculate euclidean distance
    def calc_dist(self, initial, final):
        return (abs(final[0] - initial[0]) ** 2) + (abs(final[1] - initial[1]) ** 2)

    # Helper to check if (a,b) in triangle zone (currently 10x10 supported)
    # Parameter: pos, player_id(p)
    def in_zone(self, pos, p):
        # Top left
        if p == 1:
            return pos[0] in range(0,5) and pos[1] in range(0,5 - pos[0])

        # Bottom right
        elif p == 2:
            return pos[0] in range(5,10) and pos[1] in range(10 - (pos[0] - 4), 10)

    # Calculate current state evaluation function
    # To do add: mid-lane distance, hop possibilities / vulnerabilities
    def calc_evaluation(self):
        eval_value = 0

        # Player 1
        if self.turn == 1:
            target1 = (9,9)
            target2 = (6,9)
            target3 = (9,6)
        else:
            target1 = (0,0)
            target2 = (0,3)
            target3 = (3,0)

        # Chebyshev distance total for all pieces to target
        pieces = self.get_board_pieces(self.turn)
        k = 0
        target = []
        for pos in pieces:
            eval_value -= (self.calc_dist(pos, target1) ** 2)
            #eval_value -= (self.calc_dist(pos, target2))
            #eval_value -= (self.calc_dist(pos, target3))
            
            diag = (pos[0] + pos[1]) // 2
            eval_value -= self.calc_dist(pos, (diag,diag))
            if self.in_zone(pos, 1 + (2 - self.turn)):
                eval_value += 15
                k += 1
        
        if k == 14:
            eval_value == 0

            if self.turn == 2:
                for i in range(0,5):
                    for j in range(0,5-i):
                        if self.current[i][j] // 100 != 1:
                            target = (i,j)
            
            if self.turn == 1:
                for i in range(5,10):
                    for j in range(10-(i-4),10):
                        if self.current[i][j] // 100 != 2:
                            target = (i,j)

            for p in pieces:
                if not self.in_zone(p, 1 + (2 - self.turn)):
                    pos = p

            eval_value -= self.calc_dist(pos, target)


        self.val = eval_value
        #print('~~ [evaluation]',self.move,' ==> ',self.val)
        

class HalmaPlayer03(HalmaPlayer):
    # Class Attributes
    last_move = [] # Move history (limited to n-move)
    move_dir = (0, [(1,-1),(1,0),(0,-1),(1,1),(-1,-1),(0,1),(-1,0),(-1,1)],     # Player 1
                   [(-1,1),(-1,0),(0,1),(-1,-1),(1,1),(0,-1),(1,0),(1,-1)])     # Player 2
    moves = []
    ply = 1
    prune = 0
    time_start = 0
    time_delta = 0
    turn_count = 0

    def __init(self, nama):
        super().__init__(nama)
        self.moves = []
        self.turn_count = 0


    # Game condition helper
    def valid(self, pos):
        return ((0 <= pos[0] < 10) and (0 <= pos[1] < 10))


    # Game finish condition: all pieces in target zone
    def game_finish(self, node):
        board = node.get_current()

        k = 0
        # Player 1 condition
        if node.get_turn() == 1:
            for i in range(5,10):
                for j in range(10 - (i - 4),10):
                    if (board[i][j] // 100) == 1:
                        k += 1

        # Player 2 condition
        elif node.get_turn() == 2:
            for i in range(0,5):
                for j in range(0,5 - i):
                    if (board[i][j] // 100) == 2:
                        k += 1

        return k == 15


    # Helper to check if (a,b) in triangle zone (currently 10x10 supported)
    # Parameter: pos, player_id(p)
    def in_zone(self, pos, p):
        # Top left
        if p == 1:
            return pos[0] in range(0,5) and pos[1] in range(0,5 - pos[0])

        # Bottom right
        elif p == 2:
            return pos[0] in range(5,10) and pos[1] in range(10 - (pos[0] - 4), 10)

    
    # Helper to count board piece in zone
    def count_in_target_zone(self, node):
        pieces = node.get_board_pieces(node.get_turn())
        p = 0

        # Check for every piece if in target zone (across)
        for piece in pieces:
            if in_zone(piece, 1 + (2 - node.get_turn())):
                p += 1
        
        return p
    

    # Selector
    def get_loncat_multi(self, board, pos, player):
        # Helper
        def get_loncat(pos):
            loncat = []
            for move in self.move_dir[player]:
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


    def get_all_loncat(self, node):
        loncat_all = []
        pieces = node.get_board_pieces(node.get_turn())
        board = node.get_current()

        for piece in pieces:
            hop_list = [h[1:] for h in self.get_loncat_multi(board, piece, node.get_turn())]
            if hop_list != [[]]:
                loncat_all.append([piece,hop_list])
        
        return loncat_all


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


    def minimax_node(self, turn, node, depth, alpha, beta, maximizingPlayer):
        # Termination
        if depth == self.ply or self.game_finish(node) or (time.process_time() - self.time_start) > self.time_limit:
            node.calc_evaluation()
            #print('~~ [node move]',node.get_move(),' ==> ',node.get_val())
            return node
        
        # Our turn (depth 2n - 1)
        if maximizingPlayer:
            max_eval = -9999999

            # Get max move
            max_moves = []
            # Hop
            moves_hop = self.get_all_loncat(node)
            for piece_hop in range(len(moves_hop)):
                for move in moves_hop[piece_hop][1]:
                    if move[-1] in self.last_move:
                        continue
                    max_moves.append([moves_hop[piece_hop][0]] + move + ['1'])
            # Geser
            moves_geser = self.get_all_geser(node)
            for piece_geser in range(len(moves_geser)):
                for move in moves_geser[piece_geser][1][:5]:
                    if move in self.last_move:
                        continue
                    max_moves.append([moves_geser[piece_geser][0]] + [move] + ['0'])

            # Moves traversal
            for move in max_moves:
                h = HalmaStateNode(turn, node, node.get_current(), move)
                node_eval = self.minimax_node(self.nomor, h, depth + 1, alpha, beta, False)
                
                # Get max value between alpha and node evaluation value
                if node_eval.get_val() > max_eval:
                    max_eval = node_eval.get_val()
                    max_node = node_eval
                
                # Pruning
                if beta <= alpha:
                    break
            
            return max_node

        # Opponent turn (depth 2n)
        else:
            min_eval = 9999999

            # Get min move
            min_moves = []
            # Hop
            moves_hop = self.get_all_loncat(node)
            for piece_hop in range(len(moves_hop)):
                for move in moves_hop[piece_hop][1]:
                    min_moves.append([moves_hop[piece_hop][0]] + move + ['1'])
            # Geser
            moves_geser = self.get_all_geser(node)
            for piece_geser in range(len(moves_geser)):
                for move in moves_geser[piece_geser][1][:5]:
                    min_moves.append([moves_geser[piece_geser][0]] + [move] + ['0'])

            # Moves traversal
            for move in min_moves:
                h = HalmaStateNode(turn, node, node.get_current(), move)
                node_eval = self.minimax_node(1 + (2 - self.nomor), h, depth + 1, alpha, beta, True)

                # Get min value between beta and node evaluation value
                if node_eval.get_val() < min_eval:
                    min_eval = node_eval.get_val()
                    min_node = node_eval
                
                # Pruning
                if beta <= alpha:
                    break

            return min_node


    # Called API for model
    # Return format :
    #    (x1,y1), (x0,y0), 0
    #    [(x1,y1),(x2,y2),...], (x0,y0), 1
    #    None, None, 2
    def main(self, model):
        # AI parameter
        self.ply = 8
        self.time_delta = 1
        self.time_limit = 0.3
        #self.time_limit = min(7 + (0.25 * model.getJatahWaktu(self.nomor - 1)), 9.3)
        late_treshold = 12

        # Algorithm parameter
        self.moves = []
        alpha = -9999999
        beta = 9999999
        board = [row[:] for row in model.getPapan()]    # 2-D array deepcopy

        # Time tracking
        self.time_start = time.process_time()
        self.turn_count += 1

        root_node = HalmaStateNode(self.nomor, None, board, None)

        # Late game strategy
        # Board pieces count in target zone over treshold
        # if self.count_in_target_zone(root_node) >= late_treshold

        if not self.game_finish(root_node):
            # Binary tree exploration
            node_choice = self.minimax_node(self.nomor, root_node, 0, alpha, beta, True)
            print('~~ [node choice]',node_choice.get_move())

            # Backtrace to selected first child node of root_node
            while node_choice.get_parent().get_parent() != None:
                print('~~ [node parent]',node_choice.get_parent().get_move())
                node_choice = node_choice.get_parent()
            
            # Extract move information
            print('~~ [final node choice]',node_choice.get_move())
            move_choice = node_choice.get_move()
        
            initial = move_choice[0]
            act_num = int(move_choice[-1])

            # Geser
            if act_num == 0:
                final = move_choice[1]
                self.last_move.append(final)
                action = model.A_GESER

            # Loncat
            elif act_num == 1:
                final = move_choice[1:-1]
                self.last_move.append(final[-1])
                action = model.A_LONCAT
            
            # Insert to move history
            if len(self.last_move) > 4:
                self.last_move = self.last_move[1:]
            print('~~ [last_move]',self.last_move)

            print('~~ [return]',final,',',initial,',',action)
            return final, initial, action
        
        # Game finished
        else:
            print('~~ [return] no move')
            return None,None,model.A_BERHENTI
        