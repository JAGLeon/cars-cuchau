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

def crear_car(imagen:pygame.Surface = None):
    car_images = [
        pygame.image.load("./src/assets/images/auto-1.png"),
        pygame.image.load("./src/assets/images/auto-2.png"),
        pygame.image.load("./src/assets/images/auto-3.png"),
        pygame.image.load("./src/assets/images/auto-4.png"),
        pygame.image.load("./src/assets/images/auto-5.png"),
        pygame.image.load("./src/assets/images/auto-6.png"),
        pygame.image.load("./src/assets/images/auto-7.png"),
        pygame.image.load("./src/assets/images/auto-8.png"),
        pygame.image.load("./src/assets/images/auto-9.png"),
        pygame.image.load("./src/assets/images/auto-10.png"),
    ]
    block = crear_bloque(choice(car_images),randint(MIN_WIDTH_PISTA,MAX_WIDTH_PISTA - CAR_W), randint(-HEIGHT,0 - CAR_H), CAR_W, CAR_H, YELLOW, 0, 0, 0) #randint(-HEIGHT,0 - CAR_H)
    block["speed_y"] = SPEED_Y_CAR
    return block

def crear_player(imagen:pygame.Surface = None):
    return crear_bloque(imagen,randint(MIN_WIDTH_PISTA,MAX_WIDTH_PISTA - CAR_W), HEIGHT, CAR_W, CAR_H, BLUE, 0, 0,0)

def crear_bonus_vida():
    block = crear_bloque(pygame.image.load("./src/assets/images/vida.png"),randint(MIN_WIDTH_PISTA,MAX_WIDTH_PISTA - CAR_W), randint(-HEIGHT,0 - CAR_H), 50, 50, YELLOW, 0, 0, 0) #randint(-HEIGHT,0 - CAR_H)
    block["speed_y"] = SPEED_Y_CAR
    return block

# def cargar_cars(lista, count_list):
#     for _ in range(count_list):
#         misma_posicion = True
#         while misma_posicion:
#             car = crear_car()
#             if not distancia_entre_autos(car, lista):
#                 lista.append(car)
#                 misma_posicion = False

