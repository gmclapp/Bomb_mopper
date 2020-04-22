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
        
class button:
    def __init__(self):
        self.pressed = False
        self.active = False
        self.clicked = False

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
            pass

    def draw(self):
        pass

    def is_clicked(self,mx,my):
        pass

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

    def update(self):
        pass

    def draw(self):
        GO.SURFACE_MAIN.fill(self.BG)

    def add_button(self,new_button):
        self.buttons.append(new_button)
    
def quit_nicely():
    pygame.display.quit()
    pygame.quit()

def draw_game():
    GO.screens[GO.active_screen].draw()
    pygame.display.flip()

def game_main_loop():
    game_quit = False
    LMB_down = False
    RMB_down = False
    Simul_down = False
    L_click = None
    R_click = None
    Simul_click = None
    
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
                
        if GO.active_screen == "intro":
            pass
        elif GO.active_screen == "main":
            pass
        elif GO.active_screen == "high":
            pass
        elif GO.active_screen == "options":
            pass
        else:
            print("No active screen!")
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

    new_button = button()
    options_button = button()
    high_score_button = button()

    new_button.place(0,50,intro_screen)
    options_button.place(300,50,intro_screen)
    high_score_button.place(600,50,intro_screen)
    
    back_button = button()
    back_button.place(0,0,main_screen)
    
    
    return(GO)

if __name__ == "__main__":
    GO = initialize_game()

    game_main_loop()
