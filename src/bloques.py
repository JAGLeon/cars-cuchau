import pygame
from settings import *
from random import randint, choice
from colisiones import *

def crear_bloque(imagen: pygame.Surface = None, left: int = 0, top: int = 0, width: int = 50, height: int = 50, color: tuple = WHITE, dir: int = 3, borde: int = 0, radio: int = -1) -> dict:
    """
    Crea un bloque con las especificaciones dadas.

    Args:
        imagen (pygame.Surface): La imagen que se usará para el bloque. Valor por defecto es None.
        left (int): La posición x del bloque. Valor por defecto es 0.
        top (int): La posición y del bloque. Valor por defecto es 0.
        width (int): El ancho del bloque. Valor por defecto es 50.
        height (int): La altura del bloque. Valor por defecto es 50.
        color (tuple): El color del bloque en formato RGB. Valor por defecto es WHITE.
        dir (int): La dirección del bloque. Valor por defecto es 3.
        borde (int): El grosor del borde del bloque. Valor por defecto es 0.
        radio (int): El radio del bloque. Valor por defecto es -1.

    Returns:
        dict: Un diccionario que representa el bloque creado.
    """
    if imagen:
        imagen = pygame.transform.scale(imagen, (width, height))

    return {
        "rect": pygame.Rect(left, top, width, height),
        "color": color,
        "dir": dir,
        "borde": borde,
        "radio": radio,
        "img": imagen
    }

def crear_car() -> dict:
    """
    Crea un bloque que representa un coche enemigo con una imagen aleatoria.

    Returns:
        dict: Un diccionario que representa el coche enemigo creado.
    """
    block = crear_bloque(image_car_random(), randint(MIN_WIDTH_PISTA, MAX_WIDTH_PISTA - CAR_W), randint(-HEIGHT, 0 - CAR_H), CAR_W, CAR_H, YELLOW, 0, 0, 0)
    block["speed_y"] = SPEED_Y_CAR
    return block

def crear_player(imagen: pygame.Surface = None) -> dict:
    """
    Crea un bloque que representa al jugador con la imagen proporcionada.

    Args:
        imagen (pygame.Surface): La imagen que se usará para el jugador. Valor por defecto es None.

    Returns:
        dict: Un diccionario que representa al jugador creado.
    """
    return crear_bloque(imagen, randint(MIN_WIDTH_PISTA, MAX_WIDTH_PISTA - CAR_W), HEIGHT, CAR_W, CAR_H, BLUE, 0, 0, 0)

def crear_bonus(img: pygame.Surface, speed: int) -> dict:
    """
    Crea un bloque que representa un bono con la imagen y velocidad proporcionadas.

    Args:
        img (pygame.Surface): La imagen que se usará para el bono.
        speed (int): La velocidad del bono en el eje y.

    Returns:
        dict: Un diccionario que representa el bono creado.
    """
    block = crear_bloque(img, randint(MIN_WIDTH_PISTA, MAX_WIDTH_PISTA - BONUS_W), randint(-HEIGHT, 0 - BONUS_H), 50, 50, YELLOW, 0, 0, 0)
    block["speed_y"] = speed
    return block

def image_car_random() -> pygame.Surface:
    """
    Selecciona una imagen de coche aleatoria de una lista de imágenes disponibles.

    Returns:
        pygame.Surface: Una imagen de coche seleccionada aleatoriamente.
    """
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
