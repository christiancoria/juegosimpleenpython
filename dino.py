import pygame
import random
import time

# Inicializar Pygame
pygame.init()

# Definir colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)
MARRON = (139, 69, 19)

# Tamaño de la ventana
ANCHO = 800
ALTO = 300

# Crear la ventana del juego
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego Dino - Pygame")

# Definir el reloj
reloj = pygame.time.Clock()

# Fuentes
fuente_score = pygame.font.SysFont('arial', 20)

# Dinosaurio
dino_width = 40
dino_height = 60
dino_x = 50
dino_y = ALTO - dino_height - 40
dino_vel = 10
is_jumping = False
jump_count = 10

# Obstáculos
obstaculo_width = 40
obstaculo_height = 60
obstaculo_vel = 10
obstaculos = []

# Función para mostrar el puntaje
def mostrar_puntaje(puntos):
    score_text = fuente_score.render("Puntos: " + str(puntos), True, BLANCO)
    pantalla.blit(score_text, [10, 10])

# Función para dibujar el dinosaurio
def dibujar_dino(x, y):
    pygame.draw.rect(pantalla, VERDE, [x, y, dino_width, dino_height])

# Función para dibujar obstáculos
def dibujar_obstaculos(obstaculos):
    for obstaculo in obstaculos:
        pygame.draw.rect(pantalla, MARRON, obstaculo)

# Función principal del juego
def juego():
    global dino_y, is_jumping, jump_count, obstaculos, dino_x
    puntos = 0
    dino_y = ALTO - dino_height - 40
    is_jumping = False
    jump_count = 10
    obstaculos = []
    generar_obstaculos()

    # Bucle principal del juego
    jugando = True
    while jugando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jugando = False

        # Manejar el salto
        if is_jumping:
            if jump_count >= -10:
                neg = 1
                if jump_count < 0:
                    neg = -1
                dino_y -= (jump_count ** 2) * 0.5 * neg
                jump_count -= 1
            else:
                is_jumping = False
                jump_count = 10

        # Control de teclas
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_SPACE] and not is_jumping:
            is_jumping = True

        # Mover obstáculos
        for obstaculo in obstaculos:
            obstaculo.x -= obstaculo_vel
            if obstaculo.x + obstaculo_width < 0:
                obstaculos.remove(obstaculo)
                generar_obstaculos()
                puntos += 1

        # Verificar colisiones
        for obstaculo in obstaculos:
            if (obstaculo.x < dino_x + dino_width and obstaculo.x + obstaculo_width > dino_x) and \
               (obstaculo.y < dino_y + dino_height and obstaculo.y + obstaculo_height > dino_y):
                jugando = False  # Fin del juego

        # Dibujar todo
        pantalla.fill(NEGRO)
        dibujar_dino(dino_x, dino_y)
        dibujar_obstaculos(obstaculos)
        mostrar_puntaje(puntos)

        # Actualizar la pantalla
        pygame.display.update()

        # Controlar la velocidad del juego
        reloj.tick(30)

    # Mensaje de fin de juego
    fin_de_juego(puntos)

# Función para mostrar mensaje de fin de juego
def fin_de_juego(puntos):
    fuente_fin = pygame.font.SysFont('arial', 50)
    texto_fin = fuente_fin.render(f"¡Juego terminado! Puntos: {puntos}", True, BLANCO)
    pantalla.blit(texto_fin, [ANCHO // 4, ALTO // 3])

    pygame.display.update()
    time.sleep(2)

    # Preguntar si el jugador quiere jugar otra vez
    pantalla.fill(NEGRO)
    texto_reiniciar = fuente_fin.render("¿Quieres jugar otra vez? (S/N)", True, BLANCO)
    pantalla.blit(texto_reiniciar, [ANCHO // 4, ALTO // 3 + 50])
    pygame.display.update()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_s:
                    juego()  # reiniciar el juego
                if evento.key == pygame.K_n:
                    pygame.quit()

# Función para generar obstáculos
def generar_obstaculos():
    # Generar obstáculos en posiciones aleatorias
    obstaculo = pygame.Rect(ANCHO, ALTO - obstaculo_height - 40, obstaculo_width, obstaculo_height)
    obstaculos.append(obstaculo)

# Ejecutar el juego
juego()

# Finalizar Pygame
pygame.quit()
