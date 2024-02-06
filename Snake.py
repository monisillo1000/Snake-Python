import pygame
import random

# Inicializar pygame
pygame.init()

# Definir colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

# Tamaño de la pantalla y otros parámetros
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

# Definir tamaño del bloque y velocidad del juego
BLOCK_SIZE = 20
SNAKE_SPEED = 10

# Fuente retro
FONT_STYLE = pygame.font.Font(None, 30)

# Función para mostrar mensajes en pantalla
def display_message(msg, color, y_displacement=0):
    message = FONT_STYLE.render(msg, True, color)
    message_rect = message.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + y_displacement))
    SCREEN.blit(message, message_rect)

# Función para mostrar el menú
def game_menu():
    menu = True
    while menu:
        SCREEN.fill(BLACK)
        display_message("Snake by monisillo", WHITE, -100)
        pygame.draw.rect(SCREEN, GREEN, [200, 250, 200, 75])
        display_message("Start", BLACK, 90)

        # Dibujar serpiente en el menú
        snake_head = pygame.image.load('snake_head.png').convert_alpha()
        snake_head = pygame.transform.scale(snake_head, (40, 40))
        SCREEN.blit(snake_head, (272, 160))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 200 <= mouse_x <= 400 and 250 <= mouse_y <= 325:
                    game_loop()

# Función principal del juego
def game_loop():
    game_over = False
    snake_position = [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2]
    snake_body = [[snake_position[0], snake_position[1]],
                  [snake_position[0] - BLOCK_SIZE, snake_position[1]],
                  [snake_position[0] - (2 * BLOCK_SIZE), snake_position[1]]]
    food_position = [random.randrange(1, (SCREEN_WIDTH // BLOCK_SIZE)) * BLOCK_SIZE,
                     random.randrange(1, (SCREEN_HEIGHT // BLOCK_SIZE)) * BLOCK_SIZE]
    direction = 'RIGHT'
    change_to = direction
    score = 0

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'
                elif event.key == pygame.K_UP:
                    change_to = 'UP'
                elif event.key == pygame.K_DOWN:
                    change_to = 'DOWN'

        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        elif change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'
        elif change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        elif change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'

        if direction == 'LEFT':
            snake_position[0] -= BLOCK_SIZE
        elif direction == 'RIGHT':
            snake_position[0] += BLOCK_SIZE
        elif direction == 'UP':
            snake_position[1] -= BLOCK_SIZE
        elif direction == 'DOWN':
            snake_position[1] += BLOCK_SIZE

        snake_body.insert(0, list(snake_position))
        if snake_position[0] == food_position[0] and snake_position[1] == food_position[1]:
            score += 1
            food_position = [random.randrange(1, (SCREEN_WIDTH // BLOCK_SIZE)) * BLOCK_SIZE,
                             random.randrange(1, (SCREEN_HEIGHT // BLOCK_SIZE)) * BLOCK_SIZE]
        else:
            snake_body.pop()

        SCREEN.fill(BLACK)
        for block in snake_body:
            pygame.draw.rect(SCREEN, GREEN, [block[0], block[1], BLOCK_SIZE, BLOCK_SIZE])

        pygame.draw.circle(SCREEN, RED, (food_position[0] + BLOCK_SIZE // 2, food_position[1] + BLOCK_SIZE // 2), BLOCK_SIZE // 2)

        if (snake_position[0] >= SCREEN_WIDTH or snake_position[0] < 0 or
                snake_position[1] >= SCREEN_HEIGHT or snake_position[1] < 0):
            game_over = True
        for block in snake_body[1:]:
            if snake_position[0] == block[0] and snake_position[1] == block[1]:
                game_over = True

        display_score(score)
        pygame.display.update()
        clock.tick(SNAKE_SPEED)

    display_message("Game Over!", RED, -50)
    display_message("Press C to Play Again or Q to Quit", WHITE, 50)
    pygame.display.update()
    pygame.time.wait(1500)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    game_loop()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

def display_score(score):
    score_text = FONT_STYLE.render("Score: " + str(score), True, WHITE)
    SCREEN.blit(score_text, [10, 10])

game_menu()
