def ft_statistics(*args: Any, **kwargs: Any)-> None:
    """*args : Les nombres fournis en arguments.
**kwargs : Les clés spécifiques utilisées pour indiquer les statistiques demandées.

Exemples : toto="mean", tutu="median", tata="quartile".
Statistiques à calculer :

Moyenne (mean) : La somme des nombres divisée par leur quantité.
Médiane (median) : La valeur centrale d'un ensemble trié.
Quartiles : Les valeurs qui divisent les données triées en segments de 25% :
Q1 : 25% des données en dessous.
Q3 : 75% des données en dessous.
Écart-type (std) : Mesure de la dispersion autour de la moyenne.
Variance (var) : Carré de l'écart-type."""
