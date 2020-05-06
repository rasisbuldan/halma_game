# -*- coding: utf-8 -*-
"""
Gen 3 - Team 04
Dimas Apeco Putra - 13316015
Rasis Syauqi Buldan - 13316043
Thoriq Fauzan Ariandi - 13316063
"""

import random
import time
from halma_game.halma_player import HalmaPlayer


class HalmaStateNode:
    move_dir = (0, [(1,-1),(1,0),(0,-1),(1,1),(-1,-1),(0,1),(-1,0),(-1,1)],     # Player 1
                   [(-1,-1),(0,-1),(-1,0),(-1,1),(1,-1),(0,1),(1,0),(1,1)],     # Player 2
                   [(-1,1),(-1,0),(0,1),(-1,-1),(1,1),(0,-1),(1,0),(1,-1)],     # Player 3
                   [(1,1),(0,1),(1,0),(-1,1),(1,-1),(-1,0),(0,-1),(-1,-1)])     # Player 4
    val = 0

    def __init__(self, turn, parent=None, current=None, move=None):
        # Store attributes value
        self.parent = parent
        self.current = [row[:] for row in current]      # 2-D array deepcopy
        self.move = move
        self.turn = turn

        # Run move [(x0,y0),(x1,y1),1]
        if move != None:
            self.current[move[-2][0]][move[-2][1]] = self.current[move[0][0]][move[0][1]]
            self.current[move[0][0]][move[0][1]] = 0

    # ---- Selector ----
    def get_move(self):
        return self.move

    def get_current(self):
        ''' 2D array deepcopy for independent copy of current '''
        return [row[:] for row in self.current]

    def get_parent(self):
        return self.parent
    
    def get_val(self):
        return self.val
    
    def get_turn(self):
        return self.turn
    
    def is_valid(self, pos):
        return ((0 <= pos[0] < 10) and (0 <= pos[1] < 10))
    
    def is_empty(self, pos):
        return self.current[pos[0]][pos[1]] == 0

    def is_board_piece(self, pos):
        return self.current[pos[0]][pos[1]] // 100
    

    def get_dist_reference(self, player_id):
        ''' Distance reference for player_id (initial and final reference) '''
        if player_id == 1:
            return (0,0),(9,9)
        elif player_id == 2:
            return (0,9),(9,0)
        elif player_id == 3:
            return (9,9),(0,0)
        elif player_id == 4:
            return (9,0),(0,9)
    

    def in_zone(self, pos, player_id):
        ''' Pieces with pos in zone of player_id turn '''
        
        # Player 1 (Top left)
        if player_id == 1:
            return pos[0] in range(0,4) and pos[1] in range(0, 4 - pos[0])

        # Player 2 (Top right)
        elif player_id == 2:
            return pos[0] in range(0,4) and pos[1] in range(6 + pos[0], 10)

        # Player 3 (Bottom right)
        elif player_id == 3:
            return pos[0] in range(6,10) and pos[1] in range(10 - (pos[0] - 5), 10)

        # Player 4 (Bottom left)
        elif player_id == 4:
            return pos[0] in range(6,10) and pos[1] in range(0, pos[0] - 5)

    
    def in_target_zone(self, pos, player_id):
        ''' Pieces with pos of player_id turn in target zone '''
        return self.in_zone(pos, 1 + ((player_id + 1) % 4))


    def count_in_base(self, player_id):
        ''' Count board pieces of player_id turn in base zone '''
        pieces = self.get_board_pieces(player_id)

        k = 0
        for piece in pieces:
            if self.in_zone(piece, player_id):
                k += 1
        
        return k


    def count_in_target(self, player_id):
        ''' Count board pieces of player_id turn in target zone '''
        pieces = self.get_board_pieces(player_id)

        k = 0
        for piece in pieces:
            if self.in_target_zone(piece, player_id):
                k += 1
        
        return k

    
    def game_finished(self):
        ''' Game finished check function '''
        return self.count_in_target(self.get_turn()) == 10


    def get_board_pieces(self, player_id):
        ''' Get all board pieces position of player_id (list of position) '''
        pieces = []

        # Board traversal
        for i in range(0,10):
            for j in range(0,10):
                if self.is_board_piece((i,j)) == player_id:
                    pieces.append((i,j))
        return pieces


    def get_loncat_multi(self, pos, player_id):
        ''' Get multiple hop list from pos for player_id turn '''

        # Helper
        def get_loncat(pos):
            loncat = []

            # Explore all move direction
            for move in self.move_dir[player_id]:
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


    def get_all_loncat(self, player_id):
        ''' Get all hop possibilities for each board piece in node object for player_id turn '''
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

    
    def get_loncat_count(self, player_id):
        ''' Get hop count of player_id board piece '''
        moves_hop = self.get_all_loncat(player_id)
        hop_count = 0

        for piece_hop in range(len(moves_hop)):
            hop_count += len(moves_hop[piece_hop][1])

        return hop_count
    

    def get_all_geser(self, player_id):
        ''' Get all geser possibilities for each board piece in node object '''
        geser = []
        pieces = self.get_board_pieces(player_id)
        for piece in pieces:
            geser_buf = []
            for move in self.move_dir[player_id]:
                x1 = piece[0] + move[0]
                y1 = piece[1] + move[1]
                
                if self.is_valid((x1,y1)) and self.is_empty((x1,y1)):
                    geser_buf.append((x1,y1))

            geser.append([piece,geser_buf])
        
        return geser
    

    def constraint(self, move):
        ''' Moves contstraint (work to do) '''
        return True


    def get_all_moves(self, player_id):
        ''' Get all moves (return list hop,geser) '''
        moves = []

        # Hop
        moves_hop = self.get_all_loncat(player_id)
        for piece_hop in range(len(moves_hop)):
            for move in moves_hop[piece_hop][1]:
                if self.constraint(move):
                    moves.append([moves_hop[piece_hop][0]] + move + ['1'])
        
        # Geser
        moves_geser = self.get_all_geser(player_id)
        for piece_geser in range(len(moves_geser)):
            for move in moves_geser[piece_geser][1]:
                if self.constraint(move):
                    moves.append([moves_geser[piece_geser][0]] + [move] + ['0'])
        
        return moves

    
    def calc_dist(self, initial, final):
        ''' Calculate euclidean distance (without square root) '''
        return (abs(final[0] - initial[0]) ** 2) + (abs(final[1] - initial[1]) ** 2)


    def calc_dist_normalized(self, pos, initial, final):
        ''' Normalize evaluation parameter (dist=0 -> val=1) '''
        max_val = (abs(final[0] - initial[0]) ** 2) + (abs(final[1] - initial[1]) ** 2)
        val = (abs(final[0] - pos[0]) ** 2) + (abs(final[1] - pos[1]) ** 2)
        return 1 - (val / max_val)
        
    
    def calc_evaluation(self, weight):
        '''
        Calculate evaluation function for current node
        To do : include opponent negative evaluation function
        '''
        
        # Tree call to find root turn
        par = self.parent
        while par.parent != None:
            par = par.parent
        root_id = par.turn
        eval_value = 0

        for i in range(0,4):
            turn_id = 1 + ((root_id + i - 1) % 4)
            pieces = self.get_board_pieces(turn_id)
            
            # For ourself and ally ()
            if i % 2 == 0:
                dist_val = 0
                for piece in pieces:
                    dist_val += self.calc_dist_normalized(piece, *self.get_dist_reference(turn_id))
                
                # Pieces total distance to target zone
                eval_value += (weight['dist-target'] * (dist_val / 10))
                
                # Pieces count in target zone
                eval_value += (weight['count-target'] * (self.count_in_target(turn_id) / 10))
        
        # Save evaluation value to val attribute
        self.val = eval_value



class HalmaPlayer04B(HalmaPlayer):
    # Class Attributes
    last_move = [] # Move history (limited to n-move)
    ply = 1
    late_treshold = 0
    time_start = 0
    turn_count = 0

    def __init(self, nama):
        super().__init__(nama)
        self.turn_count = 0


    def minimax_node(self, turn, node, depth, alpha, beta, weight, maximizingPlayer):
        '''
        Recursive minimax game tree exploration
        '''
        # Termination (ply reached, game finished, or time limit)
        if depth == self.ply or node.game_finished() or (time.process_time() - self.time_start) > self.time_limit:
            node.calc_evaluation(weight)
            return node
        
        # Our turn (depth 2n - 1)
        if maximizingPlayer:
            max_eval = float('-inf')

            # Get max move
            max_moves = node.get_all_moves(node.get_turn())

            # Moves traversal
            for move in max_moves:
                h = HalmaStateNode(turn, node, node.get_current(), move)
                node_eval = self.minimax_node(1 + (turn % 4), h, depth + 1, alpha, beta, weight, False)
                
                # Get max value between alpha and node evaluation value
                if node_eval.get_val() > max_eval:
                    max_eval = node_eval.get_val()
                    max_node = node_eval
                
                alpha = max(node_eval.get_val(), alpha)
                
                # Pruning
                if beta <= alpha:
                    break
            
            return max_node

        # Opponent turn (depth 2n)
        else:
            min_eval = float('inf')

            # Get min move
            min_moves = node.get_all_moves(node.get_turn())

            # Moves traversal
            for move in min_moves:
                h = HalmaStateNode(turn, node, node.get_current(), move)
                node_eval = self.minimax_node(1 + (turn % 4), h, depth + 1, alpha, beta, weight, True)

                # Get min value between beta and node evaluation value
                if node_eval.get_val() < min_eval:
                    min_eval = node_eval.get_val()
                    min_node = node_eval

                beta = min(node_eval.get_val(), beta)
                
                # Pruning
                if beta <= alpha:
                    break

            return min_node


    # Called API for model
    # Return format :
    #    GESER:     [(x1,y1)], (x0,y0), 0
    #    LONCAT:    [(x1,y1),(x2,y2),...], (x0,y0), 1
    #    BERHENTI:  None, None, 2
    def main(self, model):
        '''
            Called API for model
            Return format :
               GESER:     [(x1,y1)], (x0,y0), model.A_GESER
               LONCAT:    [(x1,y1),(x2,y2),...], (x0,y0), model.A_LONCAT
               BERHENTI:  None, None, model.A_BERHENTI
        '''

        # AI parameter
        self.ply = 2
        self.time_limit = 4
        self.late_treshold = 9
        weight = {
            'dist-target': 0.6,
            'count-target': 0.4,
        }

        # Algorithm parameter
        alpha = float('-inf')
        beta = float('inf')
        board = [row[:] for row in model.getPapan()]    # 2-D array deepcopy


        # Time and move count tracking
        self.time_start = time.process_time()
        self.turn_count += 1

        # Root node
        root_node = HalmaStateNode(self.nomor, None, board, None)

        # If game is not finished
        if not root_node.game_finished():
            # Late game constraint
            if root_node.count_in_target(self.nomor) >= self.late_treshold:
                weight = {
                    'dist-target': 0.2,
                    'count-target': 0.8,
                }
                self.ply = 8

            # Binary tree exploration
            node_choice = self.minimax_node(self.nomor, root_node, 0, alpha, beta, weight, True)
            val = node_choice.get_val()

            # Backtrace to selected first child node of root_node
            while node_choice.get_parent().get_parent() != None:
                node_choice = node_choice.get_parent()
            
            # Extract move information
            move_choice = node_choice.get_move()
        
            initial = move_choice[0]
            act_num = int(move_choice[-1])

            # Geser
            if act_num == 0:
                final = [move_choice[1]]
                action = model.A_GESER
            # Loncat
            elif act_num == 1:
                final = move_choice[1:-1]
                action = model.A_LONCAT
            
            return final, initial, action
        

        # Game finished (no move)
        else:
            return None,None,model.A_BERHENTI