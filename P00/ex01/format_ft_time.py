import time
import datetime

#recuperer la date de l'epoque 

epoch_time = time.time()

#afficher ce temps en notation normal et scientifique

print(f"Second since january 1, 1970: {epoch_time} or {epoch_time:.2e} in scientific notation", end="\n")

current_time = datetime.datetime.now()

#formatage du temps actuel

format_time = current_time.strftime("%b %d %Y")
print(f"{format_time}", end="\n")