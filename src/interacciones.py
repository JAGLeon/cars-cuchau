import pygame
from settings import *
from colisiones import *
from pygame.locals import *
import sys
import os
import csv
import json 

def terminar():
    pygame.quit()
    exit()

def mostrar_texto(superficie:pygame.Surface,coordenada:tuple[int,int] ,texto:str,fuente:pygame.font,color:tuple[int,int,int] = WHITE,bg:tuple[int,int,int] = None):
    if bg is None:
        sup_text = fuente.render(texto, True, color)
    else:
        sup_text = fuente.render(texto, True, color, bg)
    rect_texto = sup_text.get_rect()
    rect_texto.center = coordenada

    superficie.blit(sup_text,rect_texto)
    pygame.display.flip()
    return rect_texto

def botones(superficie:pygame.Surface,coordenada:tuple[int,int] ,texto:str,fuente:pygame.font,color:tuple[int,int,int] = WHITE):
    rect_button = mostrar_texto(superficie,coordenada," ",fuente,BLACK)
    rect_button.width += 200
    rect_button.height += 20
    pygame.draw.rect(superficie, color, rect_button, 5) 
    mostrar_texto(superficie, rect_button.center, texto, fuente, color)
    return rect_button

def wait_user(tecla,quit = None):
    flag_start = True
    while flag_start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminar()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == tecla:
                    flag_start = False
                if quit:    
                    if event.key == quit:
                        terminar()
                        sys.exit()

def wait_user_click(rect_button:pygame.Rect,rect_quit_button:pygame.Rect):
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
                    if punto_en_rectangulo(event.pos,rect_quit_button):
                        terminar()
                        sys.exit()

def verificar_mute(playing_music,sonido):
    if playing_music:
        sonido.play()

def cargar_csv(nombre_archivo):
    '''
        Se encarga de cargar un archivo csv
        Retorna una lista de diccionarios
    '''
    with open(f"{PATH_CSV}{nombre_archivo}.csv") as archivo:
        lista_diccionarios = []
        lector_csv = csv.DictReader(archivo)
        for fila in lector_csv:
            lista_diccionarios.append(fila)

    print("El archivo se ha cargado con éxito.")
    return lista_diccionarios

def guardar_csv(nombre_archivo:str,records:list):
    """
        Guardo el archivo csv
        En caso de existir te borra lo sobreescribe lo anterior
    """
    nueva_ruta = f"{PATH_CSV}{nombre_archivo}.csv"

    with open(nueva_ruta, 'w', newline='', encoding = "utf-8") as archivo_modificado:
        escritor_csv = csv.writer(archivo_modificado)
        escritor_csv.writerow(["id","puesto","user","nivel","tiempo"])
        
        for record in records:
            escritor_csv.writerow([record["id"], record["puesto"], record["user"], record["nivel"], record["tiempo"]])

        print(f"Archivo modificado guardado en: {nueva_ruta}")

def guardar_json(nombre_archivo:str,records:list):

    nueva_ruta = f"{PATH_JSON}{nombre_archivo}.json"
    with open(nueva_ruta, "w", encoding = "utf-8") as archivo:
        json.dump(records,archivo,indent=4)
        print(f"Archivo modificado guardado en: {nueva_ruta}")