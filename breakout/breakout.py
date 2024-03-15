"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

YOUR DESCRIPTION HERE
"""

from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics

FRAME_RATE = 40         # 100 frames per second


def main():
    graphics = BreakoutGraphics()

    ball = graphics.ball
    dx = graphics.getDx()
    dy = graphics.getDy()
    brickNum = graphics.brickNum
    
    while True:
        if graphics.gameStarted:     # new round of game started
            dx = graphics.getDx()    # initialize velocities and get ball
            dy = graphics.getDy()

            while True:              # animation loop
                ball.move(dx, dy)
                pause(FRAME_RATE)

                if graphics.hitPaddle():
                    graphics.setDy(-dy)
                    dy = graphics.getDy()
                    graphics.ball.y = graphics.window.height - graphics.paddle_offset - graphics.ball.width

                if graphics.hitCeiling():
                    graphics.setDy(-dy)
                    dy = graphics.getDy()

                if graphics.hitWall():
                    graphics.setDx(-dx)
                    dx = graphics.getDx()

                if graphics.hitBrick():
                    brickNum -= 1
                    graphics.setDy(-dy)
                    dy = graphics.getDy()
                    graphics.addScore()

                if graphics.hitGround():  # end this round
                    graphics.endRound()
                    break

                if brickNum == 0:         # no brick on the convas
                    graphics.gameWin()
                    break

        if graphics.lives == 0:           # game over
            graphics.gameloss()
            break

        pause(FRAME_RATE)


if __name__ == '__main__':
    main()
