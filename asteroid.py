################################################################################
# FILE : torpedo.py
# WRITERS : Elad_Schwartz
# DESCRIPTION: File contains asteroid class used in asteroids game. Asteroids
#              are the main obstacle in the game.
################################################################################

import math

class Asteroid:
    """Asteroids are the main obstacle in the game. Asteroids have mass and direction and will harm
    the ship in the case of a collision. Can be destroyed by torpedos"""
    def __init__(self, x, y, x_speed, y_speed, size):
        """
        Asteroid constructor
        :param x: asteroid's x location
        :param y: asteroid's y location
        :param x_speed: asteroid's speed in x direction
        :param y_speed: asteroid's speed in y direction
        :param size: Asteroids size
        """
        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.size = size


    def getx(self):
        """Gets x location"""
        return self.x

    def gety(self):
        """Gets y location"""
        return self.y

    def get_size(self):
        """Gets asteroid size"""
        return self.size

    def set_x(self, x):
        """Sets x location"""
        self.x = x

    def set_y(self, y):
        """Sets y location"""
        self.y = y

    def get_speed(self):
        """Gets x and y speeds"""
        return self.x_speed, self.y_speed

    def get_radius(self):
        """Gets radius"""
        return self.size*10-5

    def has_intersection(self, obj):
        """Function through which collisions are determined. The formula is used to
        determine whether the asteroid is close enough to the ship  to cause a crash.
        Returns True is collision is possible and False if not."""
        distance = math.sqrt((obj.getx() - self.x) ** 2 + (obj.gety() - self.y) ** 2)
        if distance <= obj.get_radius() + self.get_radius():
            return True
        return False