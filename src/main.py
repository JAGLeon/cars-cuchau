import pygame
from settings import *
from random import randint,choice
from aleatorios import *
from bloques import *
from colisiones import *
from interacciones import *
from pygame.locals import *

def verificar_mute(playing_music,sonido):
    if playing_music:
        sonido.play()

img_fondo = pygame.image.load("./src/assets/images/fondo.png")
img_fondo = pygame.transform.scale(img_fondo,SIZE_SCREEN)
img_player = pygame.image.load("./src/assets/images/player.png")
img_explosion = pygame.transform.scale(pygame.image.load("./src/assets/images/explosion.png"), (CAR_W,CAR_H))
# Carga todas la fuente
pygame.font.init() 
font = pygame.font.Font("./src/assets/fonts/dash-horizon.otf", 36)

#Cargo sonido
pygame.mixer.init()
choque = pygame.mixer.Sound('./src/assets/sounds/choque.mp3')
choque.set_volume(0.2)
frenar = pygame.mixer.Sound('./src/assets/sounds/frenar.mp3')
frenar.set_volume(0.05)
acelerar = pygame.mixer.Sound('./src/assets/sounds/avanzar.mp3')
acelerar.set_volume(0.05)
# Selecciona una imagen de auto al azar
pygame.init()

#Eventos propios
DRAW_CARS_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(DRAW_CARS_EVENT, TIME_AUTOS)
GENERATE_VIDA_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(GENERATE_VIDA_EVENT, TIME_LIVES)
LVL_UP = pygame.USEREVENT + 3
pygame.time.set_timer(LVL_UP, TIME_LVL)

#Tamaño de pantalla
SCREEN = pygame.display.set_mode(SIZE_SCREEN)
#Nombre del juego
pygame.display.set_caption("Cars Cuchau")

#Jugador
player = crear_player(img_player)

#Autos
cars = []

#Direcciones
move_left = True
move_right = True
move_up = True
move_down = True

#puntajes
lives = 3
lvl = 0
vida = None


#Musica para todo el juego
playing_music = True
pygame.mixer.music.load("./src/assets/music/fondo-furioso.mp3")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(loops=-1)

#Configuraciones
pygame.mouse.set_visible(False)
in_pause = True
start_time = pygame.time.get_ticks()

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
                verificar_mute(playing_music,frenar)
                move_down = True
                move_up = False
            if event.key == K_UP or event.key == K_w:
                verificar_mute(playing_music,acelerar)
                move_up = True
                move_down = False
            if event.key == K_LEFT or event.key == K_a:
                move_left = True
                move_right = False
            if event.key == K_RIGHT or event.key == K_d:
                move_right = True
                move_left = False
            if event.key == K_m:
                if playing_music:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
                playing_music = not playing_music
            if event.key == K_p:
                pygame.mixer.music.pause()
                mostrar_texto(SCREEN,CENTER_SCREEN,"PAUSA",font,WHITE)
                wait_user(K_p)
                if playing_music:
                    pygame.mixer.music.unpause()
                in_pause = not in_pause

        if event.type == KEYUP:
            if event.key == K_DOWN or event.key == K_s:
                move_down = False
            if event.key == K_UP or event.key == K_w:
                move_up = False
            if event.key == K_LEFT or event.key == K_a:
                move_left = False
            if event.key == K_RIGHT or event.key == K_d:
                move_right = False


        if event.type == DRAW_CARS_EVENT:
            if len(cars) < MAX_CARS_SCREEN:
                nueva_posicion_valida = False
                intentos = 0 
                while not nueva_posicion_valida and intentos < 100:
                    nuevo_car = crear_car()
                    if not distancia_entre_autos(nuevo_car, cars):
                        cars.append(nuevo_car)
                        nuevo_car["speed_y"] = SPEED_Y_CAR
                        nueva_posicion_valida = True
                    intentos += 1

        if event.type == LVL_UP:
            lvl += 1
            SPEED_Y_CAR += LVL_UP_VELOCITY

        if event.type == GENERATE_VIDA_EVENT:
            if randint(1, 10) <= 5:  
                vida = crear_bonus_vida()
    #Movimientos mios
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

    #Autos
    for car in cars[:]:
        car["rect"].move_ip(0,car["speed_y"])
        if car["rect"].top > HEIGHT:
            cars.remove(car)

    #Verificar choques con otros autos (VIDAS) 
    for car in cars[:]:
        if detectar_colision_circulos(car["rect"],player["rect"]):
            lives -= 1
            SCREEN.blit(img_explosion, car["rect"])
            pygame.display.flip()
            verificar_mute(playing_music,choque)
            cars.remove(car)
            if lives == 0:
                is_running = False
            pygame.time.delay(DELAY_COLISION) 

    #Movimiento de los autos
    for car in cars[:]:
        car["rect"].move_ip(0, car["speed_y"])
        if car["rect"].top > HEIGHT:
            cars.remove(car)
            nueva_posicion_valida = False
            intentos = 0
            while not nueva_posicion_valida and intentos < 100:
                nuevo_car = crear_car()
                nuevo_car["speed_y"] = SPEED_Y_CAR
                if not distancia_entre_autos(nuevo_car, cars):
                    cars.append(nuevo_car)
                    nueva_posicion_valida = True
                intentos += 1

    #Vida
    if vida:
        vida["rect"].move_ip(0,vida["speed_y"])
        if vida["rect"].top > HEIGHT:
            vida = None
        elif detectar_colision_circulos(vida["rect"],player["rect"]):
            lives += 1
            vida = None

    #Calcular el tiempo transcurrido
    tiempo_transcurrido = (pygame.time.get_ticks() - start_time) / 1000  # convertir a segundos
    min_transcurridos = int(tiempo_transcurrido // 60)
    seg_transcurridos = int(tiempo_transcurrido % 60)
    tiempo = f"{min_transcurridos:02}:{seg_transcurridos:02}"

    #Dibujar pantalla
    SCREEN.blit(img_fondo, (0,0))
    SCREEN.blit(player["img"],player["rect"])

    for car in cars:
        SCREEN.blit(car["img"], car["rect"])

    mostrar_texto(SCREEN,POSITION_LIVES, f"Vidas: {lives}",font,RED)
    mostrar_texto(SCREEN,POSITION_TITLE, tiempo, font, WHITE)
    mostrar_texto(SCREEN,POSITION_LVL, f"Nivel: {lvl}", font, BLUE)

    if not playing_music:
        mostrar_texto(SCREEN,POSITION_MUTE,"MUTE",font,RED)

    if vida:
        SCREEN.blit(vida["img"], vida["rect"])

    pygame.display.flip()

