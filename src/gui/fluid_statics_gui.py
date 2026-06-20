import customtkinter as ctk
from tkinter import messagebox
import numpy as np
import math
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.engines.fluid_statics_engine import FluidStaticsEngine

# ===========================
#   THEME CONSTANTS & SETUP
# ===========================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG_MAIN        = "#020817"   
BG_SIDEBAR     = "#020617"   
BG_CARD        = "#0a1128"   
CARD_BORDER    = "#1e293b"
ACCENT         = "#0ea5e9"   
ACCENT_HOVER   = "#22d3ee"
TEXT_MAIN      = "#f8fafc"
TEXT_SUB       = "#94a3b8"
WATER_COLOR    = "#0369a1"

FLUID_DB = {
    "Water (20°C)": {"rho": 998, "viscosity": "1.00 mPa·s"}, 
    "Seawater": {"rho": 1025, "viscosity": "1.08 mPa·s"},
    "Glycerin": {"rho": 1260, "viscosity": "1490 mPa·s"},
    "Mercury": {"rho": 13600, "viscosity": "1.53 mPa·s"},
}

class FluidStaticsApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("FLUID STATICS STUDIO - Advanced Lab Edition")
        self.geometry("1250x800")
        self.minsize(1150, 700)
        self.configure(fg_color=BG_MAIN)

        self.fluid_var = ctk.StringVar(value="Water (20°C)")
        self.current_page = None

        self.canvas_pressure = None
        self.canvas_motion = None
        
        # متغیر برای انیمیشن موج
        self.wave_phase = 0.0

        self._build_ui()
        self.animate_waves()
    
    def _build_ui(self):
        # Sidebar
        self.sidebar = ctk.CTkFrame(self, fg_color=BG_SIDEBAR, width=250, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Content Area
        self.content = ctk.CTkFrame(self, fg_color=BG_MAIN, corner_radius=0)
        self.content.pack(side="right", fill="both", expand=True)

        self._build_sidebar_header()
        self._build_fluid_selector()
        self._build_navigation()

        self._build_header(self.content)
        self._build_pages_container(self.content)
        self._build_statusbar()

        self.pages = {}
        self._create_pages()
        self.show_page("home")

    def _build_sidebar_header(self):
        header = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        header.pack(fill="x", padx=16, pady=(25, 15))
        ctk.CTkLabel(header, text="HYDRODYNAMICS", text_color=ACCENT, font=("Segoe UI Black", 18), justify="left").pack(anchor="w")
        ctk.CTkLabel(header, text="LABORATORY V2.0", text_color=TEXT_SUB, font=("Segoe UI", 10, "bold"), justify="left").pack(anchor="w")

    def _build_fluid_selector(self):
        container = ctk.CTkFrame(self.sidebar, fg_color=BG_CARD, corner_radius=8, border_width=1, border_color=CARD_BORDER)
        container.pack(fill="x", padx=16, pady=(10, 20))
        
        ctk.CTkLabel(container, text="🧪 Active Fluid Media:", text_color=TEXT_SUB, font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=10, pady=(10, 2))
        
        self.combo_fluid = ctk.CTkComboBox(container, variable=self.fluid_var, values=list(FLUID_DB.keys()), 
                                           command=self.on_fluid_change, fg_color=BG_MAIN, border_color=ACCENT, button_color=ACCENT)
        self.combo_fluid.pack(fill="x", padx=10, pady=(0, 10))

    def _build_navigation(self):
        nav_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        nav_frame.pack(fill="both", expand=True, padx=10, pady=10)
           
        def add_nav(icon, text, page_key):
            btn = ctk.CTkButton(nav_frame, text=f"  {icon}   {text}", command=lambda k=page_key: self.show_page(k), 
                                fg_color="transparent", text_color=TEXT_SUB, hover_color=BG_CARD, anchor="w", 
                                font=("Segoe UI", 14, "bold"), corner_radius=6, height=40)
            btn.pack(fill="x", pady=4)
            return btn

        self.nav_buttons = {
            "home": add_nav("🏠", "Overview", "home"),
            "pressure": add_nav("💧", "Hydrostatic Pressure", "pressure"),
            "surfaces": add_nav("🌊", "Forces on Surfaces", "surfaces"),
            "buoyancy": add_nav("🚢", "Buoyancy & Stability", "buoyancy"),
            "motion": add_nav("🔄", "Rigid Body Motion", "motion"),
        }

    def _build_header(self, parent):
        self.header = ctk.CTkFrame(parent, fg_color=BG_MAIN, height=70, corner_radius=0)
        self.header.pack(fill="x", padx=20, pady=(20, 0))
        
        title_frame = ctk.CTkFrame(self.header, fg_color="transparent")
        title_frame.pack(side="left")
        ctk.CTkLabel(title_frame, text="Fluid Statics Control Center", font=("Segoe UI", 26, "bold"), text_color=TEXT_MAIN).pack(anchor="w")
        
        # Animated Wave Canvas
        self.wave_canvas = ctk.CTkCanvas(self.header, bg=BG_MAIN, highlightthickness=0, height=50)
        self.wave_canvas.pack(side="right", fill="x", expand=True, padx=(40, 0))
        self.wave_canvas.bind("<Configure>", lambda e: self.draw_wave())

    def draw_wave(self):
        self.wave_canvas.delete("wave")
        width = self.wave_canvas.winfo_width()
        height = self.wave_canvas.winfo_height()
        if width > 10 and height > 10:
            points = [(0, height)]
            for x in range(0, width, 10):
                # Sine wave math for fluid effect
                y = height/2 + (height/4) * math.sin(x * 0.03 + self.wave_phase)
                points.append((x, y))
            points.append((width, height))
            self.wave_canvas.create_polygon(points, fill=WATER_COLOR, tags="wave", smooth=True)

    def animate_waves(self):
        self.wave_phase += 0.15
        self.draw_wave()
        self.after(50, self.animate_waves) # 20 FPS animation

    def _build_pages_container(self, parent):
        self.pages_frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.pages_frame.pack(fill="both", expand=True, padx=20, pady=10)

    def _build_statusbar(self):
        status_frame = ctk.CTkFrame(self, fg_color=BG_SIDEBAR, corner_radius=0, height=35)
        status_frame.pack(fill="x", side="bottom")
        self.status_label = ctk.CTkLabel(status_frame, text="🟢 Status: Nominal. Ready for computation.", text_color=TEXT_SUB, font=("Consolas", 12))
        self.status_label.pack(side="left", padx=16, pady=6)

    def set_status(self, text):
        self.status_label.configure(text=f"🟢 {text}")

    def create_card(self, parent, title=None, subtitle=None):
        card = ctk.CTkFrame(parent, fg_color=BG_CARD, corner_radius=10, border_width=1, border_color=CARD_BORDER)
        card.pack(fill="x", pady=10, padx=5)
        
        inner_frame = ctk.CTkFrame(card, fg_color="transparent")
        inner_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        if title:
            ctk.CTkLabel(inner_frame, text=title, font=("Segoe UI", 18, "bold"), text_color=TEXT_MAIN).pack(anchor="w")
        if subtitle:
            ctk.CTkLabel(inner_frame, text=subtitle, font=("Consolas", 13, "italic"), text_color=ACCENT).pack(anchor="w", pady=(2, 15))
            
        content_frame = ctk.CTkFrame(inner_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True)
        return content_frame

    def create_entry(self, parent, label, unit="", row=None, column=0, trace_cmd=None):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        if row is not None:
            frame.grid(row=row, column=column, sticky="ew", padx=10, pady=10)
        else:
            frame.pack(fill="x", pady=8)
            
        frame.columnconfigure(1, weight=1)
        ctk.CTkLabel(frame, text=label, text_color=TEXT_MAIN, font=("Segoe UI", 13)).grid(row=0, column=0, sticky="w", padx=(0, 10))
        
        entry_var = ctk.StringVar()
        if trace_cmd:
            entry_var.trace_add("write", lambda *args: trace_cmd())

        entry = ctk.CTkEntry(frame, textvariable=entry_var, width=110, fg_color=BG_MAIN, border_color=CARD_BORDER, justify="center")
        entry.grid(row=0, column=1, sticky="ew", padx=(0, 10))
        
        if unit:
            ctk.CTkLabel(frame, text=unit, text_color=TEXT_SUB, font=("Segoe UI", 12)).grid(row=0, column=2, sticky="w")
        return entry_var, entry

    def create_action_button(self, parent, text, command, color=ACCENT, hover=ACCENT_HOVER):
        btn = ctk.CTkButton(parent, text=text, command=command, fg_color=color, hover_color=hover, font=("Segoe UI", 14, "bold"), text_color="#020617", corner_radius=6, height=40)
        btn.pack(side="left", padx=(0, 15), pady=15)
        return btn

    def _create_pages(self):
        self.pages["home"] = self._create_page_home()
        self.pages["pressure"] = self._create_page_pressure()
        self.pages["surfaces"] = self._create_page_surfaces()
        self.pages["buoyancy"] = self._create_page_buoyancy()
        self.pages["motion"] = self._create_page_motion()

    def _create_page_home(self):
        page = ctk.CTkFrame(self.pages_frame, fg_color="transparent")
        
        welcome_card = self.create_card(page, title="Welcome to the Fluid Statics Laboratory", subtitle="Select a module to begin simulation.")
        ctk.CTkLabel(welcome_card, text="This advanced tool provides real-time computation and visualization for hydrostatic pressures, forces on submerged bodies, buoyancy stability, and rigid body motion of fluids.", 
                     wraplength=800, justify="left", text_color=TEXT_SUB, font=("Segoe UI", 14)).pack(anchor="w", pady=(0, 20))

        # Fluid Properties Dashboard
        self.dashboard_frame = ctk.CTkFrame(page, fg_color="transparent")
        self.dashboard_frame.pack(fill="both", expand=True)
        
        self.lbl_dash_rho = self._build_stat_box(self.dashboard_frame, "Density (ρ)", "kg/m³", 0, 0)
        self.lbl_dash_gamma = self._build_stat_box(self.dashboard_frame, "Specific Weight (γ)", "N/m³", 0, 1)
        self.lbl_dash_visc = self._build_stat_box(self.dashboard_frame, "Viscosity (μ)", "mPa·s", 0, 2)
        
        return page

    def _build_stat_box(self, parent, title, unit, row, col):
        box = ctk.CTkFrame(parent, fg_color=BG_CARD, corner_radius=10, border_width=1, border_color=CARD_BORDER)
        box.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        parent.columnconfigure(col, weight=1)
        
        ctk.CTkLabel(box, text=title, text_color=TEXT_SUB, font=("Segoe UI", 14)).pack(pady=(15, 5))
        value_lbl = ctk.CTkLabel(box, text="--", text_color=ACCENT, font=("Consolas", 28, "bold"))
        value_lbl.pack(pady=(0, 5))
        ctk.CTkLabel(box, text=unit, text_color=TEXT_SUB, font=("Segoe UI", 12)).pack(pady=(0, 15))
        return value_lbl

    def _create_page_pressure(self):
        page = ctk.CTkFrame(self.pages_frame, fg_color="transparent")
        
        left_panel = ctk.CTkFrame(page, fg_color="transparent", width=420)
        left_panel.pack(side="left", fill="y")
        
        self.pressure_plot_frame = ctk.CTkFrame(page, fg_color=BG_CARD, corner_radius=10, border_width=1, border_color=CARD_BORDER)
        self.pressure_plot_frame.pack(side="right", fill="both", expand=True, padx=(15, 0), pady=10)

        ctrl_card = self.create_card(left_panel, title="Hydrostatic Pressure", subtitle="P = P0 + ρgh")
        
        # با استفاده از trace_cmd، نمودار با هر بار تایپ آپدیت می‌شود
        self.p_rho_var, _ = self.create_entry(ctrl_card, "Density (ρ)", "kg/m³", row=0, column=0, trace_cmd=self.safe_plot_pressure)
        self.p_h_var, _ = self.create_entry(ctrl_card, "Max Depth (h)", "m", row=1, column=0, trace_cmd=self.safe_plot_pressure)
        self.p_p0_var, _ = self.create_entry(ctrl_card, "Surface Pres. (P0)", "Pa", row=2, column=0, trace_cmd=self.safe_plot_pressure)
        
        self.p_h_var.set("10.0")
        self.p_p0_var.set("101325")

        self.res_p = ctk.CTkLabel(ctrl_card, text="P =  —", text_color=ACCENT, font=("Consolas", 18, "bold"))
        self.res_p.grid(row=3, column=0, sticky="w", pady=(25, 10), padx=10)
        
        return page

    def _create_page_surfaces(self):
        page = ctk.CTkFrame(self.pages_frame, fg_color="transparent")
        ctrl_card = self.create_card(page, title="Forces on Inclined Surfaces", subtitle="F = ρgh_c A   |   y_p = y_c + I_xc / (y_c A)")
        ctrl_card.columnconfigure(0, weight=1); ctrl_card.columnconfigure(1, weight=1)

        self.s_rho_var, _ = self.create_entry(ctrl_card, "Density (ρ)", "kg/m³", row=0, column=0, trace_cmd=self.safe_calc_surfaces)
        self.s_hc_var, _ = self.create_entry(ctrl_card, "Centroid Depth (h_c)", "m", row=0, column=1, trace_cmd=self.safe_calc_surfaces)
        self.s_A_var, _ = self.create_entry(ctrl_card, "Surface Area (A)", "m²", row=1, column=0, trace_cmd=self.safe_calc_surfaces)
        self.s_yc_var, _ = self.create_entry(ctrl_card, "Slant Dist. (y_c)", "m", row=1, column=1, trace_cmd=self.safe_calc_surfaces)
        self.s_Ixc_var, _ = self.create_entry(ctrl_card, "Area Inertia (I_xc)", "m⁴", row=2, column=0, trace_cmd=self.safe_calc_surfaces)

        # Result display
        res_frame = ctk.CTkFrame(ctrl_card, fg_color=BG_MAIN, corner_radius=8, border_width=1, border_color=CARD_BORDER)
        res_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(20, 0), padx=10)
        self.res_s = ctk.CTkLabel(res_frame, text="F_R = 0.00 N      y_R = 0.00 m", text_color=ACCENT, font=("Consolas", 18, "bold"))
        self.res_s.pack(pady=15)

        btn_frame = ctk.CTkFrame(ctrl_card, fg_color="transparent")
        btn_frame.grid(row=4, column=0, columnspan=2, sticky="w", pady=15, padx=10)
        self.create_action_button(btn_frame, "📐 Open Geometry Helper", self.open_geometry_helper, color="#10b981", hover="#34d399")
        return page

    def _create_page_buoyancy(self):
        page = ctk.CTkFrame(self.pages_frame, fg_color="transparent")
        ctrl_card = self.create_card(page, title="Buoyancy & Stability", subtitle="F_B = ρgV   |   GM = I/V - BG")
        ctrl_card.columnconfigure(0, weight=1); ctrl_card.columnconfigure(1, weight=1)

        self.b_rho_var, _ = self.create_entry(ctrl_card, "Fluid Density (ρ)", "kg/m³", row=0, column=0, trace_cmd=self.safe_calc_buoyancy)
        self.b_V_var, _ = self.create_entry(ctrl_card, "Submerged Vol (V)", "m³", row=0, column=1, trace_cmd=self.safe_calc_buoyancy)
        self.b_I_var, _ = self.create_entry(ctrl_card, "Surface Inertia (I)", "m⁴", row=1, column=0, trace_cmd=self.safe_calc_buoyancy)
        self.b_BG_var, _ = self.create_entry(ctrl_card, "Distance (BG)", "m", row=1, column=1, trace_cmd=self.safe_calc_buoyancy)

        res_frame = ctk.CTkFrame(ctrl_card, fg_color=BG_MAIN, corner_radius=8, border_width=1, border_color=CARD_BORDER)
        res_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(20, 0), padx=10)
        self.res_b = ctk.CTkLabel(res_frame, text="F_B = 0.00 N      GM = 0.00 m", text_color=ACCENT, font=("Consolas", 18, "bold"))
        self.res_b.pack(pady=15)
        
        return page

    def _create_page_motion(self):
        page = ctk.CTkFrame(self.pages_frame, fg_color="transparent")
        
        left_panel = ctk.CTkFrame(page, fg_color="transparent", width=420)
        left_panel.pack(side="left", fill="y")
        
        self.motion_plot_frame = ctk.CTkFrame(page, fg_color=BG_CARD, corner_radius=10, border_width=1, border_color=CARD_BORDER)
        self.motion_plot_frame.pack(side="right", fill="both", expand=True, padx=(15, 0), pady=10)

        ctrl_card = self.create_card(left_panel, title="Rigid Body Motion", subtitle="tan(θ) = a_x/g  |  z = (ω²r²)/2g")

        self.m_ax_var, _ = self.create_entry(ctrl_card, "Linear Accel (a_x)", "m/s²", row=0, column=0, trace_cmd=self.safe_plot_motion)
        self.m_omega_var, _ = self.create_entry(ctrl_card, "Angular Vel (ω)", "rad/s", row=1, column=0, trace_cmd=self.safe_plot_motion)
        self.m_r_var, _ = self.create_entry(ctrl_card, "Tank Radius (r)", "m", row=2, column=0, trace_cmd=self.safe_plot_motion)
        
        self.m_ax_var.set("0.0")
        self.m_omega_var.set("5.0")
        self.m_r_var.set("1.0")

        res_frame = ctk.CTkFrame(ctrl_card, fg_color=BG_MAIN, corner_radius=8, border_width=1, border_color=CARD_BORDER)
        res_frame.grid(row=3, column=0, sticky="ew", pady=(25, 0), padx=10)
        self.res_m = ctk.CTkLabel(res_frame, text="θ = 0.00°\nMax z = 0.00 m", text_color=ACCENT, font=("Consolas", 16, "bold"), justify="left")
        self.res_m.pack(pady=15, padx=15, anchor="w")

        return page

    def show_page(self, key):
        if self.current_page is not None:
            self.pages[self.current_page].pack_forget()
        self.pages[key].pack(fill="both", expand=True)
        self.current_page = key
        
        for k, btn in self.nav_buttons.items():
            if k == key:
                btn.configure(fg_color=BG_CARD, text_color=ACCENT, border_width=1, border_color=CARD_BORDER)
            else:
                btn.configure(fg_color="transparent", text_color=TEXT_SUB, border_width=0)
                
        self.set_status(f"Active Module: {key.capitalize()}")

    def on_fluid_change(self, value):
        fluid = self.fluid_var.get()
        if fluid in FLUID_DB:
            rho = FLUID_DB[fluid]["rho"]
            visc = FLUID_DB[fluid]["viscosity"]
            gamma = rho * 9.81
            
            # Update Dashboard
            self.lbl_dash_rho.configure(text=f"{rho}")
            self.lbl_dash_gamma.configure(text=f"{gamma:,.0f}")
            self.lbl_dash_visc.configure(text=f"{visc}")

            # Update Inputs
            for var in [getattr(self, 'p_rho_var', None), getattr(self, 's_rho_var', None), getattr(self, 'b_rho_var', None)]:
                if var: var.set(str(rho))
                
        self.set_status(f"Fluid media updated to {fluid}")

    def _get_float(self, var):
        val = var.get()
        if not val or val == "." or val == "-": 
            return 0.0
        return float(val)

    # --- Safe Calculation Wrappers (For Real-Time Tracing) ---
    def safe_plot_pressure(self):
        try: self.plot_pressure_profile()
        except ValueError: pass

    def safe_calc_surfaces(self):
        try: self.calc_surfaces()
        except ValueError: pass

    def safe_calc_buoyancy(self):
        try: self.calc_buoyancy()
        except ValueError: pass

    def safe_plot_motion(self):
        try: self.plot_motion_3d()
        except ValueError: pass

    # --- Calculations & Plotting ---
    def plot_pressure_profile(self):
        P0 = self._get_float(self.p_p0_var)
        rho = self._get_float(self.p_rho_var)
        max_depth = self._get_float(self.p_h_var)
        
        if max_depth <= 0: return

        P_final = FluidStaticsEngine.calc_pressure(P0, rho, max_depth)
        self.res_p.configure(text=f"P = {P_final:,.2f} Pa")

        if self.canvas_pressure:
            self.canvas_pressure.get_tk_widget().destroy()

        g = 9.81
        h_values = np.linspace(0, max_depth, 50)
        p_values = P0 + (rho * g * h_values)

        fig = Figure(figsize=(5, 5), dpi=100, facecolor=BG_CARD)
        ax = fig.add_subplot(111)
        ax.set_facecolor(BG_MAIN)
        
        ax.plot(p_values, h_values, color=ACCENT, linewidth=3, label='Pressure Profile')
        ax.invert_yaxis()
        ax.fill_betweenx(h_values, P0, p_values, color=WATER_COLOR, alpha=0.4)
        
        ax.set_title('Hydrostatic Pressure Gradient', color=TEXT_MAIN, pad=15, fontweight='bold')
        ax.set_xlabel('Pressure $P$ (Pa)', color=TEXT_SUB)
        ax.set_ylabel('Depth $h$ (m)', color=TEXT_SUB)
        
        # Styling axes
        ax.spines['bottom'].set_color(CARD_BORDER)
        ax.spines['top'].set_color(CARD_BORDER)
        ax.spines['left'].set_color(CARD_BORDER)
        ax.spines['right'].set_color(CARD_BORDER)
        ax.tick_params(colors=TEXT_SUB)
        ax.grid(True, linestyle='--', color=CARD_BORDER, alpha=0.7)
        
        self.canvas_pressure = FigureCanvasTkAgg(fig, master=self.pressure_plot_frame)
        self.canvas_pressure.draw()
        self.canvas_pressure.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

    def calc_surfaces(self):
        rho = self._get_float(self.s_rho_var)
        h_c = self._get_float(self.s_hc_var)
        A = self._get_float(self.s_A_var)
        y_c = self._get_float(self.s_yc_var)
        I_xc = self._get_float(self.s_Ixc_var)

        if A == 0 or y_c == 0: return

        F_R = FluidStaticsEngine.calc_hydrostatic_force_plane(rho, h_c, A)
        y_R = FluidStaticsEngine.calc_center_of_pressure_y(y_c, A, I_xc)

        self.res_s.configure(text=f"F_R = {F_R:,.2f} N      y_R = {y_R:.4f} m")

    def calc_buoyancy(self):
        rho = self._get_float(self.b_rho_var)
        V = self._get_float(self.b_V_var)
        I = self._get_float(self.b_I_var)
        BG = self._get_float(self.b_BG_var)

        if V == 0: return

        FB, GM = FluidStaticsEngine.calc_buoyancy_and_stability(rho, V, I, BG)
        status = "✅ STABLE" if GM > 0 else "❌ UNSTABLE"
        color = "#10b981" if GM > 0 else "#ef4444"
        
        self.res_b.configure(text=f"F_B = {FB:,.2f} N      GM = {GM:.4f} m\n\nStatus: {status}", text_color=color)

    def plot_motion_3d(self):
        ax_lin = self._get_float(self.m_ax_var)
        omega = self._get_float(self.m_omega_var)
        R = self._get_float(self.m_r_var)
        
        if R <= 0: return

        theta, z_max = FluidStaticsEngine.calc_rigid_body_motion(ax_lin, omega, R)
        self.res_m.configure(text=f"Rotation Angle θ = {theta:.2f}°\nMax Paraboloid z = {z_max:.4f} m")

        if self.canvas_motion:
            self.canvas_motion.get_tk_widget().destroy()

        g = 9.81
        x = np.linspace(-R, R, 50)
        y = np.linspace(-R, R, 50)
        X, Y = np.meshgrid(x, y)
        
        R_mesh = np.sqrt(X**2 + Y**2)
        Z = (omega**2 * R_mesh**2) / (2 * g)
        Z[R_mesh > R] = np.nan

        fig = Figure(figsize=(5, 5), dpi=100, facecolor=BG_CARD)
        ax_3d = fig.add_subplot(111, projection='3d')
        ax_3d.set_facecolor(BG_CARD)
        
        surf = ax_3d.plot_surface(X, Y, Z, cmap='Blues_r', edgecolor='none', alpha=0.9)
        
        ax_3d.set_title(r'Free Surface Paraboloid ($z = \frac{\omega^2 r^2}{2g}$)', color=TEXT_MAIN, pad=15, fontweight='bold')
        ax_3d.set_xlabel('X Axis (m)', color=TEXT_SUB)
        ax_3d.set_ylabel('Y Axis (m)', color=TEXT_SUB)
        ax_3d.set_zlabel('Z Axis (m)', color=TEXT_SUB)
        
        ax_3d.tick_params(colors=TEXT_SUB)
        ax_3d.xaxis.pane.fill = False
        ax_3d.yaxis.pane.fill = False
        ax_3d.zaxis.pane.fill = False
        ax_3d.xaxis.pane.set_edgecolor(CARD_BORDER)
        ax_3d.yaxis.pane.set_edgecolor(CARD_BORDER)
        ax_3d.zaxis.pane.set_edgecolor(CARD_BORDER)

        self.canvas_motion = FigureCanvasTkAgg(fig, master=self.motion_plot_frame)
        self.canvas_motion.draw()
        self.canvas_motion.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

    def open_geometry_helper(self):
        helper = ctk.CTkToplevel(self)
        helper.title("Geometry Calculator")
        helper.geometry("350x400")
        helper.attributes("-topmost", True)
        helper.configure(fg_color=BG_MAIN)
        
        ctk.CTkLabel(helper, text="Select Section Profile:", text_color=TEXT_MAIN, font=("Segoe UI", 14, "bold")).pack(pady=(20, 10))
        
        shape_var = ctk.StringVar(value="Rectangle")
        shapes = ["Rectangle", "Circle", "Triangle"]
        ctk.CTkComboBox(helper, variable=shape_var, values=shapes, fg_color=BG_CARD, border_color=CARD_BORDER).pack(pady=5)
        
        dim1_var, _ = self.create_entry(helper, "Base / Diameter (m):", row=None)
        dim2_var, _ = self.create_entry(helper, "Height (m):", row=None)
        
        def calculate_geometry():
            try:
                shape = shape_var.get()
                d1 = float(dim1_var.get() or 0)
                d2 = float(dim2_var.get() or 0)
                
                A, I_xc = 0, 0
                
                if shape == "Rectangle":
                    A = d1 * d2
                    I_xc = (d1 * d2**3) / 12
                elif shape == "Circle":
                    A = (np.pi * d1**2) / 4
                    I_xc = (np.pi * d1**4) / 64
                elif shape == "Triangle":
                    A = (d1 * d2) / 2
                    I_xc = (d1 * d2**3) / 36
                
                self.s_A_var.set(f"{A:.4f}")
                self.s_Ixc_var.set(f"{I_xc:.6f}")
                
                helper.destroy()
                self.set_status(f"Imported calculated properties for {shape}")
                
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric dimensions.", parent=helper)

        ctk.CTkButton(helper, text="Calculate & Apply", command=calculate_geometry, fg_color=ACCENT, font=("Segoe UI", 14, "bold")).pack(pady=25)

if __name__ == "__main__":
    app = FluidStaticsApp()
    app.on_fluid_change(app.fluid_var.get())
    app.mainloop()
