import pandas as pd
import ipaddress
from stormshield.sns.sslclient import SSLClient

client = SSLClient(
    host="172.16.92.129", port=443,
    user='admin', password='Toto1234',
    sslverifyhost=False)

# Lire le fichier Excel
file_path = 'PLAN-IP-CLOSERIE.xlsx'  # Mettez ici le chemin de votre fichier Excel
df = pd.read_excel(file_path, header=None)

# Initialiser un dictionnaire pour stocker les réseaux
dict_network = {}

### FONCTION CREATE NETWORK
def create_network(net_name, net_ip):
    # Convert the CIDR notation to an IPv4Network object
    network = ipaddress.ip_network(net_ip)

    # Extract the IP address and netmask
    ip_address = str(network.network_address)
    netmask = str(network.netmask)

    # Send the commands to the client
    result1 = client.send_command(f"CONFIG OBJECT NETWORK NEW name={net_name} ip={ip_address} mask={netmask}")
    result2 = client.send_command("CONFIG OBJECT ACTIVATE")

### FONCTION CREATE SEPARATOR
def create_separator(dict_net):
    for key in dict_net:
        # Pour chaque autre clé dans le dictionnaire (différente de la clé actuelle)
        color = "99CC00"
        client.send_command(f'CONFIG FILTER RULE ADDSEP index=8 type=filter collapse=0 color=008000 comment="{key} to WAN"')
        client.send_command(f'CONFIG FILTER ACTIVATE')
        for other_key in dict_net:
            if key != other_key:
                # Afficher la ligne de configuration avec la clé actuelle et l'autre clé
                if key == "NET_DMZ":
                    color = "CC99FF"
                result = client.send_command(f'CONFIG FILTER RULE ADDSEP index=8 type=filter  collapse=0 color={color} comment="{key} to {other_key}"')
                result2 = client.send_command(f'CONFIG FILTER RULE INSERT index=8 type=filter state=off action=pass srctarget={key} dsttarget={other_key} global=0 dstport=any output=xml loglevel=log')
                result3 = client.send_command(f'CONFIG FILTER ACTIVATE')

### CREATION DICTIONAIRE DEPUIS EXCEL
# Parcourir les lignes du DataFrame pour ajouter les entrées au dictionnaire
for index, row in df.iterrows():
    # Utiliser la colonne de nom comme clé et l'adresse IP comme valeur
    network_name = row[0].strip() if isinstance(row[0], str) else row[0]
    network_ip = row[1].strip() if isinstance(row[1], str) else row[1]
    dict_network[network_name] = network_ip
    create_network(network_name, network_ip)
# Creation séparator
create_separator(dict_network)

# Afficher le dictionnaire
print(dict_network)
client.disconnect()