###Biblioteca para realizar requisição REST API###
import requests


url = ("https://login.microsoftonline.com/{TENANT-ID}/oauth2/token")

###BODY DO POST###
user_data = {
"grant_type": " client_credentials",
"client_id": " client_id",
"client_secret": " client_secret",
"resource": " https://management.azure.com/"
}
###CABEÇARIO DO BODY###
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
response = requests.post(url=url,data=user_data,headers=headers)

if response.status_code >= 200 and response.status_code <=299:
    #Sucesso
    print('Status code',response.status_code)
    #print('Texto', response.text)

    ###PEGA APENAS O TOKEN DO CAMPO access_token###
    pega_token = response.json()
    token = pega_token['access_token']

    ###Salva o token em um TXT###
    with open('token.txt', 'w') as file:
        file.write(token)

else:
    #Erros
    print('Status code', response.status_code)
    print('Reason', response.reason)
    print('Texto', response.text)




