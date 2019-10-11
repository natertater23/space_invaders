class Settings:

    def __init__(self):
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)

        # Ship settings
        self.ship_speed = 1.5
        self.ship_limit = 3
        # Laser settings
        self.laser_speed = 3
        self.laser_width = 3
        self.laser_height = 15
        self.laser_color = (255, 0, 0)
        self.lasers_allowed = 4
        # Alien settings
        self.alien_speed = 2
        self.fleet_speed = 10
        self.fleet_direction = 1  # 1 is right -1 is left
        # Game settings
        self.speed_up = 1.2
        self.initialize_dynamic_settings()
        # Score settings
        self.alien_points = 50

    def initialize_dynamic_settings(self):
        self.ship_speed = 1.5
        self.laser_speed = 3
        self.alien_speed = 1
        self.fleet_direction = 1

    def increase_speed(self):
        self.ship_speed *= self.speed_up
        self.laser_speed *= self.speed_up
        self.alien_speed *= self.speed_up
        self.alien_points = int(self.alien_points * self.speed_up)
