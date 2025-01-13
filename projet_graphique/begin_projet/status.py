from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from tinydb import TinyDB, Query


from session import Session


Builder.load_file("status.kv")

class Status(BoxLayout):
    status = StringProperty()
    cause = StringProperty()
    conseil = StringProperty()
    def preload_data(self):
        session = Session.get_session()
        cause = session['sante']["imc"]
        class_sante = session['sante']['class_sante']
        db = TinyDB("./Data/sante.json")
        sante = Query()
        data = db.get(sante.id==class_sante)
        print(data)
        self.status = data['maladie']
        self.cause = data['reason']
        self.conseil = data['conseil']
        pass
    pass