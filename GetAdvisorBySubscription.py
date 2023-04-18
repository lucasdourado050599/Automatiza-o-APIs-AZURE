# Biblioteca requests para REST API
import requests

#Conexão BLOB
from azure.storage.blob import BlobServiceClient
storage_account_key = "{storage_account_key}"
storage_account_name = "{storage_account_name}"
connection_string = "{connection_string}" #Fica em access key no storage account
container_name = "{container_name}"
###Fim Conexão BLOB###


###Pega Token####
print("Iniciando Script....")
print("Gerando Token")
url = "https://login.microsoftonline.com/{TENANT-ID}/oauth2/token"
user_data = {
    "grant_type": " client_credentials",
    "client_id": " client_id",
    "client_secret": " client_secret",
    "resource": " https://management.azure.com/"
}

headers = {'Content-Type': 'application/x-www-form-urlencoded'}
response = requests.post(url=url, data=user_data, headers=headers)
if response.status_code >= 200 and response.status_code <= 299:
    # Sucesso
    print('Suceso, status code:', response.status_code)
    #print('Response Headers: ', response.headers)
else:
    # Erros
    print('Status code', response.status_code)
    print('Reason', response.reason)
    print('Texto', )
pega_token = response.json()
token = pega_token['access_token']
print('Token = ', token)
###Fim Pega token ###



###Pega Subscription###
url = "https://management.azure.com/subscriptions?api-version=2020-01-01"
headers = {
        "Authorization": f"Bearer {token}"
    }
response = requests.get(url, headers=headers)
if response.status_code >= 200 and response.status_code <= 299:
    # Sucesso
    print('Suceso, status code:', response.status_code)
    #print('Response Headers: ', response.headers)
else:
    # Erros
    print('Status code', response.status_code)
    print('Reason', response.reason)
    print('Texto', )
contador = 0


###Armazena subscription em um array###
subscriptions = []

for item in response.json()["value"]:
    contador = contador + 1
    subscriptions.append(item["subscriptionId"])

subscription_ids = subscriptions


print("As subscriptions são:",subscriptions)
print("O total de subscriptions é: ", contador)
###Fim pega subscriptions###

###Inicio pega Recomendações###

total_chamadas= 0
###ARRAY###
vet = []
contador_insere = 0

while total_chamadas < len(subscriptions):
    subscription = subscriptions[total_chamadas]
    url = f"https://management.azure.com/subscriptions/{subscription}/providers/Microsoft.Advisor/recommendations?api-version=2022-10-01"
    headers = {
        "Authorization": f"Bearer {token}"
        }
    response = requests.get(url=url, headers=headers)
    pega_json = response.text
    retorno_json = pega_json

    print('JSON inserido no vetor', retorno_json)
    vet.insert(contador_insere, (retorno_json) + ",")
    total_chamadas = total_chamadas + 1
###Fim Pega Recomendações###


###Vetor para transcrever o vetor de trás para frente###
i=0
ii = total_chamadas
vet2 = []
while i < len(vet):
    ii = ii - 1
    vet2.insert(i,(vet[ii]))
    i+=1
###Fim vetor###



###Cconverter VETOR em String###
vetString = " ".join(vet2)
jsonfinal = ("[" + vetString + "]")

###Envia script para o BLOB###
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
blob_client = blob_service_client.get_blob_client(container=container_name, blob="advisor.json")
arquivo = open("advisor.json", "w")
blob_client.upload_blob((jsonfinal), overwrite=True)

print("Script Finalizado")