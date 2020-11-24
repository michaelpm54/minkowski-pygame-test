import pygame

# Collision detection
def minkowski_aabb(b, a):
    return pygame.Rect(
        a.left - b.right,
        a.top - b.bottom,
        a.width + b.width,
        a.height + b.height
    )

# Collision detection
def minkowski_collides(m):
    return m.collidepoint(0, 0)

# Collision response
def minkowski_min_displacement_vec(m):
    # What does it mean for a certain edge to be "the minimum"?
    # It means this edge is the one the object snaps to when moved the distance
    # detailed in the vec2 `bounds_point`.

    origin = pygame.Vector2(0, 0)

    # Assume the minimum is at the left edge.
    dist = abs(origin.x - m.left)
    bounds_point = pygame.Vector2(m.left, origin.y)

    # is the minimum at the right edge?
    if (abs(m.right - origin.x) < dist):
        dist = abs(m.right - origin.x)
        bounds_point = pygame.Vector2(m.right, origin.y)

    # is the minimum at the bottom edge?
    if (abs(m.bottom - origin.y) < dist):
        dist = abs(m.bottom - origin.y)
        bounds_point = pygame.Vector2(origin.x, m.bottom)
    
    # is the minimum at the top edge?
    if (abs(m.top - origin.y) < dist):
        dist = abs(m.top - origin.y)
        bounds_point = pygame.Vector2(origin.x, m.top)

    return bounds_point

def start():
    pygame.init()

    FPS = 60
    clock = pygame.time.Clock()
    size = width, height = 800, 600

    screen = pygame.display.set_mode(size)

    player = pygame.Rect(50, 50, 50, 50)
    
    terrain = [
        pygame.Rect(100, 150, 300, 100),
        pygame.Rect(400, 150, 300, 100),
        pygame.Rect(100, 250, 300, 100),
        pygame.Rect(100, 350, 300, 100),
    ]

    PLAYER_COLOUR_NO_COLLISION = [0,0,200,0.5]
    PLAYER_COLOUR_COLLISION = [200,0,200,0.5]
    player_colour = PLAYER_COLOUR_NO_COLLISION

    VELOCITY = 2.5

    mouse_based_movement = True
    show_minkowski = False

    run = True
    while run:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                run = False
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_q:
                    run = False
                elif ev.key == pygame.K_m:
                    mouse_based_movement = not mouse_based_movement
                elif ev.key == pygame.K_s:
                    show_minkowski = not show_minkowski
        
        if mouse_based_movement:
            (player.left, player.top) = pygame.mouse.get_pos()
            player.left -= player.width/2
            player.top -= player.height/2
        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player.left -= 1 * VELOCITY
            if keys[pygame.K_RIGHT]:
                player.right += 1 * VELOCITY
            if keys[pygame.K_UP]:
                player.top -= 1 * VELOCITY
            if keys[pygame.K_DOWN]:
                player.bottom += 1 * VELOCITY

        collision = False

        screen.fill((0,0,0))

        for t in terrain:
            m = minkowski_aabb(player, t)
            if show_minkowski:
                pygame.draw.rect(screen, [200,200,200,1], m, 1)
            if not collision:
                if minkowski_collides(m):
                    player_colour = PLAYER_COLOUR_COLLISION
                    player.move_ip(minkowski_min_displacement_vec(m))
                    collision = True
                else:
                    player_colour = PLAYER_COLOUR_NO_COLLISION

        for t in terrain:
            pygame.draw.rect(screen, [0,200,0,1], t, 1)
        screen.fill(player_colour, player)
        pygame.display.flip()
        clock.tick(FPS)

# if __name__ == "main":
start()
