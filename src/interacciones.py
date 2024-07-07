import pygame
from settings import *
from colisiones import *
from pygame.locals import *
import sys
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
        escritor_csv.writerow(["puesto","user","nivel","tiempo"])

        for record in records:
            escritor_csv.writerow([record["puesto"], record["user"], record["nivel"], record["tiempo"]])

        print(f"Archivo modificado guardado en: {nueva_ruta}")
        
def cargar_json(nombre_archivo:str):
    """
        Abro el archivo
    """
    ruta = f"{PATH_JSON}{nombre_archivo}.json"
    with open(ruta,"r",encoding = "utf-8") as archivo:
        data = json.load(archivo)
    return data

def guardar_json(nombre_archivo:str,records:list):
    """
        guardo el archivo
    """
    nueva_ruta = f"{PATH_JSON}{nombre_archivo}.json"
    with open(nueva_ruta, "w", encoding = "utf-8") as archivo:
        json.dump(records,archivo,indent=4)
        print(f"Archivo guardado en: {nueva_ruta}")

def mostrar_record(record:dict,screen,font,distancia_y):
    '''
        Valida el diccionario
        Recibe un diccionario
        Imprime en terminal cada elemento
    '''
    mostrar_texto(screen,distancia_y,f"{record["puesto"]:<20} {record["user"]:<20} {record["nivel"]:<10} {record["tiempo"]:>10}",font,RED)


def mostrar_records(records:list,screen,font):
    '''
        Valida la lista
        Recibe una lista
        Imprime en terminal la lista
        Caso contrario da un mensaje de error
    '''
    if(len(records) > 0):
        mostrar_texto(screen,(390,380),"puesto            user           nivel          tiempo",font,RED)
        y_offset = 380 + 40
        for record in records:
            distancia_y = (390, y_offset)
            mostrar_record(record, screen, font, distancia_y)
            y_offset += 40
    else:
        print('ERROR: La lista no puede ser recorrida')


def orden_lista(funct,lista:list)->None:
    '''
        Valida que sea una lista
        Recibe una lista que modifica
        Modifica segun el criterio de la funct
    '''
    tam = len(lista)
    for i in range(tam - 1):
        for j in range(i + 1, tam):
            if funct(lista[i],lista[j]):
                swaps_valores(lista,i,j)

def swaps_valores(lista:list,i:int,j:int)->None:
    '''
        Recibe una lista
        Se encarga de swappear tanto lo que viene en i y j
    '''
    aux = lista[i]
    lista[i] = lista[j]
    lista[j] = aux

def asignar_puesto(records):
    for i, record in enumerate(records):
        record["puesto"] = i + 1
    records.pop()



def writer_screen(SCREEN,font):
    #Comienzo del juego
    clock = pygame.time.Clock()
    input_text = ""
    input_active = True

    # Colores
    color_inactive = RED
    color_active = BLUE
    color = color_inactive

    # Posición y tamaño del cuadro de texto
    input_box_x = 250
    input_box_y = 270
    input_box_width = 300
    input_box_height = 36
    input_box = pygame.Rect(input_box_x, input_box_y, input_box_width, input_box_height)

    # Bucle principal
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if punto_en_rectangulo(event.pos,input_box):
                        input_active = not input_active
                    else:
                        input_active = False
                color = color_active if input_active else color_inactive
            elif event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        return input_text
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode
        SCREEN.fill(BLACK)
        mostrar_texto(SCREEN,POSITION_TITLE,"INGRESE SU NOMBRE",font,RED)
        mostrar_texto(SCREEN,POSITION_PRESS_ESCAPE,"Presionar enter para continuar",font,WHITE)
        # Renderizar el texto de entrada
        text_surface = font.render(input_text, True, color)
        # Obtener el rectángulo del texto
        input_box.w = max(input_box_width, text_surface.get_width() + 10)
        # Dibujar el cuadro de texto
        pygame.draw.rect(SCREEN, color, input_box, 2)
        # Blit el texto
        SCREEN.blit(text_surface, (input_box.x + 5, input_box.y + 5))
        pygame.display.flip()
