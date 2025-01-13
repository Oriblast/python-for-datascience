from kivy.app import *
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Ellipse, Color
from kivy.metrics import dp
from kivy.clock import Clock
from random import random

class MainWidget(Widget):
    pass

class CanvaTest(Widget):
    pass

class AnimationBall(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vy = dp(5)
        self.vx = dp(5)
        #self.canvas.add(Ellipse(pos=(dp(350), 0), size=(dp(50), dp(50))))
        with self.canvas:
            self.ball = Ellipse(pos=(dp(350), 0), size=(dp(50), dp(50)))
            self.color = Color(1, 0, 0, 0.5)
            self.ball2 = Ellipse(pos=(0, dp(350)), size=(dp(50), dp(50)))
        Clock.schedule_interval(self.my_anim, 1/120)

    def my_anim(self, dt):
        xp, yp = self.ball.pos 
        x, y = self.ball.size 
        x2, y2 = self.ball2.pos
        xs, ys = self.ball2.size

        if yp+y+self.vy >= self.height:
            self.vy = -self.vy
        if yp+self.vy <= 0:
            self.vy = - self.vy
        
        if self.vx+x2+x >= self.width:
            self.vx = -self.vx
        if self.vx + x2 <= 0:
            self.vx = -self.vx

        if xp == x2 and yp == y2:
            self.vx = -self.vx
            self.vy = -self.vy
            self.color.rgba = (random(), random(), random(), 0.5)

        self.ball.pos = (xp, yp+self.vy)
        self.ball2.pos = (x2+self.vx, y2)
        pass

class Main(App):
    pass


app = Main()
app.run()