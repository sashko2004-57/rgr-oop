import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageEnhance
import numpy as np

class ImageViewer:
    def __init__(self, master):
        # Create main frame with scrollbars
        self.main_frame = ttk.Frame(master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create canvas and scrollbars
        self.canvas = tk.Canvas(self.main_frame)
        self.h_scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.v_scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        
        # Configure canvas
        self.canvas.configure(xscrollcommand=self.h_scrollbar.set, yscrollcommand=self.v_scrollbar.set)
        
        # Grid layout
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.h_scrollbar.grid(row=1, column=0, sticky="ew")
        self.v_scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Configure grid weights
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Image attributes
        self.current_image = None
        self.original_image = None
        self.photo_image = None
        
        # Filter values
        self.filter_values = {
            'brightness': 0,
            'contrast': 0,
            'red': 0,
            'green': 0,
            'blue': 0
        }
        
        # Bind resize event
        self.canvas.bind('<Configure>', self.on_resize)

    def display_image(self, image):
        self.original_image = image
        self.apply_all_filters()

    def update_display(self):
        if self.current_image:
            # Convert PIL image to PhotoImage
            self.photo_image = ImageTk.PhotoImage(self.current_image)
            
            # Update canvas
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor="nw", image=self.photo_image)
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def apply_all_filters(self):
        if self.original_image:
            # Start with original image
            img = self.original_image.copy()
            
            # Apply brightness
            if self.filter_values['brightness'] != 0:
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(float(self.filter_values['brightness'])/100 + 1)
            
            # Apply contrast
            if self.filter_values['contrast'] != 0:
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(float(self.filter_values['contrast'])/100 + 1)
            
            # Apply RGB adjustments if any are non-zero
            if any(self.filter_values[color] != 0 for color in ['red', 'green', 'blue']):
                img_array = np.array(img)
                
                # Adjust each channel
                for channel, idx in {'red': 0, 'green': 1, 'blue': 2}.items():
                    if self.filter_values[channel] != 0:
                        adjustment = float(self.filter_values[channel]) / 100
                        img_array[:, :, idx] = np.clip(
                            img_array[:, :, idx] * (1 + adjustment),
                            0,
                            255
                        ).astype(np.uint8)
                
                img = Image.fromarray(img_array)
            
            self.current_image = img
            self.update_display()

    def adjust_brightness(self, value):
        self.filter_values['brightness'] = float(value)
        self.apply_all_filters()

    def adjust_contrast(self, value):
        self.filter_values['contrast'] = float(value)
        self.apply_all_filters()

    def adjust_color(self, channel, value):
        channel_map = {'R': 'red', 'G': 'green', 'B': 'blue'}
        self.filter_values[channel_map[channel]] = float(value)
        self.apply_all_filters()

    def on_resize(self, event):
        if self.current_image:
            self.update_display()

    def reset_filters(self):
        for key in self.filter_values:
            self.filter_values[key] = 0
        self.apply_all_filters()
