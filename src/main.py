import pygame
from settings import *
from random import randint
from bloques import *
from colisiones import *
from interacciones import *
from pygame.locals import *


img_fondo_uno = pygame.transform.scale(pygame.image.load(f"{PATH_IMG}fondo_1.png"),SIZE_SCREEN)
img_fondo = pygame.transform.scale(pygame.image.load(f"{PATH_IMG}fondo.png"),SIZE_SCREEN)
img_game_over = pygame.transform.scale(pygame.image.load(f"{PATH_IMG}game_over.png"),SIZE_SCREEN)
img_player = pygame.image.load(f"{PATH_IMG}player.png")
img_explosion = pygame.transform.scale(pygame.image.load(f"{PATH_IMG}explosion.png"), (CAR_W,CAR_H))
img_vida = pygame.transform.scale(pygame.image.load(f"{PATH_IMG}vida.png"),(BONUS_H,BONUS_W))
img_modificar_autos = pygame.image.load(f"{PATH_IMG}small_car.png")
img_escudo = pygame.transform.scale(pygame.image.load(f"{PATH_IMG}escudo.png"),(BONUS_H,BONUS_W))
img_mute = pygame.transform.scale(pygame.image.load(f"{PATH_IMG}mute.png"),(BONUS_H,BONUS_W))
# Carga todas la fuente
pygame.font.init()
font = pygame.font.Font("./src/assets/fonts/dash-horizon.otf", 36)
font_game_over = pygame.font.Font("./src/assets/fonts/dash-horizon.otf", 65)

#Cargo sonido
pygame.mixer.init()
choque = pygame.mixer.Sound(f"{PATH_SOUND}choque.mp3")
choque.set_volume(0.2)
frenar = pygame.mixer.Sound(f"{PATH_SOUND}frenar.mp3")
frenar.set_volume(0.05)
acelerar = pygame.mixer.Sound(f"{PATH_SOUND}avanzar.mp3")
acelerar.set_volume(0.05)
inmortal = pygame.mixer.Sound(f"{PATH_SOUND}inmortal.mp3")
inmortal.set_volume(0.3)
bonus = pygame.mixer.Sound(f"{PATH_SOUND}bonus.mp3")
fin = pygame.mixer.Sound(f"{PATH_SOUND}fin.mp3")
intro = pygame.mixer.Sound(f"{PATH_SOUND}intro.mp3")
intro.set_volume(0.1)
#Selecciona una imagen de auto al azar
pygame.init()

#Eventos propios
DRAW_CARS_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(DRAW_CARS_EVENT, TIME_AUTOS)
GENERATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(GENERATE_BONUS, TIME_BONUS)
LVL_UP = pygame.USEREVENT + 3
pygame.time.set_timer(LVL_UP, TIME_LVL)

#Tamaño de pantalla
SCREEN = pygame.display.set_mode(SIZE_SCREEN)
#Nombre del juego
pygame.display.set_caption("Cars Cuchau")

#Comienzo del juego
clock = pygame.time.Clock()
while True:
    config = cargar_json("config")
    playing_music = config[0]["mute"]
    clock.tick(FPS)
    records = cargar_csv("records")
    orden_lista(lambda rec_uno,rec_dos: int(rec_uno["tiempo"].replace(":", "")) < int(rec_dos["tiempo"].replace(":", "")),records)
    pygame.mouse.set_visible(True)
    if playing_music:
        intro.play()
    fin.stop()
    #pantalla inicio
    SCREEN.blit(img_fondo_uno, (0,0))
    mostrar_texto(SCREEN,POSITION_TITLE,"CAR CUCHAU",font_game_over,RED)
    rect_start_button = botones(SCREEN,POSITION_PLAY,"JUGAR",font,RED)
    rect_quit_button = botones(SCREEN,POSITION_QUIT,"SALIR",font,RED)
    mostrar_records(records,SCREEN,font)
    wait_user_click(rect_start_button,rect_quit_button)

    #Jugador
    player = crear_player(img_player)

    #Autos
    cars = []

    #Direcciones
    move_left = True
    move_right = True
    move_up = True
    move_down = True

    #puntajes - bonus
    lives = 3
    escudos = 0
    lvl = 0
    vida = None
    auto_chico = None
    escudo = None

    #Musica para todo el juego
    pygame.mixer.music.load(f"{PATH_MUSIC}fondo-furioso.mp3")
    pygame.mixer.music.set_volume(0.1)
    if playing_music:
        pygame.mixer.music.play(loops=-1)

    #Configuraciones
    pygame.mouse.set_visible(False)
    in_pause = True
    start_time = pygame.time.get_ticks()
    small_car_start_time = 0
    ignore_colision_time = None
    direction = 1

    #Comienzo del juego
    clock = pygame.time.Clock()
    is_running = True
    while is_running:
        if not pygame.mixer.music.get_busy() and playing_music:
            pygame.mixer.music.play(loops=-1)
        intro.stop()
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
                if event.key == K_SPACE:
                    if escudos > 0:
                        verificar_mute(playing_music,inmortal)
                        escudos -= 1
                        ignore_colision_time  = pygame.time.get_ticks()

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

            if event.type == GENERATE_BONUS:
                random_choice = randint(1,5)
                match random_choice:
                    case 1:
                        vida = crear_bonus(img_vida, SPEED_Y_CAR)
                    case 2:
                        auto_chico = crear_bonus(img_modificar_autos, SPEED_Y_CAR)
                    case 3:
                        escudo = crear_bonus(img_escudo, SPEED_Y_CAR)
                    case 4:
                        escudo = crear_bonus(img_vida, SPEED_Y_CAR)
                        auto_chico = crear_bonus(img_modificar_autos, SPEED_Y_CAR)
                    case 5:
                        auto_chico = crear_bonus(img_modificar_autos, SPEED_Y_CAR)
                        escudo = crear_bonus(img_escudo, SPEED_Y_CAR)


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
        if ignore_colision_time is None or pygame.time.get_ticks() - ignore_colision_time > TIME_INMORTAL:
            for car in cars[:]:
                if detectar_colision(car["rect"],player["rect"]):
                    lives -= 1
                    SCREEN.blit(img_explosion, car["rect"])
                    pygame.display.flip()
                    verificar_mute(playing_music,choque)
                    cars.remove(car)
                    if lives == 0:
                        is_running = False
                    pygame.time.delay(DELAY_COLISION)
        else:
            mostrar_texto(SCREEN,POSITION_ACTIVO_SHIELD, f"ACTIVO!",font,RED)

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
            elif detectar_colision(vida["rect"],player["rect"]):
                verificar_mute(playing_music,bonus)
                lives += 1
                vida = None

        #Autos chicos
        if auto_chico:
            auto_chico["rect"].move_ip(0, auto_chico["speed_y"])
            if auto_chico["rect"].top > HEIGHT:
                auto_chico = None
            elif detectar_colision(auto_chico["rect"], player["rect"]):
                verificar_mute(playing_music,bonus)
                small_car_start_time = pygame.time.get_ticks()
                auto_chico = None

        #Vida
        if escudo:
            escudo["rect"].move_ip(0,escudo["speed_y"])
            if escudo["rect"].top > HEIGHT:
                escudo = None
            elif detectar_colision(escudo["rect"],player["rect"]):
                verificar_mute(playing_music,bonus)
                escudos += 1
                escudo = None

        #Si el tiempo es menor a 5s
        if small_car_start_time and pygame.time.get_ticks() - small_car_start_time <= TIME_SMALL_CAR:
            for car in cars:
                car["rect"].width = SMALL_CAR_W
                car["rect"].height = SMALL_CAR_H
                car["img"] = pygame.transform.scale(car["img"], (SMALL_CAR_W, SMALL_CAR_H))

        #Calcular el tiempo transcurrido
        tiempo_transcurrido = (pygame.time.get_ticks() - start_time) / 1000
        min_transcurridos = int(tiempo_transcurrido // 60)
        seg_transcurridos = int(tiempo_transcurrido % 60)
        tiempo = f"{min_transcurridos:02}:{seg_transcurridos:02}"

        IMG_FONDO_Y += direction * SCROLL_SPEED
        #Dibujar pantalla
        SCREEN.blit(img_fondo, (0, IMG_FONDO_Y))
        SCREEN.blit(player["img"],player["rect"])

        for car in cars:
            SCREEN.blit(car["img"], car["rect"])

        mostrar_texto(SCREEN,POSITION_TITLE, tiempo, font, WHITE)
        mostrar_texto(SCREEN,POSITION_LVL, f"Nivel: {lvl}", font, BLUE)
        SCREEN.blit(img_vida, POSITION_LIVES)
        mostrar_texto(SCREEN,POSITION_CANT_LIVES, f"X: {lives}",font,WHITE)
        SCREEN.blit(img_escudo, POSITION_SHIELD)
        mostrar_texto(SCREEN,POSITION_CANT_SHIELDS, f"X: {escudos}",font,WHITE)

        if not playing_music:
            SCREEN.blit(img_mute, POSITION_MUTE)

        if vida:
            SCREEN.blit(vida["img"], vida["rect"])

        if auto_chico:
            SCREEN.blit(auto_chico["img"], auto_chico["rect"])

        if escudo:
            SCREEN.blit(escudo["img"], escudo["rect"])

        if IMG_FONDO_Y >= HEIGHT - img_fondo.get_height() or IMG_FONDO_Y <= 0:
            direction *= -1

        if lives == 0:
            fps = 60
            while fps:
                clock.tick(fps)
                fps -= 5

        pygame.display.flip()
    config[0]["mute"] = playing_music
    guardar_json("config",config)
    pygame.mouse.set_visible(True)
    pygame.mixer.music.stop()
    nombre = writer_screen(SCREEN,font)
    new_record = {"puesto":None,"user":nombre,"nivel":lvl,"tiempo":tiempo}
    records.append(new_record)
    orden_lista(lambda rec_uno,rec_dos: int(rec_uno["tiempo"].replace(":", "")) < int(rec_dos["tiempo"].replace(":", "")),records)
    asignar_puesto(records)
    guardar_csv("records",records)
    verificar_mute(playing_music,fin)
    SCREEN.blit(img_game_over,(0,0))
    mostrar_texto(SCREEN,POSITION_TITLE,"GAME OVER",font_game_over,BLUE)
    mostrar_texto(SCREEN,CENTER_USER,f"NOMBRE: {new_record["user"]}",font,WHITE)
    mostrar_texto(SCREEN,CENTER_LVL,f"NIVEL: {new_record["nivel"]}",font,WHITE)
    mostrar_texto(SCREEN,CENTER_TIME,f"TIEMPO: {new_record["tiempo"]}",font,WHITE)
    mostrar_texto(SCREEN,POSITION_PRESS_SPACE,"Presionar espacio para continuar",font,WHITE)
    mostrar_texto(SCREEN,POSITION_PRESS_ESCAPE,"Presionar escape para finalizar",font,WHITE)
    pygame.display.flip()
    wait_user(K_SPACE,K_ESCAPE)