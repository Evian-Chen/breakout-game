"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao.

YOUR DESCRIPTION HERE
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random

BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing
BRICK_WIDTH = 40       # Width of a brick (in pixels)
BRICK_HEIGHT = 15      # Height of a brick (in pixels)
BRICK_ROWS = 4        # Number of rows of bricks
BRICK_COLS = 4        # Number of columns of bricks
BRICK_OFFSET = 50      # Vertical offset of the topmost brick from the window top (in pixels)
BALL_RADIUS = 20       # Radius of the ball (in pixels)
PADDLE_WIDTH = 75      # Width of the paddle (in pixels)
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels)
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels)
INITIAL_Y_SPEED = 7    # Initial vertical speed for the ball
MAX_X_SPEED = 5        # Maximum initial horizontal speed for the ball
NUM_LIVES = 3		   # Number of attempts
HEART_SIZE = 20        # size for lives hearts


class BreakoutGraphics:

    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH, paddle_height=PADDLE_HEIGHT,
                 paddle_offset=PADDLE_OFFSET, brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS, brick_width=BRICK_WIDTH,
                 brick_height=BRICK_HEIGHT, brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING, title='Breakout'):

        # graphical window, with some extra space
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)

        # paddle
        self.paddle_offset = paddle_offset
        self.paddle = GRect(paddle_width, PADDLE_HEIGHT, x = (window_width / 2) - (PADDLE_WIDTH / 2), y = window_height - paddle_offset)
        self.paddle.filled = True
        self.window.add(self.paddle)

        # filled ball in the graphical window
        self.ball = GOval(ball_radius, ball_radius, x = window_width / 2, y = window_height / 2)
        self.ball.filled = True
        self.window.add(self.ball)

        # initial velocity for the ball
        self.__dx = 0
        self.__dy = 0

        self.lives = NUM_LIVES
        self.clickLock = True
        self.gameStarted = False
        self.brickNum = brick_rows * brick_cols

        # mouse listeners
        onmousemoved(self.movePaddle)
        onmouseclicked(self.startGame)

        # variables for counting score
        self.scores = 0
        self.scoreLabel = GLabel(f"Scores: {self.scores}", x = 10, y = self.window.height-10)
        self.scoreLabel.font = "-20"
        self.window.add(self.scoreLabel)

        self.heart1 = GOval(HEART_SIZE, HEART_SIZE, x=self.window.width-HEART_SIZE*5, y=10)
        self.heart1.filled = True
        self.heart1.fill_color = "red"
        self.window.add(self.heart1)

        self.heart2 = GOval(HEART_SIZE, HEART_SIZE, x=self.window.width-HEART_SIZE*4+10, y=10)
        self.heart2.filled = True
        self.heart2.fill_color = "red"
        self.window.add(self.heart2)

        self.heart3 = GOval(HEART_SIZE, HEART_SIZE, x=self.window.width-HEART_SIZE*3+20, y=10)
        self.heart3.filled = True
        self.heart3.fill_color = "red"
        self.window.add(self.heart3)

        # Draw bricks
        for i in range(brick_rows):
            for j in range(brick_cols):
                self.brick = GRect(brick_width, brick_height)
                self.brick.filled = True
                self.window.add(self.brick, x = (brick_width + brick_spacing) * i, y = brick_offset + (brick_height + brick_spacing) * j)
        
    # mouse listener
    def movePaddle(self, mouse):
        if mouse.x <= 0:
            self.paddle.x = 0
        elif mouse.x >= self.window.width:
            self.paddle.x = self.window.width - self.paddle.width
        else:
            self.paddle.x = mouse.x - self.paddle.width/2

    def startGame(self, mouse):
        if self.clickLock:
            self.clickLock = False
            if self.lives != 0:          # game is started
                self.setBallVelocity()
                self.gameStarted = True
    
    """
    the following methods are used to detect if the ball hit stuff
    they return a boolean and do nothing
    """
    def hitPaddle(self):  
        if self.window.get_object_at(self.ball.x + self.ball.width, self.ball.y + self.ball.width) is self.paddle:
            return True
        return False

    def hitCeiling(self):
        if self.ball.y <= 0:
            return True
        return False

    def hitWall(self):
        if self.ball.x < 0 or self.ball.x > self.window.width - self.ball.width:
            return True
        return False

    def hitGround(self):
        if self.ball.y > self.window.height:
            return True
        return False

    def hitBrick(self):
        for i in range(2):
            for j in range(2):
                obj = self.window.get_object_at(self.ball.x + self.ball.width * i, self.ball.y + self.ball.width * j)
                
                # make sure obj is not other objects on the canvas
                if obj is not self.paddle and obj is not None and obj is not self.scoreLabel and obj is not self.heart1 and obj is not self.heart2 and obj is not self.heart3:
                    self.window.remove(obj)
                    return True
        return False

    """
    The following functions are used to count the score
    """
    def addScore(self):
        self.scores += 1
        self.scoreLabel.text = f"Scores: {self.scores}"

    def setBallVelocity(self):
        self.__dx = random.randint(1, MAX_X_SPEED)
        if random.random( ) > 0.5 : 
            self.__dx  =  -self.__dx 
        self.__dy = INITIAL_Y_SPEED

    def gameloss(self):
        self.window.clear()
        lossLabel = GLabel(f"You loss!", x=self.window.width/2-30, y=self.window.height/2)
        lossLabel.font = "-25"
        self.window.add(lossLabel)

    def gameWin(self):
        self.window.clear()
        winLabel = GLabel(f"You Win!", x=self.window.width/2-30, y=self.window.height/2)
        winLabel.font = "-25"
        self.window.add(winLabel)

    def endRound(self):
        self.gameStarted = False
        self.clickLock = True

        if self.lives == 3:
            self.window.remove(self.heart3)
        elif self.lives == 2:
            self.window.remove(self.heart2)
        else:
            self.window.remove(self.heart1)
            
        self.lives -= 1
        self.window.remove(self.ball)
        self.window.add(self.ball, x=self.window.width / 2, y=self.window.height / 2)
        self.__dx = 0
        self.__dy = 0

    # getter
    def getDx(self):
        return self.__dx
    def getDy(self):
        return self.__dy

    # setter
    def setDx(self, v):
        self.__dx = v
    def setDy(self, v):
        self.__dy = v