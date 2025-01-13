from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout

from session import Session

Builder.load_file("signup_page.kv")

class SignupPage(BoxLayout):

    def check_info(self, widget):
        status = Session.get_session()["status"]
        if not status:
            widget.opacity=1
            pass
    pass

