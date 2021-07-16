import pygame
from settings import Settings
from ship import Ship
from alien import Alien
from game_stats import GameStats
from button import Button
from score_board import ScoreBoard
import game_function as gf
from pygame.sprite import Group
def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    # make a ship
    ship = Ship(ai_settings ,screen)
    # make an alien 
    alien = Alien(ai_settings, screen)
    # save stats of the game
    stats = GameStats(ai_settings)
    # make a group to store bullet
    bullets = Group()
    # make alien group
    aliens = Group()
    # make a button
    play_button = Button(ai_settings, screen, 'Play')
    #make a scoreboard
    sb = ScoreBoard(ai_settings, screen, stats)

    gf.create_fleet(ai_settings, screen, ship, aliens)
    
    while True:
        #screen.fill(ai_settings.bg_color)
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        if stats.game_active :
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)
if __name__ == '__main__':
    run_game()
