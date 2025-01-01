from tkinter import filedialog
from PIL import Image
import os

class FileHandler:
    def __init__(self):
        self.current_file = None
        self.file_types = [
            ("All supported formats", "*.bmp;*.jpg;*.jpeg;*.jp2;*.png;*.ico"),
            ("BMP files", "*.bmp"),
            ("JPEG files", "*.jpg;*.jpeg"),
            ("JPEG 2000 files", "*.jp2"),
            ("PNG files", "*.png"),
            ("ICO files", "*.ico"),
            ("PDF files", "*.pdf"),
            ("All files", "*.*")
        ]
        self.save_file_types = [
            ("BMP file", "*.bmp"),
            ("JPEG file", "*.jpg"),
            ("JPEG 2000 file", "*.jp2"),
            ("PNG file", "*.png"),
            ("ICO file", "*.ico"),
            ("PDF file", "*.pdf")
        ]

    def open_file(self):
        """Open file dialog and return selected file path"""
        filename = filedialog.askopenfilename(
            title="Відкрити зображення",
            filetypes=self.file_types
        )
        if filename:
            self.current_file = filename
            return filename
        return None

    def load_image(self, filepath):
        """Load image from file"""
        try:
            image = Image.open(filepath)
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            return image
        except Exception as e:
            print(f"Error loading image: {e}")
            return None

    def save_image(self, image):
        """Save image to current file"""
        if self.current_file:
            self._save_image_to_file(image, self.current_file)
        else:
            self.save_image_as(image)

    def save_image_as(self, image):
        """Save image with new filename"""
        filename = filedialog.asksaveasfilename(
            title="Зберегти зображення як",
            filetypes=self.save_file_types,
            defaultextension=".bmp"
        )
        if filename:
            self.current_file = filename
            self._save_image_to_file(image, filename)

    def _save_image_to_file(self, image, filepath):
        """Internal method to save image to file"""
        try:
            # Ensure the image is in RGB mode
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Get file extension
            ext = os.path.splitext(filepath)[1].lower()
            
            # Save based on format
            if ext == '.pdf':
                # For PDF, we need to handle it specially
                image.save(filepath, 'PDF', resolution=100.0)
            elif ext == '.jp2':
                # For JPEG 2000
                image.save(filepath, 'JPEG2000', quality_layers=[100])
            elif ext == '.jpg' or ext == '.jpeg':
                # For JPEG
                image.save(filepath, 'JPEG', quality=95)
            elif ext == '.png':
                # For PNG
                image.save(filepath, 'PNG')
            elif ext == '.ico':
                # For ICO, resize if too large
                max_size = 256
                if image.size[0] > max_size or image.size[1] > max_size:
                    image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                image.save(filepath, 'ICO')
            else:
                # For BMP and others, use default settings
                image.save(filepath, quality=100)
                
        except Exception as e:
            print(f"Error saving image: {e}")
            
    def get_supported_formats(self):
        """Return list of supported formats"""
        return [
            "BMP (24-bit)",
            "JPEG",
            "JPEG 2000",
            "PNG",
            "ICO",
            "PDF"
        ]
