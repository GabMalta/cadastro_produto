import json
import os
import random
from apps.data_scraping.create_covers import create_covers




path = r"D:\SITE LEGITIMA TEXTIL\CATÁLOGO DIGITAL\CREPE AMANDA D257"
cover_path = r"D:\SITE LEGITIMA TEXTIL\CATÁLOGO DIGITAL\CREPE AMANDA D257\Capa"


for i in range(1):
    create_covers(path, "CREPE AMANDA", upload_for_s3=False, create_img_info=True)
    
    input("PAUSA DRAMATICA")

        
    for arq in os.listdir(cover_path):
            path_remove = os.path.join(cover_path, arq)
            if os.path.isfile(path_remove):
                os.remove(path_remove)
