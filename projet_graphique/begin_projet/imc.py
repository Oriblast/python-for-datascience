from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from session import Session



Builder.load_file("imc.kv")

class Imc(BoxLayout):
    imc = StringProperty()
    def preload_data(self):
        session = Session.get_session()
        self.imc = str(session['sante']['imc'])
        pass
    pass