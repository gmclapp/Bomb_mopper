import pygame

GAME_WIDTH = 1280
GAME_HEIGHT = 640
PUZZLE_PAD_X = 10
PUZZLE_PAD_Y = 125
DIALOG_WIDTH = 360
DIALOG_HEIGHT = 180
DIALOG_ANCHOR_X = (GAME_WIDTH-DIALOG_WIDTH)/2
DIALOG_ANCHOR_Y = (GAME_HEIGHT-DIALOG_HEIGHT)/2

DEFAULT_BG = pygame.image.load("art/Screen background.png")
HIGHSCORE_BG = pygame.image.load("art/High Score background.png")
DIALOG_BG = pygame.image.load("art/Name Dialog.png")

S_BOMB = pygame.image.load("art/Bomb32.png")
SITE_SIZE = 32

S_LARGE_BUTTON = pygame.image.load("art/Large button32.png")
S_LARGE_BUTTON_PRESSED = pygame.image.load("art/Large button pressed32.png")
S_NEW_BUTTON_LABEL = pygame.image.load("art/New Game32.png")
S_BACK_BUTTON_LABEL = pygame.image.load("art/Back32.png")
S_HIGH_BUTTON_LABEL = pygame.image.load("art/High Score32.png")
S_OPTION_BUTTON_LABEL = pygame.image.load("art/Options32.png")
S_CONFIRM_BUTTON_LABEL = pygame.image.load("art/Confirm32.png")
S_NAME_ENTRY_BOX = pygame.image.load("art/Text entry box.png")

S_RADIO = pygame.image.load("art/Radio button32.png")
S_RADIO_SELECTED = pygame.image.load("art/Radio button selected32.png")

S_SITE = pygame.image.load("art/Button32.png")
S_SITE_PRESSED = pygame.image.load("art/Button32_Empty.png")
S_FLAG = pygame.image.load("art/Flag32.png")
S_EMPTY = pygame.image.load("art/Button32_Empty.png")
S_QUESTION = pygame.image.load("art/Question32.png")

S_NEW = pygame.image.load("art/New Game small32.png")
S_WON = pygame.image.load("art/Won game small32.png")

S_1 = pygame.image.load("art/1_32.png")
S_2 = pygame.image.load("art/2_32.png")
S_3 = pygame.image.load("art/3_32.png")
S_4 = pygame.image.load("art/4_32.png")
S_5 = pygame.image.load("art/5_32.png")
S_6 = pygame.image.load("art/6_32.png")
S_7 = pygame.image.load("art/7_32.png")
S_8 = pygame.image.load("art/8_32.png")
S_9 = pygame.image.load("art/Nine.png")
S_0 = pygame.image.load("art/Zero.png")

S_NUMBERS = {1:S_1,
             2:S_2,
             3:S_3,
             4:S_4,
             5:S_5,
             6:S_6,
             7:S_7,
             8:S_8,
             9:S_9,
             0:S_0}

S_TIMER = pygame.image.load("art/Timer32.png")
S_0_7SEG = pygame.image.load("art/0_7seg.png")
S_1_7SEG = pygame.image.load("art/1_7seg.png")
S_2_7SEG = pygame.image.load("art/2_7seg.png")
S_3_7SEG = pygame.image.load("art/3_7seg.png")
S_4_7SEG = pygame.image.load("art/4_7seg.png")
S_5_7SEG = pygame.image.load("art/5_7seg.png")
S_6_7SEG = pygame.image.load("art/6_7seg.png")
S_7_7SEG = pygame.image.load("art/7_7seg.png")
S_8_7SEG = pygame.image.load("art/8_7seg.png")
S_9_7SEG = pygame.image.load("art/9_7seg.png")

S_DIALOG = pygame.image.load("art/Name Dialog.png")
S_CONFIRM_LABEL = pygame.image.load("art/Confirm32.png")
S_TEXT_ENTRY = pygame.image.load("art/Text entry box.png")
