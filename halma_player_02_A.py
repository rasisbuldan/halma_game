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
        self.current = current
        self.move = move
        if parent != None:
            if self.depth % 2 == 1:
                self.val = self.parent.val + self.calc_evaluation()
            else:
                self.val = self.parent.val - self.calc_evaluation()
        else:
            if self.depth % 2 == 1:
                self.val = self.calc_evaluation()
            else:
                self.val = - self.calc_evaluation()

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
        pieces = self.get_board_pieces(self.turn)
        pieces_opp = self.get_board_pieces(1 + (2 - self.turn))
        
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

    # !!! Idea
    def get_optimized_move(self, node):
        # search traversal to matrix start from target zone and is empty
        # A* with hop moves only

        pass

    # Calculate chebyshev distance (omnidirectional) from initial to final (tuple)
    def calc_chebyshev(self, initial, final):
        return max(abs(final[0] - initial[0]), abs(final[1] - initial[1]))
    
    # Get hop list (multiple hop)
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
                    if (board[x1][y1] // 100 == player) and (board[x2][y2] == 0):
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
    
    def get_all_loncat(self, node):
        pieces = node.get_board_pieces(node.get_turn())
        board = node.get_current()

        for piece in pieces:
            hop_list = [h[1:] for h in self.get_loncat_multi(board, piece, node.get_turn())]
            print('\n[----- hop list -----]',piece,' -> ',*hop_list, sep='\n')

    
    # Index valid
    def valid(self, pos):
        return ((0 <= pos[0] < 10) and (0 <= pos[1] < 10))
    
    def get_all_geser(self, node):
        geser = []
        for initial in node.get_board_pieces(node.get_turn()):
            for move in self.move_dir[node.get_turn()]:
                x2 = initial[0] + move[0]
                y2 = initial[1] + move[1]
                
                if not self.valid((x2,y2)) or node.get_current()[move[0]][move[1]] != 0:
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
        

                
# Class driver
if __name__ == '__main__':
    p = HalmaPlayer02('Bob')

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
    
    N = HalmaStateNode(0,2,None,board,None)
    
    #print(*p.get_loncat_multi(board, (6,8), 2), sep='\n')
    print(p.get_all_loncat(N))


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