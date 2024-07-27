from PIL import Image
from io import BytesIO
import os

def convert_to_jpg(path:str):
    
    image = Image.open(path)
    image.convert()
    
    os.remove(path)

def convert_byte_to_jpeg(byte:bytes, path:str):
    image = Image.open(BytesIO(byte))
    
    jpeg_path = path.rsplit('.', 1)[0] + '.jpg'
    image.convert('RGB').save(jpeg_path, 'JPEG')
    image.close()
    os.remove(path)
    
def convert_folder_to_jpg(path:str):
    
    for img in os.listdir(path):
        if 'desktop.ini' in img:
            continue
        convert_to_jpg(os.path.join(path, img))