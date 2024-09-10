from apps.bling_api.bling import BlingApi
from requests_policy.http import http

class GetInfoProduct(BlingApi):
    
    
    def get_products(self):
        
        link = 'https://www.bling.com.br/Api/v3/produtos/lojas'
        
        headers = {"Authorization": f"Bearer {self.access_token}", 
                   "Content-Type": "application/json",
                   }
        
        response = http.get(link, headers=headers)
        response = response.json()
        
        return response
        

        