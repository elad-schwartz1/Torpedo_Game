################################################################################
# FILE : torpedo.py
# WRITERS : Elad_Schwartz
# DESCRIPTION: Special torpedos have the same characteristics as regular torpedos
#              except that they are guided to their target.
################################################################################

import math

class Special_Torpedo:
    """Special_Torpedos are  Torpedos who track the asteroids they are aimed at until either they
    exhaust thier life span or they destroy an asteroid"""
    def __init__(self, x, y, x_speed, y_speed, direction,life_count,speed_match):
        """
        Torpedo constructor
        :param x: Torpedo location on x axis
        :param y: Torpedo location on y axis
        :param x_speed: Torpedo speed in x axis
        :param y_speed: Torpedo speed in y axis
        :param direction: Torpedo's direction (fixed at the angle that the
                        ship was pointing when the torpedo was fired
        :param life_count: Lifespan of the Torpedo.
        :param speed_match: Boolean value showing weather torpedo is aligned with asteroid it
                            is trying to destroy.
        """
        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.dir = direction
        self.radius = 4
        self.life_count = life_count
        self.speed_match = speed_match


    def getx(self):
        """Gets torpedos x location"""
        return self.x

    def gety(self):
        """Gets torpedos y location"""
        return self.y


    def get_dir(self):
        """Gets torpedos direction (angle of nose)"""
        return self.dir

    def get_radius(self):
        """Gets torpedos radius"""
        return self.radius

    def get_life(self):
        return self.life_count

    def set_x(self, x):
        """Sets torpedos x location"""
        self.x = x


    def set_y(self, y):
        """Sets torpedos y location"""
        self.y = y

    def set_dir(self, dir):
        """Sets torpedos direction (angle of nose)"""
        self.dir = dir

    def get_size(self):
        """Gets torpedos size"""
        return self.size

    def get_speed(self):
        """Gets torpedos speed"""
        return self.x_speed, self.y_speed

    def set_speed(self, new_x_speed, new_y_speed):
        """Speed is set in the x and y directions respectively."""
        self.x_speed = new_x_speed
        self.y_speed = new_y_speed



    def has_intersection(self, obj):
        """Function through which collisions are determined. The formula is used to
        determine whether the ship is close enough to an asteroid to cause a crash.
        Returns True is collision is possible and False if not."""
        distance = math.sqrt((obj.getx() - self.x) ** 2 + (obj.gety() - self.y) ** 2)
        if distance <= obj.get_radius() + self.get_radius():
            return True
        return False
