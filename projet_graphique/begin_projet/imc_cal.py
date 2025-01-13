from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App 

from session import Session

from kivy.properties import ObjectProperty

from screen_manager import MyScreenManger

class ScreenBrowser(MyScreenManger):
    pass

class MainApp(App):
    manage = ObjectProperty()
    def build(self):
        self.manage = ScreenBrowser()
        if Session.get_session()['status']:
            self.manage.current="index"
        return self.manage
    pass

app = MainApp()
app.run()