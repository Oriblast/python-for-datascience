import pandas as pd

serie = pd.Series([10 , 20, 30, 40, 50])
print(serie)

data = { 'pays': ['france', 'italie', 'benin', 'nigeria'],
         'population': [6000000, 5000000, 110000, 20000000],
         'capital': ['Paris', 'rome', 'cotonou', 'lagos']}
fd = pd.DataFrame(data)
print(fd)