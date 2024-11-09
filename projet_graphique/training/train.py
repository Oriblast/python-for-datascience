from kivy.app import *
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label

#fonction avec des class et le widget est important
# il contient les autres elements 

class MainWidget(Widget):
    def __init__(self, **kawarg):
        super().__init__(**kawarg)
        button = Button(text="rap")
        label = Label(text="je suis un boss")
        label.pos = (200, -2)
        label.color = "lightblue"
        label.font_size = 42
        self.add_widget(button)
        self.add_widget(label)
    pass
#creation de fenetre main

class Main(App):
    def build(self):
        return MainWidget()
    pass


app = Main()
app.run()
