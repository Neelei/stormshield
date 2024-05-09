import uuid
import pandas as pd

# Charger le fichier Excel
file_path = r'C:\Users\julien.bossuet\PycharmProjects\stormshield\matrice-template.xlsx'
df = pd.read_excel(file_path, header=0)
df.fillna('', inplace=True)

def generate_firewall_rule(src_ip, dest_ip, protocol_port):
    protocol, port = protocol_port.split('-') # recuperation du type de protocol et du numero de port qui sont séparé par "-"
    rule_name = f"Rule_{uuid.uuid4().hex}"  # Utiliser UUID pour garantir un nom unique
    # Cette fonction devra être adaptée pour envoyer la commande à votre pare-feu
    return f"{rule_name}: ALLOW {src_ip} TO {dest_ip} ON {protocol.upper()} PORT {port}"

# Itérer sur les rangées et colonnes
rules = []
for index in range(len(df)):
    src_ip = df.iloc[index, 0].split('\n')[1]  # Accès par indice: première colonne de chaque ligne
    for col_index in range(1, len(df.columns)):  # Commence à l'index 1 pour ignorer la première colonne
        dest_ip = df.columns[col_index].split('\n')[1]  # Extraire l'IP destination de l'en-tête de colonne
        protocols_ports = df.iloc[index, col_index].split('\n')  # Crée une liste de chaque port pour les IP sources et IP destination
        for protocol_port in protocols_ports:
            if protocol_port:  # Vérifier si la cellule n'est pas vide
                rule = generate_firewall_rule(src_ip, dest_ip, protocol_port)
                rules.append(rule)

# Afficher ou utiliser les règles générées
for rule in rules:
    print(rule)
