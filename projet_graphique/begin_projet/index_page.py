from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

from session import Session

Builder.load_file("index_page.kv")

class IndexPage(BoxLayout):
    def logout(self):
        print("Déconnexion en cours...")  # Debug
        # Trouver le ScreenManager global
        screen_manager = self.get_screen_manager()

        if screen_manager:
            # Accéder à la page de connexion
            login_screen = screen_manager.get_screen("login")
            login_page = login_screen.children[0]  # Le premier enfant est LoginPage
            
            # Vider les champs de texte
            login_page.clear_inputs()
            
            # Effacer la session utilisateur
            Session.clear_session()
            
            # Revenir à la page de connexion
            screen_manager.current = "home"
            print("Redirection vers la page de connexion.")  # Debug
        else:
            print("ScreenManager introuvable !")  # Debug

    def get_screen_manager(self):
        # Parcourir les parents pour trouver le ScreenManager
        parent = self.parent
        while parent and not isinstance(parent, ScreenManager):
            parent = parent.parent
        return parent
    pass