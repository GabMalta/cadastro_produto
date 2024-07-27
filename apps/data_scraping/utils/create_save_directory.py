import os

def create_save_directory(save_path, folder_name):
    save_path = os.path.join(save_path, folder_name)
    #CRIA OS DIRETORIOS NECESSARIOS CASO ELES NAO EXISTAM
    if (not os.path.exists(save_path)):
        os.mkdir(save_path)
        
        pictures_directory = fr"{save_path}\Fotos"
        cover_directory = fr"{save_path}\Capa"
        os.mkdir(cover_directory)
        os.mkdir(pictures_directory)
        
    pictures_directory = fr"{save_path}\Fotos"
    cover_directory = fr"{save_path}\Capa"
    
    if not os.path.exists(pictures_directory):
        os.mkdir(pictures_directory)
    
    if not os.path.exists(cover_directory):
        os.mkdir(cover_directory)
        
    return save_path