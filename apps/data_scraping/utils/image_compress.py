from PIL import Image
import os

def image_compress(path:str, max_kb=300, quality=95):
    
    image = Image.open(path)
    while True:
        size_image = os.path.getsize(path)/1024
        if size_image > max_kb:
            image.save(path, 'JPEG', quality=quality)
            quality -= 1
        else:
            print(f'{os.path.basename(path)} - {size_image} - {quality}')
            break

def folder_image_compress(path_folder:str, mx_kb=300, quality=95):
    
    for img in os.listdir(path_folder):
        if 'desktop.ini' in img:
            continue
        path_img = os.path.join(path_folder, img)
        image_compress(path_img)    
    
    
