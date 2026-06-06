import customtkinter as ctk
import subprocess
import sys
import os


# =====================================================================
# PyInstaller Subprocess Interceptor (For .exe Compilation)
# =====================================================================
# این بخش بررسی میکند که آیا برنامه به صورت فایل اجرایی باز شده است یا خیر.
# اگر به عنوان یک پروسه فرزند باز شده باشد، ماژول درخواستی را اجرا میکند.
if getattr(sys, 'frozen', False) and len(sys.argv) > 1:
    script_name = sys.argv[1]
    base_dir = sys._MEIPASS # دایرکتوری موقت PyInstaller
    script_path = os.path.join(base_dir, script_name)
    
    if os.path.exists(script_path):
        import runpy
        # اجرای فایل پایتون به صورت اسکریپت مستقل در مموری
        runpy.run_path(script_path, run_name="__main__")
    sys.exit(0)
# =====================================================================

class MainDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Window Configuration
        self.title("Comprehensive Fluid Mechanics Software")
        self.geometry("800x650") 
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Grid Layout Configuration
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=3) # Space allocated for the 2x2 button matrix
        self.grid_rowconfigure(2, weight=1) # Space allocated for the footer
        self.grid_columnconfigure(0, weight=1)
        
        self._create_ui()

    def _create_ui(self):
        """Build the Graphical User Interface Elements"""
        # Main Title
        lbl_title = ctk.CTkLabel(
            self, 
            text="Fluid Mechanics Engineering Dashboard", 
            font=("Arial", 28, "bold")
        )
        lbl_title.grid(row=0, column=0, pady=(40, 10), sticky="s")
        
        # Subtitle
        lbl_subtitle = ctk.CTkLabel(
            self, 
            text="Please select a computational module to proceed:", 
            font=("Arial", 16),
            text_color="gray"
        )
        lbl_subtitle.grid(row=0, column=0, pady=(100, 0), sticky="n")

        # Buttons Matrix Frame (2x2 Grid)
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=1, column=0, sticky="nsew", padx=20)
        btn_frame.grid_columnconfigure((0, 1), weight=1)
        btn_frame.grid_rowconfigure((0, 1), weight=1)

        # 1. Fluid Properties (Chapter 1) - Top Left
        btn_properties = ctk.CTkButton(
            btn_frame, 
            text="Fluid Properties\n(Chapter 1)", 
            font=("Arial", 16, "bold"),
            width=260, 
            height=80,
            corner_radius=15,
            command=self.launch_properties_app
        )
        btn_properties.grid(row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="e")

        # 2. Fluid Statics (Chapter 2) - Top Right
        btn_statics = ctk.CTkButton(
            btn_frame, 
            text="Fluid Statics\n(Chapter 2)", 
            font=("Arial", 16, "bold"),
            width=260, 
            height=80,
            corner_radius=15,
            command=self.launch_statics_app
        )
        btn_statics.grid(row=0, column=1, padx=(10, 20), pady=(20, 10), sticky="w")

        # 3. Fluid Dynamics (Chapter 3) - Bottom Left
        btn_dynamics = ctk.CTkButton(
            btn_frame, 
            text="Fluid Dynamics\n(Chapter 3)", 
            font=("Arial", 16, "bold"),
            width=260, 
            height=80,
            corner_radius=15,
            command=self.launch_dynamics_app
        )
        btn_dynamics.grid(row=1, column=0, padx=(20, 10), pady=(10, 20), sticky="e")

        # 4. Dimensional Analysis (Chapter 4) - Bottom Right
        btn_dimensional = ctk.CTkButton(
            btn_frame, 
            text="Dimensional Analysis\n(Chapter 4)", 
            font=("Arial", 16, "bold"),
            width=260, 
            height=80,
            corner_radius=15,
            fg_color="#0ea5e9", 
            hover_color="#0284c7",
            command=self.launch_dimensional_app
        )
        btn_dimensional.grid(row=1, column=1, padx=(10, 20), pady=(10, 20), sticky="w")

        # --- Developer Information (Footer) ---
        footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        footer_frame.grid(row=2, column=0, sticky="s", pady=(0, 20))
        
        developer_info = (
            "Developer: Savan Mohebbi | Major: Civil Engineering\n"
            "Amirkabir University of Technology | Fluid Mechanics | Version: Beta 1.1"
        )
        
        lbl_footer = ctk.CTkLabel(
            footer_frame, 
            text=developer_info, 
            font=("Arial", 13),
            text_color="#888888",
            justify="center"
        )
        lbl_footer.pack()
    
    # ================== Module Launchers ==================

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
            # In .exe mode: Call itself (sys.executable) and pass the module name
            subprocess.Popen([sys.executable, file_path])
        else:
            # In standard Python mode
            if os.path.exists(file_path):
                subprocess.Popen([sys.executable, file_path])
            else:
                print(f"[Error] Module '{file_path}' not found in root directory.")

if __name__ == "__main__":
    app = MainDashboard()
    app.mainloop()
