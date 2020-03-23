''' 
Halma GUI (Using halma_model script)

To do :
    - Continuous timer (while AI computing moves)
    - Starting animation
    - Move history
        - Selected AI move (current: first available move list)
    - Working 'START' and 'RESET' button
        - Starting animation [v]
        - Main game loop
    - Score
    - Dark Mode (!!)
    - Tkinter integration for game start configuration
    - Customization (menu screen)
    - Embedded font assets
    - 4 player (team)
    - Human player
    - Change to 60fps on commit
    - Package installer (?)
'''
import pygame
from halma_model import HalmaModel
import threading        # Multithreading library
import multiprocessing
import time
from halma_player import HalmaPlayer
from halma_player_01_A import HalmaPlayer01
from halma_player_02_A import HalmaPlayer02
from halma_player_03_A import HalmaPlayer03
from halma_player_04_A import HalmaPlayer04

# Color Definition
colors = {
    'BLACK': (0,0,0),
    'WHITE': (255,255,255),
    'BG': (236,243,244),
    'BG_DARK': (10,31,34),
    'TEXT': (40,76,81),
    'TEXT2': (236,243,244),
    'P1': (240,111,82),
    'P2': (87,184,77)
}

p1 = HalmaPlayer01('Team 01')
p2 = HalmaPlayer01('Team 02')
p3 = HalmaPlayer01('Team 03')
p4 = HalmaPlayer01('Team 04')

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
    d = 0
    x0 = 0
    y0 = 0
    timer_time = 0
    timer_stack = 0
    move_timer = 0
    move_history = []
    click_start = False
    click_reset = False
    starting = True
    shift_i = 0

    # Font and object variable
    font_time = 0
    font_fps = 0

    # State simulator
    # Access: self.PAPAN_10_15x2[row][col]
    PAPAN_10_15x2 = [[101, 102, 104, 107, 111, 0,   0,   0,   0,   0  ],
                     [103, 0, 108, 112,   0,   0,   0,   0,   0,   0  ],
                     [106, 109, 113, 0,   0,   0,   0,   0,   0,   0  ],
                     [110, 114, 0,   0,   0,   0,   105, 0,   0,   0  ],
                     [115, 0,   0,   0,   0,   0,   0,   0,   0,   0  ],
                     [0,   0,   0,   0,   0,   0,   0,   0,   0,   215],
                     [0,   0,   0,   0,   0,   0,   0,   0,   214, 210],
                     [0,   0,   0,   211, 0,   0,   0,   213, 209, 206],
                     [0,   0,   0,   0,   0,   0,   212, 208, 205, 203],
                     [0,   0,   0,   0,   0,   0,   207, 204, 202, 201]]
    

    # Initialization
    def __init__(self, n_board, p1, p2):
        # Pygame library and variable initialization
        pygame.init()
        self.screen = pygame.display.set_mode((1280,720))    # Resolution set
        pygame.display.set_icon(pygame.image.load('assets/icon.png'))
        pygame.display.set_caption('Halma (pre-alpha) v0.1')
        self.n_board = n_board
        if self.n_board == 8:
            self.d = 75
            self.x0 = 623
            self.y0 = 63
        elif self.n_board == 10:
            self.d = 60
            self.x0 = 623
            self.y0 = 63

        # Save initial player for reset function
        self.p1_initial = p1
        self.p2_initial = p2
        
        # Game state
        self.starting = True
        self.runningState = False
        
        # Utilities
        self.xi = 0
        self.shift_i = 0

        # Game model
        self.model = HalmaModel()
        self.modelState = self.model.S_OK      # Running state
        self.model.awal(p1,p2)

        # Timer initialization
        self.clock = pygame.time.Clock()

        # Assets Import
        self.title          = [pygame.image.load('assets/title.png'), pygame.image.load('assets/title_dark.png')]
        self.info_text      = [pygame.image.load('assets/info_turn.png'), pygame.image.load('assets/info_score.png'), pygame.image.load('assets/info_timeleft.png'), pygame.image.load('assets/info_lastmove.png')]
        self.info_ai        = [pygame.image.load('assets/info_p1_ai.png'), pygame.image.load('assets/info_p2_ai.png')]
        self.button         = [pygame.image.load('assets/button/button_start.png'), pygame.image.load('assets/button/button_reset.png'), pygame.image.load('assets/button/button_8x8.png'), pygame.image.load('assets/button/button_10x10.png'), pygame.image.load('assets/button/button_dark.png')]
        self.button_active  = [pygame.image.load('assets/button/button_start_active.png'), pygame.image.load('assets/button/button_reset_active.png'), pygame.image.load('assets/button/button_8x8_active.png'), pygame.image.load('assets/button/button_10x10_active.png'), pygame.image.load('assets/button/button_dark_active.png')]
        self.button_ai      = [pygame.image.load('assets/button/button_01.png'), pygame.image.load('assets/button/button_02.png'), pygame.image.load('assets/button/button_03.png'), pygame.image.load('assets/button/button_04.png')]
        self.button_ai_active = [pygame.image.load('assets/button/button_01_active.png'), pygame.image.load('assets/button/button_02_active.png'), pygame.image.load('assets/button/button_03_active.png'), pygame.image.load('assets/button/button_04_active.png')]
        self.board_8        = [pygame.image.load('assets/board/board_8.png'), pygame.image.load('assets/board/board_8_numbered.png')]
        self.board_10       = [pygame.image.load('assets/board/board_10.png'), pygame.image.load('assets/board/board_10_numbered.png')]
        self.board_8_dark   = [pygame.image.load('assets/board/board_8_dark.png'), pygame.image.load('assets/board/board_8_numbered_dark.png')]
        self.board_10_dark  = [pygame.image.load('assets/board/board_10_dark.png'), pygame.image.load('assets/board/board_10_numbered_dark.png')]
        self.piece_8        = [0, pygame.image.load('assets/pieces_global/piece_8_1.png'), pygame.image.load('assets/pieces_global/piece_8_2.png')]
        self.piece_10       = [0, pygame.image.load('assets/pieces_global/piece_10_1.png'), pygame.image.load('assets/pieces_global/piece_10_2.png')]

        # Font import
        self.font_time          = pygame.font.SysFont('Coolvetica', 120)
        self.font_time_stack    = pygame.font.SysFont('Coolvetica', 60)
        self.font_player_name   = pygame.font.SysFont('Coolvetica', 100)
        self.font_fps           = pygame.font.SysFont('Coolvetica', 28)
        self.font_move_history  = pygame.font.SysFont('Coolvetica', 40)
        self.font_piece         = pygame.font.SysFont('Coolvetica', 40)
        self.font_score         = pygame.font.SysFont('Coolvetica', 110)
        self.font_warning       = pygame.font.SysFont('Coolvetica', 34)

    # Reinitialize player
    def reinit_model(self,p1,p2):
        self.model = HalmaModel()
        self.modelState = self.model.S_OK      # Running state
        self.model.awal(p1,p2)

    # Template Load
    def load_template(self, numbered=None):
        if self.dark_mode:
            self.screen.fill(colors['BG_DARK'])
            self.screen.blit(self.title[1], dest=(35,25))
        else:
            self.screen.fill(colors['BG'])
            self.screen.blit(self.title[0], dest=(35,25))
        self.screen.blit(self.button[0], dest=(35,120))
        self.screen.blit(self.button[1], dest=(190,120))
        if self.starting:
            self.screen.blit(self.button[2], dest=(35,230))
            self.screen.blit(self.button[3], dest=(140,230))
            if self.dark_mode:
                self.screen.blit(self.button_active[4], dest=(35,310))
            else:
                self.screen.blit(self.button[4], dest=(35,310))
            self.screen.blit(self.info_ai[0], dest=(35,450))
            self.screen.blit(self.info_ai[1], dest=(35,550))
            self.screen.blit(self.button_ai[0], dest=(180,445))
            self.screen.blit(self.button_ai[1], dest=(270,445))
            self.screen.blit(self.button_ai[2], dest=(360,445))
            self.screen.blit(self.button_ai[3], dest=(450,445))
            self.screen.blit(self.button_ai[0], dest=(180,545))
            self.screen.blit(self.button_ai[1], dest=(270,545))
            self.screen.blit(self.button_ai[2], dest=(360,545))
            self.screen.blit(self.button_ai[3], dest=(450,545))
        if not self.starting:
            self.screen.blit(self.info_text[0], dest=(35,200))
            self.screen.blit(self.info_text[1], dest=(35,285))
            self.screen.blit(self.info_text[2], dest=(35,365))
            self.screen.blit(self.info_text[3], dest=(35,460))

        # Numbered board as default
        if numbered == None:
            numbered = True

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

    # Load current state board pieces
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
                    self.draw_piece(str(piece_id),player_id,i,j)
                    #self.screen.blit(self.p_10[player_id][piece_id], dest=(self.x0 + j*self.d, self.y0 + i*self.d))

    # Timer
    def reset_timer(self):
        self.timer_time = 10000     # in millisecond
        self.clock.get_rawtime()
    
    def reset_move_timer(self, time):
        self.move_timer = time
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
        if p == 0:
            self.screen.blit(self.font_time_stack.render('({:.2f})'.format(stack),True,(colors['P1'])), dest=(400,362))
        elif p == 1:
            self.screen.blit(self.font_time_stack.render('({:.2f})'.format(stack),True,(colors['P2'])), dest=(400,362))

    # FPS by 10 pygame timer average
    def update_fps(self):
        if self.dark_mode:
            self.screen.blit(self.font_fps.render('FPS: {:.1f}'.format(self.clock.get_fps()),True,(colors['TEXT2'])), dest=(1180,690))
        else:
            self.screen.blit(self.font_fps.render('FPS: {:.1f}'.format(self.clock.get_fps()),True,(colors['TEXT'])), dest=(1180,690))

    # Player name display
    def update_player(self):
        p = self.model.getGiliran()
        player = self.model.getPemain(p)
        if p == 0:
            self.screen.blit(self.font_player_name.render(player.nama,True,(colors['P1'])), dest=(210,195))
        elif p == 1:
            self.screen.blit(self.font_player_name.render(player.nama,True,(colors['P2'])), dest=(210,195))

    # Player score display
    def update_score(self):
        # Dummy score
        if self.dark_mode:
            self.screen.blit(self.font_score.render('0 - 0',True,(colors['TEXT2'])), dest=(210,280))
        else:
            self.screen.blit(self.font_score.render('0 - 0',True,(colors['TEXT'])), dest=(210,280))

    # History display
    # Order: latest on bottom
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
            if self.move_history[i][0] == 0:
                self.screen.blit(self.font_move_history.render('{} | {} {} -> {} ({:.2f}s)'.format(name, move_type, move_hist[i][1], move_hist[i][2], move_hist[i][4]),1,(colors['P1'])), dest=(35, 510 + i*40))
            elif self.move_history[i][0] == 1:
                self.screen.blit(self.font_move_history.render('{} | {} {} -> {} ({:.2f}s)'.format(name, move_type, move_hist[i][1], move_hist[i][2], move_hist[i][4]),1,(colors['P2'])), dest=(35, 510 + i*40))

    # (helper) Coordinate in region (x0,y0: initial coordinate,  dx,dy: region dimension)    
    def in_region(self,a,x0,y0,dx,dy):
        return (x0 <= a[0] <= x0+dx and y0 <= a[1] <= y0+dy)

    # Interactive button hover/click
    def update_button(self,action_start,action_reset):
        # Get mouse coordinate
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # Start button
        if self.in_region(mouse,35,120,126,44):
            self.screen.blit(self.button_active[0], dest=(35,120))
            if click[0] == 1:
                print('[click start]')
                action_start()

        # Reset button
        if self.in_region(mouse,190,120,126,44):
            self.screen.blit(self.button_active[1], dest=(190,120))
            if click[0] == 1:
                print('[click reset]')
                action_reset()

        # 8x8 button
        if (self.in_region(mouse,35,230,92,50) or self.n_board == 8) and self.starting:
            self.screen.blit(self.button_active[2], dest=(35,230))
            if click[0] == 1:
                print('[click 8x8]')
                self.n_board = 8
                self.d = 75
                self.x0 = 626
                self.y0 = 66

        # 10x10 button
        if (self.in_region(mouse,140,230,104,50) or self.n_board == 10) and self.starting:
            self.screen.blit(self.button_active[3], dest=(140,230))
            if click[0] == 1:
                print('[click 10x10]')
                self.n_board = 10
                self.d = 60
                self.x0 = 623
                self.y0 = 63
        
        # Dark mode button
        if self.in_region(mouse,35,310,208,50 or self.dark_mode == True) and self.starting:
            self.screen.blit(self.button_active[4], dest=(35,310))
            if click[0] == 1:
                print('[click dark]')
                self.dark_mode = not self.dark_mode
                time.sleep(0.2)
                

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

    # Custom text piece (currently 10x10 supported)
    # Blit to index of board: row(i), column(j)
    def draw_piece(self,text,color,i,j):
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

    # Color shifting RGB value (for start_animation)
    def color_shift(self,val1,val2,step,i,dir):
        # Decreasing
        if dir == 0:
            return val1 - int(step*i*abs(val2-val1))
        # Increasing
        if dir == 1:
            return val1 + int(step*i*abs(val2-val1))

    # Animating board piece in starting state
    def start_animation(self,x):
        # Background color
        for i in range(0,self.n_board):
            for j in range(0,self.n_board):
                self.draw_piece("",2-x,i,j)
        
        # 10x10 board
        if self.n_board == 10:
            z = 0
        elif self.n_board == 8:
            z = 1

        # 'PRESS START TO PLAY' text
        self.draw_piece('P',1+x,1,2-z)
        self.draw_piece('R',1+x,1,3-z)
        self.draw_piece('E',1+x,1,4-z)
        self.draw_piece('S',1+x,1,5-z)
        self.draw_piece('S',1+x,1,6-z)
        
        self.draw_piece('S',1+x,3,3-z)
        self.draw_piece('T',1+x,3,4-z)
        self.draw_piece('A',1+x,3,5-z)
        self.draw_piece('R',1+x,3,6-z)
        self.draw_piece('T',1+x,3,7-z)
        
        self.draw_piece('T',1+x,5-z,2-z)
        self.draw_piece('O',1+x,5-z,3-z)
        
        self.draw_piece('P',1+x,7-z,3-z)
        self.draw_piece('L',1+x,7-z,4-z)
        self.draw_piece('A',1+x,7-z,5-z)
        self.draw_piece('Y',1+x,7-z,6-z)


    # Update all screen element
    def update_screen(self):
        print('[update_screen loop]')
        self.load_template(numbered=True)
        self.update_button(self.action_start, self.action_reset)
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
            self.clock.tick_busy_loop(60)
            
            self.xi = (self.xi + 1) % 100
            x = self.xi // 50
            
            self.load_template(numbered=True)
            self.update_button(self.action_start, self.action_reset)
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
                self.starting = False
                self.runningState = True
                break
                
            if self.click_reset:
                print('[RESET clicked]')
                self.click_reset = False
                self.__init__(self.n_board,self.p1_initial,self.p2_initial)
        
        self.load_template()
        # Game loop (1 round)
        while self.runningState and modelState == self.model.S_OK:
            # Frame and loop timing
            self.clock.tick_busy_loop(75)   # Framerate cap
            self.tick_timer()


            # AI move
            self.model.mainMulai()
            p = self.model.getPemain(self.model.getGiliran())   # get current pemain ?
            final_pos, initial_pos, action = p.main(self.model)
            selesai = self.model.getWaktu()
            time_exec = self.model.getJatahWaktu(self.model.getGiliran()) - self.model.getSisaWaktu()

            # Insert to move history (4 last move)
            self.move_history.append([self.model.getGiliran(), initial_pos, final_pos[0], action, time_exec])
            if len(self.move_history) > 4:
                self.move_history = self.move_history[-4:]
            print('[move] {} {} {}'.format(initial_pos, final_pos[0], action))
            print('[exec time] {}'.format(time_exec))
            
            # Type of action
            if action == self.model.A_LONCAT:
                print('[action: loncat]')
                for xy in final_pos:
                    modelState = self.model.mainLoncat(initial_pos[0], initial_pos[1], xy[0], xy[1])
            elif action == self.model.A_GESER:
                print('[action: geser]')
                modelState = self.model.mainGeser(initial_pos[0], initial_pos[1], final_pos[0][0], final_pos[0][1])

            # Termination
            if self.model.akhir():
                self.runningState = False
            modelState = self.model.ganti(selesai)
            self.reset_timer()


            # Update screen frame on current state
            self.update_screen()

            # Reset button
            if self.click_reset:
                print('[RESET clicked]')
                self.click_reset = False
                self.__init__(self.n_board,self.p1_initial,self.p2_initial)
                self.main()
                break
                
            # Quit event (work to do: get and process all event from GUI)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.runningState = False


    def move_ai(self, model, selesai):
        # AI move
        model.mainMulai()
        p = model.getPemain(model.getGiliran())   # get current pemain ?
        final_pos, initial_pos, action = p.main(model)
        selesai = model.getWaktu()
        time_exec = model.getJatahWaktu(model.getGiliran()) - self.model.getSisaWaktu()




######################################
### ------ WORK ON PROGRESS ------ ###
######################################

    # !!! Work on progress to utilize multiprocessing for continuous timer while AI is calculating
    def main2(self):
        # Starting condition
        self.reset_timer()
        self.update_screen()
        modelState = self.model.S_OK

        process_gui = multiprocessing.Process(target=self.update_screen, daemon=True)
        process_gui.start()

        # Game loop (1 round)
        while self.runningState and modelState == self.model.S_OK:
            # Frame and loop timing
            self.clock.tick_busy_loop(75)
            self.tick_timer()


            # AI move
            self.model.mainMulai()
            p = self.model.getPemain(self.model.getGiliran())   # get current pemain ?
            final_pos, initial_pos, action = p.main(self.model)
            selesai = self.model.getWaktu()
            time_exec = self.model.getJatahWaktu(self.model.getGiliran()) - self.model.getSisaWaktu()

            # Insert to move history (4 last move)
            self.move_history.append([self.model.getGiliran(), initial_pos, final_pos[0], action, time_exec])
            if len(self.move_history) > 4:
                self.move_history = self.move_history[-4:]
            print('[move] {} {} {}'.format(initial_pos, final_pos[0], action))
            print('[exec time] {}'.format(time_exec))
            
            # Type of action
            if action == self.model.A_LONCAT:
                print('[action: loncat]')
                for xy in final_pos:
                    modelState = self.model.mainLoncat(initial_pos[0], initial_pos[1], xy[0], xy[1])
            elif action == self.model.A_GESER:
                print('[action: geser]')
                valid = self.model.mainGeser(initial_pos[0], initial_pos[1], final_pos[0][0], final_pos[0][1])


            # Termination
            if self.model.akhir():
                self.runningState = False
            modelState = self.model.ganti(selesai)
            self.reset_timer()
            
            # Update screen frame on current state
            self.update_screen()


            # Quit event (work to do: get and process all event from GUI)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.runningState = False
            

# Execute if invoked directly from script
if __name__ == "__main__":
    g = gui(n_board=10, p1=HalmaPlayer('Pintar'), p2=HalmaPlayer('Cerdas'))
    g.main()
    pygame.quit()
