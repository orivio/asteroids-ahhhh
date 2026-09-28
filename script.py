import pygame
import random


pygame.init()
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()


class asteroid:
    def __init__(self):
        self.vec = pygame.math.Vector2(random.randint(100, 500), random.randint(100, 300))
        self.vecmove = pygame.math.Vector2(random.randint(1, 3), random.randint(1, 3))
        self.radius = random.randint(10, 30)
        self.id = random.randint(0, 999)

class spaceship:
    def __init__(self):
        self.pos = pygame.math.Vector2(300, 200)

gameloop = True

asteroids = [asteroid(), asteroid(), asteroid(), asteroid(), asteroid(), asteroid()]
ship = spaceship()
for ast in asteroids:
    for other in asteroids:
        if ast.vec == other.vec:
            ast = asteroid()
        if ast.id == other.id:
            ast = asteroid()


while gameloop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameloop = False
    screen.fill((54, 33, 12))
    for asteroid in asteroids:
        pygame.draw.circle(screen, ((88, 149, 173)), (asteroid.vec.x, asteroid.vec.y), asteroid.radius)
        asteroid.vec += asteroid.vecmove
        if asteroid.vec.x + asteroid.radius > 600 or 0 > asteroid.vec.x - asteroid.radius:
            asteroid.vecmove.x *= -1 
        if asteroid.vec.y + asteroid.radius > 400 or 0 > asteroid.vec.y - asteroid.radius:
            asteroid.vecmove.y *= -1
        for other in asteroids:
            if other.id != asteroid.id:
                if asteroid.vec.distance_to(other.vec) <= asteroid.radius + other.radius:
                    asteroid.vecmove = asteroid.vecmove - other.vecmove
                    other.vecmove = other.vecmove + asteroid.vecmove
                if asteroid.vecmove == 0:
                    asteroid.vecmove += pygame.math.Vector2(1, 1)
                asteroid.vecmove = asteroid.vecmove.normalize() * 2
    pygame.draw.rect(screen, ((0, 0, 0)), pygame.Rect(ship.pos.x + -15, ship.pos.y - 15, 30, 30))

    
    clock.tick(30)
    pygame.display.flip()


pygame.quit()
