import pygame
from settings import *
from random import randint,choice
from colisiones import *


def crear_bloque(imagen:pygame.Surface = None,left = 0,top = 0,width = 50,height = 50,color = WHITE,dir = 3,borde = 0,radio = -1):
    if imagen:
        imagen = pygame.transform.scale(imagen, (width,height))

    return {
            "rect": pygame.Rect(left,top,width,height),
            "color": color,
            "dir": dir,
            "borde":borde,
            "radio":radio,
            "img": imagen
           }

def crear_car():
    block = crear_bloque(image_car_random(),randint(MIN_WIDTH_PISTA,MAX_WIDTH_PISTA - CAR_W), randint(-HEIGHT,0 - CAR_H), CAR_W, CAR_H, YELLOW, 0, 0, 0)
    block["speed_y"] = SPEED_Y_CAR
    return block

def crear_player(imagen:pygame.Surface = None):
    return crear_bloque(imagen,randint(MIN_WIDTH_PISTA,MAX_WIDTH_PISTA - CAR_W), HEIGHT, CAR_W, CAR_H, BLUE, 0, 0,0)

def crear_bonus(img,speed):
    block = crear_bloque(img,randint(MIN_WIDTH_PISTA,MAX_WIDTH_PISTA - BONUS_W), randint(-HEIGHT,0 - BONUS_H), 50, 50, YELLOW, 0, 0, 0)
    block["speed_y"] = speed
    return block

def image_car_random():
    car_images = [
        pygame.image.load(f"{PATH_IMG}auto-1.png"),
        pygame.image.load(f"{PATH_IMG}auto-2.png"),
        pygame.image.load(f"{PATH_IMG}auto-3.png"),
        pygame.image.load(f"{PATH_IMG}auto-4.png"),
        pygame.image.load(f"{PATH_IMG}auto-5.png"),
        pygame.image.load(f"{PATH_IMG}auto-6.png"),
        pygame.image.load(f"{PATH_IMG}auto-7.png"),
        pygame.image.load(f"{PATH_IMG}auto-8.png"),
        pygame.image.load(f"{PATH_IMG}auto-9.png"),
        pygame.image.load(f"{PATH_IMG}auto-10.png"),
    ]
    return choice(car_images)

