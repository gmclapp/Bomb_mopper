import random
import pygame
import constants
import os

class game_object:
    def __init__(self):
        self.active_screen = "intro" # intro, main, high, options
        self.screens = {}
        
    def add_screen(self,new_screen):
        key = new_screen.name
        val = new_screen
        
        self.screens[key] = val

    def get_puzzle(self,screen):
        self.puzzle = Puzzle()
        self.puzzle.place(0,0,screen)

class Puzzle:
    def __init__(self):
        self.grid = [0,0,0,0,0,
                     0,1,0,0,0,
                     0,1,0,0,0,
                     1,0,0,0,0,
                     1,1,1,0,0]
        self.width = 5
        self.height = 5
        self.buttons = []

    def place(self,x,y,screen):
        self.x = x
        self.y = y
        self.screen = screen

    def is_mine(self,x,y):
        index = y*self.width + x
        return(self.buttons[index].is_mine())

    def set_numbers(self):
        for s in self.buttons:
            if s.is_mine():
                s.neighbor_mines = 0
            else:
                print("{},{} is not a mine.".format(s.grid_x,s.grid_y))
                for i in range(-1,2):
                    for j in range(-1,2):
                        if i == 0 and j == 0:
                            pass
                        elif s.grid_x+i < 0 or s.grid_x+1 > self.width-1:
                            pass
                        elif s.grid_y+j < 0 or s.grid_y+j > self.height-1:
                            pass
                        else:
                            if self.is_mine(s.grid_x+i,s.grid_y+j):
                                s.neighbor_mines += 1
                print("Site {},{} touches {} mines.".format(s.grid_x,s.grid_y,s.neighbor_mines))
        
class button:
    def __init__(self,wid,hei,art,pressed_art,label_art,action=None,RMB_action=None):
        self.pressed = False
        self.active = False
        self.clicked = False
        self.Rclicked = False

        self.wid = wid
        self.hei = hei

        self.art = art
        self.pressed_art = pressed_art
        self.label_art = label_art
        self.action = action
        self.RMB_action = RMB_action

    def place(self,x,y,screen):
        self.x = x
        self.y = y
        self.screen = screen
        screen.add_button(self)

    def update(self):
        if self.pressed:
            pass
        if self.active:
            pass
        if self.clicked:
            if self.action:
                self.action()
            else:
                print("No action assigned to left mouse button")
            self.clicked = False
        if self.Rclicked:
            if self.RMB_action:
                self.RMB_action()
            else:
                print("No action assigned to right mouse button")
            self.Rclicked = False

    def draw(self):
        if self.pressed:
            self.screen.surf.blit(self.pressed_art,(self.x,self.y))
        else:
            self.screen.surf.blit(self.art,(self.x,self.y))
        if self.label_art:
            self.screen.surf.blit(self.label_art,(self.x,self.y))

    def is_clicked(self,mx,my,MB):
        if self.x < mx < self.x + self.wid and self.y < my < self.y + self.hei:
            if MB == "LEFT":
                self.clicked = True
            if MB == "RIGHT":
                self.Rclicked = True
        else:
            self.clicked = False

    def is_pressed(self,mx,my):
        if self.x < mx < self.x + self.wid and self.y < my < self.y + self.hei:
            self.pressed = True
        else:
            self.pressed = False

class Site(button):
    def __init__(self,wid,hei,art,pressed_art,label_art,action=None,RMB_action=None,mine=False):
        super().__init__(wid,hei,art,pressed_art,label_art,action=self.open,RMB_action=self.flag)
        self.mine = mine
        self.flagged = False
        self.questioned = False
        self.neighbor_mines = 0

    def setxy(self,x,y):
        self.grid_x = x
        self.grid_y = y

    def open(self):
        self.art = constants.S_EMPTY
        self.pressed_art = constants.S_EMPTY
        if self.is_mine():
            self.label_art = constants.S_BOMB
            return(-1)
        else:
            self.label_art = constants.S_NUMBERS[self.neighbor_mines]
            return(self.neighbor_mines)

    def flag(self):
        if self.is_questioned():
            self.questioned = False
            self.label_art = None
        elif self.is_flagged():
            self.questioned = True
            self.flagged = False
            self.label_art = constants.S_QUESTION
        else:
            self.flagged = True
            self.label_art = constants.S_FLAG
            
    def is_mine(self):
        return(self.mine)
    def is_flagged(self):
        return(self.flagged)
    def is_questioned(self):
        return(self.questioned)

class screen:
    def __init__(self, name,
                 wid=constants.GAME_WIDTH,
                 hei=constants.GAME_HEIGHT):
        self.buttons = []
        self.active = False
        self.wid = wid
        self.hei = hei
        self.name = name
        self.surf = pygame.Surface((wid,hei))

    def set_BG(self,color):
        self.BG = color

    def is_pressed(self,x,y,MB):
        '''processes x,y coordinates of a mouse button press and the mouse
        button used to generate it.'''
        for b in self.buttons:
            b.is_pressed(x,y)

    def is_clicked(self,x,y,MB):
        for b in self.buttons:
            b.is_clicked(x,y,MB)

    def update(self):
        for b in self.buttons:
            b.update()

    def draw(self):
        self.surf.fill(self.BG)
        for b in self.buttons:
            b.draw()

    def add_button(self,new_button):
        self.buttons.append(new_button)

    def make_active(self):
        GO.active_screen = self.name
    
def quit_nicely():
    pygame.display.quit()
    pygame.quit()

def draw_game():
    GO.screens[GO.active_screen].draw()
    GO.SURFACE_MAIN.blit(GO.screens[GO.active_screen].surf,
                         (0,0))
    pygame.display.flip()

def update_game():
    GO.screens[GO.active_screen].update()

def game_main_loop():
    game_quit = False
    LMB_down = False
    RMB_down = False
    Simul_down = False
    L_click = None
    R_click = None
    Simul_click = None
    click_x = None
    click_y = None
    down_x = None
    down_y = None
    
    while not game_quit:
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                game_quit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if GO.active_screen == "intro":
                        GO.active_screen = "main"
                    elif GO.active_screen == "main":
                        GO.active_screen = "high"
                    elif GO.active_screen == "high":
                        GO.active_screen = "options"
                    elif GO.active_screen == "options":
                        GO.active_screen = "intro"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    LMB_down = True
                    down_x,down_y = event.pos
                elif event.button == 2:
                    RMB_down = True
                    down_x,down_y = event.pos
            if event.type == pygame.MOUSEBUTTONUP:
                click_x,click_y = event.pos
                if event.button == 1:
                    if RMB_down:
                        Simul_click = True
                    else:
                        L_click = True
                    LMB_down = False
                elif event.button == 3:
                    if LMB_down:
                        Simul_click = True
                    else:
                        R_click = True
                        print("Right click")
                    RMB_down = False

                else:
                    print("Mouse button {}".format(event.button))
                
        if LMB_down:
            GO.screens[GO.active_screen].is_pressed(down_x,down_y,"LEFT")
        if RMB_down:
            GO.screens[GO.active_screen].is_pressed(down_x,down_y,"RIGHT")
        if L_click:
            GO.screens[GO.active_screen].is_clicked(click_x,click_y,"LEFT")
            L_click = False
        if R_click:
            GO.screens[GO.active_screen].is_clicked(click_x,click_y,"RIGHT")
            R_click = False
                

        update_game()
        draw_game()
        GO.FPS.tick(60)
    quit_nicely()

def initialize_game():
    os.environ['SDL_VIDEO_WINDOW_POS'] = "5,35"
    pygame.init()
    pygame.display.set_icon(constants.S_BOMB)
    pygame.display.set_caption("Bomb Mopper")
    
    GO = game_object()
    GO.FPS = pygame.time.Clock()
    GO.SURFACE_MAIN = pygame.display.set_mode((constants.GAME_WIDTH,
                                               constants.GAME_HEIGHT))

    intro_screen = screen("intro",constants.GAME_WIDTH,constants.GAME_HEIGHT)
    high_score_screen = screen("high",constants.GAME_WIDTH,constants.GAME_HEIGHT)
    options_screen = screen("options",constants.GAME_WIDTH,constants.GAME_HEIGHT)
    main_screen = screen("main",constants.GAME_WIDTH,constants.GAME_HEIGHT)

    intro_screen.set_BG((0,200,0))
    high_score_screen.set_BG((0,0,200))
    options_screen.set_BG((200,0,0))
    main_screen.set_BG((100,100,0))

    GO.add_screen(intro_screen)
    GO.add_screen(high_score_screen)
    GO.add_screen(options_screen)
    GO.add_screen(main_screen)

    GO.get_puzzle(main_screen)

    # (self,art,pressed_art,label_art)
    new_button = button(64,32,
                        constants.S_LARGE_BUTTON,
                        constants.S_LARGE_BUTTON_PRESSED,
                        constants.S_NEW_BUTTON_LABEL,
                        main_screen.make_active)
    
    options_button = button(64,32,
                            constants.S_LARGE_BUTTON,
                            constants.S_LARGE_BUTTON_PRESSED,
                            constants.S_OPTION_BUTTON_LABEL,
                            options_screen.make_active)
    
    high_score_button = button(64,32,
                               constants.S_LARGE_BUTTON,
                               constants.S_LARGE_BUTTON_PRESSED,
                               constants.S_HIGH_BUTTON_LABEL,
                               high_score_screen.make_active)

    new_button.place(150,50,intro_screen)
    options_button.place(215,50,intro_screen)
    high_score_button.place(280,50,intro_screen)
    
    back_button = button(64,32,
                         constants.S_LARGE_BUTTON,
                         constants.S_LARGE_BUTTON_PRESSED,
                         constants.S_BACK_BUTTON_LABEL,
                         action = intro_screen.make_active)
    back_button2 = button(64,32,
                         constants.S_LARGE_BUTTON,
                         constants.S_LARGE_BUTTON_PRESSED,
                         constants.S_BACK_BUTTON_LABEL,
                         action = intro_screen.make_active)
    back_button3 = button(64,32,
                         constants.S_LARGE_BUTTON,
                         constants.S_LARGE_BUTTON_PRESSED,
                         constants.S_BACK_BUTTON_LABEL,
                         action = intro_screen.make_active)
    
    back_button.place(0,0,main_screen)
    back_button2.place(0,0,high_score_screen)
    back_button3.place(0,0,options_screen)

    for i,site in enumerate(GO.puzzle.grid):
        if site == 1:
            print("Bomb")
            new_site = Site(16,16,
                            constants.S_SITE,
                            constants.S_SITE_PRESSED,
                            None,
                            mine = True)
        else:
            print("Not a bomb")
            new_site = Site(16,16,
                            constants.S_SITE,
                            constants.S_SITE_PRESSED,
                            None,
                            mine = False)
        site_x = i%GO.puzzle.width
        site_y = int(i/GO.puzzle.width)
        new_site.setxy(site_x,site_y)
        site_art_x = constants.PUZZLE_PAD_X + site_x*16
        site_art_y = constants.PUZZLE_PAD_Y + site_y*16
        new_site.place(site_art_x,site_art_y,main_screen)
        GO.puzzle.buttons.append(new_site)
    GO.puzzle.set_numbers()
    
    
    return(GO)

if __name__ == "__main__":
    GO = initialize_game()

    game_main_loop()
