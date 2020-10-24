################################################################################
# FILE : torpedo.py
# WRITERS : Elad_Schwartz
# DESCRIPTION: File contains ship class. Ship is the tool through which game is played
#              can shoot rockets used to destroy asteroids.
################################################################################
import math

class Ship:
    """Ship class. The ship is the object of the game through which the player performs all the required
    tasks. The ship can be maneuvered, transported and used for shooting torpedos. """

    def __init__(self, x, y, x_speed, y_speed, direction):
        """
        Ship's constructor
        :param x: Ship's location on x axis
        :param y: Ship's location on y axis
        :param x_speed: Ship's speed in the x direction
        :param y_speed: Ship's speed in the y direction
        :param direction: Angle in which Ship's nose is pointed (radians) relative to North (0 deg)
        """
        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.dir = direction
        self.radius = 1
        self.size = 1


    def get_radius(self):
        """Gets ships radius"""
        return self.radius

    def get_size(self):
        """Gets ships size"""
        return self.size

    def get_speed(self):
        """gets ships x and y speeds"""
        return self.x_speed, self.y_speed

    def getx(self):
        """Gets ships x location"""
        return self.x

    def gety(self):
        """Gets ships y location"""
        return self.y

    def get_dir(self):
        """Gets ships direction (angle of nose)"""
        return self.dir

    def set_x(self, x):
        """sets ships x location"""
        self.x = x

    def set_y(self, y):
        """Sets ships y location"""
        self.y = y

    def set_dir(self, dir):
        """Sets ships direction (angle of nose)"""
        self.dir = dir

    def set_speed(self, new_x_speed, new_y_speed):
        """Speed is set in the x and y directions respectively."""
        self.x_speed = new_x_speed
        self.y_speed = new_y_speed

    def has_intersection(self, obj):
        """Function through which collisions are determined. The formula is used to
        determine whether the ship is close enough to a foreign object to cause a crash.
        Returns True is collision is possible and False if not."""
        distance = math.sqrt((obj.getx() - self.x) ** 2 + (obj.gety() - self.y) ** 2)
        if distance <= obj.get_radius() + self.get_radius():
            return True
        return False