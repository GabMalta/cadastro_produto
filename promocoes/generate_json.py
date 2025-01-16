import os,json

def generate_json(path, pictures_path):
    
    folder_list = os.listdir(pictures_path)

    colors_dict = {"sizes": "", "variations": {}}
    sizes = []
    
    try:
        for color in folder_list:
            
            if 'desktop.ini' in color or 'image_urls.json' in color:
                continue
            
            name = os.path.splitext(color)[0]
            color_name, size = name.split("-")

            os.rename(os.path.join(pictures_path, color), os.path.join(pictures_path, f'{color_name}.jpg'))

            size = size.split("_")
            size = [float(s.replace(",", ".")) for s in size]

            colors_dict['variations'][color_name] = {"size": size, 'amount': sum(size)}

            sizes.extend(size)


        colors_dict['sizes']=list(dict.fromkeys(sizes))


        with open(os.path.join(path, f'promo.json'), 'w', encoding='utf-8') as arq:
            json.dump(colors_dict, arq, ensure_ascii=False, indent=4)
            
        return colors_dict

    except Exception as e:
        print(e)
        pass