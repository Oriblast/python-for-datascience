import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Charger les données nettoyées
df = pd.read_csv('cleaned_data.csv')

# Convertir la colonne 'Date de commande' en datetime si nécessaire
df['Date de commande'] = pd.to_datetime(df['Date de commande'])

# Créer un graphique de l'évolution temporelle des ventes
plt.figure(figsize=(12, 6))
df.groupby(df['Date de commande'].dt.to_period('M'))['Montant cmd'].sum().plot()
plt.title('Évolution temporelle des ventes')
plt.xlabel('Date')
plt.ylabel('Montant des commandes')
plt.xticks(rotation=45)
plt.show()

# Créer un graphique de l'analyse des ventes par univers
plt.figure(figsize=(12, 6))
sns.barplot(x='Univers', y='Montant cmd', data=df, estimator=sum, ci=None)
plt.title('Analyse des ventes par univers')
plt.xlabel('Univers')
plt.ylabel('Montant des commandes')
plt.xticks(rotation=45)
plt.show()

# Créer un graphique de l'analyse des ventes par nature
plt.figure(figsize=(12, 6))
sns.barplot(x='Nature', y='Montant cmd', data=df, estimator=sum, ci=None)
plt.title('Analyse des ventes par nature')
plt.xlabel('Nature')
plt.ylabel('Montant des commandes')
plt.xticks(rotation=45)
plt.show()

# Créer un graphique de l'analyse des ventes par vendeur
plt.figure(figsize=(12, 6))
sns.barplot(x='Vendeur', y='Montant cmd', data=df, estimator=sum, ci=None)
plt.title('Analyse des ventes par vendeur')
plt.xlabel('Vendeur')
plt.ylabel('Montant des commandes')
plt.xticks(rotation=45)
plt.show()
