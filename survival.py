import json
import sys
import all_classes
import level_settings
import pygame


def check_alien_col(S_RECT):
    global aliens, alive, stats, ship, bullets, level, score
    collision = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collision:
        stats.money += 50
        score += 50
    if pygame.sprite.spritecollideany(ship, aliens):
        aliens.empty()

        stats.lives -= 1
        level -= 1
        return False
    for alien in aliens.copy():
        if alien.rect.left < 0:
            return True
        if alien.rect.right > S_RECT.right:
            return True
        if alien.rect.bottom > S_RECT.bottom:

            stats.lives -= 1
            level -= 1
            aliens.empty()
            return False
    return False


def init(screen, S_rect, diff):
    stats = all_classes.Stats('survival', diff)
    ship = all_classes.Ship(S_rect, screen, stats)
    bullets = pygame.sprite.Group()
    aliens = pygame.sprite.Group()
    return stats, ship, bullets, aliens


def run(screen, S_RECT, diff):
    global stats, ship, bullets, aliens, level, score
    stats, ship, bullets, aliens = init(screen, S_RECT, diff)
    font = pygame.font.Font('freesansbold.ttf', 32)
    level = 0
    clock = pygame.time.Clock()
    tracker = 300
    bullet_counter = 0
    score = 0
    pygame.mixer.music.load('IMG/sounds/background.wav')
    pygame.mixer.music.play()
    while True:
        screen.fill((30, 30, 30))
        clock.tick(30)
        keys = pygame.key.get_pressed()
        if tracker > 0:
            screen.fill((50, 50, 50))
            tracker -= 1
            # shop
        else:
            ship.update()
            bullet_counter += 1
            bullets.update()
            aliens.update(screen)
            if check_alien_col(S_RECT) or keys[pygame.K_DOWN]:
                for alien in aliens.copy():
                    alien.drop()
            for bullet in bullets.copy():
                if bullet.rect.bottom < 0:
                    bullets.remove(bullet)
            if keys[pygame.K_SPACE] and bullet_counter > stats.shooting_speed:
                bullets.add(all_classes.Bullet(ship.rect, screen))
                bullet_counter = 0
            if not aliens:

                level += 1
                if level % 5 == 0:
                    tracker = 300
                aliens = level_settings._create_fleet(S_RECT, 50)
                aliens = level_settings.speed_up_aliens(aliens, (level * 0.2) + 1)
            if stats.lives <= 0:
                text = 'please type out a 5 letter name'
                color = pygame.Color('dodgerblue2')
                running = True
                while running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            return
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                                if len(text) > 5:
                                    text = 'to big'
                                    continue
                                elif len(text) < 3:
                                    text = 'to small (like your pp)'
                                    continue
                                with open('score.json', 'r') as f:
                                    scores = json.load(f)
                                if text in scores:
                                    text = 'name already exists'
                                    continue
                                scores[text] = score
                                with open('score.json', 'w') as f:
                                    json.dump(scores, f)
                                running = False
                            elif event.key == pygame.K_BACKSPACE:
                                text = text[:-1]
                            elif event.key == pygame.K_ESCAPE:
                                return
                            else:
                                text += event.unicode

                    screen.fill((30, 30, 30))
                    txt_surface = font.render((text + '|'), True, color)
                    screen.blit(txt_surface, (50, 100))

                    pygame.display.flip()
                    clock.tick(30)
                x = 10
                with open('score.json', 'r') as f:
                    users = json.load(f)
                leader_board = {}
                total = []
                for user in users:
                    name = (user)
                    total_amount = users[user]
                    leader_board[total_amount] = name
                    total.append(total_amount)

                total = sorted(total, reverse=True)

                em = []
                index = 1
                for amt in total:
                    id_ = leader_board[amt]

                    name = id_
                    em.append((f"{index}: {name}, Aliens killed = {amt // 50}"))
                    if index == x:
                        break
                    else:
                        index += 1
                while True:
                    screen.fill((30, 30, 30))
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                return
                            if event.key == pygame.K_RETURN:
                                return
                            pass

                    for index, string in enumerate(em):
                        screen.blit(font.render(string, True, (0, 0, 200)), (0, index * 32))
                    pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_RETURN:
                    tracker = 0

        screen.blit(font.render(f'level: {level}', True, (255, 50, 50)), (0, 0))
        screen.blit(font.render(f'lives: {stats.lives}', True, (255, 50, 50)), (580, 0))
        screen.blit(font.render(f'money: {stats.money}', True, (255, 50, 50)), (1080, 0))
        pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((0, 0))
    S_RECT = pygame.display.get_surface().get_rect()
    run(screen, S_RECT, 'normal')
