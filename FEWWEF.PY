import os, re
from apps.data_scraping.import_images import create_covers

path = r'D:\SITE LEGITIMA TEXTIL\EXTRAIDOS AUTOMATICO\NOVA EXTRACAO\TEMP_GM'

pastas = os.listdir(path)

for pasta in pastas:
    path_folder = os.path.join(path, pasta)
    cover_path = os.path.join(path_folder, 'Capa')
    pictures_path = os.path.join(path_folder, 'Fotos')
    
    for i, capa in enumerate(os.listdir(cover_path)):
        capa_path = os.path.join(cover_path, capa)
        
        new_capa = capa.replace(str(i), str(i + 5))
        new_capa_path = os.path.join(cover_path, new_capa)
        
        os.rename(capa_path, new_capa_path)
    
    