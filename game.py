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

# Variable de pausa
pausado = False

# Función para mostrar la ventana de inicio para los nombres
def pedir_nombres():
    fuente = pygame.font.Font(None, 36)
    nombre_jugador_1 = ""
    nombre_jugador_2 = ""
    seleccionando_1 = True
    seleccionando_2 = False

    while True:
        ventana.fill(NEGRO)
        
        # Mostrar mensaje general "PONG"
        fuente_pong = pygame.font.Font(None, 52)
        mensaje_pong = fuente_pong.render("Precione ENTER para continuar", True, BLANCO)
        ventana.blit(mensaje_pong, (ANCHO_VENTANA // 2 - mensaje_pong.get_width() // 2, 30))

        # Dibujar los textos de instrucciones
        mensaje_instrucciones = fuente.render("Ingresar nombre del Jugador 1:", True, BLANCO)
        ventana.blit(mensaje_instrucciones, (ANCHO_VENTANA // 2 - mensaje_instrucciones.get_width() // 2, ALTO_VENTANA // 3))

        # Mostrar el nombre del jugador 1
        nombre_1 = fuente.render(nombre_jugador_1, True, BLANCO)
        ventana.blit(nombre_1, (ANCHO_VENTANA // 2 - nombre_1.get_width() // 2, ALTO_VENTANA // 2))

        if seleccionando_1:
            # Esperar la entrada del jugador 1
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN and nombre_jugador_1 != "":
                        seleccionando_1 = False
                        seleccionando_2 = True
                    elif evento.key == pygame.K_BACKSPACE:
                        nombre_jugador_1 = nombre_jugador_1[:-1]
                    else:
                        nombre_jugador_1 += evento.unicode

        if not seleccionando_1:
            mensaje_instrucciones_2 = fuente.render("Ingresar nombre del Jugador 2:", True, BLANCO)
            ventana.blit(mensaje_instrucciones_2, (ANCHO_VENTANA // 2 - mensaje_instrucciones_2.get_width() // 2, ALTO_VENTANA // 3 + 50))

            # Mostrar el nombre del jugador 2
            nombre_2 = fuente.render(nombre_jugador_2, True, BLANCO)
            ventana.blit(nombre_2, (ANCHO_VENTANA // 2 - nombre_2.get_width() // 2, ALTO_VENTANA // 2 + 100))

            # Esperar la entrada del jugador 2
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN and nombre_jugador_2 != "":
                        return nombre_jugador_1, nombre_jugador_2
                    elif evento.key == pygame.K_BACKSPACE:
                        nombre_jugador_2 = nombre_jugador_2[:-1]
                    else:
                        nombre_jugador_2 += evento.unicode

        pygame.display.update()

# Función para dibujar todo en la pantalla
def dibujar_escena(nombre_jugador_1, nombre_jugador_2):
    ventana.fill(NEGRO)  # Fondo negro
    pygame.draw.rect(ventana, BLANCO, pala_izquierda)
    pygame.draw.rect(ventana, BLANCO, pala_derecha)
    pygame.draw.ellipse(ventana, BLANCO, pelota)
    
    # Dibujar el marcador
    fuente = pygame.font.Font(None, 36)
    marcador = fuente.render(f"{puntos_izquierda} - {puntos_derecha}", True, BLANCO)
    ventana.blit(marcador, (ANCHO_VENTANA // 2 - marcador.get_width() // 2, 20))

    # Dibujar los nombres de los jugadores en las esquinas superiores
    fuente_nombres = pygame.font.Font(None, 36)
    nombre_izquierda = fuente_nombres.render(nombre_jugador_1, True, BLANCO)
    nombre_derecha = fuente_nombres.render(nombre_jugador_2, True, BLANCO)
    ventana.blit(nombre_izquierda, (10, 10))
    ventana.blit(nombre_derecha, (ANCHO_VENTANA - nombre_derecha.get_width() - 10, 10))

    # Si el juego está pausado, mostrar el mensaje de pausa
    if pausado:
        fuente_paused = pygame.font.Font(None, 72)
        mensaje_paused = fuente_paused.render("PAUSE", True, BLANCO)
        ventana.blit(mensaje_paused, (ANCHO_VENTANA // 2 - mensaje_paused.get_width() // 2, ALTO_VENTANA // 2 - mensaje_paused.get_height() // 2))

    # Mensaje "Desarrollado con <3" en la parte inferior derecha
    fuente_creditos = pygame.font.Font(None, 24)
    mensaje_creditos = fuente_creditos.render("<NzDev/>", True, BLANCO)
    ventana.blit(mensaje_creditos, (ANCHO_VENTANA - mensaje_creditos.get_width() - 10, ALTO_VENTANA - mensaje_creditos.get_height() - 10))

    pygame.display.update()

# Función principal del juego
def juego():
    global velocidad_pala_izquierda, velocidad_pala_derecha, velocidad_pelota_x, velocidad_pelota_y
    global puntos_izquierda, puntos_derecha, pausado

    # Pedir los nombres de los jugadores
    nombre_jugador_1, nombre_jugador_2 = pedir_nombres()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Pausar o reanudar el juego al presionar la tecla P
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_p:
                    pausado = not pausado

        # Si el juego no está pausado, se actualizan las posiciones
        if not pausado:
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
        dibujar_escena(nombre_jugador_1, nombre_jugador_2)

        # Establecer el límite de fotogramas
        reloj.tick(60)

# Iniciar el juego
juego()
