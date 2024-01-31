from stormshield.sns.sslclient import SSLClient
import pandas as pd

client = SSLClient(
    host="172.16.92.193", port=443,
    user='admin', password='Toto1234',
    sslverifyhost=False)

list_peer = client.send_command("CONFIG IPSEC PEER LIST")
show_peer = client.send_command("CONFIG IPSEC PEER SHOW  name=Site_SITE3-WAN1")
ipsec_list_gw = client.send_command("CONFIG IPSEC POLICY GATEWAY LIST slot=01")
list_phase1 = client.send_command("CONFIG IPSEC PROFILE PHASE1 LIST")
show_phase1 = client.send_command("CONFIG IPSEC PROFILE PHASE1 SHOW name=DR")
list_phase2 = client.send_command("CONFIG IPSEC PROFILE PHASE2 LIST")
show_phase2 = client.send_command("CONFIG IPSEC PROFILE PHASE2 PROPOSALS AUTHENTICATION LIST name=DR")
monitor_filter = client.send_command("MONITOR FILTER")


monitor_spd = client.send_command("MONITOR GETSPD")
# print(ipsec_gw_list.data['result'])
# print(monitor_spd.data['result'][1])
# print(f'LISTE PEER\n{list_peer}\n')
# print(f'SHOW PEER Site_SITE3-WAN1\n{show_peer}\n')
# print(f'LISTE IPSEC GW\n{ipsec_list_gw}\n')
# print(f'LISTE PHASE1\n{list_phase1}\n')
# print(f'SHOW PHASE1 DR\n{show_phase1}\n')
# print(f'LISTE PHASE2\n{list_phase2}\n')
# print(f'SHOW PHASE2 DR\n{show_phase2}\n')
print (monitor_filter.data['result'])
print("toto")



client.disconnect()