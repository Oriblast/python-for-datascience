from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout

from session import Session

from kivy.properties import StringProperty, NumericProperty, ObjectProperty

Builder.load_file("update_page.kv")

class UpdatePage(BoxLayout):
    pseudo = StringProperty()
    nom_prenom = StringProperty()
    age = StringProperty()
    sex = StringProperty()
    travail = StringProperty()
    taille = StringProperty()
    poids = StringProperty()

   # pasword = StringProperty(BoxLayout)

    def preload_data(self):
        session = Session.get_session()
        if session['status']:
            data = session['data']
            self.pseudo = str(data['pseudo'])
            self.nom_prenom = str(data['nom_prenom'])
            self.age = str(data['age'])
            self.sex = "Homme" if data['sex'] == 0 else "Femme"
            self.travail = data['travail']
            self.poids = str(data['poids'])
            self.taille = str(data['taille'] * 100)

            print(data)
        pass
    pass

