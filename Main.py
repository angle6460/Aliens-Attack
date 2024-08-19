import random
import survival
import level_settings
import sys
import pygame
import all_classes

pygame.init()

# when its set to 0, 0 it is automatically full screen
screen = pygame.display.set_mode((0, 0))

# getting the size of the screen as this may vary from computer to computer
S_WIDTH, S_HEIGHT = pygame.display.get_surface().get_size()
S_RECT = screen.get_rect()

# top left info
pygame.display.set_caption('Aliens Attack!!')
icon = pygame.image.load('IMG/ufo.png')
pygame.display.set_icon(icon)

# images
background = pygame.image.load('IMG/background.png')
background = pygame.transform.scale(background, (S_WIDTH, S_HEIGHT))

level = 1
stats = all_classes.Stats()
ship, bullets, aliens = level_settings.init(S_RECT, screen, stats)
font = pygame.font.Font('freesansbold.ttf', 30)
alive = False

# buttons
start_btn_img = pygame.image.load('IMG/start_btn.png')
start_btn_rect = start_btn_img.get_rect()
start_btn = all_classes.Button(S_WIDTH // 2 - 50 - start_btn_rect.width, S_HEIGHT // 2 - start_btn_rect.height // 2,
                               start_btn_img)
exit_btn_img = pygame.image.load('IMG/exit_btn.png')
exit_btn_rect = exit_btn_img.get_rect()
exit_btn = all_classes.Button(S_WIDTH // 2 + 50, S_HEIGHT // 2 - exit_btn_rect.height // 2, exit_btn_img)

shop_btn_img = pygame.image.load('IMG/shop 1 (edit).png')
shop_btn = all_classes.Button(600, 600, shop_btn_img)

# making the level buttons
list_level_buttons = level_settings.create_level_fleet(S_RECT, 17)
# making shop buttons
shop_btn_list = [all_classes.Button(0, 20, font.render(f'Speed upgrade 10,000', True, (255, 255, 255), (0, 0, 0))),
                 all_classes.Button(400, 20, font.render(f'Shooting upgrade 15,000', True, (255, 255, 255), (0, 0, 0))),
                 all_classes.Button(800, 20, font.render(f'Extra life 5,000', True, (255, 255, 255), (0, 0, 0))),
                 all_classes.Button(600, 20,
                                    font.render('New ability piercing bullet 30,000', True, (255, 255, 255), (0, 0, 0)))
                 ]
# sounds
bullet_shoot_sound = pygame.mixer.Sound('IMG/sounds/laser.wav')
hit_sound = pygame.mixer.Sound('IMG/sounds/explosion.wav')

pygame.mixer.music.load('IMG/sounds/background.wav')

bullet_counter = 0
piers = False


# playing function
def playing():
    pygame.mouse.set_visible(False)
    global alive, level, ship, bullet_counter, piers
    screen.blit(background, (0, 0))
    bullet_counter += 1
    aliens.update(screen)
    ship.update()
    bullets.update()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and bullet_counter > stats.shooting_speed:
        bullets.add(all_classes.Bullet(ship.rect, screen))
        bullet_counter = 0
        bullet_shoot_sound.play()

    print(piers)
    if keys[pygame.K_f] and stats.ability and not piers and bullet_counter > 50:
        piers = pygame.sprite.Group()
        piers.add(all_classes.Bullet(ship.rect, screen, speed=20, scale=(50, 10)))
        print(piers)
        bullet_counter = 0
    elif piers is not False:
        piers.update()
        pygame.sprite.groupcollide(piers, aliens, False, True)
        for bullet in piers.copy():
            if bullet.rect.y < 0:
                piers.empty()


    for bullet in bullets.copy():
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)

    if not aliens:
        list_level_buttons[level - 1].complete()
        alive = False

    if check_alien_col():
        for alien in aliens.copy():
            alien.drop()

    if stats.lives <= 0:
        sys.exit()


def check_alien_col():
    global aliens, alive, level
    collision = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collision:
        hit_sound.play()
        stats.money += random.randint(25 + level, 50 + level)
    if pygame.sprite.spritecollideany(ship, aliens):
        alive = False
        stats.lives -= 1
        aliens.empty()
        return False
    for alien in aliens.copy():
        if alien.rect.left < 0:
            return True
        if alien.rect.right > S_RECT.right:
            return True
        if alien.rect.bottom > S_RECT.bottom:
            alive = False
            stats.lives -= 1

            return False
    return False


counter = 0
i = 0
spot = 0
selecting = False
shopping = False


# when the player is in the main menu
def main_menu():
    global counter, i, alive, spot, ship, bullets, aliens, selecting, shopping
    pygame.mouse.set_visible(True)

    # a list of colour that the background will cycle through
    list_of_colour = [(255, 0, 0), (255, 127, 0), (255, 255, 0), (127, 255, 0), (0, 255, 0), (0, 255, 127),
                      (0, 255, 255), (0, 127, 255), (0, 0, 255), (127, 0, 255), (255, 0, 255), (255, 0, 127)]

    #
    spot += 4
    counter += 1
    if counter == 30:
        i += 1
        counter = 0
        if i == len(list_of_colour):
            i = 0

    screen.fill(list_of_colour[i])
    if selecting:
        level_selecting()
    elif shopping:
        buying()
    else:
        if start_btn.draw(screen):
            survival.run(screen, S_RECT, 'normal')
            selecting = True
        if exit_btn.draw(screen):
            sys.exit()
        if shop_btn.draw(screen):
            shopping = True
    if spot > S_WIDTH:
        spot = -150
    screen.blit(font.render('Aliens Attack!', True, (0, 0, 0)), (spot, 150))


def buying():
    global shopping
    if exit_btn.draw(screen):
        shopping = False
    for count, value in enumerate(shop_btn_list):
        # shop_btn_list = [ all_classes.Button(0, 20, font.render(f'Speed upgrade 10,000', True, (255, 255, 255), (0,
        # 0, 0))), all_classes.Button(200, 20, font.render(f'Shooting upgrade 15,000', True, (255, 255, 255), (0, 0,
        # 0))), all_classes.Button(400, 20, font.render(f'Extra life 5,000', True, (255, 255, 255), (0, 0,
        # 0)))] all_classes.Button(600, 20, font.render('New ability piercing bullet 30,000', True, (255, 255, 255),
        # (0, 0, 0)))


        if value.draw(screen):
            if count == 0:
                if stats.money >= 10000:
                    if stats.buy_this('speed'):
                        stats.money -= 10000

                    else:
                        shop_btn_list[count] = all_classes.Button(
                            0, 20, font.render(f'Out of Stock', True, (255, 255, 255), (0, 0, 0))
                        )
            elif count == 1:
                if stats.money >= 15000:
                    if stats.buy_this('shooting'):
                        stats.money -= 15000

                    else:
                        shop_btn_list[count] = all_classes.Button(
                            400, 20, font.render(f'Out of Stock', True, (255, 255, 255), (0, 0, 0))
                        )
            elif count == 2:
                if stats.money >= 5000:
                    if stats.buy_this('lives'):
                        stats.money -= 5000

                    else:
                        shop_btn_list[count] = all_classes.Button(
                            800, 20, font.render(f'Out of Stock', True, (255, 255, 255), (0, 0, 0))
                        )
            elif count == 3:
                if stats.money >= 30000:
                    if stats.buy_this('abil'):
                        stats.money -= 30000
                    else:
                        shop_btn_list[count] = all_classes.Button(
                            800, 20, font.render(f'Out of Stock', True, (255, 255, 255), (0, 0, 0))
                        )


def level_selecting():
    global list_level_buttons, selecting, level, alive
    for button in list_level_buttons:
        if button.draw(screen):
            level = button.level
            load_level()

    if exit_btn.draw(screen):
        selecting = False


def load_level():
    global level, ship, bullets, aliens, alive
    if level == 1:
        ship, bullets, aliens = level_settings.lev_1(S_RECT, screen, stats)
        alive = True
    elif level == 2 and list_level_buttons[level - 2].completed:
        ship, bullets, aliens = level_settings.lev_2(S_RECT, screen, stats)
        alive = True
    elif level == 3 and list_level_buttons[level - 2].completed:
        ship, bullets, aliens = level_settings.lev_3(S_RECT, screen, stats)
        alive = True
    elif level == 4 and list_level_buttons[level - 2].completed:
        ship, bullets, aliens = level_settings.lev_4(S_RECT, screen, stats)
        alive = True
    elif level == 5 and list_level_buttons[level - 2].completed:
        ship, bullets, aliens = level_settings.lev_5(S_RECT, screen, stats)
        alive = True
    elif level == 6 and list_level_buttons[level - 2].completed:
        ship, bullets, aliens = level_settings.lev_6(S_RECT, screen, stats)
        alive = True
    elif level == 7 and list_level_buttons[level - 2].completed:
        ship, bullets, aliens = level_settings.lev_7(S_RECT, screen, stats)
        alive = True
    elif level == 8 and list_level_buttons[level - 2].completed:
        ship, bullets, aliens = level_settings.lev_8(S_RECT, screen, stats)
        alive = True
    elif level == 9 and list_level_buttons[level - 2].completed:
        ship, bullets, aliens = level_settings.lev_9(S_RECT, screen, stats)
        alive = True
    elif level == 10 and list_level_buttons[level - 2].completed:
        ship, bullets, aliens = level_settings.lev_10(S_RECT, screen, stats)
        alive = True
    elif level == 11 and list_level_buttons[level - 2].completed:
        ship, bullets, aliens = level_settings.lev_11(S_RECT, screen, stats)
        alive = True
    elif level == 12 and list_level_buttons[level - 2].completed:
        ship, bullets, aliens = level_settings.lev_12(S_RECT, screen, stats)
        alive = True
    elif level == 13 and list_level_buttons[level - 2].completed:
        ship, bullets, aliens = level_settings.lev_13(S_RECT, screen, stats)
        alive = True
    elif level == 14 and list_level_buttons[level - 2].completed:
        ship, bullets, aliens = level_settings.lev_14(S_RECT, screen, stats)
        alive = True
    elif level == 15 and list_level_buttons[level - 2].completed:
        ship, bullets, aliens = level_settings.lev_15(S_RECT, screen, stats)
        alive = True
    elif level == 16 and list_level_buttons[level - 2].completed:
        ship, bullets, aliens = level_settings.lev_16(S_RECT, screen, stats)
        alive = True
    elif level == 17 and list_level_buttons[level - 2].completed:
        ship, bullets, aliens = level_settings.lev_17(S_RECT, screen, stats)
        alive = True


def main():
    running = True
    clock = pygame.time.Clock()
    fps = 60
    music = False

    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
        if alive:
            playing()
        else:
            main_menu()
        if alive and music is False:
            music = True
            pygame.mixer.music.play()
        elif not alive and music is True:
            pygame.mixer.music.stop()
            music = False
        screen.blit(font.render(f'Money: {stats.money}', True, (0, 0, 0)), S_RECT.midtop)
        screen.blit(font.render(f'Lives: {stats.lives}', True, (0, 0, 0)), (0, 0))
        pygame.display.update()


stats.money += 10000000
if __name__ == '__main__':
    main()
