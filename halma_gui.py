''' 
Halma GUI (Using halma_model script)

To do improvement:
    - Continuous timer (while AI computing moves)
    - Human player
    - Debug/Strategy mode

To do:
    - 4 player color picker (multiple click)
    - Button create from text
    - Pause game function
    - Decompose script to module halma_display
    - Remove 8x8 support?
    - Verbose / quiet parameter
    - Reset function redefinition
    - Analytics (avg time, move arrow)
    - Font import from assets file
    - PyPi package

To do test:
    - Round winner - next round

'''

# Module import
import pygame
from halma_model import HalmaModel
import time
import math
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/player')

# PLayer AI script import
from halma_player import HalmaPlayer
from halma_player_01_A import HalmaPlayer01A
from halma_player_01_B import HalmaPlayer01B
from halma_player_02_A import HalmaPlayer02A
from halma_player_02_B import HalmaPlayer02B
from halma_player_03_A import HalmaPlayer03A
from halma_player_03_B import HalmaPlayer03B
from halma_player_04_A import HalmaPlayer04A
from halma_player_04_B import HalmaPlayer04B

# Color Definition
colors = {
    'BLACK':    (0,0,0),
    'WHITE':    (255,255,255),
    'BG':       (236,243,244),
    'BG_DARK':  (10,31,34),
    'TEXT':     (40,76,81),
    'TEXT2':    (236,243,244),
    'BLUE':     (69,165,229),
    'CYAN':     (116,254,220),
    'GREEN':    (87,184,77),
    'ORANGE':   (243,156,18),
    'PINK':     (253,153,204),
    'PURPLE':   (155,89,182),
    'RED':      (240,111,82),
    'YELLOW':   (241,196,15)
}
colors_enum = list(enumerate(colors))

# Team AI initialization
p01 = [HalmaPlayer01A('Team 01-A'), HalmaPlayer01B('Team 01-B')]
p02 = [HalmaPlayer02A('Team 02-A'), HalmaPlayer02B('Team 02-B')]
p03 = [HalmaPlayer03A('Team 03-A'), HalmaPlayer03B('Team 03-B')]
p04 = [HalmaPlayer04A('Team 04-A'), HalmaPlayer04B('Team 04-B')]
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

    # Game variable
    p1_initial = 0
    p2_initial = 0
    xi = 0
    model = 0
    runningState = False
    n_board = 0
    n_player = 0
    timer_time = 0
    timer_stack = 0
    move_count = 0
    move_timer = 0
    move_history = []
    click_start = False
    click_reset = False
    click_pause = False
    click_prev1 = False
    click_prev2 = False
    prev_pause = False
    starting = True
    shift_i = 0
    p1_selected = 0
    p2_selected = 0
    score = [0,0]
    color_click = [0,False,False]
    color_picked = [0,0,0,0,0]

    # Font and object variable
    font_time = 0
    font_fps = 0

    # Initialization
    def __init__(self, n_board, p1, p2):
        # Pygame library and variable initialization
        pygame.init()
        self.screen = pygame.display.set_mode((1280,720))    # Resolution set
        pygame.display.set_icon(pygame.image.load('assets/icon.png'))
        pygame.display.set_caption('Halma (Beta) v0.2')
        
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

        # Player parameter initialization
        self.n_player = 2
        
        self.p1_initial = [p1[0],p1[1]]
        self.p2_initial = [p2[0],p2[1]]
        self.p1_selected = 3
        self.p2_selected = 4
        self.color_picked = [0, 6, 2, 3, 0]     # Default: p1: [red,orange], p2: [green,blue]
        
        # Game state
        self.starting = True
        self.runningState = False
        self.score = [0,0]

        # Game model
        self.model = HalmaModel()
        self.modelState = self.model.S_OK      # Running state
        self.model.awal(p1[0],p2[0])

        # Timer initialization
        self.clock = pygame.time.Clock()

        # Assets Import
        self.title              = [pygame.image.load('assets/title.png'),
                                   pygame.image.load('assets/title_dark.png')]
        self.info_text          = [pygame.image.load('assets/info/info_turn.png'),
                                   pygame.image.load('assets/info/info_score.png'),
                                   pygame.image.load('assets/info/info_timeleft.png'),
                                   pygame.image.load('assets/info/info_lastmove.png')]
        self.info_ai            = [pygame.image.load('assets/info/info_p1_ai.png'),
                                   pygame.image.load('assets/info/info_p2_ai.png')]
        self.button             = [pygame.image.load('assets/button/button_start.png'),
                                   pygame.image.load('assets/button/button_reset.png'),
                                   pygame.image.load('assets/button/button_pause.png'),
                                   pygame.image.load('assets/button/button_8x8.png'),
                                   pygame.image.load('assets/button/button_10x10.png'),
                                   pygame.image.load('assets/button/button_2p.png'),
                                   pygame.image.load('assets/button/button_4p.png'),
                                   pygame.image.load('assets/button/button_dark.png')]
        self.button_active      = [pygame.image.load('assets/button/button_start_active.png'),
                                   pygame.image.load('assets/button/button_reset_active.png'),
                                   pygame.image.load('assets/button/button_pause_active.png'),
                                   pygame.image.load('assets/button/button_8x8_active.png'),
                                   pygame.image.load('assets/button/button_10x10_active.png'),
                                   pygame.image.load('assets/button/button_2p_active.png'),
                                   pygame.image.load('assets/button/button_4p_active.png'),
                                   pygame.image.load('assets/button/button_dark_active.png')]
        self.button_ai          = [pygame.image.load('assets/button/button_01.png'),
                                   pygame.image.load('assets/button/button_02.png'),
                                   pygame.image.load('assets/button/button_03.png'),
                                   pygame.image.load('assets/button/button_04.png')]
        self.button_ai_active   = [pygame.image.load('assets/button/button_01_active.png'),
                                   pygame.image.load('assets/button/button_02_active.png'),
                                   pygame.image.load('assets/button/button_03_active.png'),
                                   pygame.image.load('assets/button/button_04_active.png')]
        self.board_8            = [pygame.image.load('assets/board/board_8.png'),
                                   pygame.image.load('assets/board/board_8_numbered.png')]
        self.board_10           = [pygame.image.load('assets/board/board_10.png'),
                                   pygame.image.load('assets/board/board_10_numbered.png')]
        self.board_8_dark       = [pygame.image.load('assets/board/board_8_dark.png'),
                                   pygame.image.load('assets/board/board_8_numbered_dark.png')]
        self.board_10_dark      = [pygame.image.load('assets/board/board_10_dark.png'),
                                   pygame.image.load('assets/board/board_10_numbered_dark.png')]
        self.piece_8            = [pygame.image.load('assets/pieces/8x8_blue.png'),
                                   pygame.image.load('assets/pieces/8x8_cyan.png'),
                                   pygame.image.load('assets/pieces/8x8_green.png'),
                                   pygame.image.load('assets/pieces/8x8_orange.png'),
                                   pygame.image.load('assets/pieces/8x8_pink.png'),
                                   pygame.image.load('assets/pieces/8x8_purple.png'),
                                   pygame.image.load('assets/pieces/8x8_red.png'),
                                   pygame.image.load('assets/pieces/8x8_yellow.png')]
        self.piece_10           = [pygame.image.load('assets/pieces/10x10_blue.png'),
                                   pygame.image.load('assets/pieces/10x10_cyan.png'),
                                   pygame.image.load('assets/pieces/10x10_green.png'),
                                   pygame.image.load('assets/pieces/10x10_orange.png'),
                                   pygame.image.load('assets/pieces/10x10_pink.png'),
                                   pygame.image.load('assets/pieces/10x10_purple.png'),
                                   pygame.image.load('assets/pieces/10x10_red.png'),
                                   pygame.image.load('assets/pieces/10x10_yellow.png')]
        self.color_picker       = [pygame.image.load('assets/pieces/cp_blue.png'),
                                   pygame.image.load('assets/pieces/cp_cyan.png'),
                                   pygame.image.load('assets/pieces/cp_green.png'),
                                   pygame.image.load('assets/pieces/cp_orange.png'),
                                   pygame.image.load('assets/pieces/cp_pink.png'),
                                   pygame.image.load('assets/pieces/cp_purple.png'),
                                   pygame.image.load('assets/pieces/cp_red.png'),
                                   pygame.image.load('assets/pieces/cp_yellow.png')]
        self.cp_selected        = pygame.image.load('assets/pieces/cpselected.png')

        # Font definition
        self.font_time          = pygame.font.SysFont('Coolvetica', 120)
        self.font_time_stack    = pygame.font.SysFont('Coolvetica', 60)
        self.font_player_name   = pygame.font.SysFont('Coolvetica', 100)
        self.font_fps           = pygame.font.SysFont('Coolvetica', 28)
        self.font_move_history  = pygame.font.SysFont('Coolvetica', 40)
        self.font_piece         = pygame.font.SysFont('Coolvetica', 40)
        self.font_score         = pygame.font.SysFont('Coolvetica', 110)
        self.font_warning       = pygame.font.SysFont('Coolvetica', 34)

    # Reinitialize player
    # to do : 4 player model init
    def reinit_model(self,p1,p2):
        self.p1_initial = p1
        self.p2_initial = p2
        self.model = HalmaModel()
        self.modelState = self.model.S_OK      # Running state
        
        if self.n_player == 2:
            self.model.awal(p1[0],p2[0])
        else:
            self.model.awal(p1[0],p2[0],p1[1],p2[1])

    # Template Load
    def load_template(self, numbered=None):
        # Background color and title
        if self.dark_mode:
            self.screen.fill(colors['BG_DARK'])
            self.screen.blit(self.title[1], dest=(35,25))
        else:
            self.screen.fill(colors['BG'])
            self.screen.blit(self.title[0], dest=(35,25))
        
        # Start, reset, and pause button
        self.screen.blit(self.button[0], dest=(35,120))
        self.screen.blit(self.button[1], dest=(190,120))
        self.screen.blit(self.button[2], dest=(345,120))
        
        # Show on starting screen
        if self.starting:
            # 8x8 and 10x10 button
            self.screen.blit(self.button[3], dest=(35,230))
            self.screen.blit(self.button[4], dest=(140,230))
            
            # Dark mode button
            if self.dark_mode:
                self.screen.blit(self.button_active[7], dest=(35,310))
            else:
                self.screen.blit(self.button[7], dest=(35,310))

            # Player count button
            self.screen.blit(self.button[5], dest=(280,230))
            self.screen.blit(self.button[6], dest=(360,230))

            # AI player select button
            self.screen.blit(self.info_ai[0], dest=(35,450))
            self.screen.blit(self.info_ai[1], dest=(35,570))
            for i in range(0,4):
                self.screen.blit(self.button_ai[i], dest=(180 + i*90,445))
                self.screen.blit(self.button_ai[i], dest=(180 + i*90,565))

            # Color picker
            for i in range(0,8):
                self.screen.blit(self.color_picker[i], dest=(180 + i*44,500))
                self.screen.blit(self.color_picker[i], dest=(180 + i*44,620))
        
        # Show on playing state
        else:
            # Playing info
            self.screen.blit(self.info_text[0], dest=(35,200))  # Player
            self.screen.blit(self.info_text[1], dest=(35,285))  # Score
            self.screen.blit(self.info_text[2], dest=(35,365))  # Clock
            self.screen.blit(self.info_text[3], dest=(35,460))  # Last Move

        # Numbered board as default
        if numbered == None:
            numbered = True

        # Board rendering
        if self.dark_mode:
            if self.n_board == 8:
                if numbered:
                    self.screen.blit(self.board_8_dark[1], dest=(582,21))
                else:
                    self.screen.blit(self.board_8_dark[0], dest=(610,50))
            elif self.n_board == 10:
                if numbered:
                    self.screen.blit(self.board_10_dark[1], dest=(582,21))
                else:
                    self.screen.blit(self.board_10_dark[0], dest=(610,50))
            else:
                print('Invalid parameter')
                return 0
        else:
            if self.n_board == 8:
                if numbered:
                    self.screen.blit(self.board_8[1], dest=(582,21))
                else:
                    self.screen.blit(self.board_8[0], dest=(610,50))
            elif self.n_board == 10:
                if numbered:
                    self.screen.blit(self.board_10[1], dest=(582,21))
                else:
                    self.screen.blit(self.board_10[0], dest=(610,50))
            else:
                print('Invalid parameter')
                return 0

    # Load current model state board pieces
    def load_pieces(self, board):
        # Array traversal
        for i in range(0,self.n_board):
            for j in range(0,self.n_board):
                # Get piece number from board and parse to player_id and piece_id
                piece = board[i][j]
                player_id = piece // 100
                piece_id = piece - (player_id * 100)
                
                # Not empty block
                if piece_id != 0:
                    self.draw_piece(str(piece_id),self.color_picked[player_id],i,j)
    
    # Custom text piece
    # Blit to index of board: row(i), column(j)
    # Color index: 0(blue), 1(cyan), 2(green), 3(orange), 4(pink), 5(purple), 6(red), 7(yellow)
    def draw_piece(self, text, color, i, j):
        # Create text object
        textSurface = self.font_piece.render(text, True, (colors['WHITE']))
        textRect = textSurface.get_rect()

        # Draw piece
        if self.n_board == 10:
            self.screen.blit(self.piece_10[color], dest=(self.x0 + j*self.d, self.y0 + i*self.d))
            textRect.center = (self.x0 + j*self.d + 27, self.y0 + i*self.d + 29)
        elif self.n_board == 8:
            self.screen.blit(self.piece_8[color], dest=(self.x0 + j*self.d, self.y0 + i*self.d))
            textRect.center = (self.x0 + j*self.d + 32, self.y0 + i*self.d + 34)

        # Draw text
        self.screen.blit(textSurface, textRect)

    # Get color dictionary by index
    def get_color(self, i):
        return colors[colors_enum[i][1]]

    # Color shifting RGB value (for start_animation)
    def color_shift(self, val1, val2, step, i, dir):
        # Decreasing
        if dir == 0:
            return val1 - int(step*i*abs(val2-val1))
        # Increasing
        if dir == 1:
            return val1 + int(step*i*abs(val2-val1))

    # Animating board piece in starting state
    def start_animation(self, x):
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
        self.draw_piece('P',self.color_picked[1+x],1,2-z)
        self.draw_piece('R',self.color_picked[1+x],1,3-z)
        self.draw_piece('E',self.color_picked[1+x],1,4-z)
        self.draw_piece('S',self.color_picked[1+x],1,5-z)
        self.draw_piece('S',self.color_picked[1+x],1,6-z)
        
        self.draw_piece('S',self.color_picked[1+x],3,3-z)
        self.draw_piece('T',self.color_picked[1+x],3,4-z)
        self.draw_piece('A',self.color_picked[1+x],3,5-z)
        self.draw_piece('R',self.color_picked[1+x],3,6-z)
        self.draw_piece('T',self.color_picked[1+x],3,7-z)
        
        self.draw_piece('T',self.color_picked[1+x],5-z,2-z)
        self.draw_piece('O',self.color_picked[1+x],5-z,3-z)
        
        self.draw_piece('P',self.color_picked[1+x],7-z,3-z)
        self.draw_piece('L',self.color_picked[1+x],7-z,4-z)
        self.draw_piece('A',self.color_picked[1+x],7-z,5-z)
        self.draw_piece('Y',self.color_picked[1+x],7-z,6-z)

    # Timer
    def reset_timer(self):
        self.timer_time = 5000     # in millisecond
        self.clock.get_rawtime()

    def tick_timer(self):
        self.timer_time -= self.clock.get_rawtime()
        self.move_timer -= self.clock.get_rawtime()

    def get_timer(self):
        return self.model.JATAH_WAKTU - (self.model.getJatahWaktu(self.model.getGiliran()) - self.model.getSisaWaktu())
    
    # Time left (from 10 seconds turn time)
    def update_timer(self):
        if self.dark_mode:
            self.screen.blit(self.font_time.render('{:.2f}'.format(self.get_timer()),True,(colors['TEXT2'])), dest=(210,360))
        else:
            self.screen.blit(self.font_time.render('{:.2f}'.format(self.get_timer()),True,(colors['TEXT'])), dest=(210,360))
    
    # Reserve time left (accumulative bonus time from previous move)
    def update_timer_stack(self):
        p = self.model.getGiliran()
        stack = self.model.getJatahWaktu(p)
        self.screen.blit(self.font_time_stack.render('({:.2f})'.format(stack),True,(self.get_color(self.color_picked[p+1] + 6))), dest=(400,362))

    # FPS by 10 pygame timer tick average
    def update_fps(self):
        if self.dark_mode:
            self.screen.blit(self.font_fps.render('FPS: {:.1f}'.format(self.clock.get_fps()),True,(colors['TEXT2'])), dest=(1180,690))
        else:
            self.screen.blit(self.font_fps.render('FPS: {:.1f}'.format(self.clock.get_fps()),True,(colors['TEXT'])), dest=(1180,690))

    # Player name display
    def update_player(self):
        p = self.model.getGiliran()
        player = self.model.getPemain(p)
        self.screen.blit(self.font_player_name.render(player.nama,True,(self.get_color(self.color_picked[p+1] + 6))), dest=(210,195))

    # Player score display
    def update_score(self):
        # Dummy score
        if self.dark_mode:
            self.screen.blit(self.font_score.render('{} - {}'.format(self.score[0], self.score[1]),True,(colors['TEXT2'])), dest=(210,280))
        else:
            self.screen.blit(self.font_score.render('{} - {}'.format(self.score[0], self.score[1]),True,(colors['TEXT'])), dest=(210,280))

    # History display (latest on top)
    def update_history(self):
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
            self.screen.blit(self.font_move_history.render('{} | {} {} -> {} ({:.2f}s)'.format(name, move_type, move_hist[i][1], move_hist[i][2], move_hist[i][4]),1,
                                (self.get_color(self.color_picked[move_hist[i][0] + 1] + 6))), dest=(35, 510 + i*40))

    # Show player wins text
    def show_winner(self,p):
        # Dummy score
        if self.dark_mode:
            self.screen.blit(self.font_warning.render('{} WIN!'.format(self.get_object(p)[0].nama[:-1]),True,(colors['TEXT2'])), dest=(650,680))
        else:
            self.screen.blit(self.font_warning.render('{} WIN!'.format(self.get_object(p)[0].nama)[:-1],True,(colors['TEXT'])), dest=(650,680))

    # (helper) Get object by 'nama' attribute
    def get_object(self, p):
        if p == 1:
            return p01
        elif p == 2:
            return p02
        elif p == 3:
            return p03
        elif p == 4:
            return p04

    # (helper) Mouse coordinate in region (x0,y0: initial coordinate,  dx,dy: region dimension)
    def in_region(self, a, x0, y0, dx, dy):
        return (x0 <= a[0] <= x0+dx and y0 <= a[1] <= y0+dy)

    # (helper) Mouse coordinate in region circle (x0,y0: initial coordinate,  d: region diameter)
    def in_region_circle(self,a,x0,y0,d):
        cx = x0 + d/2
        cy = y0 + d/2
        dist = math.sqrt((abs(a[0] - cx))**2 + (abs(a[1] - cy))**2)
        return (dist <= d/2)

    # Interactive button hover/click
    def update_button(self):
        # Get mouse coordinate and click
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # Start button
        if self.in_region(mouse,35,120,126,44):
            self.screen.blit(self.button_active[0], dest=(35,120))
            if click[0] == 1:
                print('[click start]')
                self.action_start()

        # Reset button
        if self.in_region(mouse,190,120,126,44):
            self.screen.blit(self.button_active[1], dest=(190,120))
            if click[0] == 1:
                print('[click reset]')
                self.action_reset()

        # Pause button
        if self.in_region(mouse,345,120,126,44):
            print('[hover pause]',self.prev_pause)
            self.screen.blit(self.button_active[2], dest=(345,120))
            if click[0] == 1:
                print('[click pause]')
                self.action_pause()

        # Display in starting mode
        if self.starting:
            # 8x8 button
            if (self.in_region(mouse,35,230,92,50) or self.n_board == 8):
                self.screen.blit(self.button_active[3], dest=(35,230))
                if click[0] == 1 and self.in_region(mouse,35,230,92,50):
                    self.n_board = 8
                    self.d = 75
                    self.x0 = 626
                    self.y0 = 66

            # 10x10 button
            if (self.in_region(mouse,140,230,104,50) or self.n_board == 10):
                self.screen.blit(self.button_active[4], dest=(140,230))
                if click[0] == 1 and self.in_region(mouse,140,230,104,50):
                    self.n_board = 10
                    self.d = 60
                    self.x0 = 623
                    self.y0 = 63

            # 2P button
            if (self.in_region(mouse,280,230,67,50) or self.n_player == 2):
                self.screen.blit(self.button_active[5], dest=(280,230))
                if click[0] == 1 and self.in_region(mouse,280,230,67,50):
                    self.n_player = 2
            
            # 4P button
            if (self.in_region(mouse,360,230,67,50) or self.n_player == 4):
                self.screen.blit(self.button_active[6], dest=(360,230))
                if click[0] == 1 and self.in_region(mouse,360,230,67,50):
                    self.n_player = 4

            # Dark mode button
            if (self.in_region(mouse,35,310,208,50) or self.dark_mode == True):
                self.screen.blit(self.button_active[7], dest=(35,310))
                if click[0] == 1 and self.in_region(mouse,35,310,208,50):
                    self.dark_mode = not self.dark_mode
                    time.sleep(0.2)
            
            # AI picker
            for i in range(4):
                # Row 1
                if self.in_region(mouse,180 + 90*i,445,69,50) or self.p1_selected == (i + 1):
                    self.screen.blit(self.button_ai_active[i], dest=(180 + 90*i,445))
                    if click[0] == 1 and self.in_region(mouse,180 + 90*i,445,69,50) and self.p1_selected != (i + 1):
                        print('[{}-{} selected as p1]'.format(self.get_object(i+1)[0].nama, self.get_object(i+1)[1].nama))
                        self.p1_selected = i + 1
                
                # Row 2
                if self.in_region(mouse,180 + 90*i,565,69,50) or self.p2_selected == (i + 1):
                    self.screen.blit(self.button_ai_active[i], dest=(180 + 90*i,565))
                    if click[0] == 1 and self.in_region(mouse,180 + 90*i,565,69,50) and self.p2_selected != (i + 1):
                        print('[{}-{} selected as p1]'.format(self.get_object(i+1)[0].nama, self.get_object(i+1)[1].nama))
                        self.p2_selected = i + 1

            # Color picker
            for i in range(0,8):
                # Player 1
                if self.in_region_circle(mouse,180 + 44*i,500,30) or i == self.color_picked[1] or i == self.color_picked[3]:
                    self.screen.blit(self.cp_selected, dest=(180 + 44*i,500))
                    if click[0] == 1 and self.in_region_circle(mouse,180 + 44*i,500,30):
                            self.color_picked[1] = i
                            self.color_picked[3] = i
                
                # Player 2
                if self.in_region_circle(mouse,180 + 44*i,620,30) or i == self.color_picked[2] or i == self.color_picked[4]:
                    self.screen.blit(self.cp_selected, dest=(180 + 44*i,620))
                    if click[0] == 1 and self.in_region_circle(mouse,180 + 44*i,620,30):
                        self.color_picked[2] = i
                        self.color_picked[4] = i
                

    # Start button clicked
    def action_start(self):
        if self.n_board == 10:
            self.click_start = True
        else:
            if self.dark_mode:
                self.screen.blit(self.font_warning.render('Currently only 10x10 board are supported',True,(colors['TEXT2'])), dest=(35,370))
            else:
                self.screen.blit(self.font_warning.render('Currently only 10x10 board are supported',True,(colors['TEXT'])), dest=(35,370))
    
    # Reset button clicked
    def action_reset(self):
        self.click_reset = True

    # Pause button clicked
    def action_pause(self):
        self.click_pause = not self.click_pause

    # Update all screen element (board,piece,info,button,fps)
    def update_screen(self):
        #print('[update_screen loop]')
        self.load_template(numbered=True)
        self.update_button()
        self.load_pieces(self.model.getPapan())
        self.update_player()
        self.update_score()
        self.update_timer()
        self.update_timer_stack()
        self.update_fps()
        self.update_history()
        
        pygame.display.update()


    # Main game loop
    def main(self):
        # Starting condition
        self.reset_timer()
        modelState = self.model.S_OK

        # Starting state
        while self.starting:
            # Frame and loop timing
            self.clock.tick_busy_loop(60)   # Framerate cap
            
            self.xi = (self.xi + 1) % 100
            x = self.xi // 50
            
            self.load_template(numbered=True)
            self.update_button()
            self.start_animation(x)
            self.update_fps()
            pygame.display.update()

            # Quit event (work to do: get and process all event from GUI)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.starting = False
                    self.runningState = False
            
            if self.click_start:
                print('[START clicked]')
                self.click_start = False

                # Change state
                self.starting = False
                self.runningState = True
                
                # Start game with AI selected (reinitialize model)
                self.reinit_model(self.get_object(self.p1_selected), self.get_object(self.p2_selected))
                # break
                
            if self.click_reset:    # Pretty useless?
                print('[RESET clicked]')
                self.click_reset = False

                # Reinitialize halma model
                self.reinit_model(self.p1_initial, self.p2_initial)
        
        self.load_template()
        # Game loop (1 round)
        while self.runningState and modelState == self.model.S_OK:
            # Frame and loop timing
            self.clock.tick_busy_loop(75)   # Framerate cap
            self.tick_timer()

            # AI move
            self.model.mainMulai()
            p = self.model.getPemain(self.model.getGiliran())   # get current pemain ?
            print(p.nama)
            final_pos, initial_pos, action = p.main(self.model)
            self.move_count += 1
            print('[move count] ',self.move_count)
            selesai = self.model.getWaktu()
            time_exec = self.model.getJatahWaktu(self.model.getGiliran()) - self.model.getSisaWaktu()

            # Insert to move history (4 last move, latest on top)
            self.move_history.append([self.model.getGiliran(), initial_pos, final_pos, action, time_exec])
            if len(self.move_history) > 4:
                self.move_history = self.move_history[-4:]
            print('[move] {} {} {}'.format(initial_pos, final_pos, action))
            print('[exec time] {}'.format(time_exec))
            
            # Type of action
            if action == self.model.A_LONCAT:
                print('[action: loncat]')
                for xy in final_pos:
                    modelState = self.model.mainLoncat(initial_pos[0], initial_pos[1], xy[0], xy[1])
                    initial_pos = xy
            elif action == self.model.A_GESER:
                print('[action: geser]')
                modelState = self.model.mainGeser(initial_pos[0], initial_pos[1], final_pos[0][0], final_pos[0][1])

            # Termination
            if self.n_player == 2:
                if self.model.akhir():
                    pieces = self.model.getPosisiBidak(0)
                    
                    # Count pieces
                    k = 0
                    for piece in pieces:
                        if self.model.dalamTujuan(0,piece[0],piece[1]):
                            k += 1
                    if k == 15:
                        print('[P1 Menang!]')
                        self.show_winner(self.p1_selected)
                        self.score[0] += 1
                    else:
                        print('[P2 Menang!]')
                        self.show_winner(self.p2_selected)
                        self.score[1] += 1
                    
                    # Waiting for start button press
                    self.click_start = False
                    while not self.click_start:
                        self.update_button()

                    # Reinitialize halma model (next round)
                    modelState = self.model.S_OK
                    self.reinit_model(self.get_object(self.p1_selected), self.get_object(self.p2_selected))
                    self.starting = True
                    self.main()

            elif self.n_player == 4:
                if self.model.akhirBeregu():
                    pieces1 = self.model.getPosisiBidak(0)
                    pieces3 = self.model.getPosisiBidak(2)
                    
                    # Count pieces
                    k = 0
                    for piece in pieces1:
                        if self.model.dalamTujuan(0,piece[0],piece[1]):
                            k += 1
                    for piece in pieces3:
                        if self.model.dalamTujuan(2,piece[0],piece[1]):
                            k += 1

                    if k == 26:
                        print('[P1 Menang!]')
                        self.show_winner(self.p1_selected)
                        self.score[0] += 1
                    else:
                        print('[P2 Menang!]')
                        self.show_winner(self.p2_selected)
                        self.score[1] += 1
                    
                    # Waiting for start button press
                    self.click_start = False
                    while not self.click_start:
                        self.update_button()

                    # Reinitialize halma model (next round)
                    modelState = self.model.S_OK
                    self.reinit_model(self.get_object(self.p1_selected), self.get_object(self.p2_selected))
                    self.starting = True
                    self.main()

            modelState = self.model.ganti(selesai)
            self.reset_timer()

            # Update screen frame on current state
            self.update_screen()

            # Reset button
            if self.click_reset:
                print('[RESET clicked]')
                self.click_reset = False

                # Reinitialize halma model
                self.reinit_model(self.p1_initial,self.p2_initial)

                # Revert state (recursively call main method)
                self.starting = True
                self.runningState = False
                self.main()
                # break
                
            # Quit event (work to do: get and process all event from GUI)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.runningState = False

# Execute if invoked directly from script
if __name__ == "__main__":
    # Initial value 10x10 with player1 is p03 and player 2 is p04 (changeable in starting state)
    g = gui(n_board=10, p1=p03, p2=p04)
    g.main()
    pygame.quit()
