
import sys , pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        # move to right
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        # move to left
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        #check number of bullets on screen and fire a bullet 
        fire_bullets(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        # stop moving to right
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        # stop moving to right
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                check_keydown_events(event, ai_settings, screen, ship, bullets)
            elif event.type == pygame.KEYUP:
                check_keyup_events(event, ship)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                check_play_button(ai_settings, screen, stats, sb, play_button, ship, 
                    aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, 
        aliens, bullets, mouse_x, mouse_y):

    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # reset settings when the game start
        ai_settings.initialize_dynamic_settings()

        stats.reset_stats()
        stats.game_active = True
        #reset scoreboard image
        sb.prep_score()
        sb.prep_level()
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
        pygame.mouse.set_visible(False)
        # create new fleet
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, 
        play_button):
        #draw the screen 
        screen.fill(ai_settings.bg_color)
        for bullet in bullets.sprites():
            bullet.draw_bullet()
        ship.blitme()
        aliens.draw(screen)
        sb.show_score()
        if not stats.game_active:
            play_button.draw_button()
        # make most recent drawn screen visible
        pygame.display.flip()
def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    bullets.update()
    # delete bullet out of screen
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullets_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)
    
def check_bullets_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions :
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
    if len(aliens) == 0:
        #clear bullets on screen and create new fleet
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)
        # if fleet was clear increase level by 1
        stats.level += 1
        sb.prep_level()
def fire_bullets(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullets_limit:
            new_bullet = Bullet(ai_settings, screen, ship)
            bullets.add(new_bullet)

def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2*alien_width
    number_aliens_x = int(available_space_x/ (2*alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y/ (2 * alien_height))
    return number_rows
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    # create an alien and find number of aliens in row
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, 
        alien.rect.height)
    
    # check number of rows avalialbe and create aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            #create alien and place it 
            create_alien(ai_settings, screen, aliens, alien_number, 
                row_number)
def check_fleet_edges(ai_settings, aliens):
    # if aliens reached an edge 
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break
def change_fleet_direction(ai_settings, aliens):
    # go down if aliens reached edges
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # check the fleet reached edge and update position of entire fleet
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # look for aliens ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        print("SHIP HITTED!")
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
    # look for aliens reaches bottom
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)
def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    if stats.ships_left > 0:
        # minus oen ship from stats if get hit
        stats.ships_left -= 1
        # reset the fleet and bullets
        aliens.empty()
        bullets.empty()
        # create new fleet and ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        #pause
        sleep(0.5)
        # update scoreboard when hit
        sb.prep_ships()
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    # check for aliens reached bottom of the screen
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break
    
