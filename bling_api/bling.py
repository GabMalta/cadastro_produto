import sys, os

import requests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import base64
from requests_policy.http import http
import settings

class BlingApi():
    
    def __init__(self, client_id:str = '', client_secret:str = ''):
        
        if client_id and client_secret:
        
            self.client_id = client_id
            self.client_secret = client_secret
        else:
            self.client_id = settings.CLIENT_ID
            self.client_secret = settings.CLIENT_SECRET
        
        self.generate_base64_credential()
        self.get_access_token()
        self.get_refresh_token()
        
        self.update_access_token()
        
    def generate_base64_credential(self):
        
        if self.client_id and self.client_secret:
            credential_str = f'{self.client_id}:{self.client_secret}'
            credential_bytes = credential_str.encode('utf-8')
            base64_bytes = base64.b64encode(credential_bytes)
            
            self.credential_base64 = base64_bytes.decode('utf-8')
        else:
            raise ValueError('client_id ou client_secret incorreto ou não encontrado')
           
    def get_access_token(self):
        with open('./tokens/access_token.txt', 'r') as token:
            self.access_token = token.read()
            
    def get_refresh_token(self):
        with open('./tokens/refresh_token.txt', 'r') as token:
            self.refresh_token = token.read()

    def set_access_token(self, access_token:str):
        with open('./tokens/access_token.txt', 'w') as token:
            token.write(access_token)
        
        self.get_access_token()
            
    def set_refresh_token(self, refresh_token: str):
        with open('./tokens/refresh_token.txt', 'w') as token:
            token.write(refresh_token)
            
        self.get_refresh_token()
        
    def update_access_token(self):
        
        if self.access_token and self.refresh_token:
            
            link = 'https://www.bling.com.br/Api/v3/oauth/token'
            headers = {"Content-Type": "application/x-www-form-urlencoded","Accept": "1.0", "Authorization": f"Basic {self.credential_base64}"}

            body_message = {"grant_type": "refresh_token", "refresh_token": {self.refresh_token}}

            try:
                response = http.post(link, headers=headers, data=body_message).json()
                refresh_token = response['refresh_token']
                access_token = response['access_token']
                
                self.set_refresh_token(refresh_token)
                self.set_access_token(access_token)
                    
                print('TOKEN ATUALIZADO COM SUCESSO')
                
            except requests.exceptions.HTTPError as err:
                try:
                    error = err.response.json()
                    type_error = error['error']['description']
                    
                    match type_error:
                        case 'The client credentials are invalid':
                            msg = 'client_id ou client_secret inválido!'
                        case 'Invalid refresh token':
                            msg = 'Refresh token inválido ou expirado, gere novos tokens'
                            self.set_access_token('')
                            self.set_refresh_token('')

                    print(f'{type_error}: {msg}')
                
                except Exception as exc:
                    print(exc)
        
        else:
            print('access_token e/ou refresh_token inválido ou faltando.')
            self.generate_access_token()
    
    def generate_access_token(self):
        
        print('Gerar novo access_token')
        code_authorization = input('Cole aqui o code_authorization gerado no app do bling: ')
                   
        link = 'https://www.bling.com.br/Api/v3/oauth/token'
        headers = {"Content-Type": "application/x-www-form-urlencoded","Accept": "1.0", "Authorization": f"Basic {self.credential_base64}"}

        body_message = {"grant_type": "authorization_code", "code": code_authorization}

        try:
            response = http.post(link, headers=headers, data=body_message).json()
            refresh_token = response['refresh_token']
            access_token = response['access_token']
            
            self.set_refresh_token(refresh_token)
            self.set_access_token(access_token)
                
            print('TOKEN GERADO COM SUCESSO')
            
        except requests.exceptions.HTTPError as err:
            try:
                error = err.response.json()['error']['description']
                match error:
                    case 'The authorization code has expired':
                        msg = 'Código de autorização expirado, gere um novo e lembre-se que ele tem apenas 1 minuto de duração!'
                    case "Authorization code doesn't exist or is invalid for the client":
                        msg = 'Código de autorização inválido'
                    
                print(f'{error}: {msg}')
            except Exception as ex:
                print(ex)
