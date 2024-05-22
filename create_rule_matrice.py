import uuid
import pandas as pd
import ipaddress
from stormshield.sns.sslclient import SSLClient
#
client = SSLClient(
    host="172.16.92.129", port=443,
    user='admin', password='Toto1234',
    sslverifyhost=False)


# Charger le fichier Excel
file_path = r'C:\Users\julien.bossuet\PycharmProjects\stormshield\matrice-template.xlsx'
df = pd.read_excel(file_path, header=0)
df.fillna('', inplace=True)

# Definition des réseaux
dict_network = {"NET_WAN": "192.168.250.0/29", "NET_DMZ":"172.20.1.0/24", "NET_DATABASE": "10.30.1.0/24", "NET_MGMT-NTK": "10.100.100.0/24", "NET_BACKUP": "10.20.1.0/24","NET_MGMT": "10.10.1.0/24"}

def get_network_address(ip_cidr):
    # Crée un objet réseau à partir de la notation CIDR
    network = ipaddress.ip_network(ip_cidr, strict=False)
    # Retourne l'adresse réseau
    return network.network_address

def recup_networks(ip_cidr, networks):
    # Création de l'objet IP à partir de la notation CIDR
    ip = ipaddress.ip_interface(ip_cidr)
    # Vérification pour chaque réseau dans le dictionnaire
    for network_name, network_cidr in networks.items():
        network = ipaddress.ip_network(network_cidr, strict=False)
        if ip.ip in network:
            return network_name
    return None


def create_host(host_name, host_ip):
    host_ip = host_ip.split('/')
    client.send_command(f"CONFIG OBJECT HOST NEW name={host_name} ip={host_ip[0]} resolve=static")
    client.send_command("CONFIG OBJECT ACTIVATE")

def create_service(protocol, num_port):
    service_name = f'{protocol}_{num_port}'
    if '-' in num_port:
        from_port, to_port = num_port.split('-')
        client.send_command(f'CONFIG OBJECT SERVICE NEW name={service_name} port={from_port} toport={to_port} proto={protocol}')
    else:
        client.send_command(f'CONFIG OBJECT SERVICE NEW name={service_name} port={num_port} proto={protocol}')
        client.send_command(f'CONFIG OBJECT ACTIVATE')

def check_host_exist(host_name, host_ip):
    # Commande pour lister tous les hôtes
    existing_hosts = client.send_command('CONFIG OBJECT HOST LIST')
    host_name_exist = client.send_command(f'CONFIG OBJECT LIST type=host,network start=1 search={host_name} searchfield=name')
    host_ip_exist = client.send_command(f'CONFIG OBJECT LIST type=host,network start=1 search={host_ip} searchfield=ip')
    if host_ip_exist or host_name_exist:
        return host_name_exist, host_ip_exist
    else:
        return None

def generate_firewall_rule(src_name, dest_name, src_ip, dest_ip, list_ports: list, networks):
    for e in list_ports:
        proto, num = e.split('_') # recuperation du type de protocol et du numero de port qui sont séparé par "-"
        create_service(proto,num)
    create_host(src_name, src_ip)
    create_host(dest_name, dest_ip)
    rule_name = f'Rule_{uuid.uuid4().hex}'  # Utiliser UUID pour garantir un nom unique
    # Conversion de la liste des ports en string avec une virgule comme séparateur
    string_ports = ','.join(list_ports)

    # Recuperation du nom du network de la source
    source_network_name = recup_networks(src_ip, networks)
    # Recuperation du nom du network de la destination
    destination_network_name = recup_networks(dest_ip, networks)
    #Creation du comment du séparateur
    separator_comment = f"{source_network_name} to {destination_network_name}"

    # Recherche si séparateur existe avec le comment spécifique
    response = client.send_command(f'CONFIG FILTER EXPLICIT index=8 type=filter')
    separator_found = False
    position = 1
    response_data = response.data['Filter']
    # Analyser la réponse pour trouver la position du séparateur
    for e in response_data:
        if 'separator' in e and separator_comment in e:
            parts = e.split(';')
            position_part = next((s for s in parts if 'position' in s), None)
            if position_part:
                position = int(position_part.split('=')[1])
                separator_found = True
                break
    # if separator_found == False:
    #         print(f'CONFIG FILTER RULE ADDSEP index=8 type=filter  collapse=0 position={rule_position color=C0C0C0 comment="{separator_comment}"')
    #         print(f'CONFIG FILTER ACTIVATE')



    # Insérer la règle immédiatement après le séparateur
    rule_position = position + 1
    client.send_command(f'CONFIG FILTER RULE INSERT index=8 type=filter state=off action=pass srctarget={src_name} dsttarget={dest_name} position={rule_position} global=0 dstport={string_ports} rulename={rule_name} output=xml loglevel=log')
    client.send_command(f'CONFIG FILTER ACTIVATE')



#Vérifier que l'on a bien les droit d'écriture
tata = client.send_command('MODIFY off')
toto = client.send_command('MODIFY on')
### Creer tous les séparateurs de NETWORK à NETWORK
# Pour chaque clé dans le dictionnaire
position = 6
for key in dict_network:
    # Pour chaque autre clé dans le dictionnaire (différente de la clé actuelle)
    color = "99CC00"
    for other_key in dict_network:
        if key != other_key:
            # Afficher la ligne de configuration avec la clé actuelle et l'autre clé
            if key =="NET_WAN":
                color = "FF0000"
            if key == "NET_DMZ":
                color = "CC99FF"
            result = client.send_command(f'CONFIG FILTER RULE ADDSEP index=8 type=filter  collapse=0 color={color} comment="{key} to {other_key}"')
            result = client.send_command("CONFIG FILTER ACTIVATE")


# Itérer sur les rangées et colonnes du fichier Excel
rules = []
# Itération des lignes
for row_index in range(len(df)):
    src_name = src_ip = df.iloc[row_index, 0].split('\n')[0]
    src_ip = df.iloc[row_index, 0].split('\n')[1]    # Accès par indices: première colonne de chaque ligne

    # Itération des colonnes de la ligne en cours
    for col_index in range(1, len(df.columns)):  # Commence à l'index 1 pour ignorer la première colonne
        dest_name = df.columns[col_index].split('\n')[0]
        dest_ip = df.columns[col_index].split('\n')[1]  # Extraire l'IP destination de l'en-tête de colonne
        list_ports = df.iloc[row_index, col_index].split('\n')  # Crée une liste de chaque port pour les IP sources et IP destination
        # Vérifier si la cellule contient effectivement des ports
        if len(list_ports) == 1 and list_ports[0] == '':
            continue  # on continue dans la boucle en sautant la generation de le rule car pas besoin
        else:
            rule = generate_firewall_rule(src_name, dest_name, src_ip, dest_ip, list_ports, dict_network)
            rules.append(rule)

# Afficher ou utiliser les règles générées
for rule in rules:
    print(rule)
client.disconnect()