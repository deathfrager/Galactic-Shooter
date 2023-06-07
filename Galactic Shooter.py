import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Определение размеров окна
screen_width = 1920
screen_height = 1080

# Создание окна игры
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Shooter Game")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([50, 50])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = screen_width // 2
        self.rect.y = screen_height - 70

    def update(self):
        # Обработка перемещения игрока
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

        # Ограничение игрока в пределах экрана
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > screen_width - 50:
            self.rect.x = screen_width - 50

    def shoot(self):
        # Создание пули и добавление ее в группу пуль
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

# Класс врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([30, 30])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - 30)
        self.rect.y = random.randint(-100, -40)
        self.speedy = random.randint(1, 8)

    def update(self):
        # Перемещение врага вниз по экрану
        self.rect.y += self.speedy

        # Удаление врага, если он вышел за пределы экрана
        if self.rect.top > screen_height + 10:
            self.rect.x = random.randint(0, screen_width - 30)
            self.rect.y = random.randint(-100, -40)
            self.speedy = random.randint(1, 8)

# Класс пули
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([5, 15])
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        # Перемещение пули вверх по экрану
        self.rect.y += self.speedy

        # Удаление пули, если она вышла за пределы экрана
        if self.rect.bottom < 0:
            self.kill()

# Функция вывода сообщения о проигрыше
def show_game_over_screen():
    font = pygame.font.Font(None, 64)
    text = font.render("Вы проиграли!", True, WHITE)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text, text_rect)

    button_width = 300
    button_height = 80
    button_x = (screen_width - button_width) // 2
    button_y = (screen_height + button_height) // 2 + 20

    pygame.draw.rect(screen, WHITE, (button_x, button_y, button_width, button_height))
    font = pygame.font.Font(None, 32)
    text = font.render("Начать заново", True, BLACK)
    text_rect = text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    screen.blit(text, text_rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_x <= mouse_pos[0] <= button_x + button_width and \
                        button_y <= mouse_pos[1] <= button_y + button_height:
                    return

# Создание групп спрайтов
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Создание игрока и добавление его в группу спрайтов
player = Player()
all_sprites.add(player)

# Создание врагов и добавление их в группу спрайтов
for _ in range(10):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Цикл игры
running = True
clock = pygame.time.Clock()
while running:
    clock.tick(60)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Обновление игры
    all_sprites.update()

    # Обработка столкновений пуль и врагов
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Обработка столкновений игрока и врагов
    hits = pygame.sprite.spritecollide(player, enemies, False)
    if hits:
        show_game_over_screen()
        # Удаление всех спрайтов и перезапуск игры
        all_sprites.empty()
        enemies.empty()
        bullets.empty()
        player = Player()
        all_sprites.add(player)
        for _ in range(10):
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

    # Отрисовка игры
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()

# Завершение игры
pygame.quit()
