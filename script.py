import pygame
import random
import math


pygame.init()
WIDTH = 600
HEIGHT = 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
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
        self.angle = 0
        self.basetri = [
        pygame.math.Vector2(0, -15),
        pygame.math.Vector2(-15, 20),
        pygame.math.Vector2(15, 20)]
        self.vel = pygame.math.Vector2(0, 0)
        self.accel = 0.15
        self.drag = 0.99
        self.speedlim = 6

    def forward(self):
        return pygame.math.Vector2(0, -1).rotate(self.angle)

    def update(self, thrust):
        if thrust:
            self.vel += self.accel * self.forward()
            if self.vel.length() > self.speedlim:
                self.vel.scale_to_length(self.speedlim)
        self.vel *= self.drag
        self.pos += self.vel
        self.hitbox.center = self.pos

    def points(self):
        return[self.pos + p.rotate(self.angle) for p in self.basetri]

class square_alien:
    def __init__(self, x, y):
        self.pos = pygame.math.Vector2(x, y)
        self.angle = 0
        self.detected = False
        self.chase_speed = 1.3
        self.ambient_speed = 1
        self.viewrange = 150
        self.ignore_timer = 0
        self.turn = 0.03

    def forward(self):
        return pygame.math.Vector2(math.cos(self.angle), -math.sin(self.angle))
    def track(self, player):
        player_dist = (player.pos - self.pos)
        distance = player_dist.length()
        if distance == 0:
            return
        player_dir = player_dist/distance
        self_forward = self.forward()
        dot = self_forward.dot(player_dist)

        in_fov = False
        if dot > 0.7:
            in_fov = True

        distance = self.pos.distance_to(player.pos)
        in_dist = False
        if distance < self.viewrange:
            in_dist = True

        if in_dist and in_fov:
            self.detected = True
            self.ignore_timer = 90
        elif self.ignore_timer > 0:
            self.ignore_timer -= 1
        else:
            self.detected = False

        if self.detected == True:
            self.angle = math.atan2(-player_dir.y, player_dir.x)
            self.pos += player_dir * self.chase_speed
        else:
            if random.random() < 0.03:
                self.turn = random.uniform(-0.05, 0.05)
                self.angle += self.turn
                self.pos += self.forward() * self.ambient_speed
            if not (20 < self.pos.x < 580 and 20 < self.pos.y < 380):
                dist_center = pygame.math.Vector2(300, 200) - self.pos
                self.angle = math.atan2(-dist_center.y, dist_center.x)

class bullet:
    def __init__(self, player):
        self.vec = player.forward() * 2

asteroids = [asteroid(), asteroid(), asteroid(), asteroid(), asteroid(), asteroid()]
enemies = [square_alien(100, 200)]
ship = spaceship()
bullets = []

gameloop = True

while gameloop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameloop = False

    screen.fill((0, 0, 0))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: #keys inpuits
        ship.angle -= 5
    if keys[pygame.K_RIGHT]:
        ship.angle += 5
    if keys[pygame.K_f]:
        bullets.append(bullet(ship))
    if keys[pygame.K_UP]:
        ship.update(True)
    elif not keys[pygame.K_UP]:
        ship.vel *= 0.2

    pygame.draw.polygon(screen, (150, 147, 147), ship.points())

    for asteroid in asteroids:
        pygame.draw.circle(screen, ((88, 149, 173)), (asteroid.vec.x, asteroid.vec.y), asteroid.radius)
        asteroid.vec += asteroid.vecmove
        if asteroid.vec.x + asteroid.radius > 600 or 0 > asteroid.vec.x - asteroid.radius:
            asteroid.vecmove.x *= -1 
        if asteroid.vec.y + asteroid.radius > 400 or 0 > asteroid.vec.y - asteroid.radius:
            asteroid.vecmove.y *= -1
            
        for other in asteroids:
            if other.id != asteroid.id:
                vecdif = other.vec - asteroid.vec
                if 0 < vecdif.length() <= asteroid.radius + other.radius:
                    vecdif = vecdif.normalize()
                    spd = (asteroid.vecmove - other.vecmove).dot(vecdif)
                    if spd > 0:
                        asteroid.vecmove -= vecdif * spd
                        other.vecmove += vecdif * spd

    for enemy in enemies:
        enemy.track(ship)
        pygame.draw.rect(screen, ((88, 149, 173)), (enemy.pos.x - 30, enemy.pos.y - 30, 30, 30))

    for bull in bullets:

        pygame.draw.circle(screen, (0, 255, 0), (bull.vec.x, bull.vec.y), 1)

    if ship.pos.x > WIDTH:
        ship.pos.x = 0
    elif ship.pos.x < 0:
        ship.pos.x = WIDTH
    if ship.pos.y > HEIGHT:
        ship.pos.y = 0
    elif ship.pos.y < 0:
        ship.pos.y = HEIGHT

    
    clock.tick(30)
    pygame.display.flip()

pygame.quit()
