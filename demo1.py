import pygame

pygame.init()
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True

# Player
speed = 8
y_velocity = 0
gravity = 0.6
jump_strength = 14
player_rect = pygame.Rect(100, 600, 50, 50)
screen_rect = screen.get_rect()

# Platforms
platform_rects = [
    pygame.Rect(0, 650, 1280, 70),      # ground
    pygame.Rect(1480, 500, 200, 20),
    pygame.Rect(2080, 400, 200, 20),
    pygame.Rect(1880, 550, 200, 20)
]

kill_rects = [
    pygame.Rect(0, 900, 1280, 50)  # kill zone below the screen
]

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # ---- HORIZONTAL MOVEMENT ----
    dx = 0 # this stands for delta x <- delta means change
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        dx = -speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        dx = speed

    player_rect.x = screen_width // 2  # freeze player horizontally
    for platform in platform_rects:
        platform.x -= dx

    # X collisions
    for platform in platform_rects:
        if player_rect.colliderect(platform):
            if dx > 0:  # moving right
                player_rect.right = platform.left
            elif dx < 0:  # moving left
                player_rect.left = platform.right

    # ---- VERTICAL MOVEMENT ----
    y_velocity += gravity
    player_rect.y += y_velocity

    on_ground = False

    for platform in platform_rects:
        if player_rect.colliderect(platform):
            if y_velocity > 0:  # falling
                player_rect.bottom = platform.top
                y_velocity = 0
                on_ground = True
            elif y_velocity < 0:  # jumping
                player_rect.top = platform.bottom
                y_velocity = 0
    
    for kill_rect in kill_rects:
        if player_rect.colliderect(kill_rect):
            player_rect.topleft = (100, 600)
            y_velocity = 0

    # ---- JUMPING ----
    if keys[pygame.K_SPACE] and on_ground:
        y_velocity = -jump_strength


    # ---- DRAWING ----
    screen.fill("beige")
    pygame.draw.rect(screen, "purple", player_rect)
    for platform in platform_rects:
        pygame.draw.rect(screen, "brown", platform)

    pygame.display.flip()

pygame.quit()
