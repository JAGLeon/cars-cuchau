import pygame

PATH_IMG = "./src/assets/images/"
PATH_SOUND = "./src/assets/sounds/"
PATH_MUSIC = "./src/assets/music/"
PATH_JSON = "./src/memory_card/json/"
PATH_CSV = "./src/memory_card/csv/"


WIDTH = 800
HEIGHT = 600

MAX_WIDTH_PISTA = 667
MIN_WIDTH_PISTA = 145 

SIZE_SCREEN = (WIDTH,HEIGHT)
MID_WIDTH_SCREEN = WIDTH // 2
MID_HEIGHT_SCREEN = HEIGHT // 2

HIGHT_SCORE = POSITION_TITLE = (20,50)
LAST_SCORE = (700,50)

CENTER_SCREEN = (MID_WIDTH_SCREEN,MID_HEIGHT_SCREEN)
FPS = 60
SPEED = 5
COLISION = 150
MAX_CARS_SCREEN = 6

SHIELD_X = 5
SHIELD_Y = 90

POSITION_TITLE = (MID_WIDTH_SCREEN,50)
POSITION_LVL = (745,50)
POSITION_LIVES = (5,25)
POSITION_CANT_LIVES = (80,50)
POSITION_SHIELD = (SHIELD_X,SHIELD_Y) 
POSITION_CANT_SHIELDS = (80,120)
POSITION_ACTIVO_SHIELD = (60,160)
POSITION_MUTE = (30,HEIGHT - 70)


BLUE =    (0  ,  0,255)
RED =     (255  ,0,  0)
GREEN =   (0  ,255,  0)
WHITE =   (255,255,255)
BLACK =   (0  ,  0,  0)
CYAN =    (0  ,255,255)
YELLOW =  (255,255,  0)
MAGENTA = (255,  0,255)
CUSTOM =  (108,221, 38)

CAR_W = 100
CAR_H = 150

SMALL_CAR_W = 50
SMALL_CAR_H = 100

BONUS_W = 50
BONUS_H = 50

COLORS = [BLUE,RED,GREEN,WHITE,BLACK,CYAN,YELLOW,MAGENTA]

SPEED_Y_CAR= 3

START_BUTTON_SIZE = (200,200)

TIME_INMORTAL = 3000
TIME_SMALL_CAR = 3000
TIME_BONUS = 5000
TIME_AUTOS = 2000
TIME_LVL = 10000
LVL_UP_VELOCITY = 0.20
DELAY_COLISION = 50

 
IMG_FONDO_Y = 0
SCROLL_SPEED = 10

POSITION_PLAY = (295,200)

POSITION_QUIT = (295,300)
