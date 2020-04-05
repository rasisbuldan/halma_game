# -*- coding: utf-8 -*-
"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!! WORK ON PROGRESS !!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!

Modified by Group 04
Generation 2: Work on progress

"""

import random
import time
from halma_player import HalmaPlayer

class HalmaStateNode:
    def __init__(self, depth, turn, parent=None, current=None, move=None):
        self.depth = depth
        self.turn = turn
        
        self.parent = parent
        self.current = current
        self.move = move
        if self.depth % 2 == 1:
            self.val = self.parent.val + self.calc_evaluation()
        else:
            self.val = self.parent.val - self.calc_evaluation()

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
        pieces = self.get_board_pieces(self.current, self.turn)
        pieces_opp = self.get_board_pieces(self.current, 1 + (2 - self.turn))
        
        # Chebyshev distance total for all pieces
        for pos in pieces:
            eval_value += self.calc_chebyshev(pos,target)
        
        return eval_value


class HalmaPlayer02(HalmaPlayer):
    # Player 1
    move_dir = (0, [(1,-1),(1,0),(0,-1),(1,1),(-1,-1),(0,1),(-1,0),(-1,1)],     # Player 1
                   [(-1,1),(-1,0),(0,1),(-1,-1),(1,1),(0,-1),(1,0),(1,-1)])     # Player 2

    def __init__(self, nama):
        super().__init__(nama)

    # Calculate chebyshev distance (omnidirectional) from initial to final (tuple)
    def calc_chebyshev(self, initial, final):
        return max(abs(final[0] - initial[0]), abs(final[1] - initial[1]))

    def get_loncat(self, board, pos, player, n):
        loncat = []
        for move in move_dir[player][:n]:
            x2 = pos[0] + (2 * move[0])
            y2 = pos[1] + (2 * move[1])
            
            if (not self.valid((x2,y2))) or (board[x2][y2] != 0):
                continue
            
            loncat.append([pos,(x2,y2)])
        
        return loncat
    
    def get_optimized_loncat(self, node):
        # search traversal to matrix start from target zone and is empty
        # A* with hop moves only

        pass



    # Get all loncat from initial position
    # Return list of possible loncat path
    # [[(x11,y11),(x12,y12),(x13,y13)],
    #  [(x21,y21),(x22,y22)],
    #  []]
    def get_all_loncat(self, node):
        loncat = []
        for initial in node.get_board_pieces():
            for move in move_dir[node.get_turn()]:
                pass
    
    # Index valid
    def valid(self, pos):
        return ((0 <= pos[0] < 10) and (0 <= pos[1] < 10))
    
    def get_all_geser(self, node):
        geser = []
        for initial in node.get_board_pieces(node.get_turn()):
            for move in move_dir[node.get_turn()]:
                x2 = initial[0] + move[0]
                y2 = initial[1] + move[1]
                
                if not valid((x2,y2)) or node.get_current()[move[0]][move[1]] != 0:
                    continue
                
                geser.append([initial,(x2,y2)])
        
        return geser
    
    # Get all possible final position from initial position
    def get_all_move(self, node):
        pass

    # Called API for model
    # Return: (selected final position, initial position, action type)
    def main(self, model):
        # AI parameter
        n_ply = 1
        n_move = 5

        # Get initial time
        start_time = time.process_time()

        # Initialization
        nodes = []

        # Generate root node
        root_node = HalmaStateNode(0, self.nomor, None, model.getPapan(), None)
        root_node.calc_evaluation()
        base_val = root_node.get_val()
        nodes.append(root_node)

        # To do : add time limit
        for ply in range(0,n_ply):
            moves = []
            
            # Explore parent(s)
            for node in nodes:
                moves.append(self.get_all_move(node))
                nodes_buf = []

                # Explore child(s)
                for move in moves:
                    # Run moves
                    new_state = node.get_current()
                    new_state[move[1][0]][move[1][1]] = new_state[move[0][0]][move[0][1]]
                    new_state[move[0][0]][move[0][1]] = 0
                    new_node = HalmaStateNode(node.get_depth() + 1, 1 + (2 - node.get_turn()), 
                                              node, new_state, move)
                    nodes_buf.append(new_node)
                
                nodes.remove(node)

            # Max layer
            if (ply % 2) == 0:
                # Append n selected child to nodes (max values)
                for i in range(0, n_move):
                    max_val = 0
                    max_idx = 0
                    for j in range(len(nodes_buf)):
                        val = nodes_buf.get_val()
                        if val >= max_val:
                            max_val = val
                            max_idx = j
                    
                    del nodes_buf[max_idx]
                    nodes.append(max_val)
            
            # Min layer
            else:
                # Append n selected child to nodes (max values)
                for i in range(0, n_move):
                    min_val = 0
                    min_idx = 0
                    for j in range(len(nodes_buf)):
                        val = nodes_buf.get_val()
                        if val <= min_val:
                            min_val = val
                            min_idx = j
                    
                    del nodes_buf[min_idx]
                    nodes.append(min_val)
        

                



# ------------------------------------

        
        
        """ # Random seed for pseudorandom select
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
        
        
        # Return move
        print('algorithm time: ', time.process_time()-time_mulai)

        # LONCAT
        if l != []:
            return [l[0]], b, model.A_LONCAT

        # GESER
        elif g != []:
            return g, b, model.A_GESER
        
        # If no move left (BERHENTI)
        return None, None, model.A_BERHENTI """