import os
import sys,requests
from data_scraping.utils.convert_to_jpg import convert_byte_to_jpeg

def download_picture(url, path):
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    with open(path, 'wb') as img:
        response = requests.get(url, headers=headers, stream=True)
        if not response.ok:
            print(f'{path}, não pode ser baixado')
        else:
            content_type = response.headers.get('Content-Type')
            
            if 'jpeg' in content_type:    
                img.write(response.content)
    
    if not 'jpeg' in content_type:
        convert_byte_to_jpeg(response.content, path)
        