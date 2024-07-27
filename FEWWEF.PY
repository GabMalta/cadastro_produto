from PIL import Image
import os

def croped_img(path):
    image = Image.open(path)

    n_img = image.crop((15, 15, 607, 1064))
    n_img2 = image.crop((622, 129, 1508, 1064))

    new_image = Image.new('RGB', (1527,1080), (255,255,255))


    new_image.paste(n_img, (15, 15))
    new_image.paste(n_img2, (622, 15))

    new_image.save(path)


folder = r'D:\SITE LEGITIMA TEXTIL\EXTRAIDOS AUTOMATICO\NOVA EXTRACAO\OXFORD DE NATAL P025\Fotos'

for img in os.listdir(folder):
    if 'desktop.ini' in img:
        continue
    path = os.path.join(folder, img)
    croped_img(path)