import pandas as pd
from flatten_json import flatten
import requests
import time

print('Iniciando Script')    
    
###Pega Token####
print("Gerando Token")
###Ajustar a URL com o id do tenant, client id e client secret
url = "https://login.microsoftonline.com/{IDdoSeuTenant}/oauth2/token"
user_data = {
    "grant_type": " client_credentials",
    "client_id": "ID DA SUA SERVICE PRINCIPAL",
    "client_secret": "SECRET DA SUA SERVICE PRINCIPAL",
    "resource": " https://management.azure.com/"
}

headers = {'Content-Type': 'application/x-www-form-urlencoded'}
response = requests.post(url=url, data=user_data, headers=headers)
if response.status_code >= 200 and response.status_code <= 299:
        # Sucesso
        print("Token gerado com sucesso")
else:
        # Erros
        print('Erro api')
pega_token = response.json()
token = pega_token['access_token']
print ('Token = %s', token)
###Fim Pega token ###

###Gera Relatório Custo###
print ("Gerando Relatório de Custo....")
#Colocar a subscription q deseja realizar a consulta
url = "https://management.azure.com/subscriptions/{SuaSubscription}/providers/Microsoft.CostManagement/generateCostDetailsReport?api-version=2022-10-01"
headers = {
        "Authorization": f"Bearer {token}"
    }
##Ajusar a hora desejada
body = {

        "metric": "ActualCost",
        "timePeriod": {
        "start": "COLOCAR A DATA NO FORMATO AAAA-MM-DD",
        "end": "COLOCAR A DATA NO FORMATO AAAA-MM-DD"
    }
}

response = requests.post(url, headers=headers, json=body)
if response.status_code >= 200 and response.status_code <= 299:
        # Sucesso
        print("API Relatório COST Azure consultada com sucesso")
else:
        # Erros
        print('Erro api')

pega_location = response.headers
location = pega_location['Location']
print('Location = %s', location)
###Fim Gera Relatório Custo###

###Timer de 2 minutos para consultar o relatório###
time.sleep(120)

###Get Relatório Custo###
print ("Get no relatório criado")
url = location
headers = {
        "Authorization": f"Bearer {token}"
    }
response = requests.get(url, headers=headers)
if response.status_code >= 200 and response.status_code <= 299:
        # Sucesso
        print("Relatório consultado com sucesso")
else:
        # Erros
        print('Erro api')

pega_blob = response.json()
blob = pega_blob['manifest']['blobs'][0]['blobLink']
print('blob = %s', blob)
###FimGet Relatório Custo###
print ("Lendo relatório")


data = pd.read_csv(blob)
data.to_excel('custos.xlsx', index=False)
