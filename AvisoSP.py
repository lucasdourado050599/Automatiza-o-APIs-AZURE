import requests
import pandas as pd
from flatten_json import flatten
import datetime
import smtplib
import email.message
from email.mime.text import MIMEText
from datetime import datetime
from dateutil import parser

# Gera Token
token_url = f"https://login.microsoftonline.com/{tenant}/oauth2/token"
token_data = {
    "grant_type": "client_credentials",
    "client_id":  "{client_id}",
    "client_secret":  "{client_secret}",
    "resource": "https://graph.microsoft.com"
}
token_response = requests.post(token_url, data=token_data)
access_token = token_response.json()["access_token"]
###Fim Pega Token ###

df_final = pd.DataFrame()


# Obtenha os detalhes dos APP registration
app_registration_url = f"https://graph.microsoft.com/v1.0/applications?$count=true&$select=displayName,appId,Id,createdDateTime,endDateTime,passwordCredentials&$top=999"
headers = {
"Authorization": f"Bearer {access_token}"
}
app_response = requests.get(app_registration_url, headers=headers)
retorno = app_response.json()
dict_list = []
df_final = pd.DataFrame()


for i in app_response.json()['value']:

    flat = flatten(i, '.')
    dict_list.append(flat)
    df = pd.DataFrame(dict_list)
    contador = 0


    while f'passwordCredentials.{contador}.endDateTime' in flat.keys():

        app_name = flat['displayName']
        segredo = flat[f'passwordCredentials.{contador}.displayName']
        print(flat[f"passwordCredentials.{contador}.endDateTime"])
        print(flat['displayName'])

        try:
            # Tentar analisar com milissegundos
            data_formatada = datetime.strptime(flat[f"passwordCredentials.{contador}.endDateTime"], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d")
        except ValueError:
            try:
                # Tentar analisar com microssegundos
                data_formatada = datetime.strptime(flat[f"passwordCredentials.{contador}.endDateTime"], "%Y-%m-%dT%H:%M:%S.%f").strftime("%Y-%m-%d")
            except ValueError:
                try:
                    # Tentar analisar com dateutil (lida com casas decimais variáveis)
                    data_formatada = parser.parse(flat[f"passwordCredentials.{contador}.endDateTime"]).strftime("%Y-%m-%d")
                except ValueError:
                    # Se todas as tentativas falharem, você pode tratar a data como inválida ou fazer outra ação aqui
                    data_formatada = None

        # Verifique a data de expiração do segredo
        client_secret_expiration = datetime.strptime(data_formatada, "%Y-%m-%d")
        days_until_expiration = (client_secret_expiration - datetime.utcnow()).days
        # Defina o limite de dias antes do vencimento para gerar o alerta
        days_threshold = 7

        if days_until_expiration <= days_threshold  and days_until_expiration >= 0:
            # O segredo está prestes a expirar, envie um alerta por email
            def enviar_email():  
                corpo_email = f"""
                <p>"O secret name "{segredo}" do App registration "{app_name}" vai  expirar em {days_until_expiration} dias dias. Procurar o owner"</p>
                """

                msg = email.message.Message()
                msg['Subject'] = "Alerta: Segredo do App Registration prestes a expirar"
                msg['From'] = '{email que vai enviar}'
                msg['To'] = '{email que vai receber}'
                password = '{senha}' 
                msg.add_header('Content-Type', 'text/html')
                msg.set_payload(corpo_email )

                s = smtplib.SMTP('smtp.gmail.com: 587')
                s.starttls()
                # Login Credentials for sending the mail
                s.login(msg['From'], password)
                s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
                print(f'Email de alerta do Enterprise applications "{app_name}" enviado ')

            
            enviar_email()
        contador = contador + 1


### Inicia o next link
if "@odata.nextLink" in app_response.json():
    next_link = retorno["@odata.nextLink"]
    url = next_link
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url=url, headers=headers)
    retorno1 = response.json()

    dict_list1 = []
    contador_nextlink = 0
    for i in response.json()['value']:

        flat1 = flatten(i, '.')

        while f'passwordCredentials.{contador_nextlink}.endDateTime' in flat1.keys():

            app_name = flat1['displayName']
            segredo = flat1[f'passwordCredentials.{contador_nextlink}.displayName']

            print(flat1[f"passwordCredentials.{contador_nextlink}.endDateTime"])
            print(flat1['displayName'])

            try:
                # Tentar analisar com milissegundos
                data_formatada = datetime.strptime(flat1[f"passwordCredentials.{contador_nextlink}.endDateTime"], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d")
            except ValueError:
                try:
                    # Tentar analisar com microssegundos
                    data_formatada = datetime.strptime(flat1[f"passwordCredentials.{contador_nextlink}.endDateTime"], "%Y-%m-%dT%H:%M:%S.%f").strftime("%Y-%m-%d")
                except ValueError:
                    try:
                        # Tentar analisar com dateutil (lida com casas decimais variáveis)
                        data_formatada = parser.parse(flat1[f"passwordCredentials.{contador_nextlink}.endDateTime"]).strftime("%Y-%m-%d")
                    except ValueError:
                        # Se todas as tentativas falharem, você pode tratar a data como inválida ou fazer outra ação aqui
                        data_formatada = None

            # Verifique a data de expiração do segredo
            client_secret_expiration = datetime.strptime(data_formatada, "%Y-%m-%d")
            days_until_expiration = (client_secret_expiration - datetime.utcnow()).days
            # Defina o limite de dias antes do vencimento para gerar o alerta
            days_threshold = 7

            if days_until_expiration <= days_threshold  and days_until_expiration >= 0:
                # O segredo está prestes a expirar, envie um alerta por email
                def enviar_email():  
                    corpo_email = f"""
                    <p>"O segredo do App registration nome "{app_name}" vai  expirar em {days_until_expiration} dias dias. Procurar o owner"</p>
                    """

                    msg = email.message.Message()
                    msg['Subject'] = "Alerta: Segredo da Application Registration prestes a expirar"
                    msg['From'] = '{email que vai enviar}'
                    msg['To'] = '{email que vai receber}'
                    password = '{senha}' 
                    msg.add_header('Content-Type', 'text/html')
                    msg.set_payload(corpo_email )

                    s = smtplib.SMTP('smtp.gmail.com: 587')
                    s.starttls()
                    # Login Credentials for sending the mail
                    s.login(msg['From'], password)
                    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
                    print(f'Email de alerta do Enterprise applications "{app_name}" enviado ')

        
                enviar_email()
            contador_nextlink = contador_nextlink + 1

print ("script Finalizado, bye bye")

