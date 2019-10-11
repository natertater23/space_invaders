import sys
import pygame
from laser import Laser
from alien import Alien
from time import sleep


# This will handle key presses and exiting the game
def check_user(settings, screen, stats, score, button, ship, aliens, lasers):
    for event in pygame.event.get():
        # Exit's Game
        if event.type == pygame.QUIT:
            sys.exit()
        # When key is pressed right and left arrow key respond and space bar shoots lasers
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                ship.moving_right = True
            elif event.key == pygame.K_LEFT:
                ship.moving_left = True
            elif event.key == pygame.K_SPACE:
                if len(lasers) < settings.lasers_allowed:
                    new_laser = Laser(settings, screen, ship)
                    lasers.add(new_laser)
        # Play button
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if button.rect.collidepoint(mouse_x, mouse_y) and not stats.game_active:
                settings.initialize_dynamic_settings()
                pygame.mouse.set_visible(False)
                stats.reset_stats()
                stats.game_active = True
                score.prep_score()
                score.prep_high_score()
                score.prep_level()
                score.prep_ships()
                aliens.empty()
                lasers.empty()
                create_aliens(settings, screen, ship, aliens)
                ship.center_ship()
        # Makes sure we stop moving when key is not pressed
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                ship.moving_right = False
            elif event.key == pygame.K_LEFT:
                ship.moving_left = False


# Handles the drawing and updates screen
def update_screen(settings, screen, stats, score, ship, aliens, lasers, button):
    screen.fill(settings.bg_color)
    for laser in lasers.sprites():
        laser.draw_laser()
    ship.blitme()
    aliens.draw(screen)
    score.show_score()
    if not stats.game_active:
        button.draw_button()
        pygame.mouse.set_visible(True)

    pygame.display.flip()


def update_lasers(settings, screen, stats, score, ship, aliens, lasers):
    lasers.update()
    # Remove excess lasers
    for laser in lasers.copy():
        if laser.rect.bottom <= 0:
            lasers.remove(laser)
    collisions = pygame.sprite.groupcollide(lasers, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += settings.alien_points * len(aliens)
            score.prep_score()
        check_high_score(stats, score)

    if len(aliens) == 0:
        lasers.empty()
        settings.increase_speed()
        stats.level += 1
        score.prep_level()
        create_aliens(settings, screen, ship, aliens)


def check_fleet_edges(settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(settings, aliens)
            break


def change_fleet_direction(settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += settings.fleet_speed
    settings.fleet_direction *= -1


def update_aliens(settings, screen, stats, score, ship, aliens, lasers):
    check_fleet_edges(settings, aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(settings, screen, stats, score, ship, aliens, lasers)
    # Check aliens on bottom of screen
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(settings, screen, stats, score, ship, aliens, lasers)
            break


def create_aliens(settings, screen, ship, aliens):
    # Calculate how many rows and aliens
    alien = Alien(settings, screen)
    alien_width = alien.rect.width
    avail_space_x = settings.screen_width - 2 * alien_width
    avail_space_y = (settings.screen_width - (3 * alien.rect.height) - ship.rect.height)
    num_rows = int(avail_space_y / (2 * alien.rect.height))
    num_aliens = int(avail_space_x / (2*alien_width))
    # Create aliens in the nested for loop
    for row_number in range(num_rows):
        for alien_number in range(num_aliens):
            alien = Alien(settings, screen)
            alien.x = alien_width + 2 * alien_width * alien_number
            alien.rect.x = alien.x
            aliens.add(alien)


def ship_hit(settings, screen, stats, score, ship, aliens, lasers):
    if stats.ships_left > 0:
        stats.ships_left -= 1
        score.prep_ships()
        aliens.empty()
        lasers.empty()

        create_aliens(settings, screen, ship, aliens)
        ship.center_ship()

        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_high_score(stats, score):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        score.prep_high_score()
