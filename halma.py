''' 
Halma GUI (Using halma_model script)

To do improvement:
    - Continuous timer (while AI computing moves)
    - Human player
    - Debug/Strategy mode

To do:
    - Animate move
    - 4 player color picker (multiple click)
    - Pause button (stop timer tick)
    - Button create from text
    - Dictionary asset import
    - Move history line
    - Decompose script to module halma_display
    - Remove 8x8 support?
    - Verbose / quiet parameter
    - Reset function redefinition
    - Offset font size with Font.size()
    - Analytics (avg time, move arrow)
    - Resolution (scaling?)
    - PyPi package

To do test:
    - Font size

'''

# Module import
import pygame
import pygame.gfxdraw
import time
import math
import os
import sys

from halma_game.halma_model import HalmaModel
from halma_game.halma_player import HalmaPlayer
from halma_game.halma_player_01_A import HalmaPlayer01A
from halma_game.halma_player_01_B import HalmaPlayer01B
from halma_game.halma_player_02_A import HalmaPlayer02A
from halma_game.halma_player_02_B import HalmaPlayer02B
from halma_game.halma_player_03_A import HalmaPlayer03A
from halma_game.halma_player_03_B import HalmaPlayer03B
from halma_game.halma_player_04_A import HalmaPlayer04A
from halma_game.halma_player_04_B import HalmaPlayer04B
from halma_game.halma_player_human import HalmaPlayerHuman


# Pygame initialization
pygame.init()
screen = pygame.display.set_mode((1280,720))    # Resolution set
pygame.display.set_caption('Halma (Beta) v0.3.6')


# Color Definition
colors = {
    'BLACK':        (0,0,0),
    'WHITE':        (255,255,255),
    'BG':           (236,243,244),
    'BG_DARK':      (10,31,34),
    'TEXT':         (40,76,81),
    'TEXT_DARK':    (236,243,244),
    'BLUE':         (69,165,229),
    'CYAN':         (116,254,220),
    'GREEN':        (87,184,77),
    'ORANGE':       (243,156,18),
    'PINK':         (253,153,204),
    'PURPLE':       (155,89,182),
    'RED':          (240,111,82),
    'YELLOW':       (241,196,15)
}
colors_enum = list(enumerate(colors))


# Assets Import
path = os.path.dirname(__file__)
pygame.display.set_icon(pygame.image.load('halma_game/assets/gui/icon.png'))
title = {
    'light'             : pygame.image.load('halma_game/assets/gui/title.png'),
    'dark'              : pygame.image.load('halma_game/assets/gui/title_dark.png')
}
info_text = {
    'turn'              : pygame.image.load('halma_game/assets/info/info_turn.png'),
    'score'             : pygame.image.load('halma_game/assets/info/info_score.png'),
    'time-left'         : pygame.image.load('halma_game/assets/info/info_timeleft.png'),
    'last-move'         : pygame.image.load('halma_game/assets/info/info_lastmove.png')
}
info_player = {
    'p1'                : pygame.image.load('halma_game/assets/info/info_p1.png'),
    'p2'                : pygame.image.load('halma_game/assets/info/info_p2.png')
}
button = {                   
    'start'             : pygame.image.load('halma_game/assets/button/button_start.png'),
    'start-active'      : pygame.image.load('halma_game/assets/button/button_start_active.png'),
    'reset'             : pygame.image.load('halma_game/assets/button/button_reset.png'),
    'reset-active'      : pygame.image.load('halma_game/assets/button/button_reset_active.png'),
    'pause'             : pygame.image.load('halma_game/assets/button/button_pause.png'),
    'pause-active'      : pygame.image.load('halma_game/assets/button/button_pause_active.png'),
    '8x8'               : pygame.image.load('halma_game/assets/button/button_8x8.png'),
    '8x8-active'        : pygame.image.load('halma_game/assets/button/button_8x8_active.png'),
    '10x10'             : pygame.image.load('halma_game/assets/button/button_10x10.png'),
    '10x10-active'      : pygame.image.load('halma_game/assets/button/button_10x10_active.png'),
    '2p'                : pygame.image.load('halma_game/assets/button/button_2p.png'),
    '2p-active'         : pygame.image.load('halma_game/assets/button/button_2p_active.png'),
    '4p'                : pygame.image.load('halma_game/assets/button/button_4p.png'),
    '4p-active'         : pygame.image.load('halma_game/assets/button/button_4p_active.png'),
    'dark'              : pygame.image.load('halma_game/assets/button/button_dark.png'),
    'dark-active'       : pygame.image.load('halma_game/assets/button/button_dark_active.png')
}
button_player = {
    '01'                : pygame.image.load('halma_game/assets/button/button_01.png'),
    '01-active'         : pygame.image.load('halma_game/assets/button/button_01_active.png'),
    '02'                : pygame.image.load('halma_game/assets/button/button_02.png'),
    '02-active'         : pygame.image.load('halma_game/assets/button/button_02_active.png'),
    '03'                : pygame.image.load('halma_game/assets/button/button_03.png'),
    '03-active'         : pygame.image.load('halma_game/assets/button/button_03_active.png'),
    '04'                : pygame.image.load('halma_game/assets/button/button_04.png'),
    '04-active'         : pygame.image.load('halma_game/assets/button/button_04_active.png'),
    'Human'             : pygame.image.load('halma_game/assets/button/button_human.png'),
    'Human-active'      : pygame.image.load('halma_game/assets/button/button_human_active.png')
}
board_8 = {
    'not-numbered-light': pygame.image.load('halma_game/assets/board/board_8.png'),
    'not-numbered-dark' : pygame.image.load('halma_game/assets/board/board_8_dark.png'),
    'numbered-light'    : pygame.image.load('halma_game/assets/board/board_8_numbered.png'),
    'numbered-dark'     : pygame.image.load('halma_game/assets/board/board_8_numbered_dark.png')
}
board_10 = {
    'not-numbered-light': pygame.image.load('halma_game/assets/board/board_10.png'),
    'not-numbered-dark' : pygame.image.load('halma_game/assets/board/board_10_dark.png'),
    'numbered-light'    : pygame.image.load('halma_game/assets/board/board_10_numbered.png'),
    'numbered-dark'     : pygame.image.load('halma_game/assets/board/board_10_numbered_dark.png')
}
piece_8 = {
    'blue'              : pygame.image.load('halma_game/assets/pieces/8x8_blue.png'),
    'cyan'              : pygame.image.load('halma_game/assets/pieces/8x8_cyan.png'),
    'green'             : pygame.image.load('halma_game/assets/pieces/8x8_green.png'),
    'orange'            : pygame.image.load('halma_game/assets/pieces/8x8_orange.png'),
    'pink'              : pygame.image.load('halma_game/assets/pieces/8x8_pink.png'),
    'purple'            : pygame.image.load('halma_game/assets/pieces/8x8_purple.png'),
    'red'               : pygame.image.load('halma_game/assets/pieces/8x8_red.png'),
    'yellow'            : pygame.image.load('halma_game/assets/pieces/8x8_yellow.png')
}
piece_10 = {
    'blue'              : pygame.image.load('halma_game/assets/pieces/10x10_blue.png'),
    'cyan'              : pygame.image.load('halma_game/assets/pieces/10x10_cyan.png'),
    'green'             : pygame.image.load('halma_game/assets/pieces/10x10_green.png'),
    'orange'            : pygame.image.load('halma_game/assets/pieces/10x10_orange.png'),
    'pink'              : pygame.image.load('halma_game/assets/pieces/10x10_pink.png'),
    'purple'            : pygame.image.load('halma_game/assets/pieces/10x10_purple.png'),
    'red'               : pygame.image.load('halma_game/assets/pieces/10x10_red.png'),
    'yellow'            : pygame.image.load('halma_game/assets/pieces/10x10_yellow.png')
}
piece_hover = {
    '8x8'               : pygame.image.load('halma_game/assets/pieces/8x8_hover.png'),
    '10x10'             : pygame.image.load('halma_game/assets/pieces/10x10_hover.png')
}
color_picker = {
    'blue'              : pygame.image.load('halma_game/assets/pieces/cp_blue.png'),
    'cyan'              : pygame.image.load('halma_game/assets/pieces/cp_cyan.png'),
    'green'             : pygame.image.load('halma_game/assets/pieces/cp_green.png'),
    'orange'            : pygame.image.load('halma_game/assets/pieces/cp_orange.png'),
    'pink'              : pygame.image.load('halma_game/assets/pieces/cp_pink.png'),
    'purple'            : pygame.image.load('halma_game/assets/pieces/cp_purple.png'),
    'red'               : pygame.image.load('halma_game/assets/pieces/cp_red.png'),
    'yellow'            : pygame.image.load('halma_game/assets/pieces/cp_yellow.png')
}
cp_selected            =  pygame.image.load('halma_game/assets/pieces/cpselected.png')


# Assets enumeration
bp_enum = list(enumerate(button_player))
p8_enum = list(enumerate(piece_8))
p10_enum = list(enumerate(piece_10))
cp_enum = list(enumerate(color_picker))


# Font definition
font_time              =  pygame.font.Font('halma_game/assets/fonts/coolvetica.ttf', 100)
font_time_stack        =  pygame.font.Font('halma_game/assets/fonts/coolvetica.ttf', 40)
font_player_name       =  pygame.font.Font('halma_game/assets/fonts/coolvetica.ttf', 80)
font_fps               =  pygame.font.Font('halma_game/assets/fonts/coolvetica.ttf', 18)
font_move_history      =  pygame.font.Font('halma_game/assets/fonts/coolvetica.ttf', 30)
font_piece             =  pygame.font.Font('halma_game/assets/fonts/coolvetica.ttf', 30)
font_score             =  pygame.font.Font('halma_game/assets/fonts/coolvetica.ttf', 85)
font_warning           =  pygame.font.Font('halma_game/assets/fonts/coolvetica.ttf', 30)


# Team AI initialization
p01     = [HalmaPlayer01A('AI 01-A'), HalmaPlayer01B('AI 01-B'), HalmaPlayer01A('AI 01-C'), HalmaPlayer01B('AI 01-D')]
p02     = [HalmaPlayer02A('AI 02-A'), HalmaPlayer02B('AI 02-B'), HalmaPlayer02A('AI 02-C'), HalmaPlayer02B('AI 02-D')]
p03     = [HalmaPlayer03A('AI 03-A'), HalmaPlayer03B('AI 03-B'), HalmaPlayer03A('AI 03-C'), HalmaPlayer03B('AI 03-D')]
p04     = [HalmaPlayer04A('AI 04-A'), HalmaPlayer04B('AI 04-B'), HalmaPlayer04A('AI 04-C'), HalmaPlayer04B('AI 04-D')]
pHuman  = [HalmaPlayerHuman('Human A'), HalmaPlayerHuman('Human B'), HalmaPlayerHuman('Human C'), HalmaPlayerHuman('Human D')]
p01[0].setTeman(p01[1])
p02[0].setTeman(p02[1])
p03[0].setTeman(p03[1])
p04[0].setTeman(p04[1])


# GUI Class
class gui:
    # GUI Assets
    screen = 0
    clock = 0
    p_8  = [0,[0],[0]]
    p_10 = [0,[0],[0]]
    dark_mode = False
    color_text = colors['TEXT']

    # Game variable
    finish = False
    winner = 0
    p1_initial = 0
    p2_initial = 0
    xi = 0
    model = 0
    running = False
    n_board = 0
    n_player = 0
    timer_time = 0
    timer_stack = 0
    move_count = 0
    move_timer = 0
    move_history = []
    move_line = [0,[],[],[],[]]
    click_start = False
    click_reset = False
    click_pause = False
    click_prev = False
    click_pmove = False
    click_human = None
    click_mode = 'piece'
    prev_pause = False
    starting = True
    shift_i = 0
    p1_selected = 0
    p2_selected = 0
    score = [0,0]
    color_click = [0,False,False]
    color_picked = [0,0,0,0,0]
    times_up = False


    # Initialization
    def __init__(self, n_board, p1, p2):
        '''
        GUI initialization with n_board size with player object array p1 and p2

        Executing halma_model initialization

        Parameter:
        - n_board : size of board
        - p1,p2 : player object array (for 2 player used first object only)
        '''

        # Player parameter initialization
        self.n_player = 2
        
        self.p1_initial = [p1[0], p1[1]]
        self.p2_initial = [p2[0], p2[1]]
        self.p1_selected = 4
        self.p2_selected = 'Human'
        self.color_picked = [0, 6, 2, 3, 0]     # Default: p1: [red,orange], p2: [green,blue]

        # Board parameter initialization
        self.n_board = n_board
        if self.n_board == 8:
            self.d = 75
            self.x0 = 623
            self.y0 = 63
        elif self.n_board == 10:
            self.d = 60
            self.x0 = 623
            self.y0 = 63
        
        # Game state
        self.starting = True
        self.running = False
        self.score = [0,0]

        # Game model
        self.model = HalmaModel()
        self.modelState = self.model.S_OK      # Running state
        self.model.awal(p1[0], p2[0])

        # Timer initialization
        self.clock = pygame.time.Clock()


    def reinit_model(self,p1,p2):
        ''' Player reinitialization with player object array p1,p2. Player number and board size can't be changed '''

        self.p1_initial = p1
        self.p2_initial = p2
        self.model = HalmaModel()
        self.modelState = self.model.S_OK      # Running state
        
        # Player selection are not same
        if self.p1_selected != self.p2_selected:
            if self.n_player == 2:
                self.model.awal(p1[0],p2[0])
            else:
                self.model.awal(p1[0],p2[0],p1[1],p2[1])
        
        # Player selection are same
        else:
            if self.n_player == 2:
                self.model.awal(p1[0],p1[2])
            else:
                self.model.awal(p1[0],p1[2],p1[1],p1[3])


    def load_template(self, numbered=None):
        ''' 
        Load game GUI template
        
        Parameter
        - Numbered (optional) (boolean): numbered board

        Included
        - Background color with colors['BG'] and ['BG_DARK']
        - Title in title variable (index 0 for light, 1 for dark)
        - Board with number or not (default numbered)
        - Start, reset, and pause button (inactive)
        - 8x8 and 10x10 button (active for selected) - Starting screen
        - Dark mode button (active for dark mode on) - Starting screen
        - Player count button (active for selected) - Starting screen
        - Player select button for p1 and p2 (active for selected) - Starting screen
            - 1-4 : AI number 1-4 (file number with suffix A/B in one team)
            - Human : Human player
        - Color picker for p1 and p2 (active for selected) - Starting screen
        - Player, score, time left, and last move info text - Playing screen
        '''

        # Background color and title
        if self.dark_mode:
            screen.fill(colors['BG_DARK'])
            screen.blit(title['dark'], dest=(35,25))
        else:
            screen.fill(colors['BG'])
            screen.blit(title['light'], dest=(35,25))
        
        # Numbered board as default
        if numbered == None:
            numbered = True

        # Board rendering
        if self.dark_mode:
            if self.n_board == 8:
                if numbered:
                    screen.blit(board_8['numbered-dark'], dest=(582,21))
                else:
                    screen.blit(board_8['not-numbered-dark'], dest=(610,50))
            elif self.n_board == 10:
                if numbered:
                    screen.blit(board_10['numbered-dark'], dest=(582,21))
                else:
                    screen.blit(board_10['not-numbered-dark'], dest=(610,50))
        else:
            if self.n_board == 8:
                if numbered:
                    screen.blit(board_8['numbered-light'], dest=(582,21))
                else:
                    screen.blit(board_8['not-numbered-light'], dest=(610,50))
            elif self.n_board == 10:
                if numbered:
                    screen.blit(board_10['numbered-light'], dest=(582,21))
                else:
                    screen.blit(board_10['not-numbered-light'], dest=(610,50))

        # Start, reset, and pause button
        screen.blit(button['start'], dest=(35,120))
        screen.blit(button['reset'], dest=(190,120))
        screen.blit(button['pause'], dest=(345,120))

        # Show on starting screen
        if self.starting:
            # 8x8 and 10x10 button
            screen.blit(button['8x8'], dest=(35,230))
            screen.blit(button['10x10'], dest=(140,230))
            
            # Dark mode button
            if self.dark_mode:
                screen.blit(button['dark-active'], dest=(35,310))
                self.color_text = colors['TEXT_DARK']
            else:
                screen.blit(button['dark'], dest=(35,310))
                self.color_text = colors['TEXT']

            # Player count button
            screen.blit(button['2p'], dest=(280,230))
            screen.blit(button['4p'], dest=(360,230))

            # AI player select button
            screen.blit(info_player['p1'], dest=(35,450))
            screen.blit(info_player['p2'], dest=(35,570))
            for i in range(0,5):
                screen.blit(button_player[bp_enum[2*i][1]], dest=(110 + i*80,445))
                screen.blit(button_player[bp_enum[2*i][1]], dest=(110 + i*80,565))

            # Color picker
            for i in range(0,8):
                screen.blit(color_picker[cp_enum[i][1]], dest=(110 + i*44,500))
                screen.blit(color_picker[cp_enum[i][1]], dest=(110 + i*44,620))
        

        # Show on playing state
        else:
            # Playing info
            screen.blit(info_text['turn'], dest=(35,200))  # Player
            screen.blit(info_text['score'], dest=(35,285))  # Score
            screen.blit(info_text['time-left'], dest=(35,365))  # Clock
            screen.blit(info_text['last-move'], dest=(35,460))  # Last Move


    def load_pieces(self, board):
        ''' Load all pieces with corresponding player color and piece id from board (2d array of board pieces coordinate) '''

        # Array traversal
        for i in range(0,self.n_board):
            for j in range(0,self.n_board):
                # Get piece number from board and parse to player_id and piece_id
                piece = board[i][j]
                player_id = piece // 100
                piece_id = piece - (player_id * 100)
                
                # Not empty block
                if piece_id != 0:
                    self.draw_piece(str(piece_id), self.color_picked[player_id], i, j)


    def draw_piece(self, text, color, i, j, opacity=None):
        ''' 
        Draw custom text and color board piece into board coordinate i,j 
        
        Parameter:
        - text (string): text to be displayed (centered with manual offset)
        - color (int): enumeration of piece color (or colors_enum-6)
            - 0(blue), 1(cyan), 2(green), 3(orange), 4(pink), 5(purple), 6(red), 7(yellow)
        - i,j: coordinate to draw (in board index i(row), j(column))
        - opacity (optional) (default=full): opacity in range 0-100 -> converted to alpha 0-255 (truncated)
        '''

        # Create text object
        textSurface = font_piece.render(text, True, (colors['WHITE']))
        textRect = textSurface.get_rect()

        # Copy board piece object
        if self.n_board == 10:
            piece = piece_10[p10_enum[color][1]].copy()
        elif self.n_board == 8:
            piece = piece_8[p8_enum[color][1]].copy()

        # Transparent
        if opacity != None:
            alpha = max(min((255 / 100) * opacity, 255),0)  # Ensure alpha value between 0-255
            piece.fill((255,255,255,alpha), None, pygame.BLEND_RGBA_MULT)

        # Draw piece to screen
        if self.n_board == 10:
            screen.blit(piece, dest=(self.x0 + j*self.d, self.y0 + i*self.d))
            textRect.center = (self.x0 + j*self.d + 27, self.y0 + i*self.d + 25)

        # Draw text to screen
        screen.blit(textSurface, textRect)

    
    def animate_move(self, initial, final):
        '''
        Animate move for smooth transition from initial to final
        '''
        pass
    

    def update_hover(self):
        ''' 
        Hover indicator for board object (piece or empty space) - currently 10x10 supported
        Blit piece_hover to hovered valid position
        
        Return: 
            - Clicked in valid position: tuple (row,column)
            - Not clicked or clicked in invalid position: None

        Mode (class variable click_mode):
        - 'piece': hover over current-player turn board-pieces 
            (references model.getBidak(row,col) and model.getGiliran())
            - left mouse button click: returning piece position (row,column)
        - 'target': hover over possible move from initial position (class variable click_human)
            (references model.bolehGeser(), model.bolehLoncat())
            - left mouse button click: returning piece position (row,column)
        '''

        # Get mouse coordinate
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.click_mode == 'piece':
            if self.n_board == 10:
                for i in range(10):
                    for j in range(10):
                        if (self.in_region(mouse, (self.x0) + j*self.d, (self.y0) + i*self.d, self.d - 1, self.d - 1) 
                                            and (self.model.getBidak(i,j) // 100 == self.model.getGiliran() + 1)):
                            if click[0] and not self.click_pmove:
                                # print('[click]',i,j)
                                self.click_pmove = True
                                #self.click_human = (i,j)
                                return (i,j)
                            elif not click[0]:
                                self.click_pmove = False
                            screen.blit(piece_hover['10x10'], dest=(self.x0 + j*self.d - 4, self.y0 + i*self.d - 4))
        
        elif self.click_mode == 'target':
            if self.n_board == 10:
                for i in range(10):
                    for j in range(10):
                        if (self.in_region(mouse, (self.x0) + j*self.d, (self.y0) + i*self.d, self.d - 1, self.d - 1) 
                                            and ((i,j) in [m[-2] for m in self.model.get_all_moves(self.model.getGiliran() + 1) if m[0] == self.click_human]
                                            or self.model.getBidak(i,j) // 100 == self.model.getGiliran() + 1)):
                            if click[0] and not self.click_pmove:
                                # print('[click]',i,j)
                                self.click_pmove = True
                                return (i,j)
                            elif not click[0]:
                                self.click_pmove = False
                            screen.blit(piece_hover['10x10'], dest=(self.x0 + j*self.d - 4, self.y0 + i*self.d - 4))


    def update_possible_moves(self, p):
        '''
        Display all possible moves (intended for human playaer) with faded (60% opacity) in empty board spaces

        Parameter:
        - p: player id
        '''

        moves = []
        board = self.model.getPapan()

        # Filter duplicate final position
        for move in self.model.get_all_moves(p):
            if move[-2] not in [m[-1] for m in moves]:
                if self.click_human != None:
                    if move[0] == self.click_human:
                        moves.append(move[0:-1])
                else:
                    moves.append(move[0:-1])

        
        displayed = []
        # Display moves 
        for move in moves:
            piece_id = board[move[0][0]][move[0][1]] % 100

            for m in move:
                if m not in displayed:
                    self.draw_piece('', self.color_picked[p], m[0], m[1], 40)
                    displayed.append(m)

    
    def draw_line(self, initial, final, thick, p):
        '''
        Draw anti-aliased line from initial to final(list) with thickness thick and player id p
        
        Parameter:
        - initial (tuple): initial position
        - final (tuple): final position (can be multiple final position as 1 continuous line)
        - thick (int): thickness of line (in pixel)
        - p (int): player id (1-4)
        '''
        init = (650 + 60 * initial[1], 90 + 60 * initial[0])

        for f_idx in final:
            f = (650 + 60 * f_idx[1], 90 + 60 * f_idx[0])
            center_L = ((init[0] + f[0]) / 2, (init[1] + f[1]) / 2)
            length = math.sqrt((abs(f[0] - init[0]) ** 2) + (abs(f[1] - init[1]) ** 2))
            thickness = thick
            angle = math.atan2(init[1] - f[1], init[0] - f[0])

            UL = (center_L[0] + (length / 2.) * math.cos(angle) - (thickness / 2.) * math.sin(angle),
                center_L[1] + (thickness / 2.) * math.cos(angle) + (length / 2.) * math.sin(angle))
            UR = (center_L[0] - (length / 2.) * math.cos(angle) - (thickness / 2.) * math.sin(angle),
                center_L[1] + (thickness / 2.) * math.cos(angle) - (length / 2.) * math.sin(angle))
            BL = (center_L[0] + (length / 2.) * math.cos(angle) + (thickness / 2.) * math.sin(angle),
                center_L[1] - (thickness / 2.) * math.cos(angle) + (length / 2.) * math.sin(angle))
            BR = (center_L[0] - (length / 2.) * math.cos(angle) + (thickness / 2.) * math.sin(angle),
                center_L[1] - (thickness / 2.) * math.cos(angle) - (length / 2.) * math.sin(angle))

            pygame.gfxdraw.aapolygon(screen, (UL, UR, BR, BL), self.get_color(self.color_picked[p] + 6))
            pygame.gfxdraw.filled_polygon(screen, (UL, UR, BR, BL), self.get_color(self.color_picked[p] + 6))

            init = f


    def update_move_line(self):
        '''
        Draw move line of player pieces from class variable move_line (calls draw_line)

        move_line[p][m][pos]
        - p: player id (1-4)
        - m: move id (number of pieces have moved in last n number of moves)
        - pos: position (row,col) for move line
            - 0: initial position
            - 1-..: final position (or hop list)
        '''

        for p in range(1,5):
            for m in range(0,len(self.move_line[p])):
                init = self.move_line[p][m][0]
                final = self.move_line[p][m][1:]
                self.draw_line(init, final, 10, p)

    
    def get_color(self, i):
        ''' Get colors RGB value from colors enumeration (0 - n) '''

        return colors[colors_enum[i][1]]


    def start_animation(self):
        ''' Starting animation "PRESS START TO PLAY" with changing piece color picked by player 1 and 2 '''

        # Starting animation index
        self.xi = (self.xi + 1) % 100
        x = self.xi // 50

        # Background color
        for i in range(0,self.n_board):
            for j in range(0,self.n_board):
                self.draw_piece("",self.color_picked[2-x],i,j)
        
        # 10x10 board
        if self.n_board == 10:
            z = 0
        elif self.n_board == 8:
            z = 1

        # 'PRESS START TO PLAY' text
        self.draw_piece('P',self.color_picked[1+x], 1, 2-z)
        self.draw_piece('R',self.color_picked[1+x], 1, 3-z)
        self.draw_piece('E',self.color_picked[1+x], 1, 4-z)
        self.draw_piece('S',self.color_picked[1+x], 1, 5-z)
        self.draw_piece('S',self.color_picked[1+x], 1, 6-z)
        
        self.draw_piece('S',self.color_picked[1+x], 3, 3-z)
        self.draw_piece('T',self.color_picked[1+x], 3, 4-z)
        self.draw_piece('A',self.color_picked[1+x], 3, 5-z)
        self.draw_piece('R',self.color_picked[1+x], 3, 6-z)
        self.draw_piece('T',self.color_picked[1+x], 3, 7-z)
        
        self.draw_piece('T',self.color_picked[1+x], 5-z, 2-z)
        self.draw_piece('O',self.color_picked[1+x], 5-z, 3-z)
        
        self.draw_piece('P',self.color_picked[1+x], 7-z, 3-z)
        self.draw_piece('L',self.color_picked[1+x], 7-z, 4-z)
        self.draw_piece('A',self.color_picked[1+x], 7-z, 5-z)
        self.draw_piece('Y',self.color_picked[1+x], 7-z, 6-z)


    def reset_timer(self):
        ''' Set timer_time to initial value '''

        self.timer_time = 20000     # in millisecond
        self.clock.get_rawtime()


    def tick_timer(self):
        ''' Substract timer with elapsed time '''
        
        self.clock.tick_busy_loop(60)   # Framerate cap
        self.timer_time -= self.clock.get_rawtime()
        self.move_timer -= self.clock.get_rawtime()


    def get_timer(self):
        ''' Get timer from model calculation '''
        time_left = self.model.JATAH_WAKTU - (self.model.getJatahWaktu(self.model.getGiliran()) - self.model.getSisaWaktu())
        if time_left > 0:
            return time_left
        else:
            return 0
    

    def update_timer(self):
        ''' Update time left on screen '''

        screen.blit(font_time.render('{:.2f}'.format(self.get_timer()), True, self.color_text), dest=(210,340))
    

    def update_timer_stack(self):
        ''' Update accumulative reserved time for specific player turn on screen '''

        p = self.model.getGiliran()
        stack = self.model.getJatahWaktu(p)
        time_left = self.model.JATAH_WAKTU - (self.model.getJatahWaktu(self.model.getGiliran()) - self.model.getSisaWaktu())
        if time_left <= 0:
            stack -= (0 - time_left)
        
        if stack < 0:
            self.times_up = p + 1
            self.winner = 2 - p
            screen.blit(font_time_stack.render('(TIMES UP!)', True, self.get_color(self.color_picked[p+1] + 6)), dest=(420,355))
        else:
            screen.blit(font_time_stack.render('({:.2f})'.format(stack), True, self.get_color(self.color_picked[p+1] + 6)), dest=(420,355))


    def update_move_count(self):
        ''' Display move count (all player combined) '''
        
        screen.blit(font_fps.render('Move: {}'.format(self.move_count), True, self.color_text), dest=(1100,685))


    def update_fps(self):
        ''' Display FPS by 10 pygame timer tick average '''
        
        screen.blit(font_fps.render('FPS: {:.1f}'.format(self.clock.get_fps()), True, self.color_text), dest=(1180,685))


    def update_player(self):
        ''' Display player name with corresponding player color picked '''
        p = self.model.getGiliran()
        player = self.model.getPemain(p)
        screen.blit(font_player_name.render(player.nama, True, self.get_color(self.color_picked[p+1] + 6)), dest=(210,175))


    def update_score(self):
        ''' Player score display from class attribute score[0:2] '''

        screen.blit(font_score.render('{} - {}'.format(self.score[0], self.score[1]), True, self.color_text), dest=(210,260))


    def update_history(self):
        ''' 
        Display move history with n = 4 from attribute move_history, blit to screen
        
        move_history[hist_no][i]
            (0) turn index,
            (1) initial position,
            (2) final position (list of final position),
            (3) move action (0,1,2) - geser,loncat,berhenti,
            (4) move execution time
        '''

        n = 4   # History size
        move_hist = self.move_history.copy()
        move_hist.reverse()

        for i in range(0,len(move_hist)):
            name = self.model.getPemain(move_hist[i][0]).nama
            if move_hist[i][3] == self.model.A_GESER:
                move_type = 'GESER'
            elif move_hist[i][3] == self.model.A_LONCAT:
                move_type = 'LONCAT'
            elif move_hist[i][3] == self.model.A_BERHENTI:
                move_type = 'BERHENTI'

            # Player 1 move
            screen.blit(font_move_history.render('{} | {} {} -> {} ({:.2f}s)'.format(name, move_type, move_hist[i][1], move_hist[i][2], move_hist[i][4]),1,
                                (self.get_color(self.color_picked[move_hist[i][0] + 1] + 6))), dest=(35, 510 + i*40))


    def show_winner(self,p):
        ''' Show winner text '{team name} WIN!' after each round '''

        screen.blit(font_warning.render(self.get_object(p)[0].nama[:-2] + ' WIN!', True, self.color_text), dest=(650,670))


    def get_object(self, p):
        ''' 
        Get object with object id 
        
        Values:
            AI : 1-4 (team number)
            Human : 'Human' 
        '''

        if p == 1:
            return p01
        elif p == 2:
            return p02
        elif p == 3:
            return p03
        elif p == 4:
            return p04
        elif p == 'Human':
            return pHuman


    def in_region(self, a, x0, y0, dx, dy):       
        ''' Check position a (tuple x,y) in region box with boundary x0 and y0 (left and upper) with size of dx and dy '''

        return (x0 <= a[0] <= x0 + dx) and (y0 <= a[1] <= y0 + dy)


    def in_region_circle(self, a, x0, y0, d):
        ''' Check position a (tuple x,y) in region box with boundary x0 and y0 (left and upper) with circle diameter d '''

        cx = x0 + d/2
        cy = y0 + d/2
        dist = math.sqrt((abs(a[0] - cx)) ** 2 + (abs(a[1] - cy)) ** 2)
        return dist <= d/2


    def update_button(self):
        '''
        Button hover and click with mouse check, change to active based on state or click
        
        Include:
        - Start, reset, pause button
        - 8x8, 10x10 button
        - 2P, 4P button
        - Dark mode button
        - AI picker (1-4) and Human
        - Color picker
        '''

        # Get mouse coordinate and click
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # Start button
        if self.in_region(mouse,35,120,126,44):
            screen.blit(button['start-active'], dest=(35,120))
            if click[0] == 1:
                # print('[click start]')
                self.action_start()

        # Reset button
        if self.in_region(mouse,190,120,126,44):
            screen.blit(button['reset-active'], dest=(190,120))
            if click[0] == 1:
                # print('[click reset]')
                self.action_reset()

        # Pause button
        if self.in_region(mouse,345,120,126,44):
            screen.blit(button['pause-active'], dest=(345,120))
            if click[0] and not self.click_prev:
                # print('[click pause]')
                self.click_prev = True
                self.action_pause()
            elif not click[0]:
                self.click_prev = False

        # Display in starting mode
        if self.starting:
            # 8x8 button
            if (self.in_region(mouse,35,230,92,50) or self.n_board == 8):
                screen.blit(button['8x8-active'], dest=(35,230))
                if click[0] == 1 and self.in_region(mouse,35,230,92,50):
                    self.n_board = 8
                    self.d = 75
                    self.x0 = 626
                    self.y0 = 66

            # 10x10 button
            if (self.in_region(mouse,140,230,104,50) or self.n_board == 10):
                screen.blit(button['10x10-active'], dest=(140,230))
                if click[0] == 1 and self.in_region(mouse,140,230,104,50):
                    self.n_board = 10
                    self.d = 60
                    self.x0 = 623
                    self.y0 = 63

            # 2P button
            if (self.in_region(mouse,280,230,67,50) or self.n_player == 2):
                screen.blit(button['2p-active'], dest=(280,230))
                if click[0] == 1 and self.in_region(mouse,280,230,67,50):
                    self.n_player = 2
            
            # 4P button
            if (self.in_region(mouse,360,230,67,50) or self.n_player == 4):
                screen.blit(button['4p-active'], dest=(360,230))
                if click[0] == 1 and self.in_region(mouse,360,230,67,50):
                    self.n_player = 4

            # Dark mode button
            if (self.in_region(mouse,35,310,208,50) or self.dark_mode == True):
                screen.blit(button['dark-active'], dest=(35,310))
                if click[0] == 1 and self.in_region(mouse,35,310,208,50):
                    self.dark_mode = not self.dark_mode
                    time.sleep(0.2)
            
            # AI picker
            for i in range(1,4):
                # Row 1 (AI)
                if self.in_region(mouse,110 + 80*i,445,69,50) or self.p1_selected == (i + 1):
                    screen.blit(button_player[bp_enum[(i * 2) + 1][1]], dest=(110 + 80*i,445))
                    if click[0] == 1 and self.in_region(mouse,110 + 80*i,445,69,50) and self.p1_selected != (i + 1):
                        # print('[{}-{} selected as p1]'.format(self.get_object(i+1)[0].nama, self.get_object(i+1)[1].nama))
                        self.p1_selected = i + 1
                
                # Row 1 (Human)
                if self.in_region(mouse,430,445,137,50) or self.p1_selected == 'Human':
                    screen.blit(button_player['Human-active'], dest=(430,445))
                    if click[0] == 1 and self.in_region(mouse,430,445,137,50) and self.p1_selected != 'Human':
                        # print('[Human is selected as p1]')
                        self.p1_selected = 'Human'

                # Row 2
                if self.in_region(mouse,110 + 80*i,565,69,50) or self.p2_selected == (i + 1):
                    screen.blit(button_player[bp_enum[(i * 2) + 1][1]], dest=(110 + 80*i,565))
                    if click[0] == 1 and self.in_region(mouse,110 + 80*i,565,69,50) and self.p2_selected != (i + 1):
                        # print('[{}-{} selected as p2]'.format(self.get_object(i+1)[0].nama, self.get_object(i+1)[1].nama))
                        self.p2_selected = i + 1

                # Row 2 (Human)
                if self.in_region(mouse,430,565,137,50) or self.p2_selected == 'Human':
                    screen.blit(button_player['Human-active'], dest=(430,565))
                    if click[0] == 1 and self.in_region(mouse,430,565,137,50) and self.p2_selected != 'Human':
                        # print('[Human is selected as p2]')
                        self.p2_selected = 'Human'

            # Color picker
            for i in range(0,8):
                # Player 1
                if self.in_region_circle(mouse,110 + 44*i,500,30) or i == self.color_picked[1] or i == self.color_picked[3]:
                    screen.blit(cp_selected, dest=(110 + 44*i,500))
                    if click[0] == 1 and self.in_region_circle(mouse,110 + 44*i,500,30):
                            self.color_picked[1] = i
                            self.color_picked[3] = i
                
                # Player 2
                if self.in_region_circle(mouse,110 + 44*i,620,30) or i == self.color_picked[2] or i == self.color_picked[4]:
                    screen.blit(cp_selected, dest=(110 + 44*i,620))
                    if click[0] == 1 and self.in_region_circle(mouse,110 + 44*i,620,30):
                        self.color_picked[2] = i
                        self.color_picked[4] = i
                

    def action_start(self):
        ''' Action when START button is clicked '''
        
        if self.n_board == 10:
            self.click_start = True
        else:
            screen.blit(font_warning.render('Currently only 10x10 board are supported', True, self.color_text), dest=(35,370))


    def action_reset(self):
        ''' Action when RESET button is clicked '''
        
        self.click_reset = True


    def action_pause(self):
        ''' Action when PAUSE button is clicked '''
        
        self.click_pause = not self.click_pause


    def update_screen(self):
        '''
        Update all screen and interaction element per frame
        
        Included:
        - Template (load_template)
        - Button checker
        - Move line
        - Board pieces
        - Hovering pieces (if player is Human)
        - Player, score, timer, timer stack and move history information
        - FPS and move count
        - Winner text (if round is finished)
        '''

        # Frame and loop timing
        self.clock.tick_busy_loop(60)   # Framerate cap

        # Check event
        self.check_event()

        self.load_template(numbered=True)
        self.update_button()
        self.update_fps()

        # Starting state only
        if self.starting:
            self.start_animation()
        
        # Playing state only
        elif self.running:
            #self.update_move_line()
            if self.p.getType() == 'Human':
                self.update_possible_moves(self.p.nomor)
                if self.click_human != None :
                    screen.blit(piece_hover['10x10'], dest=(self.x0 + self.click_human[1]*self.d - 4, 
                                                                self.y0 + self.click_human[0]*self.d - 4))
            self.load_pieces(self.model.getPapan())
            self.update_player()
            self.update_score()
            self.update_timer()
            self.update_timer_stack()
            self.update_move_count()
            self.update_history()
        
        # Round finished only
        if self.finish or self.times_up:
            self.show_winner(self.winner)
        
        pygame.display.update()
        

    def check_event(self):
        '''
        Pygame event checker (quit, mouse, keyboard, etc). 
        Terminate execution when quit event is triggered
        '''

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()


    def starting_screen(self):
        '''
        Starting screen GUI handler

        Start clicked: update running variable to True and starting variable to False
        Reset clicked: reinit model with selected player object

        - GUI screen, button, and event update
        '''

        self.update_screen()
        
        # Start button clicked
        if self.click_start:
            self.click_start = False

            # Change state
            self.starting = False
            self.running = True
            
            # Start game with AI selected (reinitialize model)
            self.reinit_model(self.get_object(self.p1_selected), self.get_object(self.p2_selected))
            self.p = self.model.getPemain(self.model.getGiliran())
        
        # Pause button clicked
        while self.click_pause:
            self.update_screen()

        # Reset button clicked (Pretty useless?)
        if self.click_reset:
            self.click_reset = False

            # Reinitialize halma model
            self.reinit_model(self.p1_initial, self.p2_initial)
    
    def get_player_move(self):
        '''
        Get player move (from AI and Human)
        
        Return: initial_pos(tuple), final_pos(tuple), action(int)
        
        Action: (model.A_GESER, model.A_LONCAT, model.A_BERHENTI)
        '''

        self.model.mainMulai()
        self.p = self.model.getPemain(self.model.getGiliran())
        
        # AI player
        if self.p.getType() == 'AI':
            self.update_screen()
            final_pos, initial_pos, action = self.p.main(self.model)

        # Human player
        elif self.p.getType() == 'Human':
            self.click_human = None
            initial_pos = None
            final = None
            click2 = None

            # Waiting for initial position click
            self.click_mode = 'piece'
            while initial_pos == None:
                self.tick_timer()
                self.update_screen()
                initial_pos = self.update_hover()
                pygame.display.update()
            self.click_human = initial_pos
            
            # Waiting for final position click
            self.click_mode = 'target'
            while final == None:
                self.tick_timer()
                self.update_screen()
                click2 = self.update_hover()
                if click2 != None:
                    if self.model.is_board_piece(click2):
                        initial_pos = click2
                        self.click_human = initial_pos
                    else:
                        final = click2
                pygame.display.update()

            # Determine type of action
            if (abs(final[0] - initial_pos[0]) ** 2 + abs(final[1] - initial_pos[1]) ** 2) > 2:
                final_pos = self.model.calc_path_hop(initial_pos, final)[1:]
                action = self.model.A_LONCAT
            elif (abs(final[0] - initial_pos[0]) ** 2 + abs(final[1] - initial_pos[1]) ** 2) > 0:
                final_pos = [final]
                action = self.model.A_GESER
            else:
                action = self.model.BERHENTI
            
        self.move_count += 1
        return initial_pos, final_pos, action

    
    def check_termination(self):
        '''
        Check if state is terminal condition (all board pieces of player in target zone)

        Reinitialize model and recursively calls main for next round
        '''

        # 2-Player
        if self.n_player == 2:
            if self.model.akhir() or self.times_up:
                pieces = self.model.getPosisiBidak(0)
                self.finish = True
                
                if self.times_up == 1:
                    # print('[P2 Menang!]')
                    self.show_winner(self.p2_selected)
                    self.score[1] += 1
                    self.winner = self.p2_selected
                elif self.times_up == 2:
                    # print('[P1 Menang!]')
                    self.show_winner(self.p1_selected)
                    self.score[0] += 1
                    self.winner = self.p1_selected
                else:
                    # Count pieces
                    k = 0
                    for piece in pieces:
                        if self.model.dalamTujuan(0,piece[0],piece[1]):
                            k += 1
                    if k == 15:
                        # print('[P1 Menang!]')
                        self.show_winner(self.p1_selected)
                        self.score[0] += 1
                        self.winner = self.p1_selected
                    else:
                        # print('[P2 Menang!]')
                        self.show_winner(self.p2_selected)
                        self.score[1] += 1
                        self.winner = self.p2_selected
                
                # Waiting for start button press
                self.times_up = False
                self.click_start = False
                while not self.click_start:
                    self.update_screen()

                # Reinitialize halma model (next round)
                modelState = self.model.S_OK
                self.reinit_model(self.get_object(self.p1_selected), self.get_object(self.p2_selected))
                self.starting = True
                self.main()

        # 4-Player
        elif self.n_player == 4:
            if self.model.akhirBeregu():
                pieces1 = self.model.getPosisiBidak(0)
                pieces3 = self.model.getPosisiBidak(2)
                self.finish = True
                
                # Count pieces in target zone (player 1 and 3)
                k = 0
                for piece in pieces1:
                    if self.model.dalamTujuan(0,piece[0],piece[1]):
                        k += 1
                for piece in pieces3:
                    if self.model.dalamTujuan(2,piece[0],piece[1]):
                        k += 1

                # If pieces count in player 1 and 3 is full
                if k == 20:
                    # print('[P1 Menang!]')
                    self.show_winner(self.p1_selected)
                    self.score[0] += 1
                    self.winner = self.p1_selected
                else:
                    # print('[P2 Menang!]')
                    self.show_winner(self.p2_selected)
                    self.score[1] += 1
                    self.winner = self.p2_selected
                
                self.update_screen()

                # Sleep for 20s
                time.sleep(20)

                # Reinitialize halma model (next round)
                modelState = self.model.S_OK
                self.reinit_model(self.get_object(self.p1_selected), self.get_object(self.p2_selected))
                self.starting = True
                self.main()


    def main(self):
        '''
        Main GUI loop, handling starting screen and playing screen
        '''

        # Starting condition
        self.reset_timer()
        modelState = self.model.S_OK
        

        # Starting state (title screen and game configuration)
        while self.starting:
            self.starting_screen()
        
        self.update_screen()

        # Playing state (board piece and game information)
        while self.running and modelState == self.model.S_OK:
            # Pause button clicked
            while self.click_pause:
                self.update_screen()
            
            # Frame and loop timing
            self.tick_timer()

            # Get player move (piece, target position, and action)
            initial_pos, final_pos, action = self.get_player_move()

            # Save move timer
            move_finish = self.model.getWaktu()
            time_exec = self.model.getJatahWaktu(self.model.getGiliran()) - self.model.getSisaWaktu()

            # Insert to move line
            if action != self.model.A_BERHENTI:
                p_num = self.p.nomor
                self.move_line[p_num].append([initial_pos] + final_pos)
                #self.move_line[p_num] = self.move_line[p_num][-8:] (limit)

            # Insert to move history (4 last move, latest on top)
            self.move_history.append([self.model.getGiliran(), initial_pos, final_pos, action, time_exec])
            if len(self.move_history) > 4:
                self.move_history = self.move_history[-4:]

            # Run move action
            if action == self.model.A_LONCAT:
                # print('[action: loncat] {} {} {}'.format(initial_pos, final_pos, action))
                for xy in final_pos:
                    modelState = self.model.mainLoncat(initial_pos[0], initial_pos[1], xy[0], xy[1])
                    initial_pos = xy
                    time.sleep(0.08)
                    self.update_screen()
            elif action == self.model.A_GESER:
                # print('[action: geser] {} {} {}'.format(initial_pos, final_pos, action))
                modelState = self.model.mainGeser(initial_pos[0], initial_pos[1], final_pos[0][0], final_pos[0][1])
            
            # Update screen frame on current state
            self.update_screen()

            # Check termination of round (all board pieces in target zone)
            self.check_termination()

            # Next turn
            modelState = self.model.ganti(move_finish)

            # Reset button clicked
            if self.click_reset:
                self.click_reset = False

                # Reinitialize halma model
                self.reinit_model(self.p1_initial,self.p2_initial)

                # Revert state (recursively call main method)
                self.starting = True
                self.running = False
                self.main()


# Execute if invoked directly from script
if __name__ == "__main__":
    # Initial value 10x10 with player1 is p03 and player 2 is p04 (changeable in starting screen)
    g = gui(n_board=10, p1=p04, p2=pHuman)
    g.main()
    pygame.quit()
