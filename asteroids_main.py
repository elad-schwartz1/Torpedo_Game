################################################################################
# FILE : torpedo.py
# WRITERS : Elad_Schwartz
# DESCRIPTION: Gamerunner is main function used to run 'asteroids' game to completion.
################################################################################

from screen import Screen
from ship import Ship
from asteroid import Asteroid
from torpedo import Torpedo
from special_torp import Special_Torpedo
import sys
import random
import math
import decimal

DEFAULT_ASTEROIDS_NUM = 5


class GameRunner:
    """Gamerunner initializes and operates the asteroids game until its conclusion."""
    def __init__(self, asteroids_amount):
        """
        Game contains
        :param asteroids_amount:
        """
        self.__screen = Screen()


        # Dimensions of the space in which the game is played
        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y

        # Initialization of ship
        ship_x = random.randint(Screen.SCREEN_MIN_X, Screen.SCREEN_MAX_X)
        ship_y = random.randint(Screen.SCREEN_MIN_Y, Screen.SCREEN_MAX_Y)
        self.__screen.draw_ship(ship_x, ship_y, 0)
        self.__player = Ship(ship_x, ship_y, 0, 0, 0)

        # Initialisation of asteroids.
        ast_speeds = list(range(-4, 0)) + list(range(1, 5))
        ast_xs, ast_ys = self.non_colliding_start(self.__player, asteroids_amount)
        self.__ast_size = 3
        self.__ast_ls =[]
        for i in range(asteroids_amount):
            as_x_sp = random.choice(ast_speeds)
            as_y_sp = random.choice(ast_speeds)
            asteroid = Asteroid(ast_xs[i], ast_ys[i], as_x_sp, as_y_sp, self.__ast_size)
            self.__ast_ls.append(asteroid)
            self.__screen.register_asteroid(asteroid, self.__ast_size)
            self.__screen.draw_asteroid(asteroid, ast_xs[i], ast_ys[i])


        self.__life_count = 3 #Life count of ship
        self.__score = 0 # Game score

        #Lists of torpedos and special torpedos in play
        self.__torpedo_ls = []
        self.__sp_torpedo_ls = []


    def non_colliding_start(self, ship, asteroids_amount):
        """
        This will return a list of coordinates where the player is not hitting the
        any of the asteroids at the start of creating the game.
        :param ship: is the player
        :param asteroids_amount: the number of asteroids
        :return: x and y coordinates
        """

        MAX_X = self.__screen_max_x
        MAX_Y = self.__screen_max_y
        MIN_X = self.__screen_min_x
        MIN_Y = self.__screen_min_y

        ast_xs = []
        ast_ys = []
        ast_size = 3
        # ensure there are no collisions of asteroids and the player
        while len(ast_xs) <= asteroids_amount or len(ast_ys) <= asteroids_amount:
            x = random.randint(MIN_X, MAX_X)
            if x not in list(range(ship.getx() - ast_size, ship.getx() + ast_size+1)) \
                    and len(ast_xs) <= asteroids_amount:
                ast_xs.append(x)
            y = random.randint(MIN_Y, MAX_Y)
            if y not in list(range(ship.gety() - ast_size, ship.gety() + ast_size+1)) \
                    and len(ast_ys) <= asteroids_amount:
                ast_ys.append(y)

        return ast_xs, ast_ys



    def move(self, obj):
        """Function moves objects through 2 dimensional space within the game. Object speed
        will determine its movement."""
        axis_delta = self.__screen_max_x - self.__screen_min_x
        new_x = (obj.x_speed + obj.getx() - self.__screen_min_x) % axis_delta + self.__screen_min_x
        new_y = (obj.y_speed + obj.gety() - self.__screen_min_y) % axis_delta + self.__screen_min_y
        obj.set_x(new_x)
        obj.set_y(new_y)

    def move_dir(self, ship, turn_left, turn_right):
        """Defines ships moving direction"""
        if turn_left: ship.set_dir(ship.dir + 7)
        elif turn_right: ship.set_dir(ship.dir - 7)

    def speed_up(self, ship, up_pressed):
        """Ship will speed up when 'up' arrow is pressed on the keyboard. Speed increase will increase in
        the direction its nose is pointing."""
        if up_pressed:
            heading_rad = math.radians(ship.dir)
            x_speed = ship.get_speed()[0] + math.cos(heading_rad)
            y_speed = ship.get_speed()[1] + math.sin(heading_rad)
            ship.set_speed(x_speed, y_speed)

    def run(self):
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        # You don't need to change this method!
        self._game_loop()

        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def shoot(self, ship):
        """Function is responsible for shooting normal torpedos.
        Pressing space will initialize a torpedo launch."""
        space_pressed = self.__screen.is_space_pressed()

        if space_pressed and len(self.__torpedo_ls) <= 10:
            ship_dir = math.radians(ship.get_dir())
            x_speed = ship.get_speed()[0] + 2*math.cos(ship_dir)
            y_speed = ship.get_speed()[1] + 2*math.sin(ship_dir)
            torpedo = Torpedo(ship.getx(),ship.gety(), x_speed, y_speed, ship.get_dir(),0)
            self.__screen.register_torpedo(torpedo)
            self.__screen.draw_torpedo(torpedo, ship.getx(),ship.gety(), ship.get_dir())
            self.__torpedo_ls.append(torpedo)

    def teleport(self,ship):
        """Function translates ships location to another random location on the board. The condition
        for successful translation is that the new location is not already occupied by an asteroid. Function
        will perform multiple iterations until a free location is randomly selected."""
        occupied = True
        while occupied:
            possiblex = random.randint(Screen.SCREEN_MIN_X+20, Screen.SCREEN_MAX_X-20)
            possibley = random.randint(Screen.SCREEN_MIN_Y+20, Screen.SCREEN_MAX_Y-20)
            free = True
            for ast in self.__ast_ls:
                if abs(possiblex-ast.x)<ast.get_radius()+30: free = False
                if abs(possibley-ast.y)<ast.get_radius()+30: free = False
                # if  ship.has_intersection(ast) and  ast.has_intersection(ship) == True:
                #     free = False
            if free == True:
                    occupied = False
        return possiblex,possibley

    def update_score(self,ast):
        """Function updates score on screen"""
        if ast.get_size() == 3:
            self.__score += 20
        elif ast.get_size() == 2:
            self.__score += 50
        elif ast.get_size() == 1:
            self.__score += 100
        self.__screen.set_score(self.__score)


    def split_ast(self, ast,tor):
        """Function either splits large asteroid into 2 smaller ones or eliminates asteroid completely.
        Will be implemented after a collision with a torpedo."""
        #Equation used to calculate the speed an dir of new smaller asteriod
        n_speed_x = (tor.x_speed + ast.x_speed)/(math.sqrt(ast.x_speed**2+ast.y_speed**2))
        n_speed_y = (tor.y_speed + ast.y_speed)/(math.sqrt(ast.x_speed**2+ast.y_speed**2))

        self.update_score(ast)

        #Larger  asteroid (that has been destroyed) is unregestered and removed from asteroid list
        self.__screen.unregister_asteroid(ast)
        self.__ast_ls.remove(ast)
        self.__screen.unregister_torpedo(tor)

        # Torpedo (or special torpedo) removed from list of torps in play
        if isinstance(tor,Special_Torpedo):
            for torpedo in self.__sp_torpedo_ls:
                if tor == torpedo[0]:
                    self.__sp_torpedo_ls.remove(torpedo)
        elif isinstance(tor,Torpedo):
            self.__torpedo_ls.remove(tor)


        if ast.size == 1: return #Asteroid of size 1 cannot be broken down any more

        # Ast of size 3 will be broken down into 2 ast's of size 2. New asteroids created will have
        # the same speed and opposite directions
        elif ast.size == 3:
            new_ast1 = Asteroid(ast.x,ast.y,n_speed_x,n_speed_y,2)
            new_ast2 = Asteroid(ast.x, ast.y, -n_speed_x, -n_speed_y, 2) # -ve sign gives opposing dir
        elif ast.size == 2:
            new_ast1 = Asteroid(ast.x, ast.y, n_speed_x, n_speed_y,1)
            new_ast2 = Asteroid(ast.x, ast.y, -n_speed_x, -n_speed_y,1)

        # Once new asteroids have been created they must be registered and added to asteroid list
        # before being added to the game.
        self.__ast_ls.append(new_ast1)
        self.__ast_ls.append(new_ast2)
        self.__screen.register_asteroid(new_ast1,2)
        self.__screen.register_asteroid(new_ast2,2)
        self.__screen.draw_asteroid(new_ast1,ast.x,ast.y)
        self.__screen.draw_asteroid(new_ast2,ast.x,ast.y)


    def get_nearest_ast(self,ship,asteroids):
        """Used for special torpedo. Returns the asteroid that is closest to the ship
        when special torpedo is fired"""
        min = math.hypot(asteroids[0].x - ship.x, asteroids[0].y - ship.y)
        min_asteroid = asteroids[0]
        for asteroid in asteroids:
            dis = math.hypot(asteroid.x-ship.x,asteroid.y-ship.y)
            if dis < min:
                min = dis
                min_asteroid = asteroid
        return min_asteroid

    def speed_adjuster(self,ship,special_torp,asteroid):
        """Changes torpedo's speed relative to the asteroid it is tracking. Speed change is
        proportional to the torpedo's distance from the asteroid."""
        if special_torp.x > asteroid.x and special_torp.y> asteroid.y:
            special_torp.set_speed(-abs((asteroid.x-special_torp.x)/50),-abs((asteroid.y-special_torp.y)/50))
        elif special_torp.x< asteroid.x and special_torp.y> asteroid.y:
            special_torp.set_speed(abs((asteroid.x-special_torp.x)/50),-abs((asteroid.y-special_torp.y)/50))
        elif special_torp.x > asteroid.x and special_torp.y< asteroid.y:
            special_torp.set_speed(-abs((asteroid.x-special_torp.x)/50),abs((asteroid.y-special_torp.y)/50))
        elif special_torp.x< asteroid.x and special_torp.y < asteroid.y:
            special_torp.set_speed(abs((asteroid.x-special_torp.x)/50),abs((asteroid.y-special_torp.y)/50))

    def drange(self,x, y, jump):
        """Produces a list of float speeds of asteroid of precision 2. If torp speed is
        in this list, torp 'lock' will be activated"""
        decimal.getcontext().prec = 2
        while x < y:
            yield float(x)
            x = decimal.Decimal(x) + decimal.Decimal(jump)

    def move_to_nearest_ast(self,ship,special_torp,asteroid):
        """Main tracking function for special torpedo. Uses torpedo's location relative to the asteroid
        it is tracking to change its speed in order to move closer to the asteroid. Once its speed has,
        aligned with the asteroid, its speed should match that of the asteroid, when this happens, the
        torpedo with switch to 'locked' speed."""

        #Function first checks if speeds are already equal (meaning that alignment has happened). If aligned
        # then torpedo status changes to 'locked'
        torp_x = round(float(special_torp.get_speed()[0]),1)
        torp_y = round(float(special_torp.get_speed()[1]),1)
        x_range = list(self.drange(asteroid.get_speed()[0]-1,asteroid.get_speed()[0]+2,0.1))
        y_range = list(self.drange(asteroid.get_speed()[1] - 1, asteroid.get_speed()[1] + 2, 0.1))
        if torp_x in x_range and torp_y in y_range and special_torp.get_life()>=30:
            special_torp.speed_match = True
            return True
        self.speed_adjuster(ship,special_torp,asteroid)

        # Direction of torp nose calculated using the arctan of the ratio between the x and y differences
        # in the location of the ship and the location of the asteroid.
        x_diff = asteroid.getx()-ship.getx()
        y_diff = asteroid.gety()-ship.gety()
        if x_diff == 0 and special_torp.getx() > asteroid.getx():
            direction = math.pi
        elif  x_diff == 0 and special_torp.getx() < asteroid.getx():
            direction = 0
        else:
            direction = math.atan2(y_diff,x_diff)
        special_torp.set_dir(direction)
        self.move(special_torp)
        self.__screen.draw_torpedo(special_torp,special_torp.x,special_torp.y,direction)


    def locked(self,ship,special_torp,asteroid):
        """Once torpedo is aligned with asteroid, its direction of movement will change to
        that of the asteroid it is following and its speed will change to triple that of the
        asteroid in order to allow it to 'catch up' and destroy the asteroid."""
        special_torp.set_speed(asteroid.get_speed()[0] * 3, asteroid.get_speed()[1] * 3)
        x_diff = asteroid.getx() - ship.getx()
        y_diff = asteroid.gety() - ship.gety()
        if x_diff == 0 and special_torp.getx() > asteroid.getx():
            direction = math.pi
        elif x_diff == 0 and special_torp.getx() < asteroid.getx():
            direction = 0
        else:
            direction = math.atan2(y_diff, x_diff)
        special_torp.set_dir(direction)
        self.move(special_torp)
        self.__screen.draw_torpedo(special_torp, special_torp.x, special_torp.y, direction)


    def _game_loop(self):
        """Game loop runs the game until one of the ending conditions is met (eg all lives lost or
        played descision to quit)."""

        # Here direction variables are set.
        ship = self.__player
        left = self.__screen.is_left_pressed()
        right = self.__screen.is_right_pressed()
        up_pressed = self.__screen.is_up_pressed()

        self.move_dir(ship, left, right)
        self.move(ship)

        self.speed_up(ship, up_pressed)
        self.__screen.draw_ship(ship.x, ship.y, ship.dir)
        self.shoot(ship)

        for i in range(len(self.__torpedo_ls)):
            tor = self.__torpedo_ls[i]
            self.move(tor)
            self.__screen.draw_torpedo(tor, tor.getx(),tor.gety(), tor.get_dir())

        # While loop runs continuously through the asteroids in play to determine weather
        # one may have collided with the ship
        i = 0
        while i <= len(self.__ast_ls)-1:
            asteroid = self.__ast_ls[i]
            self.move(asteroid)
            self.__screen.draw_asteroid(asteroid, asteroid.getx(), asteroid.gety())

            if asteroid.has_intersection(ship) and ship.has_intersection(asteroid)\
                    and self.__life_count>0:
                self.__screen.show_message('CRASH OCCURRED ', 'Ship crashed, Be careful!')
                self.__screen.remove_life()
                self.__screen.unregister_asteroid(asteroid)
                del self.__ast_ls[i]
                self.__life_count -= 1
            i = i + 1

        #for loop runs through torpedos in play to check for collision with any of the asteroids
        # in play.
        for tor in self.__torpedo_ls:
            tor.life_count += 1
            if tor.life_count == 200: # Regular torpedos have life count of 200
                self.__screen.unregister_torpedo(tor)
                self.__torpedo_ls.remove(tor)
            j = 0
            while j <= len(self.__ast_ls) - 1:
                ast = self.__ast_ls[j]
                if tor.has_intersection(ast) and ast.has_intersection(tor):
                    self.__screen.set_score(self.__score)
                    self.split_ast(ast, tor)
                j += 1

        # pressing 't' k will activate ship teleportation.
        t_pressed = self.__screen.is_teleport_pressed()
        if t_pressed:
            self.__player.set_x(self.teleport(self.__player)[0])
            self.__player.set_y(self.teleport(self.__player)[1])


       # There are 3 ways in which the game can end:
        q_pressed = self.__screen.should_end() # Player choses to quit
        if q_pressed:
            self.__screen.show_message('You have chosen to quit', 'Thank you for playing')
            sys.exit()

        elif self.__life_count == 0: # Player life count reaches zero
            self.__screen.show_message('Game over', 'Out of lives: Game Over')
            sys.exit()

        elif len(self.__ast_ls) == 0: # Player has destroyed all the asteroids in play
            self.__screen.show_message('Game completed', 'Well done, you have completed the game!')
            sys.exit()


        # s_pressed is activated when played presses the 's' button and will initialise launch
        # of a special torpedo
        s_pressed = self.__screen.is_special_pressed()
        if s_pressed and len(self.__sp_torpedo_ls) <= 5: # Cant have more than 5 in play at any time.
            nearest_asteroid = self.get_nearest_ast(ship,self.__ast_ls)
            s_torp_x_speed = self.__player.x_speed
            s_torp_y_speed = self.__player.y_speed
            x_diff = nearest_asteroid.getx() - ship.getx()
            y_diff = nearest_asteroid.gety() - ship.gety()
            fraction = y_diff / x_diff
            direction = math.tan(fraction)
            special_torp = Special_Torpedo(ship.x,ship.y,s_torp_x_speed,s_torp_y_speed,direction,0,False)
            self.__screen.register_torpedo(special_torp)
            self.__screen.draw_torpedo(special_torp,special_torp.getx(),special_torp.gety(),
                                       special_torp.get_dir())
            self.__sp_torpedo_ls.append((special_torp,nearest_asteroid))

        # For loop runs through all special torpedos in play to check for collisions with any
        # of the asteroids in play.
        for torpedo in self.__sp_torpedo_ls:
            torpedo[0].life_count += 1
            if torpedo[0].life_count == 150: #Special torpedos have life span of 150 iterations.
                self.__screen.unregister_torpedo(torpedo[0])
                self.__sp_torpedo_ls.remove(torpedo)

            else:
                if torpedo[0].speed_match == False:
                    self.move_to_nearest_ast(self.__player,torpedo[0],torpedo[1])
                else:
                    self.locked(self.__player,torpedo[0],torpedo[1]) # after alignment torpedo changes speed.
                for ast in self.__ast_ls:
                    if torpedo[0].has_intersection(ast) and ast.has_intersection(torpedo[0]):
                        # Points added depending on size of asteroid destroyed.
                        self.split_ast(ast,torpedo[0])





def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)