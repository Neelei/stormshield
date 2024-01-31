import pandas as pd

# Exemple de réponse JSON de la commande 'MONITOR GETSPD'
monitor_spd_response = {
    'rulename': '188e9c85e31_2',
    'ikerulename': 'Site_SITE3-WAN1',
    'src': '172.31.1.1',
    'srcmask': '32',
    'srcname': 'NAT_MAINCARE_PPROD',
    'dst': '172.30.1.1',
    'dstmask': '32',
    'dstname': 'NAT_CALIMED_PPROD',
    'srcgw': '172.16.92.193',
    'srcgwname': 'Firewall_WAN1',
    'dstgw': '172.16.92.129',
    'dstgwname': 'SITE3-WAN1',
    'type': 'gateway',
    'global': '0',
    'localid': 'C=MC, ST=MONACO, L=Monaco, O=Monaco Digital, OU=Monaco Digital, CN=CERT-SITE4',
    'peerid': '',
    'ike': '2',
    'enc': 'esp',
    'policy': 'tunnel',
    'maxlifetime': '34560'
}

# Création d'un DataFrame à partir du JSON
df = pd.DataFrame([{
    'Référence': monitor_spd_response['rulename'],
    'IP source Public': monitor_spd_response['src'],
    'IP destination Public': monitor_spd_response['dst'],
    'IP INTERFACE': monitor_spd_response['srcgw'],
    'IP Interface Remote': monitor_spd_response['dstgw'],
    'Phase 1': monitor_spd_response['localid'],
    'Phase 2': monitor_spd_response['policy'],
}])

# Sauvegarde du DataFrame en fichier Excel
excel_path = 'VPN_IPsec_Data.xlsx'
df.to_excel(excel_path, index=False)

print("Fichier Excel créé : " + excel_path)
