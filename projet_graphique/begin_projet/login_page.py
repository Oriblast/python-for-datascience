from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.uix.label import Label

from session import Session

Builder.load_file("login_page.kv")

class LoginPage(BoxLayout):
    msg = StringProperty()
    def check_session(self, widget:Label, ):
        session = Session.get_session()
        stat = session['status']
        if not stat:
            widget.text="utilisateur non trouver" #fait la meme chose que le self plus bas
            widget.opacity=1
        #self.msg = "ta grand mere"
        pass
    def clear_inputs(self):
        self.ids.pseudo.text = ""
        self.ids.password.text = ""
        pass
    pass