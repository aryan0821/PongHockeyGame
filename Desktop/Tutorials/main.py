from turtle import onclick
import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty,
    ReferenceListProperty,
    ObjectProperty,
    ColorProperty,
)
from kivy.vector import Vector
from kivy.uix.button import Button

from kivy.clock import Clock
import time
from kivy.core.window import Window


class PongPaddle(Widget):
    score = NumericProperty(0)
    mult = NumericProperty(1)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.5
            ball.velocity = vel.x, vel.y + offset


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    smash_circle = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(PongGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == "w" and self.player1.center_y < self.height:
            self.player1.center_y += 50
        elif keycode[1] == "s" and self.player1.center_y > 0:
            self.player1.center_y -= 50
        elif keycode[1] == "d" and self.player1.center_x < self.width / 2:
            self.player1.center_x += 50
        elif keycode[1] == "a" and self.player1.center_x > 0:
            self.player1.center_x -= 50
        elif keycode[1] == "up" and self.player2.center_y < self.height:
            self.player2.center_y += 50
        elif keycode[1] == "down" and self.player2.center_y > 0:
            self.player2.center_y -= 50
        elif keycode[1] == "right" and self.player2.center_x < self.width:
            self.player2.center_x += 50
        elif keycode[1] == "left" and self.player2.center_x > self.width / 2:
            self.player2.center_x -= 50
        else:
            pass
        return True

    def serve_ball(self, vel=(5, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel
        self.player1.center_x = self.player1.width / 2 + 30
        self.player2.center_x = self.width - (self.player2.width / 2 + 30)
        self.player1.center_y = self.center_y
        self.player2.center_y = self.center_y

    def pause_game(self, dt):
        
        pass

    def update(self, dt):
        self.ball.move()
        self.ball.resistance()

        if (self.ball.y < 5) or (self.ball.top > self.height - 5):
            self.ball.velocity_y *= -1

        if (
            self.ball.x < self.x
            and self.height / 3 < self.ball.y
            and self.ball.y < 2 * self.height / 3
        ):  # player 2 scores
            self.player2.score += 1
            self.serve_ball(vel=(5, 0))

        elif self.ball.x < self.x:  # player 2 side wall bounce
            self.ball.velocity_x *= -1

        if (
            self.ball.right > self.width
            and self.height / 3 < self.ball.y
            and self.ball.y < 2 * self.height / 3
        ):  # player 1 scores
            self.player1.score += 1
            self.serve_ball(vel=(-5, 0))

        elif self.ball.right > self.width:  # player 1 side wall bounce
            self.ball.velocity_x *= -1

    def update_bounce(self, dt):
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        if self.velocity_x > 15:
            self.velocity_x = 14
        if self.velocity_x < -15:
            self.velocity_x = -14
        if self.velocity_y > 15:
            self.velocity_y = 14
        if self.velocity_y < -15:
            self.velocity_y = -14
        self.pos = Vector(*self.velocity) + self.pos

    def resistance(self):
        if self.velocity_x < -8:
            self.velocity_x += 0.01
        elif self.velocity_x < 0:
            self.velocity_x += 0.005
        elif self.velocity_x > 8:
            self.velocity_x -= 0.01
        else:
            self.velocity_x -= 0.005

        if self.velocity_y < -8:
            self.velocity_y += 0.01
        elif self.velocity_y < 0:
            self.velocity_y += 0.005
        elif self.velocity_y > 8:
            self.velocity_y -= 0.01
        else:
            self.velocity_y -= 0.005


class PongGoal(Widget):
    background = ColorProperty()


class PongApp(App):
    def build(self):
        game = PongGame()
        Window.clearcolor = (1, 1, 1, 1)
        Clock.schedule_interval(game.update, 1.0 / 150.0)
        Clock.schedule_interval(game.update_bounce, 1.0 / 150.0)
        return game


if __name__ == "__main__":
    PongApp().run()
