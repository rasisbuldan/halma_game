''' 
Halma GUI (Using halma_model script)

To do :
    - Integrate HalmaModel
        - Multithreading/multiprocessing for continous timer
    - Move history
        - Selected AI move (current: first available move list)
    - Working 'START' and 'RESET' button
    - Tkinter integration for game start configuration
    - Customization (menu screen)
    - Embedded font assets
    - 4 player (team)
    - Human player
    - Change to 60fps on commit
    - Package installer (?)
'''

import pygame
import threading        # Multithreading library
import multiprocessing
from halma_model import HalmaModel
from halma_player import HalmaPlayer

# Color Definition
colors = {
    'BLACK': (0,0,0),
    'WHITE': (255,255,255),
    'BG': (236,243,244),
    'TEXT': (40,76,81),
    'P1': (240,111,82),
    'P2': (87,184,77)
}

# GUI Class
class gui:
    # GUI Assets
    screen = 0
    clock = 0
    title = 0
    info_text = 0
    button = []
    board_8 = []
    board_10 = []
    p_8  = [0,[0],[0]]
    p_10 = [0,[0],[0]]

    # Game variable
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

    # Font and object variable
    font_time = 0
    font_fps = 0

    # State simulator
    # Access: self.PAPAN_10_15x2[row][col]
    PAPAN_10_15x2 = [[101, 102, 104, 107, 111, 0,   0,   0,   0,   0  ],
                     [103, 0, 108, 112, 0,   0,   0,   0,   0,   0  ],
                     [106, 109, 113, 0,   0,   0,   0,   0,   0,   0  ],
                     [110, 114, 0,   0,   0,   0,   105,   0,   0,   0  ],
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
        self.runningState = True
        self.n_board = n_board
        if self.n_board == 8:
            self.d = 75
        elif self.n_board == 10:
            self.d = 60
            self.x0 = 623
            self.y0 = 63

        # Halma Model initialization
        self.model = HalmaModel()
        self.modelState = self.model.S_OK      # Running state
        self.model.awal(p1,p2)

        # Timer initialization
        self.clock = pygame.time.Clock()

        # Assets Import
        self.title = pygame.image.load('assets/title.png')
        self.info_text = [pygame.image.load('assets/info_turn.png'), pygame.image.load('assets/info_score.png'), pygame.image.load('assets/info_time.png'), pygame.image.load('assets/info_history.png')]
        self.button = [pygame.image.load('assets/button_start.png'), pygame.image.load('assets/button_reset.png')]
        self.board_8 = [pygame.image.load('assets/board/board_8.png'), pygame.image.load('assets/board/board_8_numbered.png')]
        self.board_10 = [pygame.image.load('assets/board/board_10.png'), pygame.image.load('assets/board/board_10_numbered.png')]
        
        # Pieces Import
        for i in range(1,11):
            self.p_8[1].append(pygame.image.load('assets/pieces/8x8/' + str(100+i) + '.png'))
            self.p_8[2].append(pygame.image.load('assets/pieces/8x8/' + str(200+i) + '.png'))
        for i in range(1,16):
            self.p_10[1].append(pygame.image.load('assets/pieces/10x10/' + str(100+i) + '.png'))
            self.p_10[2].append(pygame.image.load('assets/pieces/10x10/' + str(200+i) + '.png'))

        # Font import
        self.font_time          = pygame.font.SysFont('Coolvetica', 120)
        self.font_time_stack    = pygame.font.SysFont('Coolvetica', 60)
        self.font_player_name   = pygame.font.SysFont('Coolvetica', 100)
        self.font_fps           = pygame.font.SysFont('Coolvetica', 28)
        self.font_move_history  = pygame.font.SysFont('Coolvetica', 40)
    
    # Template Load
    def load_template(self, numbered=None):
        self.screen.fill(colors['BG'])
        self.screen.blit(self.title, (35,25))
        self.screen.blit(self.button[0], (35,120))
        self.screen.blit(self.button[1], (190,120))
        self.screen.blit(self.info_text[0], (35,200))
        self.screen.blit(self.info_text[1], (35,285))
        self.screen.blit(self.info_text[2], (35,365))
        self.screen.blit(self.info_text[3], (35,460))

        # Numbered board as default
        if numbered == None:
            numbered = True

        if self.n_board == 8:
            if numbered:
                self.screen.blit(self.board_8[1], (582,21))
            else:
                self.screen.blit(self.board_8[0], (610,50))
        elif self.n_board == 10:
            if numbered:
                self.screen.blit(self.board_10[1], (582,21))
            else:
                self.screen.blit(self.board_10[0], (610,50))
        else:
            print('Invalid parameter')
            return 0
    
    # Load initial pieces
    def load_initial(self, n_player):
        if n_player == 2:
            # Upper Left
            k = 1
            x0 = 623
            y0 = 63
            for i in range(0,5):
                for j in range(0,i+1):
                    x = x0 + (i-j)*self.d
                    y = y0 + j*self.d
                    self.screen.blit(self.p_10[1][k], (x,y))
                    k += 1

            # Lower Right
            k = 1
            x0 = 1163
            y0 = 603
            for i in range(0,5):
                for j in range(0,i+1):
                    x = x0 - (i-j)*self.d
                    y = y0 - j*self.d
                    self.screen.blit(self.p_10[2][k], (x,y))
                    k += 1
        else:
            print('Invalid Parameter')

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
                    self.screen.blit(self.p_10[player_id][piece_id], (self.x0 + j*self.d, self.y0 + i*self.d))

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
        #print(self.get_timer())
        print('timer: ',self.get_timer())
        self.screen.blit(self.font_time.render('{0:.2f}'.format(self.get_timer()),1,(colors['TEXT'])), (210,360))
    
    # Reserve time left (accumulative bonus time from previous move)
    def update_timer_stack(self):
        p = self.model.getGiliran()
        stack = self.model.getJatahWaktu(p)
        if p == 0:
            self.screen.blit(self.font_time_stack.render('({0:.2f})'.format(stack),1,(colors['P1'])), (400,360))
        elif p == 1:
            self.screen.blit(self.font_time_stack.render('({0:.2f})'.format(stack),1,(colors['P2'])), (400,360))

    def update_fps(self):
        self.screen.blit(self.font_fps.render('FPS: {0:.1f}'.format(self.clock.get_fps()),1,(colors['TEXT'])), (1180,690))

    def update_player(self):
        p = self.model.getGiliran()
        player = self.model.getPemain(p)
        if p == 0:
            self.screen.blit(self.font_player_name.render(player.nama,1,(colors['P1'])), (210,195))
        elif p == 1:
            self.screen.blit(self.font_player_name.render(player.nama,1,(colors['P2'])), (210,195))

    def update_history(self):
        n = 4   # History size
        for i in range(0,len(self.move_history)):
            name = self.model.getPemain(self.move_history[i][0]).nama
            if self.move_history[i][3] == self.model.A_GESER:
                move_type = 'GESER'
            elif self.move_history[i][3] == self.model.A_LONCAT:
                move_type = 'LONCAT'
            # Player 1 move
            if self.move_history[i][0] == 0:
                self.screen.blit(self.font_move_history.render('{} | {} {} -> {} ({}s)'.format(name, move_type, self.move_history[i][1], self.move_history[i][2], self.move_history[i][4]),1,(colors['P1'])), (35, 510+40*i))
            elif self.move_history[i][0] == 1:
                self.screen.blit(self.font_move_history.render('{} | {} {} -> {} ({}s)'.format(name, move_type, self.move_history[i][1], self.move_history[i][2], self.move_history[i][4]),1,(colors['P2'])), (35, 510+40*i))
    # Update all screen element
    def update_screen(self):
        print('[update_screen loop]')
        self.load_template(numbered=True)
        self.load_pieces(self.model.getPapan())
        self.update_player()
        self.update_timer()
        self.update_timer_stack()
        self.update_fps()
        self.update_history()
        pygame.display.update()

    def action_move(self,selesai):
        print('[action_move loop]')
        # Get move
        self.model.mainMulai()
        print(*self.model.getPapan(), sep='\n')
        p = self.model.getPemain(self.model.getGiliran())   # get current pemain ?
        final_pos, initial_pos, action = p.main(self.model)
        selesai = self.model.getWaktu()
        
        # Type of action
        if action == self.model.A_LONCAT:
            print('[action: loncat]')
            for xy in final_pos:
                modelState = self.model.mainLoncat(initial_pos[0], initial_pos[1], xy[0], xy[1])
        elif action == self.model.A_GESER:
            print('[action: geser]')
            valid = self.model.mainGeser(initial_pos[0], initial_pos[1], final_pos[0][0], final_pos[0][1])

    def main(self):
        # Starting condition
        self.reset_timer()
        self.update_screen()
        modelState = self.model.S_OK

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

    # !!! Work on progress to utilize multiprocessing
    def main2(self):
        self.reset_timer()
        self.reset_move_timer(1000)
        modelState = self.model.S_OK
        selesai = 1
        
        while self.runningState:
            print('[gui loop]')
            
            # Update rate
            self.clock.tick_busy_loop(60)   # Locked frame rate
            self.tick_timer()

            process_gui = multiprocessing.Process(target=self.update_screen, daemon=True)
            process_gui.start()
            
            while modelState == self.model.S_OK and selesai != 0:
                selesai = 0
                print('[move loop]')
                # Threading
                process_ai = multiprocessing.Process(target=self.action_move, args=(selesai,), daemon=True)
                process_ai.start()

                ''' if self.get_timer() < 0:
                    # time's up?
                    self.reset_timer() '''

                # Termination
                if self.model.akhir():
                    self.runningState = False
                modelState = self.model.ganti(selesai)
                self.reset_timer()
                process_ai.join()
                break
            
            
            # Quit event (work to do: get and process all event from GUI)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.runningState = False
            

# Execute if invoked directly from script
if __name__ == "__main__":
    g = gui(n_board=10, p1=HalmaPlayer('Pintar'), p2=HalmaPlayer('Cerdas'))
    g.main()
    pygame.quit()
