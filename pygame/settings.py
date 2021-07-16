
class Settings():
    def __init__(self) -> None:
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (10 , 10, 10)
        #ship settings
        self.ship_speed_factor = 1.5
        self.ship_limit = 3

        #bullet settings
        self.bullet_speed_factor = 5
        self.bullet_width = 300
        self.bullet_height = 25
        self.bullet_color = (57, 255, 20)
        self.bullets_limit = 10

        #alien settings
        self.alien_speed_factor = 0.8
        self.fleet_drop_speed = 30
        # 1 means right, -1 means left
        self.fleet_direction = 1
        
        # speed up the game
        self.speedup_scale = 1.2
        # speed up ponits gain
        self.score_scale = 1.5

        self.initialize_dynamic_settings()
    def initialize_dynamic_settings(self):
        # init settings
        self.ship_speed_factor = 2
        self.alien_speed_factor = 0.7
        self.bullet_speed_factor = 5
        self.fleet_direction = 1
        self.alien_points = 50  

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)