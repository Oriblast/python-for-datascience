from kivy.uix.screenmanager import ScreenManager
from package.Data import Data
from package.User import User
from session import Session

class MyScreenManger(ScreenManager):
    def get_gender(self, sex):
            if sex=="Homme":
                return 0
            else:
                return 1
    def check_login(self, pseudo:str, password:str):
        print(f"{pseudo} : {password}")
        get_user = Data.get_user(pseudo, password)
        print(get_user)
        if get_user['status']:
            self.current="index"
            Session.make_session(get_user)
            return
        Session.clear_session()


    def check_signup(self, pseudo:str, password:str, passrep:str, nom_prenom, age, sex, taille, poids, travail):
        if (password == passrep and passrep and nom_prenom and age and sex and taille and poids and travail):
            user = User(pseudo, password, nom_prenom, int(age), self.get_gender(sex), int(taille)/100, int(poids), travail)
            data = Data(user)
            stat = Data.get_user(pseudo, password)
            print("inscription éffectué")
            data.update()
            self.current="index"
            get_user = Data.get_user(pseudo, password)
            Session.make_session(get_user)

        else:
            print("information non correct")
        pass



    def check_update(self, pseudo:str, password:str, passrep:str, nom_prenom, age, sex, taille, poids, travail):
        old_pass = Session.get_session()['data']["mot_de_passe"]

        if password == "" and passrep == "":
            password = old_pass
        user = User(pseudo, password, nom_prenom, int(age), self.get_gender(sex), float(taille)/100,float(poids), travail)
        data = Data(user)
        stat = Data.get_user(pseudo, password)
        print("update")
        data.update()
        if passrep == password:
            self.current="index"
        elif (passrep != password and password != ""):
            print("mot de pass ne correspond pas")
        pass
    pass