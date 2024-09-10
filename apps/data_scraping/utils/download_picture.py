import os
import sys,requests
from apps.data_scraping.utils.convert_to_jpg import convert_byte_to_jpeg

def download_picture(url, path):
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    response = requests.get(url, headers=headers, stream=True)
    content_type = response.headers.get('Content-Type')
    
    if not response.ok:
        print(f'{path}, não pode ser baixado')
    else:
        with open(path, 'wb') as img:
                if 'image' in content_type:    
                    img.write(response.content)
        
        if not 'jpeg' in content_type:
            convert_byte_to_jpeg(response.content, path)
        
    response.close()
        