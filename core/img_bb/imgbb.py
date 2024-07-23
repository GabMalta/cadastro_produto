import base64
import requests
from core.senha import IMGBB_TOKEN, IMGBB_TOKEN_2, IMGBB_TOKEN_3, IMGBB_TOKEN_4, IMGBB_TOKEN_5



def hospeda_imagem(caminho_img,nome):
    
    token = IMGBB_TOKEN
    with open(caminho_img, "rb") as file:
        img_b64 = base64.b64encode(file.read())
    
    def tentativa(token):
        link = "https://api.imgbb.com/1/upload"
        
        
        body = {
            "key": token,
            "image": img_b64,
            "name" : nome
        }
        
        requisicao = requests.post(link, body)
        resposta = requisicao.json()
        

        url = resposta['data']['url']
        status = resposta['status']
            

            
        return url
    
    try:
        url = tentativa(token)
        print(f'URL HOSPEDADA: {url}')
    
    except Exception as e:
        try:
            print('except img_bb 2 \n', e)
            token = IMGBB_TOKEN_2
            url = tentativa(token)
    
        except:
            try:
                print('except img_bb 3 \n', e)
                token=IMGBB_TOKEN_3
                url = tentativa(token)
            except:
                try:
                    print('except img_bb 4 \n', e)
                    token=IMGBB_TOKEN_4
                    url = tentativa(token)
                except:
                    try:
                        print('except img_bb 5 \n', e)
                        token=IMGBB_TOKEN_5
                        url = tentativa(token)
                    except:
                        pass
                
        

    return url
