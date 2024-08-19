import pygame
from pygame.sprite import Sprite


class Button:
    def __init__(self, x: int = 0, y: int = 0,
                 image: pygame.image.load('IMG/background.png') = pygame.surface.Surface((100, 100)).fill(
                     (255, 255, 255))):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False
        self.completed = None

    def draw(self, screen):
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed(3)[0] == 1 and self.clicked is False:

                action = True
                self.clicked = True

        if pygame.mouse.get_pressed(3)[0] == 0:
            self.clicked = False

        # draw button
        screen.blit(self.image, self.rect)

        return action

    def get_x(self):
        return self.rect.x

    def make_level_button(self, level, font):
        self.completed = False
        self.level = level
        self.font = font

    def complete(self):
        self.completed = True
        self.image = self.font.render(f'Level {self.level}', True, (0, 0, 0), (0, 255, 0))


class Stats:
    def __init__(self, mode='level', diff='normal'):
        self.diff = diff
        if mode == 'level':
            self.lives = 3
            self.money = 0
            self.speed = 8
            self.shooting_speed = 7
            self.ability = False
            return
        if diff == 'easy':
            self.lives = 3
            self.money = 0
            self.speed = 10
            self.shooting_speed = 6
            self.ability = False
            return
        if diff == 'normal':
            self.lives = 2
            self.money = 0
            self.speed = 8
            self.shooting_speed = 7
            self.ability = False
            return
        if diff == 'hard':
            self.lives = 1
            self.money = 0
            self.speed = 6
            self.shooting_speed = 9
            self.ability = False
            return
        return

    def buy_this(self, what: str):
        if what == 'lives':
            self.lives += 1
            return True
        if what == 'speed':
            if self.speed > 15:
                return False
            self.speed += 1
            return True
        if what == 'shooting':
            if self.shooting_speed < 0:
                return False
            self.shooting_speed -= 1
            return True
        if what == 'abil':
            if self.ability:
                return False
            self.ability = True
            return True
        return False


class Ship:
    def __init__(self, WIN_RECT, screen, stats):
        image = pygame.image.load('IMG/spaceship.png')
        self.image = pygame.transform.scale(image, (64, 64))
        self.rect = self.image.get_rect()
        self.rect.midbottom = WIN_RECT.midbottom
        self.speed = stats.speed
        self.screen_rect = WIN_RECT
        self.screen = screen

    def update(self):
        keys = pygame.key.get_pressed()

        # checking left and right movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed

        # checking for collision with the edge of the screen
        if self.rect.right > self.screen_rect.right:
            self.rect.x -= self.speed
        if self.rect.x < 0:
            self.rect.x += self.speed

        self.screen.blit(self.image, self.rect)

    def get_mid_bottom(self):
        return self.rect.midbottom

    def reset(self):
        self.rect.midbottom = self.screen_rect.midbottom


class Alien(Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('IMG/enemy 2.png')
        self.image = pygame.transform.rotozoom(self.image, 0, 0.2)
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.x = self.rect.x
        self.speed = 2

    def update(self, screen):
        try:
            if not self.screen:
                self.screen = screen

        except:

            self.screen = screen
        self.screen.blit(self.image, self.rect)
        self.rect.x += self.speed

    def drop(self):
        self.rect.y += self.screen.get_rect().bottom * 0.1
        self.speed *= -1


class Bullet(Sprite):
    def __init__(self, ship_rect, screen, speed=10, colour: str = 'red', scale:tuple=(5, 10)):
        super().__init__()
        image = pygame.image.load('IMG/laser_thing.jpg')
        self.image = pygame.transform.scale(image, scale)
        self.rect = self.image.get_rect()
        self.rect.midbottom = ship_rect.midtop
        self.screen = screen
        self.speed = speed

    def update(self):
        self.screen.blit(self.image, self.rect)
        self.rect.y -= self.speed
