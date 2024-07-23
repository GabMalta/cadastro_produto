import requests
import time
import sys, os

sys.path.append(os.path.abspath(os.curdir))


def ler_senhas():
        with open(fr"./core/bling/tokens/access_token_bling.txt",'r') as token:
            acess_token_bling = token.read()

        # TOKEN DE ATUALIZACAO BLING    
        with open(fr"./core/bling/tokens/refresh_token_bling.txt",'r') as token:
            refresh_token_bling = token.read()
        
        return acess_token_bling, refresh_token_bling
    

# credenciais_base64 = 'NzUyYzUwYzBkYzVhNzM1MTAzNjBkYmI0ODRjZjMwMTdhMTRkMzVkNDoyMmM3OWQyNzI4NjY1ZTY0ZjRmMDBhMDNkOWI3ZTU3NzlhMmRlYjAxNzM2ZjgzMTI4ZDUxZjUwZGExZTU='

#CREDENCIAL LEGITIMA
credenciais_base64 = 'YTU1MjVlNjJjMzA2YjAxM2RmOWQwNDdhMTExZDQwN2JkYmZkN2EwNzozNTU0NDNhNGEzNjFjYjcyZjI2MjhlMzg0OWEyZGI5MmU3MjViY2U3ODU0ODMyYmQ1ZWUzZDIxMTE1ZjQ='


def atualiza_token():
    refresh_token_bling = ler_senhas()[1]
    link = 'https://www.bling.com.br/Api/v3/oauth/token'
    headers = {"Content-Type": "application/x-www-form-urlencoded","Accept": "1.0", "Authorization": f"Basic {credenciais_base64}"}

    body_message = {"grant_type": "refresh_token", "refresh_token": {refresh_token_bling}}

    requisicao = requests.post(link, headers=headers, data=body_message)
    resposta = requisicao.json()
    
    try:
        refresh_token = resposta['refresh_token']
        access_token = resposta['access_token']
        with open (fr".\core\bling\tokens\refresh_token_bling.txt", 'w') as arq:
            arq.write(refresh_token)
    
        with open (fr".\core\bling\tokens\access_token_bling.txt", 'w') as arq:
            arq.write(access_token)
            
        print('TOKEN ATUALIZADO COM SUCESSO')
        
        return ler_senhas()
    except:
        print(resposta)
        
atualiza_token()
        
    
        
        
