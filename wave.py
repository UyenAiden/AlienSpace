"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in
the Alien Invaders game.  Instances of Wave represent a single wave. Whenever
you move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on
screen. These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or
models.py. Whether a helper method belongs in this module or models.py is
often a complicated issue.  If you do not know, ask on Piazza and we will
answer.

# YOUR NAME(S) AND NETID(S) HERE
# DATE COMPLETED HERE
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary.
    It also marches the aliens back and forth across the screen until they are
    all destroyed or they reach the defense line (at which point the player
    loses). When the wave is complete, you  should create a NEW instance of
    Wave (in Invaders) if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.  This
    class will be similar to than one in how it interacts with the main class
    Invaders.

    All of the attributes of this class ar to be hidden. You may find that
    you want to access an attribute in class Invaders. It is okay if you do,
    but you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter
    and/or setter for any attribute that you need to access in Invaders.
    Only add the getters and setters that you need for Invaders. You can keep
    everything else hidden.

    """
    # HIDDEN ATTRIBUTES:
    # Attribute _ship: the player ship to control
    # Invariant: _ship is a Ship object or None
    #
    # Attribute _aliens: the 2d list of aliens in the wave
    # Invariant: _aliens is a rectangular 2d list containing Alien objects or None
    #
    # Attribute _bolts: the laser bolts currently on screen
    # Invariant: _bolts is a list of Bolt objects, possibly empty
    #
    # Attribute _dline: the defensive line being protected
    # Invariant : _dline is a GPath object
    #
    # Attribute _lives: the number of lives left
    # Invariant: _lives is an int >= 0
    #
    # Attribute _time: the amount of time since the last Alien "step"
    # Invariant: _time is a float >= 0s
    #
    # You may change any attribute above, as long as you update the invariant
    # You may also add any new attributes as long as you document them.
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    # Attribute _left: true = left, false=right
    # Invariant: _left is a boolean

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)


    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self):
        """
        Initializes the subcontroller.
        """
        self._initialiens()
        self._ship = GImage(x=GAME_WIDTH//2,y=SHIP_BOTTOM,height=SHIP_HEIGHT,
                            width=SHIP_WIDTH,source='ship.png')
        self._dline = GPath(points=[0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE],
                            linewidth=3, linecolor='navy')
        self._time = 0
        self._bolts = []
        self._left = False


    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self, input, dt):
        """
        Animates the ship, aliens, and laser bolts.

        Parameter input: Creates a new input handler.
        Precondition: input is an instance of GInput.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        if input.is_key_down('left'):
            self._ship.x -= SHIP_MOVEMENT
            if self._ship.x < 0:
                self._ship.x = 0
        if input.is_key_down('right'):
            self._ship.x += SHIP_MOVEMENT
            if self._ship.x > GAME_WIDTH:
                self._ship.x = GAME_WIDTH

        #count the number of seconds has passed since the last frame: dt
        #_time: the amount of time since the last Alien "step"
        #each time the aliens move: _time = 0
        #if the aliens don't move: _time = _time + dt
        #Move the Aliens to the Right
        #self._aliens.x += ALIEN_H_SEP
        #If dt is increase the ALIEN_SPEED is smaller\
        movedown = False
        if self._time < ALIEN_SPEED:
            self._time = self._time + dt
        if self._time > ALIEN_SPEED:
            if self._left:
                distance = -ALIEN_H_SEP
            else:
                distance = ALIEN_H_SEP
            self._time = 0
            for i in self._aliens:
                for k in i:
                    k.x += distance
                    if k.right > GAME_WIDTH - ALIEN_H_SEP:
                        movedown = True
                    if k.left < ALIEN_H_SEP:
                        movedown = True
            if movedown:
                for i in self._aliens:
                    for k in i:
                        k.y -= ALIEN_V_SEP
                        k.x -= distance
                movedown = False
                self._left = not self._left


        #Move the Alien to the left:
        #find the rightmost alien in the wave = rightmostAlien
        #if the distance of rightmostAlien and the right of the Window < ALIEN_H_SEP
        # --> move the alien down: self._aliens.y -= ALIEN_V_SEP
        # then move them back to the left: self._aliens.x -= ALIEN_H_SEP

        # --> Repeat the whole steps (There are two HELPER METHODS I SUGGEST)

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self, view):
        """
        """
        for i in self._aliens:
            for j in i:
                j.draw(view)
        self._ship.draw(view)
        self._dline.draw(view)
        for i in self._bolts:
            for b in i:
                b.draw(view)


    # HELPER METHODS FOR COLLISION DETECTION
    def _initialiens(self):
        """
        Help initialize the attribute _aliens.
        """
        self._aliens = []
        y = GAME_HEIGHT - ALIEN_CEILING
        for r in range(ALIEN_ROWS):#POS OF EACH ROW
            row = []
            x = ALIEN_H_SEP + ALIEN_WIDTH//2
            image = self._aliens_row_helper(r)
            for a in range(ALIENS_IN_ROW):#POS OF EACH ALIEN IN ROW
                hey = Alien(x=x, y=y, source=image)
                x = x + ALIEN_WIDTH + ALIEN_H_SEP
                row.append(hey)
            y = y - (ALIEN_HEIGHT + ALIEN_V_SEP)
            self._aliens.append(row)

    #change the source based on i
    #make the source a variable that is dependent on i
    #use math to figure out what i should be
    #how many rows? How many aliens in each row?
    def _aliens_row_helper(self, r):
        """
        Determines the image for each row.

        Parameter r: the number of row
        Precondition: r is an int >=0
        """
        #There is a mathematical formula that sets the image for pos r
        aliens = {}
        aliens[(ALIEN_ROWS - 1) % 6] = ALIEN_IMAGES[0]
        aliens[(ALIEN_ROWS - 2) % 6] = ALIEN_IMAGES[0]
        aliens[(ALIEN_ROWS - 3) % 6] = ALIEN_IMAGES[1]
        aliens[(ALIEN_ROWS - 4) % 6] = ALIEN_IMAGES[1]
        aliens[(ALIEN_ROWS - 5) % 6] = ALIEN_IMAGES[2]
        aliens[(ALIEN_ROWS - 6) % 6] = ALIEN_IMAGES[2]

        return aliens[r % 6]
