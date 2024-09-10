import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests, os
from io import BytesIO

class ImageSelectorApp:
    def __init__(self, root, image_urls):
        self.root = root
        self.image_urls = image_urls
        self.selected_images = []
        self.create_ui()
    
    def create_ui(self):
        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack()

        self.images = []
        self.checkbuttons = []
        self.vars = []

        for i, url in enumerate(self.image_urls):
            response = requests.get(url)
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            img.thumbnail((100, 100), Image.Resampling.LANCZOS)
            self.images.append(ImageTk.PhotoImage(img))
            
            var = tk.IntVar()
            chk = tk.Checkbutton(self.root, image=self.images[i], variable=var)
            self.canvas.create_window((i % 5) * 150 + 50, (i // 5) * 150 + 50, window=chk)
            
            self.vars.append(var)
            self.checkbuttons.append(chk)
        
        self.download_button = tk.Button(self.root, text="Download Selected Images", command=self.download_selected_images)
        self.canvas.create_window(400, 550, window=self.download_button)
    
    def download_selected_images(self):
        selected_urls = [self.image_urls[i] for i, var in enumerate(self.vars) if var.get() == 1]
        
        if not selected_urls:
            messagebox.showinfo("No Selection", "No images selected for download.")
            return

        for url in selected_urls:
            self.download_image(url)
        
        messagebox.showinfo("Success", "Selected images downloaded successfully.")

    def download_image(self, url):
        response = requests.get(url)
        img_data = response.content
        img_name = os.path.basename(url.split("?")[0])
        with open(img_name, 'wb') as img_file:
            img_file.write(img_data)