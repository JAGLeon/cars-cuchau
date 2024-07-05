def detectar_colision(block_1,block_2):
    if  punto_en_rectangulo(block_1.topleft,block_2) or \
        punto_en_rectangulo(block_1.topright,block_2) or \
        punto_en_rectangulo(block_1.bottomleft,block_2) or \
        punto_en_rectangulo(block_1.bottomleft,block_2) or \
        punto_en_rectangulo(block_2.topleft,block_1) or \
        punto_en_rectangulo(block_2.topright,block_1) or \
        punto_en_rectangulo(block_2.bottomleft,block_1) or \
        punto_en_rectangulo(block_2.bottomleft,block_1):
        return True
    else: 
        return False
    
def punto_en_rectangulo(punto,rect):
    coordenada_x, coordenada_y = punto
    return rect.left <= coordenada_x and rect.right >= coordenada_x and rect.top <= coordenada_y and rect.bottom >= coordenada_y

def distancia_entre_autos(new_car, cars):
    for car in cars:
        if detectar_colision(new_car["rect"], car["rect"]):
            return True
    return False