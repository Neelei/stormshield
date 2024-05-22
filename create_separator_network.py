import pandas as pd

# Lire le fichier Excel
file_path = 'PLAN-IP-CLOSERIE.xlsx'  # Mettez ici le chemin de votre fichier Excel
df = pd.read_excel(file_path, header=None)

# Initialiser un dictionnaire pour stocker les réseaux
dict_network = {}

# Parcourir les lignes du DataFrame pour ajouter les entrées au dictionnaire
for index, row in df.iterrows():
    # Utiliser la colonne de nom comme clé et l'adresse IP comme valeur
    network_name = row[0].strip() if isinstance(row[0], str) else row[0]
    network_ip = row[1].strip() if isinstance(row[1], str) else row[1]
    dict_network[network_name] = network_ip

# Afficher le dictionnaire
print(dict_network)
