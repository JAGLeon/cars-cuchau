from random import randint , randrange

def get_random_element(lista:list) -> any:
    TAM = len(lista)
    return lista[randint(0,TAM-1)]


def get_random_color(colors:list) -> tuple:
    return get_random_element(colors)

def random_color()->tuple[int,int,int]:
    r = randrange(256)
    g = randrange(256)
    b = randrange(256)
    return (r,g,b)