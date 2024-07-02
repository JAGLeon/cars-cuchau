import pygame
from settings import *
from random import randint,choice
from aleatorios import *
from bloques import *
from colisiones import *
from interacciones import *
from pygame.locals import *

img_fondo = pygame.image.load("./src/assets/images/fondo.png")
img_fondo = pygame.transform.scale(img_fondo,SIZE_SCREEN)
img_player = pygame.image.load("./src/assets/images/player.png")
# Carga todas las imágenes de autos en una lista


# Selecciona una imagen de auto al azar
pygame.init()

#Tamaño de pantalla
SCREEN = pygame.display.set_mode(SIZE_SCREEN)
#Nombre del juego
pygame.display.set_caption("Cars Cuchau")

#Jugador
player = crear_player(img_player)
#autos
cars = []
cargar_cars(cars,INITIAL_CARS)
#Direcciones
move_left = True
move_right = True
move_up = True
move_down = True


#Comienzo del juego
clock = pygame.time.Clock()
is_running = True
while is_running:
    #Frames
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == KEYDOWN:
            if event.key == K_DOWN or event.key == K_s:
                move_down = True
                move_up = False
            if event.key == K_UP or event.key == K_w:
                move_up = True
                move_down = False
            if event.key == K_LEFT or event.key == K_a:
                move_left = True
                move_right = False
            if event.key == K_RIGHT or event.key == K_d:
                move_right = True
                move_left = False

        if event.type == KEYUP:
            if event.key == K_DOWN or event.key == K_s:
                move_down = False
            if event.key == K_UP or event.key == K_w:
                move_up = False
            if event.key == K_LEFT or event.key == K_a:
                move_left = False
            if event.key == K_RIGHT or event.key == K_d:
                move_right = False

    #movimientos
    if move_left and player["rect"].left > MIN_WIDTH_PISTA:
        player["rect"].x -= SPEED
        if player["rect"].left < MIN_WIDTH_PISTA:
            player["rect"].left = MIN_WIDTH_PISTA
    if move_right and player["rect"].right < MAX_WIDTH_PISTA:
        player["rect"].x += SPEED
        if player["rect"].right > MAX_WIDTH_PISTA:
            player["rect"].right = MAX_WIDTH_PISTA
    if move_up and player["rect"].top > 0:
        player["rect"].y -= SPEED
        if player["rect"].top < 0:
            player["rect"].top = 0
    if move_down and player["rect"].bottom < HEIGHT:
        player["rect"].y += SPEED
        if player["rect"].bottom > HEIGHT:
            player["rect"].bottom = HEIGHT

    #autos
    for car in cars:
        car["rect"].move_ip(0,car["speed_y"])
        if car["rect"].top > HEIGHT:
            car["rect"].bottom = 0

    # Mover autos
    for car in cars:
        car["rect"].move_ip(0, car["speed_y"])
        if car["rect"].top > HEIGHT:
            while True:
                if distancia_entre_autos(car, cars):
                    break
    
    #dibujar pantalla
    SCREEN.blit(img_fondo, (0,0))
    SCREEN.blit(player["img"],player["rect"])
    for car in cars:
        SCREEN.blit(car["img"],car["rect"])
        
    pygame.display.flip()

