import pygame

def detectar_colision(block_1: pygame.Rect, block_2: pygame.Rect) -> bool:
    """
    Detecta si hay colisión entre dos rectángulos (blocks).

    Args:
        block_1 (pygame.Rect): Primer rectángulo.
        block_2 (pygame.Rect): Segundo rectángulo.

    Returns:
        bool: True si hay colisión, False en caso contrario.
    """
    if (punto_en_rectangulo(block_1.topleft, block_2) or
        punto_en_rectangulo(block_1.topright, block_2) or
        punto_en_rectangulo(block_1.bottomleft, block_2) or
        punto_en_rectangulo(block_1.bottomright, block_2) or
        punto_en_rectangulo(block_2.topleft, block_1) or
        punto_en_rectangulo(block_2.topright, block_1) or
        punto_en_rectangulo(block_2.bottomleft, block_1) or
        punto_en_rectangulo(block_2.bottomright, block_1)):
        return True
    return False

def punto_en_rectangulo(punto: tuple, rect: pygame.Rect) -> bool:
    """
    Verifica si un punto está dentro de un rectángulo.

    Args:
        punto (tuple): Coordenadas (x, y) del punto.
        rect (pygame.Rect): El rectángulo en el que se comprobará el punto.

    Returns:
        bool: True si el punto está dentro del rectángulo, False en caso contrario.
    """
    coordenada_x, coordenada_y = punto
    return rect.left <= coordenada_x <= rect.right and rect.top <= coordenada_y <= rect.bottom

def distancia_entre_autos(new_car: dict, cars: list) -> bool:
    """
    Verifica si hay colisión entre un nuevo coche y una lista de coches.

    Args:
        new_car (dict): Diccionario que representa el nuevo coche.
        cars (list): Lista de diccionarios que representan los coches existentes.

    Returns:
        bool: True si hay colisión, False en caso contrario.
    """
    for car in cars:
        if detectar_colision(new_car["rect"], car["rect"]):
            return True
    return False
