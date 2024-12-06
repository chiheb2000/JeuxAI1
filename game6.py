import pygame
import random
import math

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Deep Blue Challenge")

# Couleurs
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Charger les images des bateaux et de l'île
player_boat_img = pygame.image.load("resized_bateau.png")
ai_boat_img = pygame.image.load("resized_1085959.png")
island_img = pygame.image.load("island.png")  

# Redimensionner les images
player_boat_img = pygame.transform.scale(player_boat_img, (60, 60))
ai_boat_img = pygame.transform.scale(ai_boat_img, (60, 60))
island_img = pygame.transform.scale(island_img, (100, 100))  

# Initialisation de l'horloge
clock = pygame.time.Clock()

# Variables globales
player_speed = 5
fuel_initial = 100
ai_speed_initial = 2
time_to_survive_initial = 10
messages = []
game_over = False
level = 1
time_to_survive = time_to_survive_initial
ai_speed = ai_speed_initial
fuel = fuel_initial
islands = []  # Liste des îles
start_ticks = pygame.time.get_ticks()  

# Bonus et pièges
bonus_rect = None
last_bonus_spawn = 0
bonus_spawn_interval = 5  
is_trap = False  
bonus_fuel_amount = 20  
penalty_fuel_amount = -15  

# Messages de sensibilisation
sensibilisation_messages = [
    "Réduisez votre consommation de plastique.",
    "Les océans absorbent 30% du CO2 produit par l'homme.",
    "Protégez la biodiversité marine : stop à la pollution.",
    "Chaque année, 8 millions de tonnes de plastique finissent dans les océans.",
    "Ensemble, sauvons les récifs coralliens.",
]

scroll_speed = 2
scroll_position = WIDTH

# Fonction pour réinitialiser le jeu
def reset_game():
    global player_rect, ai_rect, fuel, level, time_to_survive, ai_speed, start_ticks, game_over, scroll_position, islands, bonus_rect
    player_rect = player_boat_img.get_rect(center=(WIDTH // 2, HEIGHT - 100))
    ai_rect = ai_boat_img.get_rect(center=(random.randint(50, WIDTH - 50), 100))
    fuel = fuel_initial
    level = 1
    time_to_survive = time_to_survive_initial
    ai_speed = ai_speed_initial
    start_ticks = pygame.time.get_ticks()
    messages.clear()
    game_over = False
    scroll_position = WIDTH
    islands = []  
    bonus_rect = None  

# Ajouter une remarque
def add_message(message):
    messages.append(message)
    if len(messages) > 5:
        messages.pop(0)

# Fonction pour afficher les remarques sur le tableau de bord
def draw_messages():
    font = pygame.font.SysFont(None, 24)
    y_offset = HEIGHT - 100
    for message in messages:
        text = font.render(message, True, WHITE)
        screen.blit(text, (10, y_offset))
        y_offset += 20

# Fonction pour déplacer l'IA
def move_ai(ai_rect, player_rect, ai_speed):
    dx = player_rect.x - ai_rect.x
    dy = player_rect.y - ai_rect.y
    distance = math.sqrt(dx**2 + dy**2)
    if distance == 0:
        return
    dx /= distance
    dy /= distance
    ai_rect.x += dx * ai_speed
    ai_rect.y += dy * ai_speed
    ai_rect.x = max(0, min(WIDTH - ai_rect.width, ai_rect.x))
    ai_rect.y = max(0, min(HEIGHT - ai_rect.height, ai_rect.y))

# Fonction pour ajouter des îles dynamiquement
def add_islands(number):
    for _ in range(number):
        x = random.randint(100, WIDTH - 100)
        y = random.randint(100, HEIGHT - 200)
        islands.append(island_img.get_rect(center=(x, y)))

# Fonction pour afficher le texte déroulant dans une zone définie
def draw_scrolling_text():
    global scroll_position
    font = pygame.font.SysFont(None, 32)
    sensibilisation_text = " | ".join(sensibilisation_messages)
    text_surface = font.render(sensibilisation_text, True, WHITE)

    text_area = pygame.Rect(0, HEIGHT - 40, WIDTH, 40)
    pygame.draw.rect(screen, BLACK, text_area)

    screen.blit(text_surface, (scroll_position, HEIGHT - 30))

    scroll_position -= scroll_speed
    if scroll_position < -text_surface.get_width():
        scroll_position = WIDTH

# Fonction pour gérer les bonus/pièges
def spawn_bonus():
    global is_trap
    x = random.randint(50, WIDTH - 50)
    y = random.randint(50, HEIGHT - 150)  
    is_trap = random.choice([True, False])  # 50% de chances d'être un piège
    return pygame.Rect(x, y, 20, 20)

# Fonction pour afficher l'écran de fin de partie
def show_game_over_screen():
    screen.fill(BLACK)
    font = pygame.font.SysFont(None, 48)
    text = font.render("You Lose!", True, WHITE)
    try_again_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
    pygame.draw.rect(screen, RED, try_again_button)
    button_text = font.render("Try Again", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 100))
    screen.blit(button_text, (WIDTH // 2 - button_text.get_width() // 2, HEIGHT // 2 + 5))
    pygame.display.flip()
    return try_again_button

# Initialisation du jeu
reset_game()

# État du jeu
game_active = False

# Fonction pour afficher l'écran de login
def show_login_screen():
    screen.fill(BLACK)
    font = pygame.font.SysFont(None, 48)
    text = font.render("Bienvenue dans Deep Blue Challenge", True, WHITE)
    start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
    pygame.draw.rect(screen, RED, start_button)
    button_text = font.render("Commencer", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 100))
    screen.blit(button_text, (WIDTH // 2 - button_text.get_width() // 2, HEIGHT // 2 + 5))
    pygame.display.flip()
    return start_button

# Boucle principale du jeu
running = True
while running:
    if game_over:
        try_again_button = show_game_over_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and try_again_button.collidepoint(event.pos):
                reset_game()
                game_active = True
    elif not game_active:
        start_button = show_login_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and start_button.collidepoint(event.pos):
                reset_game()
                game_active = True
    else:
        screen.fill(BLUE)

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Contrôles du joueur
        keys = pygame.key.get_pressed()
        if fuel > 0:
            if keys[pygame.K_LEFT] and player_rect.left > 0:
                player_rect.x -= player_speed
                fuel -= 0.1 / level
            if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
                player_rect.x += player_speed
                fuel -= 0.1 / level
            if keys[pygame.K_UP] and player_rect.top > 0:
                player_rect.y -= player_speed
                fuel -= 0.1 / level
            if keys[pygame.K_DOWN] and player_rect.bottom < HEIGHT - 40:
                player_rect.y += player_speed
                fuel -= 0.1 / level
        else:
            add_message("Carburant épuisé ! Game Over.")
            game_over = True

        # Déplacement de l'IA
        move_ai(ai_rect, player_rect, ai_speed)

        # Gérer les bonus/pièges
        current_time = pygame.time.get_ticks() / 1000
        if not bonus_rect and current_time - last_bonus_spawn > bonus_spawn_interval:
            bonus_rect = spawn_bonus()
            last_bonus_spawn = current_time

        if bonus_rect and player_rect.colliderect(bonus_rect):
            if is_trap:
                fuel += penalty_fuel_amount
                add_message("Piège ! Carburant réduit.")
            else:
                fuel += bonus_fuel_amount
                add_message("Bonus ! Carburant augmenté.")
            bonus_rect = None 

        # Vérifier collision avec l'IA
        if player_rect.colliderect(ai_rect):
            add_message("Collision avec l'IA ! Game Over.")
            game_over = True

        # Vérifier collision avec les îles
        for island in islands:
            if player_rect.colliderect(island):
                add_message("Collision avec une île ! Game Over.")
                game_over = True

        # Vérifier le temps pour passer au niveau suivant
        if current_time >= time_to_survive + start_ticks / 1000:
            level += 1
            time_to_survive += 5
            ai_speed += 1
            fuel = fuel_initial
            start_ticks = pygame.time.get_ticks()
            add_islands(1)  
            add_message(f"Niveau {level} atteint !")

        # Dessiner les îles
        for island in islands:
            screen.blit(island_img, island.topleft)

        # Dessiner les bonus/pièges
        if bonus_rect:
            color = RED if is_trap else GREEN
            pygame.draw.rect(screen, color, bonus_rect)

        # Dessiner les bateaux
        screen.blit(player_boat_img, player_rect.topleft)
        screen.blit(ai_boat_img, ai_rect.topleft)

        # Afficher les informations
        font = pygame.font.SysFont(None, 36)
        fuel_text = font.render(f"Carburant : {int(fuel)}%", True, WHITE)
        level_text = font.render(f"Niveau : {level}", True, WHITE)
        time_text = font.render(f"Temps restant : {int(time_to_survive - (current_time - start_ticks / 1000))}s", True, WHITE)
        screen.blit(fuel_text, (10, 10))
        screen.blit(level_text, (10, 50))
        screen.blit(time_text, (10, 90))

        draw_messages()
        draw_scrolling_text()

        pygame.display.flip()
        clock.tick(60)

pygame.quit()