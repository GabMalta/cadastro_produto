from search_inspirations.search_images import search_images
from search_inspirations.interface_download import ImageSelectorApp
import tkinter as tk


if __name__ == "__main__":
    query = "Damask Liturgico"
    image_urls = search_images(query, 20)

    root = tk.Tk()
    app = ImageSelectorApp(root, image_urls)
    root.mainloop()