import pygame
from settings import *
from random import randint
from aleatorios import *
from bloques import *
from colisiones import *
from pygame.locals import *
import sys

def terminar():
    pygame.quit()
    exit()

def mostrar_texto(superficie:pygame.Surface,coordenada:tuple[int,int] ,texto:str,fuente:pygame.font,color:tuple[int,int,int] = WHITE,bg:tuple[int,int,int] = BLACK):
    sup_text = fuente.render(texto,True,color,bg)
    rect_texto = sup_text.get_rect()
    rect_texto.center = coordenada

    superficie.blit(sup_text,rect_texto)
    pygame.display.flip()

def wait_user(tecla,tecla2 = None):
    flag_start = True
    while flag_start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminar()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == tecla:
                    flag_start = False
                if tecla2:    
                    if event.key == tecla2:
                        terminar()
                        sys.exit()

def wait_user_click(rect_button:pygame.Rect):
    flag_start = True
    while flag_start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if punto_en_rectangulo(event.pos,rect_button):
                        flag_start = False

#img 
img_ovni = pygame.image.load("./src/assets/images/ovni.png")
img_fondo = pygame.image.load("./src/assets/images/fondo.jpg")
img_asteroide = pygame.image.load("./src/assets/images/asteroide.png")
img_asteroide_2 = pygame.image.load("./src/assets/images/asteroide2.png")
img_fondo = pygame.image.load("./src/assets/images/fondo.jpg")
img_fondo = pygame.transform.scale(img_fondo,SIZE_SCREEN)
img_start_button = pygame.image.load("./src/assets/images/start_button.png")
img_start_button = pygame.transform.scale(img_start_button,START_BUTTON_SIZE)

icono = pygame.image.load("./src/assets/images/start_button.png")
pygame.display.set_icon(icono)

NEWCOINEVENT = USEREVENT + 1
TIMEOUT = USEREVENT + 2

pygame.init()

SCREEN = pygame.display.set_mode(SIZE_SCREEN)
pygame.display.set_caption("Jogo bonito")

clock = pygame.time.Clock()

# font = pygame.font.SysFont(None, 36)
font = pygame.font.Font("./src/assets/fonts/dash-horizon.otf", 36)
coins_colision = 0
score_text = font.render(f"Coins colisionados: {coins_colision}",True,BLUE)

#cargo sonido
pygame.mixer.init()
colision_sonido = pygame.mixer.Sound("./src/assets/sounds/coin.mp3")
exito_sonido = pygame.mixer.Sound("./src/assets/sounds/exito.mp3")

gamer_over_sonido = pygame.mixer.Sound("./src/assets/sounds/game_over.mp3")
gamer_over_sonido.set_volume(0.2)

playing_music = True
pygame.time.set_timer(NEWCOINEVENT,5000)


#musica para todo el juego
pygame.mixer.music.load("./src/assets/music/musica_fondo.mp3")
pygame.mixer.music.set_volume(0.1)
high_score = 0  
while True:
    pygame.mouse.set_visible(True)
    #pantalla inicio
    SCREEN.fill(BLACK)
    mostrar_texto(SCREEN,POSITION_TITLE,"CAR CUCHAU",font,RED)
    rect_start_button = img_start_button.get_rect(center = CENTER_SCREEN)
    SCREEN.blit(img_start_button , rect_start_button)
    pygame.display.flip()
    wait_user_click(rect_start_button)

    pygame.mouse.set_visible(False)

    #CREAR JUGADOR
    block = crear_player(img_ovni)
    coins = []
    cargar_coins(coins,INITIAL_COINS,img_asteroide_2)
    #Direcciones
    move_left = True
    move_right = True
    move_up = True
    move_down = True
    #puntajes
    score = 0
    counter_colision = 0
    laser = None
    lives = 3

    pygame.mixer.music.play()
    pygame.time.set_timer(TIMEOUT,TIME_GAME,1)
    in_pause = True
    is_running = True
    while is_running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            #teclas awsd
            if event.type == KEYDOWN:
                if event.key == K_f:
                    if not laser:
                        laser = create_laser(block["rect"].midtop)

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
                if event.key == K_m:
                    if playing_music:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                    playing_music = not playing_music
                if event.key == K_p:
                    pygame.mixer.music.pause()
                    mostrar_texto(SCREEN,CENTER_SCREEN,"PAUSE",font,MAGENTA)
                    wait_user(K_p)
                    if playing_music:
                        pygame.mixer.music.unpause()
                    in_pause = not in_pause
                if event.key == K_SPACE:
                    print("Hola")

            if event.type == KEYUP:
                if event.key == K_DOWN or event.key == K_s:
                    move_down = False
                if event.key == K_UP or event.key == K_w:
                    move_up = False
                if event.key == K_LEFT or event.key == K_a:
                    move_left = False
                if event.key == K_RIGHT or event.key == K_d:
                    move_right = False

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    new_coin = crear_coin()
                    new_coin["color"] = MAGENTA
                    new_coin["rect"].center = event.pos
                    coins.append(new_coin)

            if event.type == MOUSEMOTION:
                block["rect"].center = event.pos

            if event.type == NEWCOINEVENT:
                new_coin = crear_coin()
                new_coin["color"] = RED
                coins.append(new_coin)

            if event.type == TIMEOUT:
                is_running = False
        #movimientos
        if move_left and block["rect"].left > 0:
            block["rect"].x -= SPEED
            if block["rect"].left < 0:
                block["rect"].left = 0
        if move_right and block["rect"].right < WIDTH:
            block["rect"].x += SPEED
            if block["rect"].right > WIDTH:
                block["rect"].right = WIDTH
        if move_up and block["rect"].top > 0:
            block["rect"].y -= SPEED
            if block["rect"].top < 0:
                block["rect"].top = 0
        if move_down and block["rect"].bottom < HEIGHT:
            block["rect"].y += SPEED
            if block["rect"].bottom > HEIGHT:
                block["rect"].bottom = HEIGHT

        pygame.mouse.set_pos(block["rect"].center)

        for coin in coins:
            coin["rect"].move_ip(0,coin["speed_y"])
            if coin["rect"].top > HEIGHT:
                coin["rect"].bottom = 0

        if laser:
            laser["rect"].move_ip(0,-laser["speed"])
            if laser["rect"].bottom < 0:
                laser = None

        for coin in coins[:]:
            if laser:
                if detectar_colision(coin["rect"],laser["rect"]):
                    colision_sonido.play()
                    coins.remove(coin)
                    laser = None
                    score += 1
                    if len(coins) == 0:
                        exito_sonido.play()
                        cargar_coins(coins,INITIAL_COINS,img_asteroide)

        for coin in coins[:]:
            if detectar_colision_circulos(coin["rect"],block["rect"]):
                coins.remove(coin)
                lives -= 1
                if lives == 0:
                    is_running = False


        if counter_colision > 10:
            counter_colision -= 1
            block["rect"].width = player_w + 5

        #dibujar pantalla
        SCREEN.blit(img_fondo, (0,0))

        SCREEN.blit(block["img"],block["rect"])

        if laser:
            pygame.draw.rect(SCREEN,laser["color"],laser["rect"])

        for coin in coins:
            if coin["img"]:
                SCREEN.blit(coin["img"],coin["rect"])
            else:    
                pygame.draw.rect(SCREEN, coin["color"], coin["rect"],coin["borde"],coin["radio"])

        mostrar_texto(SCREEN,POSICION_SCORE, f"Score: {score}",font,BLUE)
        mostrar_texto(SCREEN,LAST_SCORE, f"Lives: {lives}",font,CYAN)
        #actualizar pantalla
        pygame.display.flip()


    #pantalla fin
    if score > high_score:
        high_score = score
    pygame.mixer.music.stop()
    gamer_over_sonido.play()
    SCREEN.fill(BLACK)
    mostrar_texto(SCREEN,LAST_SCORE,f"Last score: {score}",font,RED)
    mostrar_texto(SCREEN,HIGHT_SCORE,f"Higth score: {high_score}",font,RED)
    mostrar_texto(SCREEN,CENTER_SCREEN,"GAME OVER",font,RED)
    mostrar_texto(SCREEN,(MID_WIDTH_SCREEN,HEIGHT - 50),"Presiones espacio para comenzar",font,BLUE)
    pygame.display.flip()
    wait_user(K_SPACE)
terminar()