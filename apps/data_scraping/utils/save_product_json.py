import json, os

def save_product_json(path_folder, data):
    
    path = os.path.join(path_folder, 'image_urls.json')

    with open(path, 'w', encoding='utf-8') as arq:
        json.dump(data, arq, ensure_ascii=False, indent=4)
    
    