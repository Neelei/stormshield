import pandas
from stormshield.sns.sslclient import SSLClient
#
# client = SSLClient(
#     host="185.243.3.103", port=443,
#     user='admin', password='',
#     sslverifyhost=False)

excel_data_df = pandas.read_excel('matrice-template.xlsx')
print(excel_data_df['VM1\n172.16.1.0/24'].to_dict())

# dict_network = {"NET_WAN": "192.168.250.0/29", "NET_DMZ":"172.20.1.0/24", "NET_DATABASE": "10.30.1.0/24", "NET_MGMT-NTK": "10.100.100.0/24", "NET_BACKUP": "10.20.1.0/24","NET_MGMT": "10.10.1.0/24"}

# Pour chaque clé dans le dictionnaire
# position = 6
# for key in dict_network:
#     # Pour chaque autre clé dans le dictionnaire (différente de la clé actuelle)
#     color = "99CC00"
#     for other_key in dict_network:
#         if key != other_key:
#             # Afficher la ligne de configuration avec la clé actuelle et l'autre clé
#             if key =="NET_WAN":
#                 color = "FF0000"
#             if key == "NET_DMZ":
#                 color = "CC99FF"
#             print(f'CONFIG FILTER RULE ADDSEP index=5 type=filter  collapse=0 color={color} comment="{key} to {other_key}"')
#             print(f'CONFIG FILTER RULE INSERT index=5 type=filter state=off action=pass srctarget={key} dsttarget={other_key} global=0 dstport=any output=xml loglevel=log')
# print("CONFIG FILTER ACTIVATE")

# list_peer = client.send_command("CONFIG IPSEC PEER LIST")
# show_peer = client.send_command("CONFIG IPSEC PEER SHOW  name=Site_SITE3-WAN1")
# ipsec_list_gw = client.send_command("CONFIG IPSEC POLICY GATEWAY LIST slot=01")
# list_phase1 = client.send_command("CONFIG IPSEC PROFILE PHASE1 LIST")
# show_phase1 = client.send_command("CONFIG IPSEC PROFILE PHASE1 SHOW name=DR")
# list_phase2 = client.send_command("CONFIG IPSEC PROFILE PHASE2 LIST")
# show_phase2 = client.send_command("CONFIG IPSEC PROFILE PHASE2 PROPOSALS AUTHENTICATION LIST name=DR")
# monitor_filter = client.send_command("MONITOR FILTER")
# add_separator = client.send_command("CONFIG FILTER RULE ADDSEP index=5 type=filter collapse=0 color=C0C0C0 comment=tootoo")
# add_rule = client.send_command("CONFIG FILTER RULE INSERT index=5 type=filter state=on action=pass srctarget=Network_internals dsttarget=internet dstport=http loglevel=minor")
# config_filter_activate = client.send_command("CONFIG FILTER ACTIVATE")
# config_slot_activate = client.send_command("CONFIG SLOT ACTIVATE type=filter slot=5")
# create_object = client.send_command("CONFIG OBJECT HOST NEW name=DNS_SRV ip=192.168.250.150 resolve=static")
# config_object_activate = client.send_command("CONFIG OBJECT ACTIVATE")
# monitor_spd = client.send_command("MONITOR GETSPD")
# print(ipsec_gw_list.data['result'])
# print(monitor_spd.data['result'][1])
# print(add_separator['result'][1])

# print(f'LISTE PEER\n{list_peer}\n')
# print(f'SHOW PEER Site_SITE3-WAN1\n{show_peer}\n')
# print(f'LISTE IPSEC GW\n{ipsec_list_gw}\n')
# print(f'LISTE PHASE1\n{list_phase1}\n')
# print(f'SHOW PHASE1 DR\n{show_phase1}\n')
# print(f'LISTE PHASE2\n{list_phase2}\n')
# print(f'SHOW PHASE2 DR\n{show_phase2}\n')
# print (monitor_filter.data['result'])




# client.disconnect()