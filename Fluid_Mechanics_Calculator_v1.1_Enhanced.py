import customtkinter as ctk
import subprocess
import sys
import os
from tkinter import messagebox


# =====================================================================
# PyInstaller Subprocess Interceptor (For .exe Compilation)
# =====================================================================
if getattr(sys, 'frozen', False) and len(sys.argv) > 1:
    script_name = sys.argv[1]
    base_dir = sys._MEIPASS
    script_path = os.path.join(base_dir, script_name)
    
    if os.path.exists(script_path):
        import runpy
        runpy.run_path(script_path, run_name="__main__")
    sys.exit(0)
# =====================================================================

# =====================================================================
# Splash Screen Class
# =====================================================================
class SplashScreen(ctk.CTkToplevel):
    """Modern animated splash screen"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("")
        self.geometry("600x400")
        self.resizable(False, False)
        self.overrideredirect(True)
        
        # Center window
        self.update_idletasks()
        width = 600
        height = 400
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
        self.configure(fg_color="#0a0e1a")
        self.progress = 0
        
        self._create_ui()
        self._animate()
    
    def _create_ui(self):
        container = ctk.CTkFrame(self, fg_color="#141b2d", corner_radius=20, border_width=2, border_color="#00d4ff")
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        icon_frame = ctk.CTkFrame(container, fg_color="transparent")
        icon_frame.pack(pady=(40, 20))
        
        icon_label = ctk.CTkLabel(icon_frame, text="🌊", font=("Segoe UI", 80))
        icon_label.pack()
        
        title_label = ctk.CTkLabel(container, text="Fluid Mechanics Calculator", 
                                    font=("Segoe UI", 28, "bold"), text_color="#ffffff")
        title_label.pack(pady=(0, 5))
        
        version_label = ctk.CTkLabel(container, text="Version 1.1", 
                                      font=("Segoe UI", 14), text_color="#00d4ff")
        version_label.pack(pady=(0, 30))
        
        self.progress_bar = ctk.CTkProgressBar(container, width=400, height=8, corner_radius=4,
                                                fg_color="#1a2332", progress_color="#00d4ff")
        self.progress_bar.pack(pady=(0, 15))
        self.progress_bar.set(0)
        
        self.status_label = ctk.CTkLabel(container, text="Initializing...", 
                                          font=("Segoe UI", 12), text_color="#8b95a8")
        self.status_label.pack(pady=(0, 20))
        
        dev_label = ctk.CTkLabel(container, text="Developed by Savan Mohebbi • AUT Civil Engineering",
                                 font=("Segoe UI", 10), text_color="#64748b")
        dev_label.pack(side="bottom", pady=(0, 20))
    
    def _animate(self):
        if self.progress < 1.0:
            self.progress += 0.02
            self.progress_bar.set(self.progress)
            
            if self.progress < 0.3:
                self.status_label.configure(text="Loading modules...")
            elif self.progress < 0.6:
                self.status_label.configure(text="Initializing calculation engines...")
            elif self.progress < 0.9:
                self.status_label.configure(text="Setting up interface...")
            else:
                self.status_label.configure(text="Ready to launch!")
            
            self.after(50, self._animate)
        else:
            self.after(500, self.destroy)

# =====================================================================
# Enhanced Color Schemes for v1.1
# =====================================================================
THEMES = {
    "dark": {
        "bg_main": "#0a0e1a",
        "bg_secondary": "#141b2d",
        "bg_card": "#1a2332",
        "bg_hover": "#253047",
        "accent": "#00d4ff",
        "accent_hover": "#00b8e6",
        "text_main": "#ffffff",
        "text_secondary": "#8b95a8",
        "border": "#2a3548",
        "success": "#10b981",
        "warning": "#f59e0b",
        "error": "#ef4444"
    },
    "light": {
        "bg_main": "#f8fafc",
        "bg_secondary": "#ffffff",
        "bg_card": "#ffffff",
        "bg_hover": "#f1f5f9",
        "accent": "#0ea5e9",
        "accent_hover": "#0284c7",
        "text_main": "#0f172a",
        "text_secondary": "#64748b",
        "border": "#e2e8f0",
        "success": "#10b981",
        "warning": "#f59e0b",
        "error": "#ef4444"
    }
}

class MainDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Hide main window initially
        self.withdraw()
        
        # Show splash screen
        splash = SplashScreen(self)
        self.wait_window(splash)
        
        # Now show main window
        self.deiconify()
        
        # Application State
        self.current_theme = "dark"
        self.theme = THEMES[self.current_theme]
        
        # Window Configuration
        self.title("Fluid Mechanics Calculator - v1.1")
        self.geometry("900x750")
        self.minsize(850, 700)
        ctk.set_appearance_mode(self.current_theme)
        ctk.set_default_color_theme("blue")
        
        # Grid Layout Configuration
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)
        
        self._create_ui()

    def _create_ui(self):
        """Build Enhanced UI for v1.1"""
        self._create_header()
        self._create_main_content()
        self._create_footer()
    
    def _create_header(self):
        """Enhanced header with theme toggle and settings"""
        header_frame = ctk.CTkFrame(self, fg_color=self.theme["bg_secondary"], corner_radius=0, height=100)
        header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        header_frame.grid_propagate(False)
        
        left_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        left_frame.pack(side="left", padx=30, pady=20)
        
        title_label = ctk.CTkLabel(left_frame, text="🌊 Fluid Mechanics Calculator",
                                    font=("Segoe UI", 32, "bold"), text_color=self.theme["text_main"])
        title_label.pack(anchor="w")
        
        version_label = ctk.CTkLabel(left_frame, text="Professional Engineering Suite • Version 1.1",
                                      font=("Segoe UI", 13), text_color=self.theme["text_secondary"])
        version_label.pack(anchor="w", pady=(2, 0))
        
        right_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        right_frame.pack(side="right", padx=30, pady=20)
        
        theme_btn = ctk.CTkButton(right_frame, text="🌙" if self.current_theme == "dark" else "☀️",
                                   width=45, height=45, corner_radius=10, fg_color=self.theme["bg_card"],
                                   hover_color=self.theme["bg_hover"], font=("Segoe UI", 20),
                                   command=self.toggle_theme)
        theme_btn.pack(side="left", padx=5)
        
        about_btn = ctk.CTkButton(right_frame, text="ℹ️", width=45, height=45, corner_radius=10,
                                   fg_color=self.theme["bg_card"], hover_color=self.theme["bg_hover"],
                                   font=("Segoe UI", 20), command=self.show_about)
        about_btn.pack(side="left", padx=5)
    
    def _create_main_content(self):
        """Enhanced main content area with better card design"""
        content_frame = ctk.CTkFrame(self, fg_color=self.theme["bg_main"], corner_radius=0)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(0, weight=0)
        content_frame.grid_rowconfigure(1, weight=1)
        
        instruction_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        instruction_frame.grid(row=0, column=0, sticky="ew", padx=40, pady=(30, 20))
        
        instruction_label = ctk.CTkLabel(instruction_frame, text="Select a computational module to begin analysis:",
                                          font=("Segoe UI", 16), text_color=self.theme["text_secondary"])
        instruction_label.pack(anchor="w")

        btn_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        btn_frame.grid(row=1, column=0, sticky="nsew", padx=40, pady=(0, 30))
        btn_frame.grid_columnconfigure((0, 1), weight=1)
        btn_frame.grid_rowconfigure((0, 1), weight=1)

        modules = [
            {"title": "Fluid Properties", "chapter": "Chapter 1", "icon": "💧",
             "description": "Density, Viscosity, Surface Tension", "color": "#3b82f6",
             "command": self.launch_properties_app, "row": 0, "col": 0},
            {"title": "Fluid Statics", "chapter": "Chapter 2", "icon": "⚖️",
             "description": "Pressure, Buoyancy, Hydrostatics", "color": "#8b5cf6",
             "command": self.launch_statics_app, "row": 0, "col": 1},
            {"title": "Fluid Dynamics", "chapter": "Chapter 3", "icon": "🌀",
             "description": "Flow Analysis, Bernoulli, Energy", "color": "#10b981",
             "command": self.launch_dynamics_app, "row": 1, "col": 0},
            {"title": "Dimensional Analysis", "chapter": "Chapter 4", "icon": "📐",
             "description": "Similitude, Pi Theorem, Scaling", "color": "#f59e0b",
             "command": self.launch_dimensional_app, "row": 1, "col": 1}
        ]
        
        for module in modules:
            self._create_module_card(btn_frame, module)
    
    def _create_module_card(self, parent, module_data):
        """Create an enhanced, interactive module card"""
        card = ctk.CTkFrame(parent, fg_color=self.theme["bg_card"], corner_radius=15,
                             border_width=2, border_color=self.theme["border"])
        card.grid(row=module_data["row"], column=module_data["col"], padx=15, pady=15, sticky="nsew")
        
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=25, pady=25)
        
        top_frame = ctk.CTkFrame(inner, fg_color="transparent")
        top_frame.pack(fill="x", pady=(0, 15))
        
        icon_label = ctk.CTkLabel(top_frame, text=module_data["icon"], font=("Segoe UI", 40))
        icon_label.pack(side="left")
        
        chapter_label = ctk.CTkLabel(top_frame, text=module_data["chapter"],
                                       font=("Segoe UI", 11, "bold"), text_color=module_data["color"])
        chapter_label.pack(side="right", anchor="ne")
        
        title_label = ctk.CTkLabel(inner, text=module_data["title"], font=("Segoe UI", 20, "bold"),
                                    text_color=self.theme["text_main"], anchor="w")
        title_label.pack(fill="x", pady=(0, 8))
        
        desc_label = ctk.CTkLabel(inner, text=module_data["description"], font=("Segoe UI", 12),
                                   text_color=self.theme["text_secondary"], anchor="w")
        desc_label.pack(fill="x", pady=(0, 20))
        
        launch_btn = ctk.CTkButton(inner, text="Open Module →", font=("Segoe UI", 14, "bold"),
                                     fg_color=module_data["color"],
                                     hover_color=self._darken_color(module_data["color"]),
                                     height=45, corner_radius=10, command=module_data["command"])
        launch_btn.pack(fill="x")
        
        def on_enter(e):
            card.configure(border_color=module_data["color"])
        
        def on_leave(e):
            card.configure(border_color=self.theme["border"])
        
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        for widget in card.winfo_children():
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
    
    def _create_footer(self):
        """Enhanced footer with better styling"""
        footer_frame = ctk.CTkFrame(self, fg_color=self.theme["bg_secondary"], corner_radius=0, height=80)
        footer_frame.grid(row=2, column=0, sticky="ew", padx=0, pady=0)
        footer_frame.grid_propagate(False)
        
        left_info = ctk.CTkFrame(footer_frame, fg_color="transparent")
        left_info.pack(side="left", padx=30, pady=20)
        
        dev_label = ctk.CTkLabel(left_info, text="👨‍💻 Developer: Savan Mohebbi",
                                 font=("Segoe UI", 12, "bold"), text_color=self.theme["text_main"])
        dev_label.pack(anchor="w")
        
        uni_label = ctk.CTkLabel(left_info, text="🎓 Amirkabir University of Technology • Civil Engineering",
                                 font=("Segoe UI", 11), text_color=self.theme["text_secondary"])
        uni_label.pack(anchor="w")
        
        right_info = ctk.CTkFrame(footer_frame, fg_color="transparent")
        right_info.pack(side="right", padx=30, pady=20)
        
        status_label = ctk.CTkLabel(right_info, text="🟢 All Systems Operational",
                                     font=("Segoe UI", 11), text_color=self.theme["success"])
        status_label.pack(anchor="e")
    
    def _darken_color(self, hex_color, factor=0.8):
        """Darken a hex color by a factor"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        darkened = tuple(int(c * factor) for c in rgb)
        return '#%02x%02x%02x' % darkened
    
    def toggle_theme(self):
        """Toggle between dark and light themes"""
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        self.theme = THEMES[self.current_theme]
        ctk.set_appearance_mode(self.current_theme)
        
        for widget in self.winfo_children():
            widget.destroy()
        self._create_ui()
    
    def show_about(self):
        """Show about dialog"""
        about_text = """Fluid Mechanics Calculator v1.1
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

A comprehensive engineering tool for fluid mechanics 
analysis covering fundamental principles and advanced 
calculations.

Modules:
• Fluid Properties (Ch. 1)
• Fluid Statics (Ch. 2)  
• Fluid Dynamics (Ch. 3)
• Dimensional Analysis (Ch. 4)

Developer: Savan Mohebbi
Institution: Amirkabir University of Technology
Department: Civil Engineering
Course: Fluid Mechanics

© 2024-2025 All Rights Reserved"""
        
        messagebox.showinfo("About", about_text)
    
    def launch_properties_app(self):
        self._run_process("FLUID_PROPERTIES_GUI.py")

    def launch_statics_app(self):
        self._run_process("fluid_statics_gui.py")
        
    def launch_dynamics_app(self):
        self._run_process("fluid_dynamic_gui.py")

    def launch_dimensional_app(self):
        self._run_process("DIMENSIONAL_ANALYSIS_GUI.py")

    def _run_process(self, file_path: str):
        """Advanced execution method compatible with both .py and .exe"""
        if getattr(sys, 'frozen', False):
            subprocess.Popen([sys.executable, file_path])
        else:
            if os.path.exists(file_path):
                subprocess.Popen([sys.executable, file_path])
            else:
                messagebox.showerror("Error", f"Module '{file_path}' not found.")

if __name__ == "__main__":
    app = MainDashboard()
    app.mainloop()
