import customtkinter as ctk
from tkinter import Canvas
import math

class SplashScreen(ctk.CTkToplevel):
    """Modern animated splash screen for Fluid Mechanics Calculator"""
    
    def __init__(self, parent, on_complete=None):
        super().__init__(parent)
        self.on_complete = on_complete
        
        # Window Configuration
        self.title("")
        self.geometry("600x400")
        self.resizable(False, False)
        
        # Remove window decorations
        self.overrideredirect(True)
        
        # Center the window
        self.update_idletasks()
        width = 600
        height = 400
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
        # Set dark background
        self.configure(fg_color="#0a0e1a")
        
        # Progress tracking
        self.progress = 0
        self.animation_step = 0
        
        self._create_ui()
        self._animate()
    
    def _create_ui(self):
        """Create splash screen UI elements"""
        
        # Main container
        container = ctk.CTkFrame(self, fg_color="#141b2d", corner_radius=20, border_width=2, border_color="#00d4ff")
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # App icon/logo area
        icon_frame = ctk.CTkFrame(container, fg_color="transparent")
        icon_frame.pack(pady=(40, 20))
        
        # Large emoji icon
        icon_label = ctk.CTkLabel(
            icon_frame,
            text="🌊",
            font=("Segoe UI", 80)
        )
        icon_label.pack()
        
        # App title
        title_label = ctk.CTkLabel(
            container,
            text="Fluid Mechanics Calculator",
            font=("Segoe UI", 28, "bold"),
            text_color="#ffffff"
        )
        title_label.pack(pady=(0, 5))
        
        # Version
        version_label = ctk.CTkLabel(
            container,
            text="Version 1.1",
            font=("Segoe UI", 14),
            text_color="#00d4ff"
        )
        version_label.pack(pady=(0, 30))
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            container,
            width=400,
            height=8,
            corner_radius=4,
            fg_color="#1a2332",
            progress_color="#00d4ff"
        )
        self.progress_bar.pack(pady=(0, 15))
        self.progress_bar.set(0)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            container,
            text="Initializing...",
            font=("Segoe UI", 12),
            text_color="#8b95a8"
        )
        self.status_label.pack(pady=(0, 20))
        
        # Developer info
        dev_label = ctk.CTkLabel(
            container,
            text="Developed by Savan Mohebbi • AUT Civil Engineering",
            font=("Segoe UI", 10),
            text_color="#64748b"
        )
        dev_label.pack(side="bottom", pady=(0, 20))
    
    def _animate(self):
        """Animate the splash screen"""
        if self.progress < 1.0:
            # Update progress
            self.progress += 0.02
            self.progress_bar.set(self.progress)
            
            # Update status text based on progress
            if self.progress < 0.3:
                self.status_label.configure(text="Loading modules...")
            elif self.progress < 0.6:
                self.status_label.configure(text="Initializing calculation engines...")
            elif self.progress < 0.9:
                self.status_label.configure(text="Setting up interface...")
            else:
                self.status_label.configure(text="Ready to launch!")
            
            # Continue animation
            self.after(50, self._animate)
        else:
            # Animation complete - close splash and notify the owner without blocking mainloop.
            self.after(500, self._finish)

    def _finish(self):
        if self.winfo_exists():
            self.destroy()
        if self.on_complete:
            self.on_complete()
    
    def show(self):
        """Show the splash screen"""
        self.grab_set()
        self.focus_set()


def show_splash(parent, duration=2500, on_complete=None):
    """Show splash screen for specified duration without blocking the Tk event loop."""
    splash = SplashScreen(parent, on_complete=on_complete)
    parent.after(duration, splash._finish)
    return splash
