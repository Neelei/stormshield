import ipaddress

# # Créer un réseau IPv4
# net = ipaddress.ip_network('192.168.1.0/24')
# print(f"Réseau: {net}")
# # Itérer sur toutes les adresses dans ce réseau
# for addr in net:
#     print(addr)
#
# ip = ipaddress.ip_address('192.168.2.2')
# print(f"Est dans le réseau: {ip in net}")

def get_network_address(ip_cidr):
    # Crée un objet réseau à partir de la notation CIDR
    network = ipaddress.ip_network(ip_cidr, strict=False)
    # Retourne l'adresse réseau
    return network.network_address

# Exemple d'utilisation
ip_cidr = '172.16.1.42/24'
network_address = get_network_address(ip_cidr)
print(f"L'adresse réseau de {ip_cidr} est {network_address}")
