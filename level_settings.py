import all_classes
import pygame


def init(screen_rect, screen, stats):  # for the ship and bullets list
    ship = all_classes.Ship(screen_rect, screen, stats)
    aliens = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    return ship, bullets, aliens


def lev_1(screen_rect, screen, stats):
    ship, bullets, aliens = init(screen_rect, screen, stats)
    aliens = _create_fleet(screen_rect, 10)
    return ship, bullets, aliens


def lev_2(screen_rect, screen, stats):
    ship, bullets, aliens = init(screen_rect, screen, stats)
    aliens = _create_fleet(screen_rect, 15)
    aliens = speed_up_aliens(aliens, 1.5)
    return ship, bullets, aliens


def lev_3(screen_rect, screen, stats):
    ship, bullets, aliens = init(screen_rect, screen, stats)
    aliens = _create_fleet(screen_rect, 20)
    aliens = speed_up_aliens(aliens, 1.5)
    return ship, bullets, aliens


def lev_4(screen_rect, screen, stats):
    ship, bullets, aliens = init(screen_rect, screen, stats)
    aliens = _create_fleet(screen_rect, 50)
    aliens = speed_up_aliens(aliens, 1)
    return ship, bullets, aliens


def lev_5(screen_rect, screen, stats):
    ship, bullets, aliens = init(screen_rect, screen, stats)
    aliens = _create_fleet(screen_rect, 100)
    aliens = speed_up_aliens(aliens, 2)
    return ship, bullets, aliens


def lev_6(screen_rect, screen, stats):
    ship, bullets, aliens = init(screen_rect, screen, stats)
    aliens = _create_fleet(screen_rect, 6)
    aliens = speed_up_aliens(aliens, 5)
    return ship, bullets, aliens


def lev_7(screen_rect, screen, stats):
    ship, bullets, aliens = init(screen_rect, screen, stats)
    aliens = _create_fleet(screen_rect, 1)
    aliens = speed_up_aliens(aliens, 10)
    return ship, bullets, aliens


def lev_8(screen_rect, screen, stats):
    ship, bullets, aliens = init(screen_rect, screen, stats)
    aliens = _create_fleet(screen_rect, 1)
    aliens = speed_up_aliens(aliens, 30)
    return ship, bullets, aliens


def lev_9(screen_rect, screen, stats):
    ship, bullets, aliens = init(screen_rect, screen, stats)
    aliens = _create_fleet(screen_rect, 200)
    aliens = speed_up_aliens(aliens, 1.6)
    return ship, bullets, aliens


def lev_10(screen_rect, screen, stats):
    ship, bullets, aliens = init(screen_rect, screen, stats)
    aliens = _create_fleet(screen_rect, 50)
    aliens = speed_up_aliens(aliens, 3)

    return ship, bullets, aliens


def lev_11(screen_rect, screen, stats):
    ship, bullets, aliens = init(screen_rect, screen, stats)
    aliens = _create_fleet(screen_rect, 10)
    aliens = speed_up_aliens(aliens, 2)
    return ship, bullets, aliens


def lev_12(screen_rect, screen, stats):
    ship, bullets, aliens = init(screen_rect, screen, stats)
    aliens = _create_fleet(screen_rect, 1)
    aliens = speed_up_aliens(aliens, 2 * 1.1)
    return ship, bullets, aliens


def lev_13(screen_rect, screen, stats):
    ship, bullets, aliens = init(screen_rect, screen, stats)
    aliens = _create_fleet(screen_rect, 10)
    aliens = speed_up_aliens(aliens, 2 * 1.1 * 1.1)
    return ship, bullets, aliens


def lev_14(screen_rect, screen, stats):
    ship, bullets, aliens = init(screen_rect, screen, stats)
    aliens = _create_fleet(screen_rect, 20)
    aliens = speed_up_aliens(aliens, 3)
    return ship, bullets, aliens


def lev_15(screen_rect, screen, stats):
    ship, bullets, aliens = init(screen_rect, screen, stats)
    aliens = _create_fleet(screen_rect, 30)
    aliens = speed_up_aliens(aliens, 5)
    return ship, bullets, aliens


def lev_16(screen_rect, screen, stats):
    ship, bullets, aliens = init(screen_rect, screen, stats)
    aliens = _create_fleet(screen_rect, 1)
    aliens = speed_up_aliens(aliens, 50)
    return ship, bullets, aliens


def lev_17(screen_rect, screen, stats):
    ship, bullets, aliens = init(screen_rect, screen, stats)
    aliens = _create_fleet(screen_rect, 1)
    aliens = speed_up_aliens(aliens, 200)
    return ship, bullets, aliens


def _create_fleet(screen_rect, num_of_aliens):
    # Create the alien fleet
    # creating one alien ship and find the number of aliens that will fit in the row
    aliens = pygame.sprite.Group()
    counter = 0
    alien = all_classes.Alien()
    alien_width, alien_height = alien.rect.size
    available_space_x = screen_rect.right - (2 * alien_width)
    number_aliens_x = available_space_x // (2 * alien_width)
    row_number = -1

    running = True
    while running:
        row_number += 1
        for alien_number in range(number_aliens_x):
            if counter >= num_of_aliens:
                running = False
                break
            aliens.add(_create_aliens(alien_number, row_number))
            counter += 1
    return aliens


def _create_aliens(alien_number, row_number):
    alien = all_classes.Alien()
    alien_width, alien_height = alien.rect.size
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height - 2 * alien.rect.height * row_number

    return alien


def speed_up_aliens(aliens, scale):
    gruop = pygame.sprite.Group()
    for alien in aliens.copy():
        alien.speed *= scale
        gruop.add(alien)
    return gruop


def create_level_fleet(screen_rect, num_of_levels):
    # Create the alien fleet
    # creating one alien ship and find the number of aliens that will fit in the row
    font = pygame.font.Font('freesansbold.ttf', 20)
    aliens = []
    counter = 0 + 1
    alien = all_classes.Button(image=font.render(f'level: {counter}', True, (255, 255, 255), (0, 0, 0)))
    alien_width, alien_height = alien.rect.size
    available_space_x = screen_rect.right
    number_aliens_x = available_space_x // (2 * alien_width)
    row_number = -1

    running = True
    while running:
        row_number += 1
        for alien_number in range(number_aliens_x):
            if counter >= num_of_levels + 1:
                running = False
                break
            aliens.append(create_level_button(alien_number, row_number, counter, font))
            counter += 1
    return aliens


def create_level_button(level_num, row_num, counter, font):
    alien = all_classes.Button(image=font.render(f'level: {counter}', True, (255, 255, 255), (0, 0, 0)))
    alien_width, alien_height = alien.rect.size
    alien.x = alien_width + 1.5 * alien_width * level_num
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_num
    alien.make_level_button(counter, font)

    return alien


def make_dummy_button():
    pass
