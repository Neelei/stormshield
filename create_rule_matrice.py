import uuid
import pandas as pd

# Charger le fichier Excel
file_path = r'C:\Users\julien.bossuet\PycharmProjects\stormshield\matrice-template.xlsx'
df = pd.read_excel(file_path, header=0)
df.fillna('', inplace=True)

def create_host(host_name, host_ip):
    print(f"CONFIG OBJECT HOST NEW name={host_name} ip={host_ip} resolve=static")
    print("CONFIG OBJECT ACTIVATE")

def create_service(protocol, num_protocol):
    service_name = f'{protocol}-{num_protocol}'
    client.send_command(f'CONFIG OBJECT SERVICE NEW name={service_name} port={num_protocol} proto={protocol}')
    client.send_command(f'CONFIG OBJECT ACTIVATE')

def generate_firewall_rule(src_ip, dest_ip, list_ports: list):
    # protocol, port = protocol_port.split('-') # recuperation du type de protocol et du numero de port qui sont séparé par "-"
    rule_name = f"Rule_{uuid.uuid4().hex}"  # Utiliser UUID pour garantir un nom unique
    # Conversion de la liste des ports en string avec une virgule comme séparateur
    string_ports = ','.join(list_ports)
    # Cette fonction devra être adaptée pour envoyer la commande à votre pare-feu
    print(f'CONFIG FILTER RULE INSERT index=5 type=filter state=off action=pass srctarget={src_ip} dsttarget={dest_ip} global=0 dstport={string_ports} rulename={rule_name=} output=xml loglevel=log')
    # return f"{rule_name}: ALLOW {src_ip} TO {dest_ip} ON {protocol.upper()} PORT {port}"


# Itérer sur les rangées et colonnes
rules = []
for index in range(len(df)):
    src_ip = df.iloc[index, 0].split('\n')[1]  # Accès par indice: première colonne de chaque ligne
    for col_index in range(1, len(df.columns)):  # Commence à l'index 1 pour ignorer la première colonne
        dest_ip = df.columns[col_index].split('\n')[1]  # Extraire l'IP destination de l'en-tête de colonne
        list_ports = df.iloc[index, col_index].split('\n')  # Crée une liste de chaque port pour les IP sources et IP destination
        if list_ports:  # Vérifier si la cellule n'est pas vide
            rule = generate_firewall_rule(src_ip, dest_ip, list_ports)
            rules.append(rule)

# Afficher ou utiliser les règles générées
for rule in rules:
    print(rule)
