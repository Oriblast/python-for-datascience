import time
import datetime

#recuperer la date de l'epoque 

e_time = time.time()

#afficher ce temps en notation normal et scientifique

print(f"Second since january 1, 1970: {e_time} or {e_time:.2e} in scientific notation", end="\n")

#temps actuel 
current_time = datetime.datetime.now()

#formatage du temps actuel

format_time = current_time.strftime("%b %d %Y")
print(f"{format_time}", end="\n")