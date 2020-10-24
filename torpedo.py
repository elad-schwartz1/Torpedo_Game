################################################################################
# FILE : torpedo.py
# WRITERS : Elad_Schwartz
# DESCRIPTION: File contains torpedo class used in asteroids game. Torpedos are used
#              to destroy asteroids
################################################################################
import math

class Torpedo:
    """Torpedo Class is the Ship's ammunition. Torpedos are shot by the Ship and used to destroy
    asteroids. Torpedos are destroyed either through collisions with asteroids or by exhausting their
    lifespan"""
    def __init__(self, x, y, x_speed, y_speed, direction,life_count):
        """
        Torpedo constructor
        :param x: Torpedo location on x axis
        :param y: Torpedo location on y axis
        :param x_speed: Torpedo speed in x axis
        :param y_speed: Torpedo speed in y axis
        :param direction: Torpedo's direction (fixed at the angle that the
                        ship was pointing when the torpedo was fired
        :param life_count: Lifespan of the Torpedo.

        """
        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.dir = direction
        self.radius = 4
        self.life_count = life_count



    def getx(self):
        """Gets x location"""
        return self.x

    def gety(self):
        """Gets y location"""
        return self.y


    def get_dir(self):
        """Gets direction (angle of torpedo)"""
        return self.dir

    def get_radius(self):
        """Gets radius of torpedo"""
        return self.radius

    def set_x(self, x):
        """Sets x location of torpedo"""
        self.x = x

    def set_y(self, y):
        """Sets y location of torpedo"""
        self.y = y

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