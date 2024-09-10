from PIL import Image, ImageDraw, ImageFont
import os, random

class CoverPicture():
    
    def __init__(self, path_pictures:str, path_cover:str, size_cover:tuple=(1280,1280)):
        self.path_pictures = path_pictures
        self.path_cover = path_cover
        self.size_cover = size_cover
        
        if not os.path.exists(self.path_cover):
            os.mkdir(self.path_cover)
            
    def get_pictures(self):
        pictures = []
        for picture in os.listdir(self.path_pictures):
            if 'desktop.ini' in picture or '.json' in picture:
                continue
            
            pictures.append(os.path.join(self.path_pictures, picture))
        return pictures
            
    def get_len_path_pictures(self):
        self.len_path_pictures = len(os.listdir(self.path_pictures))
        return self.len_path_pictures
    
    def get_size_images(self, cover_width, cover_height, number_of_images):
        width = int((cover_width - 10) / (number_of_images / 2))
        height = int((cover_height - 10) / (number_of_images / 2))
        return (width, height)
        
    
    def set_size_images(self, number_of_images):
        
        if number_of_images > self.get_len_path_pictures():
            print('Número de imagens definido é maior que o número de imagens na pasta, será usado o número de imagens na pasta')
            number_of_images = self.len_path_pictures
        
        image_sizes = self.get_size_images(*self.size_cover, number_of_images)
        
        return image_sizes
    
    def compose_cover(self, name_saved, cover_title=None, number_of_images=4, max_letters=16, letter_color='#5DC1B9', font_color='#050A30'):
        
        images_size = self.set_size_images(number_of_images)
        positions = [(0,0), (640,0), (0,640), (640,640)]
        pictures = self.get_pictures()
        pictures_random = random.sample(pictures, 4 if len(pictures) > 4 else len(pictures))
        background = Image.new('RGB', self.size_cover)
        
        for i, picture in enumerate(pictures_random):
            img = Image.open(picture).resize(images_size)
            background.paste(img, positions[i])
        
        if cover_title:
            self.write_cover_title(name_saved, cover_title, background, max_letters, letter_color, font_color)
        else:
            background.save(os.path.join(self.path_cover, f'{name_saved}.jpg'))
    
    def write_cover_title(self, name_saved, cover_title:str, background_image: Image.Image | str, max_letters=16, letter_color='#5DC1B9', font_color='#050A30'):
        if type(background_image) != Image.Image:
            background_image = Image.open(background_image)
        
        draw = ImageDraw.Draw(background_image)
        font = ImageFont.truetype("impact.ttf",size=110)
        
        draw.rectangle((200,490,1067,795), fill=letter_color, outline= '#0000') # -> LEGITIMA
        draw.text((640, 640),cover_title, fill=font_color, font=font, align='center', stroke_fill='white', stroke_width=3, anchor='mm',)
        
        background_image.save(os.path.join(self.path_cover, f'{name_saved}.jpg'))
    
    def line_break(self, title, max_letters=16):

        title = title.split()
        
        i = 0
        ln1 = ''
        while True:
            ln1 = f'{ln1} {title[i]}'
            
            if len(ln1) < max_letters:
                if (len(ln1) + len(title[i+1]) > 16):
                    ln2 = f'{' '.join(title[i+1:])}'
                    title = f'{ln1}\n{ln2}'
                    return title
            i+=1


