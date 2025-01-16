from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError
import os, random


class CoverProduct:
    

    def __init__(self, path, size_cover: int | float = 1280):
        
        if not isinstance(size_cover, (int,float)):
            raise ValueError("O Parametro size_cover deve ser um int ou float")
        
        self.path = path
        self.size_cover = self.int_round(size_cover)

    def set_paths_cover(self):
        self.path_images = os.path.join(self.path, "Fotos")
        self.path_save = os.path.join(self.path, "Capa")

        self.images = os.listdir(self.path_images)
      
        if 'desktop.ini' in self.images:
            self.images.remove('desktop.ini')
            
        for img in self.images:
            try:
                with Image.open(os.path.join(self.path_images, img)) as image:
                    image.verify()
            except (UnidentifiedImageError, FileNotFoundError):
                self.images.remove(img)
        
        self.len_path_images = len(self.images)

        if not os.path.exists(self.path_save):
            os.mkdir(self.path_save)

    def new_background(self, color=(255, 255, 255)):
        return Image.new("RGB", (self.size_cover, self.size_cover), color)
    
    def int_round(self, value):
        return int(round(value))
    
    def percent_of_size(self, percent):
        return self.int_round(self.size_cover * percent)

    def cover_grid(self, name_save):

        self.set_paths_cover()
        
        if self.len_path_images < 9:
            return print(
                "\nERROR: A PASTA FOTOS DEVE TER PELO MENOS 9 IMAGENS PARA SE CRIAR ESSE TIPO DE CAPA"
            )
        background = self.new_background()

        resize_value = self.percent_of_size(0.32421875)
        position_1 = 0
        position_2 = self.percent_of_size(0.33828125)
        position_3 = self.percent_of_size(0.67578125)

        positions_coord = [position_1, position_2, position_3]

        positions = [(x, y) for x in positions_coord for y in positions_coord]

        images = random.sample(self.images, 9)
            
        for i, picture in enumerate(images):

            path_img = os.path.join(self.path_images, picture)

            img_mask = Image.open(path_img).resize((resize_value, resize_value))

            background.paste(img_mask, positions[i])

            if i == 8:
                break

        cover_save = os.path.join(self.path_save, f'{name_save}.jpg')
        
        background.save(cover_save)
        return cover_save

    def cover_three(self, name_save):
        self.set_paths_cover()

        if self.len_path_images < 3:
            return print(
                "\nERROR: A PASTA FOTOS DEVE TER PELO MENOS 3 IMAGENS PARA SE CRIAR ESSE TIPO DE CAPA"
            )

        background = self.new_background()
        

        images = random.sample(self.images, 3)
        
        for i,img in enumerate(images):
            
            image = Image.open(os.path.join(self.path_images, img))
            
            size = self.percent_of_size(0.49296875)
            position = self.percent_of_size(0.50703125)
            
            match i:
                case 0:
                    props = {'resize': (size, self.size_cover), 'positions': (0, 0)}
                case 1:
                    props = {'resize': (size,size), 'positions': (position, position)}
                case 2:
                    props = {'resize': (size,size), 'positions': (position, 0)}
                
            
            image = image.resize(props['resize'])
            background.paste(image, props['positions'])
        
        cover_save = os.path.join(self.path_save, f'{name_save}.jpg')
        
        background.save(cover_save)
        return cover_save
            
    def cover_grid_2(self, name_save):
        self.set_paths_cover()

        if self.len_path_images < 5:
            return print(
                "\nERROR: A PASTA FOTOS DEVE TER PELO MENOS 3 IMAGENS PARA SE CRIAR ESSE TIPO DE CAPA"
            )

        background = self.new_background()
        

        images = random.sample(self.images, 5)
        
        for i,img in enumerate(images):
            
            image = Image.open(os.path.join(self.path_images, img))
            
            size_rectangle_h = (self.percent_of_size(0.7), self.percent_of_size(0.29375))
            size_rectangle_v = (self.percent_of_size(0.29375), self.percent_of_size(0.7))
            size_square = self.percent_of_size(0.4)
            size_square = (size_square, size_square)
            
            match i:
                case 0:
                    props = {"resize": size_rectangle_h, "positions": (0, 0)}
                case 1:
                    props = {"resize": size_rectangle_v, "positions": (0, self.percent_of_size(0.3))}
                case 2:
                    props = {"resize": size_rectangle_h, "positions": (self.percent_of_size(0.3), self.percent_of_size(0.70625))}
                case 3:
                    props = {"resize": size_rectangle_v, "positions": (self.percent_of_size(0.70625), 0)}
                case 4:
                    props = {"resize": size_square, "positions": (self.percent_of_size(0.3), self.percent_of_size(0.3))}
            
            image = image.resize(props['resize'])
            background.paste(image, props['positions'])
            
        
        cover_save = os.path.join(self.path_save, f'{name_save}.jpg')
        
        background.save(cover_save)
        return cover_save
    
    def cover_grid_3(self, name_save):
        self.set_paths_cover()

        if self.len_path_images < 6:
            return print(
                "\nERROR: A PASTA FOTOS DEVE TER PELO MENOS 6 IMAGENS PARA SE CRIAR ESSE TIPO DE CAPA"
            )

        background = self.new_background()
        

        images = random.sample(self.images, 6)
        
        for i,img in enumerate(images):
            image = Image.open(os.path.join(self.path_images, img))
            
            size_rectangle_v = (self.percent_of_size(0.2453125), self.percent_of_size(0.32265625))
            size_rectangle_h = (self.percent_of_size(0.4984375), self.percent_of_size(0.32265625))
            size_square = self.percent_of_size(0.4921875)
            size_square = (size_square, size_square)
            
            match i:
                case 0:
                    props = {'resize': size_rectangle_h, "positions": (0,0)}
                case 1:
                    props = {'resize': size_rectangle_h, "positions": (0,self.percent_of_size(0.67734375))}
                case 2:
                    props = {'resize': size_rectangle_v, "positions": (0,self.percent_of_size(0.3390625))}
                case 3:
                    props = {'resize': size_rectangle_v, "positions": (self.percent_of_size(0.253125),self.percent_of_size(0.3390625))}
                case 4:
                    props = {'resize': size_square, "positions": (self.percent_of_size(0.5078125),0)}
                case 5:
                    props = {'resize': size_square, "positions": (self.percent_of_size(0.5078125),self.percent_of_size(0.5078125))}

            image = image.resize(props['resize'])
            
            background.paste(image, props['positions'])
        
        cover_save = os.path.join(self.path_save, f'{name_save}.jpg')
        
        background.save(cover_save)
        return cover_save
