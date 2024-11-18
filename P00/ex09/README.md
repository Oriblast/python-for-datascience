# ft_package

A sample test package.

## Installation

```bash
pip install ./dist/ft_package-0.0.1.tar.gz

ex09/
│
├── ft_package/
│   ├── __init__.py
│   └── ft_package.py
├── README.md
├── LICENSE
├── pyproject.toml
├── setup.cfg
└── setup.py

Fichier pyproject.toml
Ce fichier configure l'environnement de build pour votre package.

Fichier setup.py
Ce fichier contient les informations nécessaires à la création du package.

Fichier setup.cfg
Le fichier setup.cfg est utilisé pour configurer setuptools de manière plus détaillée.

9. Création du Package
Créer l'archive source et le fichier wheel :

Ouvrez un terminal et naviguez vers le répertoire contenant vos fichiers (le répertoire ex09).
Exécutez les commandes suivantes pour créer le package :
bash
Copier le code
python3 setup.py sdist bdist_wheel
Cela va générer un dossier dist/ contenant les fichiers :

ft_package-0.0.1.tar.gz
ft_package-0.0.1-py3-none-any.whl
Installer le package localement :

Utilisez pip pour installer le package :
bash
Copier le code
pip install ./dist/ft_package-0.0.1-py3-none-any.whl
Vérification :

Après l'installation, vous pouvez vérifier les informations du package avec :
