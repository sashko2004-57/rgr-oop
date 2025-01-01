import tkinter as tk
from tkinter import ttk
from modules.viewer import ImageViewer
from modules.toolbar import ToolBar
from modules.files import FileHandler

class ImageProcessingApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Image Processing Application")
        
        # Create menu bar
        self.create_menu()
        
        # Create toolbar
        self.toolbar = ToolBar(self.root, self.handle_tool_action)
        
        # Create main viewer
        self.viewer = ImageViewer(self.root)
        
        # Create file handler
        self.file_handler = FileHandler()
        
        # Configure window
        self.root.geometry("800x600")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Відкрити...", command=self.open_image)
        file_menu.add_command(label="Зберегти", command=self.save_image)
        file_menu.add_command(label="Зберегти як...", command=self.save_image_as)
        file_menu.add_separator()
        file_menu.add_command(label="Вихід", command=self.on_closing)

    def open_image(self):
        image_path = self.file_handler.open_file()
        if image_path:
            image = self.file_handler.load_image(image_path)
            if image:
                self.viewer.display_image(image)

    def save_image(self):
        if self.viewer.current_image:
            self.file_handler.save_image(self.viewer.current_image)

    def save_image_as(self):
        if self.viewer.current_image:
            self.file_handler.save_image_as(self.viewer.current_image)

    def handle_tool_action(self, action, value=None):
        if self.viewer.current_image:
            if action == "brightness":
                self.viewer.adjust_brightness(value)
            elif action == "contrast":
                self.viewer.adjust_contrast(value)
            elif action == "red":
                self.viewer.adjust_color('R', value)
            elif action == "green":
                self.viewer.adjust_color('G', value)
            elif action == "blue":
                self.viewer.adjust_color('B', value)

    def on_closing(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ImageProcessingApp()
    app.run()
