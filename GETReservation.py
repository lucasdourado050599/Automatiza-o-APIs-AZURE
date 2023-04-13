# Biblioteca requests para REST API
import requests

#Conexão BLOB
from azure.storage.blob import BlobServiceClient

storage_account_key = "{storage_account_key}"
storage_account_name = "{storage_account_name}"
connection_string = "{connection_string}" #Fica em access key no storage account
container_name = "{container_name}"

###Pega Token e  armazena na variável "token"####
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
    print('Response Headers: ', response.headers)
else:
    # Erros
    print('Status code', response.status_code)
    print('Reason', response.reason)
    print('Texto', )
pega_token = response.json()
token = pega_token['access_token']
print('Token = ', token)
###Fim Pega token ###

# CHAMADA API
print('Iniciando chamada na API Reservation...')

url = "https://management.azure.com/providers/Microsoft.Capacity/reservations?api-version=2022-11-01"
headers = {
    "Authorization": f"Bearer {token}"
}
print('Endpoint: ', url)
print('headers: ', headers)
# Retorno dos status code
if response.status_code >= 200 and response.status_code <= 299:
    # Sucesso
    print('Suceso, status code:', response.status_code)
    print('Response Headers: ', response.headers)
else:
    # Erros
    print('Status code', response.status_code)
    print('Reason', response.reason)
    print('Texto', )


#REQUEST ENVIADO
response = requests.get(url=url, headers=headers)


###Fim primeira chamada reservation ###

##PEGA LINK DA PAGINAÇÃO###
pega_link = response.json()
link = pega_link['nextLink']


####PEGA JSON PARA ARRAY###
pega_json = response.text
retorno_json = pega_json

###FLAG WHILE###
flag = 0

###ARRAY###
vet = []
contador_insere = 0

###Validação###
total_chamadas = 0

###While para percorrer todas as páginas da API ###
while (flag == 0):
    ###Contador de chamadas###
    total_chamadas = total_chamadas + 1
    ####Insere JSON no vetor###
    print('JSON inserido no vetor',retorno_json)
    vet.insert(contador_insere,(retorno_json)+ ",")

    url = link
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url=url, headers=headers)

    pega_json = response.text
    retorno_json = pega_json

    pega_link = response.json()

    ###Verifica se existe próxima pagina###
    if 'nextLink' in (pega_link):
        flag = 0
        link = pega_link['nextLink']
    else:
        vet.insert(contador_insere, (retorno_json))
        total_chamadas = total_chamadas + 1
        flag = 1



else:
    print("total de GETs na API Reservation = ",total_chamadas)
###Fim While###

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
blob_client = blob_service_client.get_blob_client(container=container_name, blob="reservation3.json")
arquivo = open("reservation3.json", "w")
blob_client.upload_blob((jsonfinal), overwrite=True)


print("Script Finalizado")