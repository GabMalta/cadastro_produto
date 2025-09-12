from PIL import Image
def path_is_image(path):

    try:
        with Image.open(path) as img:
            img.verify()
        return True

    except:
        return False
