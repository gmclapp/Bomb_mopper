import random
import pygame
import constants
import os
import time
import datetime as dt
import json

class game_object:
    def __init__(self):
        self.active_screen = "intro" # intro, main, high, options
        self.screens = {}
        self.dialogs = {}
        self.won = False
        self.lost = False
        self.wid = 6
        self.hei = 6
        self.mines = 6
        self.game_mode = Var()
        self.highscore_mode = Var()
        self.highscore_flags = Var()
        
        self.time = stringVar()
        self.bombs = stringVar()

        self.timer = None
        self.bomb_counter = None
    
        self.puzzle = None
        self.load_stats()
        self.score_labels = []

        # Stats variables for pending win data entry  

    def load_stats(self):
        try:
            with open('stats.txt','r') as f:
                self.stats = json.load(f)
                for i in self.stats["Beginner"]:
                    if not ("Player" in i):
                        i["Player"]="Unknown"
                    if not ("Flags" in i):
                        i["Flags"]=True
                        
                for i in self.stats["Intermediate"]:
                    if not ("Player" in i):
                        i["Player"]="Unknown"
                    if not ("Flags" in i):
                        i["Flags"]=True
                        
                for i in self.stats["Expert"]:
                    if not ("Player" in i):
                        i["Player"]="Unknown"
                    if not ("Flags" in i):
                        i["Flags"]=True
                    
        except FileNotFoundError:
            self.stats = {'Beginner': [],
                          'Intermediate': [],
                          'Expert':[]}
            self.save_stats()
            
    def save_stats(self):
        with open('stats.txt','w') as f:
            f.write(json.dumps(self.stats,indent=4))
    
    def add_screen(self,new_screen):
        key = new_screen.name
        val = new_screen
        
        self.screens[key] = val

    def add_dialog(self,new_dialog):
        key = new_dialog.name
        val = new_dialog
        
        self.dialogs[key] = val
        
    def get_puzzle(self):
        if self.puzzle:
            for b in self.puzzle.buttons:
                self.screens['main'].remove_button(b)
        self.puzzle = Puzzle(self.wid,self.hei,self.mines,self)
        self.puzzle.place(0,0,self.screens['main'])
        self.lost = False
        self.won = False

    def refresh_scores(self):
        player_name_x_anchor = 10
        score_x_anchor = 507
        date_x_anchor = 900
        
        y_anchor = 114
        
        difficulty_dict = {0:"Beginner",
                           1:"Intermediate",
                           2:"Expert",
                           3:"Custom"}
        difficulty = difficulty_dict[self.highscore_mode.get()]
        
        for i in self.score_labels:
            self.screens['high'].remove_button(i)
            
        self.score_labels = []
        self.stats["Beginner"].sort(key=lambda x: x["Score"],reverse=False)
        self.stats["Intermediate"].sort(key=lambda x: x["Score"],reverse=False)
        self.stats["Expert"].sort(key=lambda x: x["Score"],reverse=False)

        for i in range(20):
            try:
                y_anchor_temp = y_anchor+16*(i+1)
                player_label_str = '{:2}. {}'.format(i+1,self.stats[difficulty][i]["Player"])
                score_label_str = '{:4.2f}'.format(self.stats[difficulty][i]["Score"])
                date_label_str = '{}'.format(self.stats[difficulty][i]["Date"])

                player_label = Label(stringVar(player_label_str))
                score_label = Label(stringVar(score_label_str))
                date_label = Label(stringVar(date_label_str))

                player_label.place(player_name_x_anchor,y_anchor_temp,self.screens['high'])
                score_label.place(score_x_anchor,y_anchor_temp,self.screens['high'])
                date_label.place(date_x_anchor,y_anchor_temp,self.screens['high'])

                self.score_labels.append(player_label)
                self.score_labels.append(score_label)
                self.score_labels.append(date_label)
            except IndexError:
                break

    def change_active_screen(self,screen):
        if self.active_screen != screen:
            self.active_screen = screen
            if screen == 'main':
                self.get_puzzle()

            else:
                pass        

    def update(self):
        if self.game_mode.get() == 0: # Beginner
            self.wid = 9
            self.hei = 9
            self.mines = 10
        elif self.game_mode.get() == 1: # Intermediate
            self.wid = 16
            self.hei = 16
            self.mines = 40
        elif self.game_mode.get() == 2: # Expert
            self.wid = 32
            self.hei = 16
            self.mines = 99
        elif self.game_mode.get() == 3: # Custom
            pass
        if not self.puzzle.finished:
            self.current_time = time.time() - self.puzzle.start_time
            self.time.set("{:4.2f}".format(self.current_time))
        if self.timer:
            self.timer.update(self.current_time)
        if self.bomb_counter:
            self.bomb_counter.update(int(self.bombs.get()))
            
    def attach_timer(self,timer):
        self.timer = timer
    def attach_bombcount(self,timer):
        self.bomb_counter = timer

class Puzzle:
    def __init__(self,wid,hei,mines,GO):
         
        self.width = wid
        self.height = hei
        self.mines = mines
        GO.bombs.set(mines)
        self.buttons = []
        self.grid = []
        self.start_time = time.time()
        self.finish_time = None
        self.finished = False
        self.flags = False
        
        for i,item in enumerate(range(self.width*self.height)):
            if i < self.mines:
                self.grid.append(1)
            else:
                self.grid.append(0)
        random.shuffle(self.grid)                    
        
        for i,site in enumerate(self.grid):
            if site == 1:
                new_site = Site(constants.SITE_SIZE,constants.SITE_SIZE,
                                constants.S_SITE,
                                constants.S_SITE_PRESSED,
                                None,
                                mine = True)
            else:
                new_site = Site(32,32,
                                constants.S_SITE,
                                constants.S_SITE_PRESSED,
                                None,
                                mine = False)
            site_x = i%self.width
            site_y = int(i/self.width)
            new_site.setxy(site_x,site_y)
            site_art_x = constants.PUZZLE_PAD_X + site_x*constants.SITE_SIZE
            site_art_y = constants.PUZZLE_PAD_Y + site_y*constants.SITE_SIZE
            new_site.place(site_art_x,site_art_y,GO.screens['main'])
            self.buttons.append(new_site)
        self.set_numbers()

    def __str__(self):
        string = ''
        for i,b in enumerate(self.buttons):
            if b.is_mine():
                string += ' * '
            else:
                string += ' {} '.format(b.neighbor_mines)
            if i%self.width == self.width-1:
                string += '\n'
        return(string)
                
    

    def place(self,x,y,screen):
        self.x = x
        self.y = y
        self.screen = screen

    def is_mine(self,x,y):
        index = y*self.width + x
        return(self.buttons[index].is_mine())

    def open(self,x,y):
        if 0 <= x < self.width and 0 <= y < self.height:
            index = y*self.width + x
            if not self.buttons[index].is_opened():
                self.buttons[index].open()

    def chain_reaction(self):
        for b in self.buttons:
            if b.is_mine() and not b.is_opened():
                b.open()

    def win_check(self):
        count = 0
        for b in self.buttons:
            if not b.is_mine() and not b.is_opened():
                count += 1
        if count == 0:
            GO.won = True
            
    def set_numbers(self):
        for s in self.buttons:
            s.neighbor_mines = 0
            for i in range(-1,2):
                for j in range(-1,2):
                    if i == 0 and j == 0:
                        pass
                    elif s.grid_x+i < 0 or s.grid_x+i > self.width-1:
                        pass
                    elif s.grid_y+j < 0 or s.grid_y+j > self.height-1:
                        pass
                    else:
                        if self.is_mine(s.grid_x+i,s.grid_y+j):
                            s.neighbor_mines += 1
        
class button:
    def __init__(self,wid,hei,art,pressed_art,label_art,action=None,RMB_action=None,Simul_action=None):
        self.pressed = False
        self.active = False
        self.clicked = False
        self.Rclicked = False
        self.Simul_clicked = False
        
        self.wid = wid
        self.hei = hei

        self.art = art
        self.pressed_art = pressed_art
        self.label_art = label_art
        self.action = action
        self.RMB_action = RMB_action
        self.Simul_action = Simul_action

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
            self.pressed = False
        if self.Rclicked:
            if self.RMB_action:
                self.RMB_action()
            else:
                print("No action assigned to right mouse button")
            self.Rclicked = False
            self.pressed = False
            
        if self.Simul_clicked:
            if self.Simul_action:
                self.Simul_action()
            else:
                print("No action assigned to a simultaneous click.")
                self.Simul_clicked = False
                self.pressed = False

    def draw(self):
        if self.pressed:
            self.screen.surf.blit(self.pressed_art,(self.x,self.y))
        else:
            self.screen.surf.blit(self.art,(self.x,self.y))
        if self.label_art:
            self.screen.surf.blit(self.label_art,(self.x,self.y))

    def is_clicked(self,mx,my,MB):
        mx -= self.screen.x
        my -= self.screen.y
        if self.x < mx < self.x + self.wid and self.y < my < self.y + self.hei:
            if MB == "LEFT":
                self.clicked = True
            if MB == "RIGHT":
                self.Rclicked = True
            if MB == "BOTH":
                self.Simul_clicked = True
        else:
            self.clicked = False

    def is_pressed(self,mx,my):
        if self.x < mx < self.x + self.wid and self.y < my < self.y + self.hei:
            self.pressed = True
        else:
            self.pressed = False

class Label(button):
    def __init__(self,text):
        super().__init__(0,0,None,None,None,action=None,RMB_action=None)
        self.text = text
        self.font = pygame.font.SysFont("Arial",16)
        self.txt_surface = self.font.render(self.text.get(),True,(0,0,0),16)

    def draw(self):
        self.font = pygame.font.SysFont("Arial",16)
        self.txt_surface = self.font.render(self.text.get(),True,(0,0,0),16)
        self.screen.surf.blit(self.txt_surface,(self.x,self.y))
        
class RadioButtonManager:
    '''Object which controls multiple radio buttons. Pass a Var which is an integer
    this manager will set to indicate which button out of the list of buttons it is
    managing is currently active.'''
    def __init__(self,var):
        self.var = var
        self.button_list = []
        self.action = None

    def add_button(self,button):
        button.setParent(self)
        button.setIndex(len(self.button_list))
        self.button_list.append(button)

    def toggle_button(self,index):
        '''Called by one of the buttons in the button list, this tells the parent object to
        turn off other buttons in the manager if they're active.'''
        self.var.set(index)
        for b in self.button_list:
            if b.index == index:
                b.art = constants.S_RADIO_SELECTED
                b.pressed_art = constants.S_RADIO_SELECTED
            else:
                b.art = constants.S_RADIO
                b.pressed_art = constants.S_RADIO
        if self.action:
            self.action()

    def action_on_change(self,action=None):
        '''Pass a function to this function and that function will be excecuted any time
        The radio button manager switches state from one selection to another.'''
        self.action = action

class Radiobutton(button):
    def __init__(self,wid,hei,art,pressed_art,label_art,action=None,RMB_action=None):
        super().__init__(wid,hei,art,pressed_art,label_art,action=self.toggle_var,RMB_action=None)
        self.label = None
        
    def toggle_var(self):
        '''Tells the parent manager that this button has been pushed so it can reassign update the
        relevant variable.'''
        self.parent.toggle_button(self.index)

    def setParent(self,parent):
        '''Pass the RadioButtonManager which will control this radio button.
        Only one radio button controlled by a given RadioButtonManager can be active at a time.'''
        self.parent = parent

    def setIndex(self,index):
        self.index = index

    def set_label(self,label_txt):
        '''Pass a string which will be displayed next to this radio button.'''
        self.label = Label(stringVar(label_txt))
        self.label.place(self.x + 32,self.y+8,self.screen)

    def draw(self):
        super().draw()
        if self.label:
            self.label.draw()
        

class Var:
    def __init__(self):
        self.val = 0

    def set(self,new):
        self.val = new

    def get(self):
        return(self.val)

class stringVar:
    def __init__(self,val=''):
        self.val = val
    def __str__(self):
        return(self.val)
    def set(self,new):
        self.val = str(new)
    def get(self):
        return(self.val)

class Site(button):
    def __init__(self,wid,hei,art,pressed_art,label_art,action=None,RMB_action=None,Simul_action=None,mine=False):
        super().__init__(wid,hei,art,pressed_art,label_art,action=self.open,RMB_action=self.flag,Simul_action=self.open_neighbors)
        self.mine = mine
        self.flagged = False
        self.questioned = False
        self.opened = False
        self.neighbor_mines = 0

    def setxy(self,x,y):
        self.grid_x = x
        self.grid_y = y

    def open(self):
        if not self.is_opened() and not self.is_flagged() and not self.is_questioned() and not GO.puzzle.finished:
            self.opened = True
            self.art = constants.S_EMPTY
            self.pressed_art = constants.S_EMPTY
            if self.is_mine():
                self.label_art = constants.S_BOMB
                GO.lost = True
            else:
                if self.neighbor_mines == 0:
                    self.open_neighbors()
                else:
                    self.label_art = constants.S_NUMBERS[self.neighbor_mines]
            
                return(self.neighbor_mines)
    def open_neighbors(self):
        for i in range(-1,2):
            for j in range (-1,2):
                if not (i == 0 and j == 0):
                    GO.puzzle.open(self.grid_x+i,self.grid_y+j)

    def flag(self):
        if not self.is_opened() and not GO.puzzle.finished:
            if self.is_questioned():
                self.questioned = False
                self.label_art = None
            elif self.is_flagged():
                self.questioned = True
                self.flagged = False
                GO.bombs.set(int(GO.bombs.get()) + 1)
                self.label_art = constants.S_QUESTION
            else:
                self.flagged = True
                GO.puzzle.flags = True
                GO.bombs.set(int(GO.bombs.get()) - 1)
                self.label_art = constants.S_FLAG
            
    def is_mine(self):
        return(self.mine)
    def is_flagged(self):
        return(self.flagged)
    def is_questioned(self):
        return(self.questioned)
    def is_opened(self):
        return(self.opened)

class screen:
    def __init__(self, name, x=0, y=0,
                 wid=constants.GAME_WIDTH,
                 hei=constants.GAME_HEIGHT):
        self.buttons = []
        self.sprites = []
        self.active = False
        self.x = x
        self.y = y
        self.wid = wid
        self.hei = hei
        self.name = name
        self.surf = pygame.Surface((wid,hei))

    def set_BG(self,background):
        self.BG = background

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
        self.surf.blit(self.BG,(0,0))
        for b in self.buttons:
            b.draw()
        for s in self.sprites:
            s.draw()

    def add_button(self,new_button):
        self.buttons.append(new_button)

    def remove_button(self,button):
        self.buttons.remove(button)

    def add_sprite(self,new_sprite):
        self.sprites.append(new_sprite)

    def remove_sprite(self,sprite):
        self.sprites.remove(sprite)
        
    def make_active(self):
        GO.change_active_screen(self.name)

class Dialog(screen):
    def __init__(self, name, x=0, y=0,
                 wid=constants.GAME_WIDTH,
                 hei=constants.GAME_HEIGHT):
        super().__init__(name, x, y,
                         wid,
                         hei)
class timer:
    def __init__(self,wid,hei,art):
        self.wid=wid
        self.height=hei
        self.art=art
        self.digit_dict = {0: constants.S_0_7SEG,
                           1: constants.S_1_7SEG,
                           2: constants.S_2_7SEG,
                           3: constants.S_3_7SEG,
                           4: constants.S_4_7SEG,
                           5: constants.S_5_7SEG,
                           6: constants.S_6_7SEG,
                           7: constants.S_7_7SEG,
                           8: constants.S_8_7SEG,
                           9: constants.S_9_7SEG}
        
        self.number = 0000.0 # The number that the timer will display
        self.dig1 = self.digit_dict[int(self.number//1000)]
        self.dig2 = self.digit_dict[int((self.number%1000)//100)]
        self.dig3 = self.digit_dict[int((self.number%100)//10)]
        self.dig4 = self.digit_dict[int((self.number%10)//1)]

    def place(self,x,y,screen):
        self.x = x
        self.y = y
        self.screen = screen
        screen.add_sprite(self)
        
    def draw(self):
        self.screen.surf.blit(self.art,(self.x,self.y))
        self.screen.surf.blit(self.dig1,(self.x+35,self.y+12))
        self.screen.surf.blit(self.dig2,(self.x+107,self.y+12))
        self.screen.surf.blit(self.dig3,(self.x+178,self.y+12))
        self.screen.surf.blit(self.dig4,(self.x+251,self.y+12))
        
    def update(self,number=0000.0):
        self.number = number
        try:
            self.dig1 = self.digit_dict[int(self.number//1000)]
            self.dig2 = self.digit_dict[int((self.number%1000)//100)]
            self.dig3 = self.digit_dict[int((self.number%100)//10)]
            self.dig4 = self.digit_dict[int((self.number%10)//1)]
        except KeyError:
            pass
        
        
def parse_date(date):
    year,month,day = [int(x) for x in date.split('-')]
    d = dt.date(year,month,day)
    return(d)

def unpack_date(date):
    year=date.year
    month=date.month
    day=date.day
    return(year,month,day)

def quit_nicely():
    pygame.display.quit()
    pygame.quit()

def draw_game():
    GO.screens[GO.active_screen].draw()
    
            
    GO.SURFACE_MAIN.blit(GO.screens[GO.active_screen].surf,
                         (0,0))
    for Diag in GO.dialogs:
        if GO.dialogs[Diag].active:
            GO.dialogs[Diag].draw()
            GO.SURFACE_MAIN.blit(GO.dialogs[Diag].surf,
                                 (GO.dialogs[Diag].x,GO.dialogs[Diag].y))
    pygame.display.flip()

def lose_game():
    print("You Lose!")
    GO.puzzle.chain_reaction()
    GO.lost = False

def win_game():
    GO.dialogs["name"].active = True
    
def record_win():
    print("You win!")
    win_time = GO.current_time
    win_date = unpack_date(dt.date.today())
    win_flags = GO.puzzle.flags
    modes = {0:'Beginner',
             1:'Intermediate',
             2:'Expert',
             3:'Custom'}
    
    GO.stats[modes[GO.game_mode.get()]].append({"Date":win_date,
                                                "Score":win_time,
                                                "Flags":win_flags,
                                                "Player":win_player})
    GO.save_stats()
    GO.refresh_scores()
    
def update_game():
    if GO.lost and not GO.puzzle.finished:
        lose_game()
        GO.puzzle.finished = True
    elif GO.won and not GO.puzzle.finished:
        win_game()
        GO.puzzle.finished = True
    else:
        GO.puzzle.win_check()
    GO.update()
    GO.screens[GO.active_screen].update()
    for Diag in GO.dialogs:
        if GO.dialogs[Diag].active:
            GO.dialogs[Diag].update()

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
                elif event.button == 3:
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
                    RMB_down = False

                else:
                    print("Mouse button {}".format(event.button))
                
        if LMB_down:
            Dialog_active = False
            for Diag in GO.dialogs:
                if GO.dialogs[Diag].active:
                    Dialog_active = True
                    GO.dialogs[Diag].is_pressed(down_x,down_y,"LEFT")
            if not Dialog_active:
                GO.screens[GO.active_screen].is_pressed(down_x,down_y,"LEFT")
                
        if RMB_down:
            Dialog_active = False
            for Diag in GO.dialogs:
                if GO.dialogs[Diag].active:
                    Dialog_active = True
                    GO.dialogs[Diag].is_pressed(down_x,down_y,"RIGHT")
            if not Dialog_active:
                GO.screens[GO.active_screen].is_pressed(down_x,down_y,"RIGHT")

        if L_click:
            Dialog_active = False
            for Diag in GO.dialogs:
                if GO.dialogs[Diag].active:
                    Dialog_active = True
                    GO.dialogs[Diag].is_clicked(click_x,click_y,"LEFT")
            if not Dialog_active:
                GO.screens[GO.active_screen].is_clicked(click_x,click_y,"LEFT")
            L_click = False
                
        if R_click:
            Dialog_active = False
            for Diag in GO.dialogs:
                if GO.dialogs[Diag].active:
                    Dialog_active = True
                    GO.dialogs[Diag].is_clicked(click_x,click_y,"RIGHT")
            if not Dialog_active:
                GO.screens[GO.active_screen].is_clicked(click_x,click_y,"RIGHT")
            R_click = False
        if Simul_click:
            Dialog_active = False
            for Diag in GO.dialogs:
                if GO.dialogs[Diag].active:
                    Dialog_active = True
                    GO.dialogs[Diag].is_clicked(click_x,click_y,"BOTH")
            if not Dialog_active:
                GO.screens[GO.active_screen].is_clicked(click_x,click_y,"BOTH")
            Simul_click = False
                

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

    # Build game screens
    intro_screen = screen("intro",0,0,constants.GAME_WIDTH,constants.GAME_HEIGHT)
    high_score_screen = screen("high",0,0,constants.GAME_WIDTH,constants.GAME_HEIGHT)
    options_screen = screen("options",0,0,constants.GAME_WIDTH,constants.GAME_HEIGHT)
    main_screen = screen("main",0,0,constants.GAME_WIDTH,constants.GAME_HEIGHT)

    # Build dialog boxes
    name_entry = Dialog("name",constants.DIALOG_ANCHOR_X,
                        constants.DIALOG_ANCHOR_Y,
                        constants.DIALOG_WIDTH,
                        constants.DIALOG_HEIGHT)

    # Set background art for screens and dialog boxes
    intro_screen.set_BG(constants.DEFAULT_BG)
    high_score_screen.set_BG(constants.HIGHSCORE_BG)
    options_screen.set_BG(constants.DEFAULT_BG)
    main_screen.set_BG(constants.DEFAULT_BG)
    name_entry.set_BG(constants.DIALOG_BG)

    # Attach screens and dialog boxes to the game object
    GO.add_screen(intro_screen)
    GO.add_screen(high_score_screen)
    GO.add_screen(options_screen)
    GO.add_screen(main_screen)
    GO.add_dialog(name_entry)

    # Get a new puzzle
    GO.get_puzzle()

    # Build buttons for screens and dialog boxes
    new_button = button(128,64,
                        constants.S_LARGE_BUTTON,
                        constants.S_LARGE_BUTTON_PRESSED,
                        constants.S_NEW_BUTTON_LABEL,
                        main_screen.make_active)
    
    options_button = button(128,64,
                            constants.S_LARGE_BUTTON,
                            constants.S_LARGE_BUTTON_PRESSED,
                            constants.S_OPTION_BUTTON_LABEL,
                            options_screen.make_active)
    
    high_score_button = button(128,64,
                               constants.S_LARGE_BUTTON,
                               constants.S_LARGE_BUTTON_PRESSED,
                               constants.S_HIGH_BUTTON_LABEL,
                               high_score_screen.make_active)

    new_button.place(256,288,intro_screen)
    options_button.place(576,288,intro_screen)
    high_score_button.place(896,288,intro_screen)
    
    back_button = button(128,64,
                         constants.S_LARGE_BUTTON,
                         constants.S_LARGE_BUTTON_PRESSED,
                         constants.S_BACK_BUTTON_LABEL,
                         action = intro_screen.make_active)
    back_button2 = button(128,64,
                         constants.S_LARGE_BUTTON,
                         constants.S_LARGE_BUTTON_PRESSED,
                         constants.S_BACK_BUTTON_LABEL,
                         action = intro_screen.make_active)
    back_button3 = button(128,64,
                         constants.S_LARGE_BUTTON,
                         constants.S_LARGE_BUTTON_PRESSED,
                         constants.S_BACK_BUTTON_LABEL,
                         action = intro_screen.make_active)
    new_button_small = button(32,32,
                        constants.S_SITE,
                        constants.S_SITE_PRESSED,
                        constants.S_NEW,
                        action = GO.get_puzzle)

    confirm_button = button(128,64,
                            constants.S_LARGE_BUTTON,
                            constants.S_LARGE_BUTTON_PRESSED,
                            constants.S_CONFIRM_BUTTON_LABEL,
                            action = record_win)

    # Attach buttons to screens and dialog boxes
    back_button.place(10,10,main_screen)
    new_button_small.place(constants.GAME_WIDTH/2,20,main_screen)
    back_button2.place(10,10,high_score_screen)
    back_button3.place(10,10,options_screen)
    confirm_button.place((constants.DIALOG_WIDTH-128)/2,
                         (constants.DIALOG_HEIGHT-64)/2,
                         name_entry)

    # Build game mode radio buttons
    beginner_button = Radiobutton(constants.SITE_SIZE,constants.SITE_SIZE,
                                  constants.S_RADIO,
                                  constants.S_RADIO,
                                  None)
    intermediate_button = Radiobutton(constants.SITE_SIZE,constants.SITE_SIZE,
                                  constants.S_RADIO,
                                  constants.S_RADIO,
                                  None)
    expert_button = Radiobutton(constants.SITE_SIZE,constants.SITE_SIZE,
                                  constants.S_RADIO,
                                  constants.S_RADIO,
                                  None)
    custom_button = Radiobutton(constants.SITE_SIZE,constants.SITE_SIZE,
                                  constants.S_RADIO,
                                  constants.S_RADIO,
                                  None)

    
    game_mode_manager = RadioButtonManager(GO.game_mode)
    game_mode_manager.add_button(beginner_button)
    game_mode_manager.add_button(intermediate_button)
    game_mode_manager.add_button(expert_button)
    game_mode_manager.add_button(custom_button)
    beginner_button.toggle_var() # On start up, this button will be selected.

    beginner_button.place(40,80,options_screen)
    intermediate_button.place(40,120,options_screen)
    expert_button.place(40,160,options_screen)
    custom_button.place(40,200,options_screen)

    beginner_button.set_label("Beginner")
    intermediate_button.set_label("Intermediate")
    expert_button.set_label("Expert")
    custom_button.set_label("Custom")

    # Build high score screen radio buttons
    beg_scores_button = Radiobutton(constants.SITE_SIZE,constants.SITE_SIZE,
                                    constants.S_RADIO,
                                    constants.S_RADIO,
                                    None)
    int_scores_button = Radiobutton(constants.SITE_SIZE,constants.SITE_SIZE,
                                    constants.S_RADIO,
                                    constants.S_RADIO,
                                    None)
    expert_scores_button = Radiobutton(constants.SITE_SIZE,constants.SITE_SIZE,
                                    constants.S_RADIO,
                                    constants.S_RADIO,
                                    None)
    custom_scores_button = Radiobutton(constants.SITE_SIZE,constants.SITE_SIZE,
                                    constants.S_RADIO,
                                    constants.S_RADIO,
                                    None)

    beg_scores_button.place(142,10,high_score_screen)
    int_scores_button.place(142,41,high_score_screen)
    expert_scores_button.place(276,10,high_score_screen)
    custom_scores_button.place(276,41,high_score_screen)

    beg_scores_button.set_label("Beginner")
    int_scores_button.set_label("Intermediate")
    expert_scores_button.set_label("Expert")
    custom_scores_button.set_label("Custom")
    
    high_mode_manager = RadioButtonManager(GO.highscore_mode)
    high_mode_manager.add_button(beg_scores_button)
    high_mode_manager.add_button(int_scores_button)
    high_mode_manager.add_button(expert_scores_button)
    high_mode_manager.add_button(custom_scores_button)
    beg_scores_button.toggle_var()# This button will be selected on start up
    high_mode_manager.action_on_change(GO.refresh_scores)
    
    # Build flags vs. no flags options for high scores
    flags_button = Radiobutton(constants.SITE_SIZE,constants.SITE_SIZE,
                                    constants.S_RADIO,
                                    constants.S_RADIO,
                                    None)
    no_flags_button = Radiobutton(constants.SITE_SIZE,constants.SITE_SIZE,
                                    constants.S_RADIO,
                                    constants.S_RADIO,
                                    None)

    flags_button.place(500,10,high_score_screen)
    no_flags_button.place(500,41,high_score_screen)

    flags_button.set_label("Flags")
    no_flags_button.set_label("No flags")
    

    flag_mode_manager = RadioButtonManager(GO.highscore_flags)
    flag_mode_manager.add_button(flags_button)
    flag_mode_manager.add_button(no_flags_button)
    flags_button.toggle_var()# This button will be selected on start up
    flag_mode_manager.action_on_change(GO.refresh_scores)
    

    # Build game screen timers and counters  
    time_display = timer(345,126,constants.S_TIMER)
    time_display.place(142, 10, main_screen)
    GO.attach_timer(time_display)

    bomb_display = timer(345,126,constants.S_TIMER)
    bomb_display.place(750,10,main_screen)
    GO.attach_bombcount(bomb_display)

    # Build highscore tables
    beginner_scores_label = Label(stringVar("Beginner"))
    intermediate_scores_label = Label(stringVar("Intermediate"))
    expert_scores_label = Label(stringVar("Expert"))

    beginner_anchor = 32
    intermediate_anchor = 300
    expert_anchor = 600
    
    GO.refresh_scores()
    return(GO)

if __name__ == "__main__":
    GO = initialize_game()

    game_main_loop()
