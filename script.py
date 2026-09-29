import pygame
import random
import math


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
        self.hitbox = pygame.Rect(self.pos.x - 9, self.pos.y, 20, 20)
        self.dir = pygame.math.Vector2(0, 1)
        self.basetri = [
        pygame.math.Vector2(self.pos.x, self.pos.y - 15),
        pygame.math.Vector2(self.pos.x - 15, self.pos.y + 25),
        pygame.math.Vector2(self.pos.x + 15, self.pos.y + 25)]
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

    screen.fill((0, 0, 0))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: #keys inpuits
        newplist = []
        for p in ship.basetri:
            rotated = p.rotate(5)
            new = ship.pos + rotated
            newplist.append(new) #test
        pygame.draw.polygon(screen, (150, 147, 147), newplist)
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
                    asteroid.vecmove = pygame.math.Vector2(1, 1)
                asteroid.vecmove = asteroid.vecmove.normalize() * 2

    
    clock.tick(30)
    pygame.display.flip()


pygame.quit()
