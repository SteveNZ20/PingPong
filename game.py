import pygame
import sys
from settings import *

# Inicializar Pygame
pygame.init()

# Crear la ventana del juego
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Pong")

# Definir las palas y la pelota
pala_izquierda = pygame.Rect(30, ALTO_VENTANA // 2 - 60, 10, 120)
pala_derecha = pygame.Rect(ANCHO_VENTANA - 40, ALTO_VENTANA // 2 - 60, 10, 120)
pelota = pygame.Rect(ANCHO_VENTANA // 2 - 15, ALTO_VENTANA // 2 - 15, 30, 30)

# Velocidades de movimiento
velocidad_pelota_x = VELOCIDAD_PELOTA
velocidad_pelota_y = VELOCIDAD_PELOTA
velocidad_pala_izquierda = 0
velocidad_pala_derecha = 0

# Puntos de los jugadores
puntos_izquierda = 0
puntos_derecha = 0

# Definir el reloj
reloj = pygame.time.Clock()

# Función para dibujar todo en la pantalla
def dibujar_escena():
    ventana.fill(NEGRO)  # Fondo negro
    pygame.draw.rect(ventana, BLANCO, pala_izquierda)
    pygame.draw.rect(ventana, BLANCO, pala_derecha)
    pygame.draw.ellipse(ventana, BLANCO, pelota)
    
    # Dibujar el marcador
    fuente = pygame.font.Font(None, 36)
    marcador = fuente.render(f"{puntos_izquierda} - {puntos_derecha}", True, BLANCO)
    ventana.blit(marcador, (ANCHO_VENTANA // 2 - marcador.get_width() // 2, 20))
    
    pygame.display.update()

# Función principal del juego
def juego():
    global velocidad_pala_izquierda, velocidad_pala_derecha, velocidad_pelota_x, velocidad_pelota_y
    global puntos_izquierda, puntos_derecha

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Movimiento de las palas
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_w]:
            velocidad_pala_izquierda = -VELOCIDAD_PALA
        elif teclas[pygame.K_s]:
            velocidad_pala_izquierda = VELOCIDAD_PALA
        else:
            velocidad_pala_izquierda = 0

        if teclas[pygame.K_UP]:
            velocidad_pala_derecha = -VELOCIDAD_PALA
        elif teclas[pygame.K_DOWN]:
            velocidad_pala_derecha = VELOCIDAD_PALA
        else:
            velocidad_pala_derecha = 0

        # Mover las palas
        pala_izquierda.y += velocidad_pala_izquierda
        pala_derecha.y += velocidad_pala_derecha

        # Mover la pelota
        pelota.x += velocidad_pelota_x
        pelota.y += velocidad_pelota_y

        # Detectar colisiones con las paredes
        if pelota.top <= 0 or pelota.bottom >= ALTO_VENTANA:
            velocidad_pelota_y = -velocidad_pelota_y
        
        # Detectar colisiones con las palas
        if pelota.colliderect(pala_izquierda) or pelota.colliderect(pala_derecha):
            velocidad_pelota_x = -velocidad_pelota_x

        # Detectar si un jugador marca un gol
        if pelota.left <= 0:  # Gol para el jugador de la derecha
            puntos_derecha += 1
            pelota.x = ANCHO_VENTANA // 2 - 15  # Resetear la pelota al centro
            pelota.y = ALTO_VENTANA // 2 - 15
            velocidad_pelota_x = -VELOCIDAD_PELOTA  # Cambiar dirección de la pelota

        if pelota.right >= ANCHO_VENTANA:  # Gol para el jugador de la izquierda
            puntos_izquierda += 1
            pelota.x = ANCHO_VENTANA // 2 - 15  # Resetear la pelota al centro
            pelota.y = ALTO_VENTANA // 2 - 15
            velocidad_pelota_x = VELOCIDAD_PELOTA  # Cambiar dirección de la pelota

        # Dibujar todo
        dibujar_escena()

        # Establecer el límite de fotogramas
        reloj.tick(60)

# Iniciar el juego
juego()