import pygame
from settings import *
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

def wait_user(tecla):
    flag_start = True
    while flag_start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminar()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == tecla:
                    flag_start = False

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