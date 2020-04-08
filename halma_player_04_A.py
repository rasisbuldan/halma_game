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
    - Increase ply
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

    # Calculate current state evaluation function
    # To do add: mid-lane distance, hop possibilities / vulnerabilities
    def calc_evaluation(self):
        eval_value = 0

        # Player 1
        if self.turn == 1:
            target = (9,9)
        else:
            target = (0,0)

        # Chebyshev distance total for all pieces to target
        pieces = self.get_board_pieces(self.turn)
        for pos in pieces:
            eval_value -= (self.calc_dist(pos, target) ** 2)
            #eval_value += (self.calc_dist(pos, (9,0)))
            #eval_value += (self.calc_dist(pos, (0,9)))
            #for i in range(0,10):
            #    eval_value -= (self.calc_dist(pos, (i,i)))

        self.val = eval_value
        #print('~~ [evaluation]',self.move,' ==> ',self.val)
        

class HalmaPlayer04(HalmaPlayer):
    # Class Attributes
    move_dir = (0, [(1,-1),(1,0),(0,-1),(1,1),(-1,-1),(0,1),(-1,0),(-1,1)],     # Player 1
                   [(-1,1),(-1,0),(0,1),(-1,-1),(1,1),(0,-1),(1,0),(1,-1)])     # Player 2
    moves = []
    ply = 1
    prune = 0

    def __init(self, nama):
        super().__init__(nama)
        self.moves = []

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
        elif node.get_turn() == 2:
            for i in range(0,5):
                for j in range(0,5 - i):
                    if (board[i][j] // 100) == 2:
                        k += 1

        return k == 15
    
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
        if depth == self.ply or self.game_finish(node):
            node.calc_evaluation()
            #print('~~ [node move]',node.get_move(),' ==> ',node.get_val())
            return node
        
        # Our turn (depth 2n - 1)
        if maximizingPlayer:
            max_eval = -999999

            # Get max move
            max_moves = []
            # Hop
            moves_hop = self.get_all_loncat(node)
            #print('~~ [moves hop max]')
            #print(*moves_hop, sep ='\n')
            for piece_hop in range(len(moves_hop)):
                for move in moves_hop[piece_hop][1]:
                    max_moves.append([moves_hop[piece_hop][0]] + move + ['1'])
            # Geser
            moves_geser = self.get_all_geser(node)
            #print('~~ [moves geser max]')
            #print(*moves_geser, sep ='\n')
            for piece_geser in range(len(moves_geser)):
                for move in moves_geser[piece_geser][1][:5]:
                    max_moves.append([moves_geser[piece_geser][0]] + [move] + ['0'])

            #random.shuffle(max_moves)

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
                    #print('Pruning!')
                    break
            
            return max_node

        # Opponent turn (depth 2n)
        else:
            min_eval = 999999

            # Get min move
            min_moves = []
            # Hop
            moves_hop = self.get_all_loncat(node)
            #print('~~ [moves hop min]')
            #print(*moves_hop, sep ='\n')
            for piece_hop in range(len(moves_hop)):
                for move in moves_hop[piece_hop][1]:
                    min_moves.append([moves_hop[piece_hop][0]] + move + ['1'])
            # Geser
            moves_geser = self.get_all_geser(node)
            #print('~~ [moves geser min]')
            #print(*moves_geser, sep ='\n')
            for piece_geser in range(len(moves_geser)):
                for move in moves_geser[piece_geser][1][:5]:
                    min_moves.append([moves_geser[piece_geser][0]] + [move] + ['0'])

            #random.shuffle(min_moves)

            for move in min_moves:
                h = HalmaStateNode(turn, node, node.get_current(), move)
                node_eval = self.minimax_node(1 + (2 - self.nomor), h, depth + 1, alpha, beta, True)

                # Get min value between beta and node evaluation value
                if node_eval.get_val() < min_eval:
                    min_eval = node_eval.get_val()
                    min_node = node_eval
                
                # Pruning
                if beta <= alpha:
                    #print('Pruning!')
                    break

            return min_node

    # Called API for model
    # Return format :
    #    (x1,y1), (x0,y0), 0
    #    [(x1,y1),(x2,y2),...], (x0,y0), 1
    #    None, None, 2
    def main(self, model):
        # AI parameter
        self.ply = 2
        self.prune = 0

        # Algorithm parameter
        self.moves = []
        alpha = -999999
        beta = 999999
        board = [row[:] for row in model.getPapan()]    # 2-D array deepcopy

        # Generate root nodes
        root_node = HalmaStateNode(self.nomor, None, board, None)

        node_choice = self.minimax_node(self.nomor, root_node, 0, alpha, beta, True)
        print('~~ [node choice]',node_choice.get_move())

        # Backtrace to selected first child node of root_node
        while node_choice.get_parent().get_parent() != None:
            print('~~ [node parent]',node_choice.get_parent().get_move())
            node_choice = node_choice.get_parent()
        
        # Extract move information
        print('~~ [final node choice]',node_choice.get_move())
        if node_choice.get_move() != None:
            move_choice = node_choice.get_move()
        
            initial = move_choice[0]
            act_num = int(move_choice[-1])
            if act_num == 0:
                final = move_choice[1]
                action = model.A_GESER
                print('~~ [return]',final,',',initial,',',action)
                return final, initial, action
            elif act_num == 1:
                final = move_choice[1:-1]
                action = model.A_LONCAT
                print('~~ [return]',final,',',initial,',',action)
                return final, initial, action
        
        # No move available
        else:
            print('~~ [return] no move')
            return None,None,model.A_BERHENTI
        