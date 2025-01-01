import tkinter as tk
from tkinter import ttk

class ToolBar:
    def __init__(self, master, callback):
        self.frame = ttk.Frame(master)
        self.frame.pack(fill=tk.X, padx=5, pady=2)
        self.callback = callback
        
        # Create tooltips manager
        self.tooltip = ToolTip()
        
        # Create controls
        self.create_adjustment_controls()

    def create_adjustment_controls(self):
        # Brightness control
        brightness_frame = ttk.LabelFrame(self.frame, text="Яскравість")
        brightness_frame.pack(side=tk.LEFT, padx=5)
        self.brightness_scale = ttk.Scale(
            brightness_frame,
            from_=-100,
            to=100,
            orient=tk.HORIZONTAL,
            command=lambda v: self.callback("brightness", v)
        )
        self.brightness_scale.pack(padx=5, pady=5)
        self.tooltip.bind_tooltip(brightness_frame, "Регулювання яскравості зображення")
        
        # Contrast control
        contrast_frame = ttk.LabelFrame(self.frame, text="Контраст")
        contrast_frame.pack(side=tk.LEFT, padx=5)
        self.contrast_scale = ttk.Scale(
            contrast_frame,
            from_=-100,
            to=100,
            orient=tk.HORIZONTAL,
            command=lambda v: self.callback("contrast", v)
        )
        self.contrast_scale.pack(padx=5, pady=5)
        self.tooltip.bind_tooltip(contrast_frame, "Регулювання контрасту зображення")
        
        # RGB controls
        rgb_frame = ttk.LabelFrame(self.frame, text="RGB Корекція")
        rgb_frame.pack(side=tk.LEFT, padx=5)
        
        # Red channel
        self.red_scale = ttk.Scale(
            rgb_frame,
            from_=-100,
            to=100,
            orient=tk.HORIZONTAL,
            command=lambda v: self.callback("red", v)
        )
        ttk.Label(rgb_frame, text="R").pack(side=tk.LEFT, padx=2)
        self.red_scale.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Green channel
        self.green_scale = ttk.Scale(
            rgb_frame,
            from_=-100,
            to=100,
            orient=tk.HORIZONTAL,
            command=lambda v: self.callback("green", v)
        )
        ttk.Label(rgb_frame, text="G").pack(side=tk.LEFT, padx=2)
        self.green_scale.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Blue channel
        self.blue_scale = ttk.Scale(
            rgb_frame,
            from_=-100,
            to=100,
            orient=tk.HORIZONTAL,
            command=lambda v: self.callback("blue", v)
        )
        ttk.Label(rgb_frame, text="B").pack(side=tk.LEFT, padx=2)
        self.blue_scale.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.tooltip.bind_tooltip(rgb_frame, "Регулювання RGB компонент")

    def reset_controls(self):
        self.brightness_scale.set(0)
        self.contrast_scale.set(0)
        self.red_scale.set(0)
        self.green_scale.set(0)
        self.blue_scale.set(0)

class ToolTip:
    def __init__(self):
        self.tooltip_window = None
        self.widget_id = None

    def bind_tooltip(self, widget, text):
        widget.bind('<Enter>', lambda e: self.show_tooltip(e, text))
        widget.bind('<Leave>', self.hide_tooltip)

    def show_tooltip(self, event, text):
        x, y, _, _ = event.widget.bbox("insert")
        x += event.widget.winfo_rootx() + 25
        y += event.widget.winfo_rooty() + 20
        
        self.tooltip_window = tk.Toplevel(event.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        
        label = ttk.Label(self.tooltip_window, text=text, background="#ffffe0",
                         relief='solid', borderwidth=1)
        label.pack()

    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None
