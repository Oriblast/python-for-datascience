import json


class Session():
    @classmethod
    def get_session(cls):
        with open("./Data/session.json", "r") as file:
            data = json.load(file)
            return data

        pass
    @classmethod
    def make_session(cls, data):
        with open("./Data/session.json","w") as file:
            json.dump(data, file)
            return data
        pass
    @classmethod
    def clear_session(cls):
        data = {"status": False, "data":
        {"mot_de_passe": "", "pseudo": 
        "*", "nom_prenom": "", 
        "age": None, "sex": None, "taille": None, "poids":
        None, "travail": ""}}
        with open("./Data/session.json","w") as file:
            json.dump(data, file)
        pass

    pass

if __name__ == "__main__":
        print(Session.get_session())
        Session.clear_session()
        print(Session.get_session())