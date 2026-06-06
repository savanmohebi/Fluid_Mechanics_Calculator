import math
import tkinter as tk
from tkinter import messagebox
import numpy as np
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# فراخوانی موتور محاسبات
import FLUID_PROPERTIES_ENGINE as fe

# ===========================
#   THEME CONFIGURATION
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
DANGER         = "#ef4444"
DANGER_HOVER   = "#f97373"

FLUID_DB = {
    "Water (20°C)": {"rho": 998, "mu": 1.002e-3, "sigma": 0.0736}, 
    "Engine Oil (40°C)": {"rho": 870, "mu": 0.27, "sigma": 0.035},
    "Glycerin": {"rho": 1260, "mu": 1.49, "sigma": 0.063},
    "Air (25°C)": {"rho": 1.184, "mu": 1.85e-5, "sigma": 0.0},
}

class FluidAppModernCTK(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("FLUIDPROP STUDIO – Advanced Fluid Mechanics Lab")
        self.geometry("1250x800")
        self.minsize(1150, 700)
        self.configure(fg_color=BG_MAIN)

        self.fluid_var = ctk.StringVar(value="Water (20°C)")
        self.current_page = None
        
        self.canvas_rotvisco = None
        self.wave_phase = 0.0

        self._build_ui()
        self.animate_waves()
    
    def _build_ui(self):
        # سایدبار
        self.sidebar = ctk.CTkFrame(self, fg_color=BG_SIDEBAR, width=260, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # بخش محتوا
        self.content = ctk.CTkFrame(self, fg_color=BG_MAIN, corner_radius=0)
        self.content.pack(side="right", fill="both", expand=True)

        self._build_sidebar_header()
        self._build_fluid_selector()
        self._build_navigation()
        self._build_sidebar_footer()

        self._build_header(self.content)
        self._build_pages_container(self.content)
        self._build_statusbar()

        self.pages = {}
        self._create_pages()
        self.show_page("home")

    def _build_sidebar_header(self):
        header = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        header.pack(fill="x", padx=16, pady=(25, 15))
        ctk.CTkLabel(header, text="FLUIDPROP STUDIO", text_color=ACCENT, font=("Segoe UI Black", 18), justify="left").pack(anchor="w")
        ctk.CTkLabel(header, text="LABORATORY V2.0", text_color=TEXT_SUB, font=("Segoe UI", 10, "bold"), justify="left").pack(anchor="w")

    def _build_fluid_selector(self):
        container = ctk.CTkFrame(self.sidebar, fg_color=BG_CARD, corner_radius=8, border_width=1, border_color=CARD_BORDER)
        container.pack(fill="x", padx=16, pady=(10, 20))
        
        ctk.CTkLabel(container, text="🧪 Active Fluid Media:", text_color=TEXT_SUB, font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=10, pady=(10, 2))
        
        self.combo_fluid = ctk.CTkComboBox(
            container, variable=self.fluid_var, values=list(FLUID_DB.keys()), 
            command=self.on_fluid_change, fg_color=BG_MAIN, border_color=ACCENT, button_color=ACCENT
        )
        self.combo_fluid.pack(fill="x", padx=10, pady=(0, 10))

    def _build_navigation(self):
        self.nav_frame = ctk.CTkScrollableFrame(self.sidebar, fg_color="transparent", scrollbar_button_color=BG_MAIN)
        self.nav_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
           
        self.nav_buttons = {}
        
        def add_nav(icon, text, page_key):
            btn = ctk.CTkButton(
                self.nav_frame, text=f"  {icon}   {text}", anchor="w", 
                fg_color="transparent", text_color=TEXT_SUB, hover_color=BG_CARD, 
                font=("Segoe UI", 13, "bold"), corner_radius=6, height=38,
                command=lambda k=page_key: self.show_page(k)
            )
            btn.pack(fill="x", pady=2)
            self.nav_buttons[page_key] = btn

        add_nav("🏠", "Dashboard / Overview", "home")
        add_nav("🌊", "Kinematic Viscosity", "kinematic")
        add_nav("💧", "Capillarity Dynamics", "capillary")
        add_nav("🔄", "Rotational Viscometer", "rotvisco")
        add_nav("⚙️", "Narrow Gap Shaft", "narrow_gap")
        add_nav("🎡", "Flywheel Experiment", "flywheel")
        add_nav("🗜️", "Compressibility", "compress")
        add_nav("💦", "Droplet Pressure", "droplet")

    def _build_sidebar_footer(self):
        footer = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        footer.pack(fill="x", side="bottom", padx=16, pady=15)
        ctk.CTkLabel(footer, text="FluidProp Studio v2.0\nInteractive Environment", font=("Segoe UI", 11), text_color=TEXT_SUB, justify="left").pack(anchor="w")

    def _build_header(self, parent):
        self.header = ctk.CTkFrame(parent, fg_color=BG_MAIN, height=70, corner_radius=0)
        self.header.pack(fill="x", padx=20, pady=(20, 0))
        
        title_frame = ctk.CTkFrame(self.header, fg_color="transparent")
        title_frame.pack(side="left")
        ctk.CTkLabel(title_frame, text="Fluid Property Lab", font=("Segoe UI", 26, "bold"), text_color=TEXT_MAIN).pack(anchor="w")
        self.lbl_fluid_badge = ctk.CTkLabel(title_frame, text=self._fluid_badge_text(), font=("Consolas", 11, "bold"), text_color=ACCENT_HOVER)
        self.lbl_fluid_badge.pack(anchor="w")
        
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
                y = height/2 + (height/4) * math.sin(x * 0.03 + self.wave_phase)
                points.append((x, y))
            points.append((width, height))
            self.wave_canvas.create_polygon(points, fill=WATER_COLOR, tags="wave", smooth=True)

    def animate_waves(self):
        self.wave_phase += 0.15
        self.draw_wave()
        self.after(50, self.animate_waves)

    def _fluid_badge_text(self):
        return f"ACTIVE FLUID: {self.fluid_var.get().upper()}"

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

    def create_action_button(self, parent, text, command, style="accent"):
        btn_color = DANGER if style == "danger" else ACCENT
        hover_col = DANGER_HOVER if style == "danger" else ACCENT_HOVER
        text_col = "#ffffff" if style == "danger" else "#020617"
        
        btn = ctk.CTkButton(
            parent, text=text, command=command, 
            fg_color=btn_color, hover_color=hover_col, 
            text_color=text_col, font=("Segoe UI", 14, "bold"),
            corner_radius=6, height=40
        )
        btn.pack(side="left", padx=(0, 15), pady=15)
        return btn

    def _create_pages(self):
        self.pages["home"] = self._create_page_home()
        self.pages["kinematic"] = self._create_page_kinematic()
        self.pages["capillary"] = self._create_page_capillary()
        self.pages["rotvisco"] = self._create_page_rot_viscometer()
        self.pages["narrow_gap"] = self._create_page_narrow_gap()
        self.pages["flywheel"] = self._create_page_flywheel()
        self.pages["compress"] = self._create_page_compressibility()
        self.pages["droplet"] = self._create_page_droplet()

    def _create_page_home(self):
        page = ctk.CTkFrame(self.pages_frame, fg_color="transparent")
        
        welcome_card = self.create_card(page, title="Welcome to FluidProp Studio", subtitle="Select a module to begin computation.")
        ctk.CTkLabel(welcome_card, text="This advanced tool provides real-time computation for fluid properties, viscosimetry, and surface phenomena.", 
                     wraplength=800, justify="left", text_color=TEXT_SUB, font=("Segoe UI", 14)).pack(anchor="w", pady=(0, 20))

        # Dashboard Stats
        self.dashboard_frame = ctk.CTkFrame(page, fg_color="transparent")
        self.dashboard_frame.pack(fill="both", expand=True)
        
        self.lbl_dash_rho = self._build_stat_box(self.dashboard_frame, "Density (ρ)", "kg/m³", 0, 0)
        self.lbl_dash_mu = self._build_stat_box(self.dashboard_frame, "Dynamic Viscosity (μ)", "Pa·s", 0, 1)
        self.lbl_dash_sigma = self._build_stat_box(self.dashboard_frame, "Surface Tension (σ)", "N/m", 0, 2)
        
        self.on_fluid_change() # Init stats
        return page

    def _build_stat_box(self, parent, title, unit, row, col):
        box = ctk.CTkFrame(parent, fg_color=BG_CARD, corner_radius=10, border_width=1, border_color=CARD_BORDER)
        box.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        parent.columnconfigure(col, weight=1)
        
        ctk.CTkLabel(box, text=title, text_color=TEXT_SUB, font=("Segoe UI", 14)).pack(pady=(15, 5))
        value_lbl = ctk.CTkLabel(box, text="--", text_color=ACCENT, font=("Consolas", 26, "bold"))
        value_lbl.pack(pady=(0, 5))
        ctk.CTkLabel(box, text=unit, text_color=TEXT_SUB, font=("Segoe UI", 12)).pack(pady=(0, 15))
        return value_lbl

    # ================== MODULE PAGES ==================
    def _create_page_kinematic(self):
        page = ctk.CTkFrame(self.pages_frame, fg_color="transparent")
        ctrl_card = self.create_card(page, title="Kinematic Viscosity Module", subtitle=r"\nu = \mu / \rho")
        ctrl_card.columnconfigure(0, weight=1); ctrl_card.columnconfigure(1, weight=1)

        self.mu_var, _ = self.create_entry(ctrl_card, "Dynamic viscosity (μ)", "Pa·s", row=0, column=0, trace_cmd=self.safe_calc_kinematic)
        self.rho_var, _ = self.create_entry(ctrl_card, "Density (ρ)", "kg/m³", row=0, column=1, trace_cmd=self.safe_calc_kinematic)

        self.result_kin_visco = ctk.CTkLabel(ctrl_card, text="ν =  —", text_color=ACCENT, font=("Consolas", 18, "bold"))
        self.result_kin_visco.grid(row=1, column=0, columnspan=2, sticky="w", pady=(25, 10), padx=10)
        return page

    def _create_page_capillary(self):
        page = ctk.CTkFrame(self.pages_frame, fg_color="transparent")
        ctrl_card = self.create_card(page, title="Capillarity Dynamics", subtitle=r"h = (2\sigma \cos\theta) / (\rho g R)")
        ctrl_card.columnconfigure(0, weight=1); ctrl_card.columnconfigure(1, weight=1)

        self.sigma_var, _ = self.create_entry(ctrl_card, "Surface tension (σ)", "N/m", row=0, column=0, trace_cmd=self.safe_calc_capillary)
        self.theta_var, _ = self.create_entry(ctrl_card, "Contact angle (θ)", "deg", row=0, column=1, trace_cmd=self.safe_calc_capillary)
        self.rho_cap_var, _ = self.create_entry(ctrl_card, "Density (ρ)", "kg/m³", row=1, column=0, trace_cmd=self.safe_calc_capillary)
        self.radius_var, _ = self.create_entry(ctrl_card, "Tube radius (R)", "m", row=1, column=1, trace_cmd=self.safe_calc_capillary)
        
        self.theta_var.set("0.0")
        self.radius_var.set("0.001")

        self.result_capillary = ctk.CTkLabel(ctrl_card, text="h =  —", text_color=ACCENT, font=("Consolas", 18, "bold"))
        self.result_capillary.grid(row=2, column=0, columnspan=2, sticky="w", pady=(25, 10), padx=10)
        return page

    def _create_page_rot_viscometer(self):
        page = ctk.CTkFrame(self.pages_frame, fg_color="transparent")
        
        left_panel = ctk.CTkFrame(page, fg_color="transparent", width=420)
        left_panel.pack(side="left", fill="y")
        
        self.rotvisco_plot_frame = ctk.CTkFrame(page, fg_color=BG_CARD, corner_radius=10, border_width=1, border_color=CARD_BORDER)
        self.rotvisco_plot_frame.pack(side="right", fill="both", expand=True, padx=(15, 0), pady=10)

        ctrl_card = self.create_card(left_panel, title="Rotational Viscometer", subtitle=r"T = 4\pi\mu L R_i^3 \omega / (R_o - R_i)")

        self.Ri_var, _ = self.create_entry(ctrl_card, "Inner radius (Rᵢ)", "m", row=0, column=0, trace_cmd=self.safe_plot_rotvisco)
        self.Ro_var, _ = self.create_entry(ctrl_card, "Outer radius (Rₒ)", "m", row=1, column=0, trace_cmd=self.safe_plot_rotvisco)
        self.Lcyl_var, _ = self.create_entry(ctrl_card, "Cyl length (L)", "m", row=2, column=0, trace_cmd=self.safe_plot_rotvisco)
        self.omega_var, _ = self.create_entry(ctrl_card, "Angular vel (ω)", "rad/s", row=3, column=0, trace_cmd=self.safe_plot_rotvisco)
        self.mu_rot_var, _ = self.create_entry(ctrl_card, "Viscosity (μ)", "Pa·s", row=4, column=0, trace_cmd=self.safe_plot_rotvisco)

        self.Ri_var.set("0.1")
        self.Ro_var.set("0.102")
        self.Lcyl_var.set("0.4")
        self.omega_var.set("10.0")

        self.result_rotvisco = ctk.CTkLabel(ctrl_card, text="T =  —\nP =  —", text_color=ACCENT, font=("Consolas", 16, "bold"), justify="left")
        self.result_rotvisco.grid(row=5, column=0, sticky="w", pady=(20, 10), padx=10)
        return page

    def _create_page_narrow_gap(self):
        page = ctk.CTkFrame(self.pages_frame, fg_color="transparent")
        ctrl_card = self.create_card(page, title="Narrow Gap Shaft", subtitle=r"T = (2\pi \mu R^3 \omega L) / t")
        ctrl_card.columnconfigure(0, weight=1); ctrl_card.columnconfigure(1, weight=1)

        self.ng_D_var, _ = self.create_entry(ctrl_card, "Shaft Diameter (D)", "m", row=0, column=0, trace_cmd=self.safe_calc_narrow_gap)
        self.ng_L_var, _ = self.create_entry(ctrl_card, "Shaft Length (L)", "m", row=0, column=1, trace_cmd=self.safe_calc_narrow_gap)
        self.ng_t_var, _ = self.create_entry(ctrl_card, "Gap Thickness (t)", "m", row=1, column=0, trace_cmd=self.safe_calc_narrow_gap)
        self.ng_rpm_var, _ = self.create_entry(ctrl_card, "Rotational Speed", "rpm", row=1, column=1, trace_cmd=self.safe_calc_narrow_gap)
        self.ng_mu_var, _ = self.create_entry(ctrl_card, "Dynamic Viscosity (μ)", "Pa·s", row=2, column=0, trace_cmd=self.safe_calc_narrow_gap)
        
        self.ng_pi_var, _ = self.create_entry(ctrl_card, "Custom π value", "", row=2, column=1, trace_cmd=self.safe_calc_narrow_gap)
        self.ng_pi_var.set(str(math.pi))
        
        self.ng_D_var.set("0.05")
        self.ng_L_var.set("0.2")
        self.ng_t_var.set("0.001")
        self.ng_rpm_var.set("1500")

        self.result_ng = ctk.CTkLabel(ctrl_card, text="T =  —\nP =  —", text_color=ACCENT, font=("Consolas", 16, "bold"), justify="left")
        self.result_ng.grid(row=3, column=0, columnspan=2, sticky="w", pady=(25, 10), padx=10)
        return page

    def _create_page_flywheel(self):
        page = ctk.CTkFrame(self.pages_frame, fg_color="transparent")
        ctrl_card = self.create_card(page, title="Flywheel Viscosity", subtitle=r"\mu \approx (4 c I \alpha) / (\pi d^3 L \omega_0)")
        ctrl_card.columnconfigure(0, weight=1); ctrl_card.columnconfigure(1, weight=1)

        self.W_var, _ = self.create_entry(ctrl_card, "Flywheel weight (W)", "N", row=0, column=0, trace_cmd=self.safe_calc_flywheel)
        self.k_var, _ = self.create_entry(ctrl_card, "Radius gyration (k)", "m", row=0, column=1, trace_cmd=self.safe_calc_flywheel)
        self.omega0_var, _ = self.create_entry(ctrl_card, "Initial speed (ω₀)", "rad/s", row=1, column=0, trace_cmd=self.safe_calc_flywheel)
        self.alpha_var, _ = self.create_entry(ctrl_card, "Deceleration (α)", "rad/s²", row=1, column=1, trace_cmd=self.safe_calc_flywheel)
        self.d_shaft_var, _ = self.create_entry(ctrl_card, "Shaft diameter (d)", "m", row=2, column=0, trace_cmd=self.safe_calc_flywheel)
        self.L_bearing_var, _ = self.create_entry(ctrl_card, "Bearing length (L)", "m", row=2, column=1, trace_cmd=self.safe_calc_flywheel)
        self.c_clearance_var, _ = self.create_entry(ctrl_card, "Radial clearance (c)", "m", row=3, column=0, trace_cmd=self.safe_calc_flywheel)

        self.result_flywheel = ctk.CTkLabel(ctrl_card, text="μ =  —", text_color=ACCENT, font=("Consolas", 18, "bold"))
        self.result_flywheel.grid(row=4, column=0, columnspan=2, sticky="w", pady=(25, 10), padx=10)
        return page

    def _create_page_compressibility(self):
        page = ctk.CTkFrame(self.pages_frame, fg_color="transparent")
        ctrl_card = self.create_card(page, title="Bulk Modulus", subtitle=r"\Delta P = K \times (\Delta V / V)")
        ctrl_card.columnconfigure(0, weight=1); ctrl_card.columnconfigure(1, weight=1)

        self.k_bulk_var, _ = self.create_entry(ctrl_card, "Bulk Modulus (K)", "GPa", row=0, column=0, trace_cmd=self.safe_calc_compress)
        self.vol_change_var, _ = self.create_entry(ctrl_card, "Vol Reduction (ΔV/V)", "%", row=0, column=1, trace_cmd=self.safe_calc_compress)

        self.k_bulk_var.set("2.2") # Water approx
        self.vol_change_var.set("1.0")

        self.result_compress = ctk.CTkLabel(ctrl_card, text="ΔP =  —", text_color=ACCENT, font=("Consolas", 18, "bold"))
        self.result_compress.grid(row=1, column=0, columnspan=2, sticky="w", pady=(25, 10), padx=10)
        return page

    def _create_page_droplet(self):
        page = ctk.CTkFrame(self.pages_frame, fg_color="transparent")
        ctrl_card = self.create_card(page, title="Droplet Pressure", subtitle=r"P_{in} = P_{out} + 4\sigma/D")
        ctrl_card.columnconfigure(0, weight=1); ctrl_card.columnconfigure(1, weight=1)

        self.droplet_d_var, _ = self.create_entry(ctrl_card, "Droplet Diameter (D)", "mm", row=0, column=0, trace_cmd=self.safe_calc_droplet)
        self.p_out_var, _ = self.create_entry(ctrl_card, "External Press (P_out)", "kPa", row=0, column=1, trace_cmd=self.safe_calc_droplet)

        self.droplet_d_var.set("2.0")
        self.p_out_var.set("101.325")

        self.result_droplet = ctk.CTkLabel(ctrl_card, text="P_in =  —", text_color=ACCENT, font=("Consolas", 18, "bold"))
        self.result_droplet.grid(row=1, column=0, columnspan=2, sticky="w", pady=(25, 10), padx=10)
        return page

    # ================== LOGIC AND ACTIONS ==================
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

        self.set_status(f"Active module: {key.capitalize()}")

    def _get_float(self, var):
        val = var.get()
        if not val or val in [".", "-"]: return 0.0
        return float(val)

    def on_fluid_change(self, event=None):
        fluid = self.fluid_var.get()
        if fluid in FLUID_DB:
            props = FLUID_DB[fluid]
            
            # Update Dashboard
            if hasattr(self, 'lbl_dash_rho'):
                self.lbl_dash_rho.configure(text=f"{props.get('rho', '--')}")
                self.lbl_dash_mu.configure(text=f"{props.get('mu', '--'):.2e}")
                self.lbl_dash_sigma.configure(text=f"{props.get('sigma', '--'):.4f}")

            # Update Inputs globally
            for var in [getattr(self, 'rho_var', None), getattr(self, 'rho_cap_var', None)]:
                if var: var.set(str(props.get("rho", "")))
            for var in [getattr(self, 'mu_var', None), getattr(self, 'mu_rot_var', None), getattr(self, 'ng_mu_var', None)]:
                if var: var.set(str(props.get("mu", "")))
            if hasattr(self, 'sigma_var'):
                self.sigma_var.set(str(props.get("sigma", "")))

        self.lbl_fluid_badge.configure(text=self._fluid_badge_text())
        self.set_status(f"Fluid changed to: {fluid}")

    # ================== SAFE CALC WRAPPERS (Real-Time Tracing) ==================
    def safe_calc_kinematic(self):
        try:
            mu = self._get_float(self.mu_var)
            rho = self._get_float(self.rho_var)
            if rho <= 0: return
            nu = fe.calc_kinematic_viscosity(mu, rho)
            self.result_kin_visco.configure(text=f"ν = {nu:.6e} m²/s")
        except Exception: pass

    def safe_calc_capillary(self):
        try:
            sigma = self._get_float(self.sigma_var)
            theta_deg = self._get_float(self.theta_var)
            rho = self._get_float(self.rho_cap_var)
            R = self._get_float(self.radius_var)
            if rho <= 0 or R <= 0: return
            h = fe.calc_capillarity(sigma, theta_deg, rho, R)
            self.result_capillary.configure(text=f"h = {h:.6e} m")
        except Exception: pass

    def safe_plot_rotvisco(self):
        try:
            Ri = self._get_float(self.Ri_var)
            Ro = self._get_float(self.Ro_var)
            L = self._get_float(self.Lcyl_var)
            omega = self._get_float(self.omega_var)
            mu = self._get_float(self.mu_rot_var)
            
            if Ro <= Ri or L <= 0: return
            T, P = fe.calc_rot_viscometer(Ri, Ro, L, omega, mu)
            self.result_rotvisco.configure(text=f"T = {T:.4e} N·m\nP = {P:.4e} W")
            
            # Update Plot
            if self.canvas_rotvisco:
                self.canvas_rotvisco.get_tk_widget().destroy()

            fig = Figure(figsize=(5, 5), dpi=100, facecolor=BG_CARD)
            ax = fig.add_subplot(111)
            ax.set_facecolor(BG_MAIN)

            omega_range = np.linspace(0, max(omega*2, 50), 100)
            T_range = (4 * np.pi * mu * L * (Ri**3) * omega_range) / (Ro - Ri)

            ax.plot(omega_range, T_range, color=ACCENT, linewidth=2)
            ax.scatter([omega], [T], color=DANGER, s=50, zorder=5) # highlight current point
            ax.set_xlabel(r"Angular Velocity $\omega$ (rad/s)", color=TEXT_SUB)
            ax.set_ylabel(r"Torque $T$ (N·m)", color=TEXT_SUB)
            ax.set_title("Torque Characteristic Curve", color=TEXT_MAIN, pad=15)
            
            ax.tick_params(colors=TEXT_SUB)
            ax.grid(True, linestyle="--", alpha=0.3, color=CARD_BORDER)
            for spine in ax.spines.values(): spine.set_edgecolor(CARD_BORDER)

            self.canvas_rotvisco = FigureCanvasTkAgg(fig, master=self.rotvisco_plot_frame)
            self.canvas_rotvisco.draw()
            self.canvas_rotvisco.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        except Exception: pass

    def safe_calc_narrow_gap(self):
        try:
            D = self._get_float(self.ng_D_var)
            L = self._get_float(self.ng_L_var)
            t = self._get_float(self.ng_t_var)
            rpm = self._get_float(self.ng_rpm_var)
            mu = self._get_float(self.ng_mu_var)
            pi_val = self._get_float(self.ng_pi_var)
            if t <= 0: return

            if hasattr(fe, 'calc_shaft_power_narrow_gap'):
                T, P = fe.calc_shaft_power_narrow_gap(D, L, t, rpm, mu, pi_val)
            else:
                omega = rpm * (2 * pi_val) / 60.0
                R = D / 2.0
                T = (2 * pi_val * mu * (R**3) * omega * L) / t
                P = T * omega

            self.result_ng.configure(text=f"T = {T:.4f} N·m\nP = {P:.4f} W")
        except Exception: pass

    def safe_calc_flywheel(self):
        try:
            W = self._get_float(self.W_var)
            k = self._get_float(self.k_var)
            omega0 = self._get_float(self.omega0_var)
            alpha = self._get_float(self.alpha_var)
            d = self._get_float(self.d_shaft_var)
            L = self._get_float(self.L_bearing_var)
            c = self._get_float(self.c_clearance_var)
            if d <= 0 or L <= 0 or omega0 <= 0: return
            mu = fe.calc_flywheel_viscosity(W, k, omega0, alpha, d, L, c)
            self.result_flywheel.configure(text=f"μ = {mu:.6e} Pa·s")
        except Exception: pass

    def safe_calc_compress(self):
        try:
            K_GPa = self._get_float(self.k_bulk_var)
            delta_v_percent = self._get_float(self.vol_change_var)
            K_Pa = K_GPa * 1e9
            delta_P_Pa = fe.calc_bulk_modulus_pressure(K_Pa, delta_v_percent)
            delta_P_MPa = delta_P_Pa / 1e6
            self.result_compress.configure(text=f"ΔP = {delta_P_MPa:.3f} MPa")
        except Exception: pass

    def safe_calc_droplet(self):
        try:
            D_mm = self._get_float(self.droplet_d_var)
            P_out_kPa = self._get_float(self.p_out_var)
            fluid_name = self.fluid_var.get()
            sigma = FLUID_DB.get(fluid_name, {}).get("sigma", 0.0)
            
            if D_mm <= 0: return
            D_m = D_mm / 1000.0
            P_out_Pa = P_out_kPa * 1000.0
            P_in_Pa = fe.calc_droplet_pressure(P_out_Pa, sigma, D_m)
            P_in_kPa = P_in_Pa / 1000.0
            self.result_droplet.configure(text=f"P_in = {P_in_kPa:.3f} kPa")
        except Exception: pass

if __name__ == "__main__":
    app = FluidAppModernCTK()
    app.mainloop()
