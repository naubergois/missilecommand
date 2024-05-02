import pygame
import random
import math

pygame.init()

# Configurações da tela
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Missile Command")

# Cores
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Parâmetros do jogo
missile_speed = 5
enemy_missile_speed = 3
explosion_radius = 40
explosion_duration = 60
player_score = 0

# Fonte para Textos
font = pygame.font.Font(None, 24)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

class Cannon:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        pygame.draw.rect(screen, blue, (self.x - 15, self.y - 15, 30, 30), 0)

class Missile:
    def __init__(self, x, y, target_x, target_y, is_enemy):
        self.x = x
        self.y = y
        self.target_x = target_x
        self.target_y = target_y
        self.is_enemy = is_enemy
        angle = math.atan2(target_y - y, target_x - x)
        self.vx = math.cos(angle) * missile_speed
        self.vy = math.sin(angle) * missile_speed
        self.active = True

    def move(self):
        if self.active:
            self.x += self.vx
            self.y += self.vy

    def draw(self):
        if self.active:
            color = red if self.is_enemy else white
            pygame.draw.line(screen, color, (self.x, self.y), (self.x + self.vx, self.y + self.vy), 2)

class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.timer = explosion_duration

    def draw(self):
        if self.timer > 0:
            radius = ((explosion_duration - self.timer) / explosion_duration) * explosion_radius
            pygame.draw.circle(screen, white, (int(self.x), int(self.y)), int(radius))
            self.timer -= 1

class Enemy:
    def __init__(self, x, y, life=3):
        self.x = x
        self.y = y
        self.life = life
        self.speed = random.uniform(0.5, 1.5)

    def move(self):
        self.x += self.speed
        if self.x > screen_width or self.x < 0:
            self.speed *= -1

    def draw(self):
        pygame.draw.circle(screen, red, (int(self.x), int(self.y)), 10)
        draw_text(f'Life: {self.life}', font, white, screen, self.x - 20, self.y - 20)

    def hit(self):
        self.life -= 1
        if self.life <= 0:
            return True
        return False

# Inicialização de objetos
cannons = [Cannon(100, screen_height - 50), Cannon(400, screen_height - 50), Cannon(700, screen_height - 50)]
enemies = [Enemy(random.randint(100, screen_width - 100), 50) for _ in range(5)]
missiles = []
explosions = []

# Loop principal do jogo
running = True
while running:
    screen.fill(black)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            # Decidindo de qual canhão disparar com base na posição do clique
            if x < screen_width / 3:
                cannon_choice = cannons[0]
            elif x < 2 * screen_width / 3:
                cannon_choice = cannons[1]
            else:
                cannon_choice = cannons[2]
            missiles.append(Missile(cannon_choice.x, cannon_choice.y, x, y, False))

    # Movimento e desenho dos canhões
    for cannon in cannons:
        cannon.draw()

    # Movimento e desenho dos inimigos
    for enemy in enemies:
        enemy.move()
        enemy.draw()

    # Lançamento de mísseis pelos inimigos
    for enemy in enemies:
        if random.random() < 0.01:  # Chance de lançar um míssil
            missiles.append(Missile(enemy.x, enemy.y, random.randint(0, screen_width), screen_height, True))

    # Movimento e desenho dos mísseis
    for missile in missiles:
        missile.move()
        missile.draw()

    # Detecção de colisão e remoção de inimigos
    for missile in missiles[:]:
        if missile.y < 0 or missile.y > screen_height or missile.x < 0 or missile.x > screen_width:
            missiles.remove(missile)
        else:
            for enemy in enemies[:]:
                if math.hypot(missile.x - enemy.x, missile.y - enemy.y) < 20 and not missile.is_enemy:
                    if enemy.hit():
                        explosions.append(Explosion(enemy.x, enemy.y))
                        enemies.remove(enemy)
                        player_score += 100  # Aumenta a pontuação ao destruir um inimigo

    # Desenho das explosões
    for explosion in explosions:
        explosion.draw()

    # Mostrar a pontuação do jogador
    draw_text(f'Score: {player_score}', font, white, screen, 5, 5)

    pygame.display.flip()
    pygame.time.Clock().tick(30)

pygame.quit()
