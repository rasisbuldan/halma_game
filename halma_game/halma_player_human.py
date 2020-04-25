# -*- coding: utf-8 -*-
"""
Modified by Group 04
"""

import random
import time
from halma_game.halma_player import HalmaPlayer
from halma_game.halma_model import HalmaModel


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


class HalmaPlayerHuman(HalmaPlayer):
    type = 'Human'

    def __init(self, nama):
        super().__init__(nama)
        

    # Calculate path from initial to final position using a-star search
    def calc_path(self, board, initial, final):
        def is_valid(pos):
            return (0 <= pos[0] < 10 and 0 <= pos[1] < 10)

        def is_board_piece(pos):
            return (board[pos[0]][pos[1]] != 0)

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
                visit.append(child)
    