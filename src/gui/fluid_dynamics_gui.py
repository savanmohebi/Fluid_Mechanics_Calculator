import math
import tkinter as tk
import numpy as np
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# فراخوانی موتور محاسبات دینامیک سیالات
from src.engines import fluid_dynamics_engine as fde

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
    "Water (20°C)": {"rho": 998, "mu": 1.002e-3}, 
    "Air (25°C)": {"rho": 1.184, "mu": 1.85e-5},
    "Engine Oil (40°C)": {"rho": 870, "mu": 0.27},
    "Glycerin": {"rho": 1260, "mu": 1.49},
}

class FluidDynamicsApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("FLUID DYNAMICS STUDIO – Advanced Mechanics Lab")
        self.geometry("1250x800")
        self.minsize(1150, 700)
        self.configure(fg_color=BG_MAIN)

        self.fluid_var = ctk.StringVar(value="Water (20°C)")
        self.current_page = None
        self.canvas_drag = None
        self.wave_phase = 0.0

        self._build_ui()
        self.animate_waves()
    
    def _build_ui(self):
        self.sidebar = ctk.CTkFrame(self, fg_color=BG_SIDEBAR, width=260, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

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
        ctk.CTkLabel(header, text="FLUID DYNAMICS", text_color=ACCENT, font=("Segoe UI Black", 18), justify="left").pack(anchor="w")
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
        add_nav("🌀", "Reynolds Number", "reynolds")
        add_nav("➡️", "Continuity Equation", "continuity")
        add_nav("⚖️", "Bernoulli Theorem", "bernoulli")
        add_nav("📉", "Darcy-Weisbach", "darcy")
        add_nav("🚀", "Drag Force Dynamics", "drag")
        add_nav("🎛️", "Venturi Meter", "venturi")

    def _build_sidebar_footer(self):
        footer = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        footer.pack(fill="x", side="bottom", padx=16, pady=15)
        ctk.CTkLabel(footer, text="Dynamics Studio v2.0\nInteractive Environment", font=("Segoe UI", 11), text_color=TEXT_SUB, justify="left").pack(anchor="w")

    def _build_header(self, parent):
        self.header = ctk.CTkFrame(parent, fg_color=BG_MAIN, height=70, corner_radius=0)
        self.header.pack(fill="x", padx=20, pady=(20, 0))
        title_frame = ctk.CTkFrame(self.header, fg_color="transparent")
        title_frame.pack(side="left")
        ctk.CTkLabel(title_frame, text="Fluid Dynamics Lab", font=("Segoe UI", 26, "bold"), text_color=TEXT_MAIN).pack(anchor="w")
        self.lbl_fluid_badge = ctk.CTkLabel(title_frame, text=self._fluid_badge_text(), font=("Consolas", 11, "bold"), text_color=ACCENT_HOVER)
        self.lbl_fluid_badge.pack(anchor="w")
        
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

    def _create_pages(self):
        self.pages["home"] = self._create_page_home()
        self.pages["reynolds"] = self._create_page_reynolds()
        self.pages["continuity"] = self._create_page_continuity()
        self.pages["bernoulli"] = self._create_page_bernoulli()
        self.pages["darcy"] = self._create_page_darcy()
        self.pages["drag"] = self._create_page_drag()
        self.pages["venturi"] = self._create_page_venturi()

    def _create_page_home(self):
        page = ctk.CTkFrame(self.pages_frame, fg_color="transparent")
        welcome_card = self.create_card(page, title="Welcome to Fluid Dynamics Studio", subtitle="Select a dynamic flow module to begin.")
        ctk.CTkLabel(welcome_card, text="This tool evaluates kinematics and dynamics of fluid flow in real-time.", 
                     wraplength=800, justify="left", text_color=TEXT_SUB, font=("Segoe UI", 14)).pack(anchor="w", pady=(0, 20))

        self.dashboard_frame = ctk.CTkFrame(page, fg_color="transparent")
        self.dashboard_frame.pack(fill="both", expand=True)
        self.lbl_dash_rho = self._build_stat_box(self.dashboard_frame, "Density (ρ)", "kg/m³", 0, 0)
        self.lbl_dash_mu = self._build_stat_box(self.dashboard_frame, "Dynamic Viscosity (μ)", "Pa·s", 0, 1)
        
        self.on_fluid_change()
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
    def _create_page_reynolds(self):
        page = ctk.CTkFrame(self.pages_frame, fg_color="transparent")
        ctrl_card = self.create_card(page, title="Reynolds Number", subtitle=r"Re = \rho V D / \mu")
        ctrl_card.columnconfigure(0, weight=1); ctrl_card.columnconfigure(1, weight=1)

        self.re_v_var, _ = self.create_entry(ctrl_card, "Velocity (V)", "m/s", row=0, column=0, trace_cmd=self.safe_calc_reynolds)
        self.re_d_var, _ = self.create_entry(ctrl_card, "Diameter (D)", "m", row=0, column=1, trace_cmd=self.safe_calc_reynolds)
        self.re_rho_var, _ = self.create_entry(ctrl_card, "Density (ρ)", "kg/m³", row=1, column=0, trace_cmd=self.safe_calc_reynolds)
        self.re_mu_var, _ = self.create_entry(ctrl_card, "Viscosity (μ)", "Pa·s", row=1, column=1, trace_cmd=self.safe_calc_reynolds)
        
        self.re_v_var.set("2.5")
        self.re_d_var.set("0.05")

        self.result_re = ctk.CTkLabel(ctrl_card, text="Re = —\nRegime = —", text_color=ACCENT, font=("Consolas", 18, "bold"), justify="left")
        self.result_re.grid(row=2, column=0, columnspan=2, sticky="w", pady=(25, 10), padx=10)
        return page

    def _create_page_continuity(self):
        page = ctk.CTkFrame(self.pages_frame, fg_color="transparent")
        ctrl_card = self.create_card(page, title="Continuity Equation", subtitle=r"A_1 V_1 = A_2 V_2 = Q")
        ctrl_card.columnconfigure(0, weight=1); ctrl_card.columnconfigure(1, weight=1)

        self.cont_a1_var, _ = self.create_entry(ctrl_card, "Area 1 (A₁)", "m²", row=0, column=0, trace_cmd=self.safe_calc_continuity)
        self.cont_v1_var, _ = self.create_entry(ctrl_card, "Velocity 1 (V₁)", "m/s", row=0, column=1, trace_cmd=self.safe_calc_continuity)
        self.cont_a2_var, _ = self.create_entry(ctrl_card, "Area 2 (A₂)", "m²", row=1, column=0, trace_cmd=self.safe_calc_continuity)

        self.cont_a1_var.set("0.1")
        self.cont_v1_var.set("5.0")
        self.cont_a2_var.set("0.05")

        self.result_cont = ctk.CTkLabel(ctrl_card, text="V₂ = —\nQ = —", text_color=ACCENT, font=("Consolas", 18, "bold"), justify="left")
        self.result_cont.grid(row=2, column=0, columnspan=2, sticky="w", pady=(25, 10), padx=10)
        return page

    def _create_page_bernoulli(self):
        page = ctk.CTkFrame(self.pages_frame, fg_color="transparent")
        ctrl_card = self.create_card(page, title="Bernoulli Equation", subtitle=r"P_1 + 0.5\rho V_1^2 + \gamma z_1 = P_2 + 0.5\rho V_2^2 + \gamma z_2")
        ctrl_card.columnconfigure(0, weight=1); ctrl_card.columnconfigure(1, weight=1)

        self.bern_p1_var, _ = self.create_entry(ctrl_card, "Pressure 1 (P₁)", "Pa", row=0, column=0, trace_cmd=self.safe_calc_bernoulli)
        self.bern_v1_var, _ = self.create_entry(ctrl_card, "Velocity 1 (V₁)", "m/s", row=0, column=1, trace_cmd=self.safe_calc_bernoulli)
        self.bern_z1_var, _ = self.create_entry(ctrl_card, "Elevation 1 (z₁)", "m", row=1, column=0, trace_cmd=self.safe_calc_bernoulli)
        
        self.bern_v2_var, _ = self.create_entry(ctrl_card, "Velocity 2 (V₂)", "m/s", row=1, column=1, trace_cmd=self.safe_calc_bernoulli)
        self.bern_z2_var, _ = self.create_entry(ctrl_card, "Elevation 2 (z₂)", "m", row=2, column=0, trace_cmd=self.safe_calc_bernoulli)
        self.bern_rho_var, _ = self.create_entry(ctrl_card, "Density (ρ)", "kg/m³", row=2, column=1, trace_cmd=self.safe_calc_bernoulli)

        self.bern_p1_var.set("150000")
        self.bern_v1_var.set("2.0")
        self.bern_z1_var.set("0.0")
        self.bern_v2_var.set("4.0")
        self.bern_z2_var.set("5.0")

        self.result_bern = ctk.CTkLabel(ctrl_card, text="P₂ = —", text_color=ACCENT, font=("Consolas", 18, "bold"))
        self.result_bern.grid(row=3, column=0, columnspan=2, sticky="w", pady=(25, 10), padx=10)
        return page

    def _create_page_darcy(self):
        page = ctk.CTkFrame(self.pages_frame, fg_color="transparent")
        ctrl_card = self.create_card(page, title="Darcy-Weisbach Head Loss", subtitle=r"h_f = f (L/D) (V^2/2g)")
        ctrl_card.columnconfigure(0, weight=1); ctrl_card.columnconfigure(1, weight=1)

        self.dw_f_var, _ = self.create_entry(ctrl_card, "Friction Factor (f)", "", row=0, column=0, trace_cmd=self.safe_calc_darcy)
        self.dw_l_var, _ = self.create_entry(ctrl_card, "Length (L)", "m", row=0, column=1, trace_cmd=self.safe_calc_darcy)
        self.dw_d_var, _ = self.create_entry(ctrl_card, "Diameter (D)", "m", row=1, column=0, trace_cmd=self.safe_calc_darcy)
        self.dw_v_var, _ = self.create_entry(ctrl_card, "Velocity (V)", "m/s", row=1, column=1, trace_cmd=self.safe_calc_darcy)

        self.dw_f_var.set("0.02")
        self.dw_l_var.set("100.0")
        self.dw_d_var.set("0.1")
        self.dw_v_var.set("3.0")

        self.result_dw = ctk.CTkLabel(ctrl_card, text="h_f = —", text_color=ACCENT, font=("Consolas", 18, "bold"))
        self.result_dw.grid(row=2, column=0, columnspan=2, sticky="w", pady=(25, 10), padx=10)
        return page

    def _create_page_drag(self):
        page = ctk.CTkFrame(self.pages_frame, fg_color="transparent")
        
        left_panel = ctk.CTkFrame(page, fg_color="transparent", width=420)
        left_panel.pack(side="left", fill="y")
        
        self.drag_plot_frame = ctk.CTkFrame(page, fg_color=BG_CARD, corner_radius=10, border_width=1, border_color=CARD_BORDER)
        self.drag_plot_frame.pack(side="right", fill="both", expand=True, padx=(15, 0), pady=10)

        ctrl_card = self.create_card(left_panel, title="Drag Force Dynamics", subtitle=r"F_D = 0.5 \rho V^2 C_D A")

        self.drag_cd_var, _ = self.create_entry(ctrl_card, "Drag Coeff (C_D)", "", row=0, column=0, trace_cmd=self.safe_plot_drag)
        self.drag_rho_var, _ = self.create_entry(ctrl_card, "Density (ρ)", "kg/m³", row=1, column=0, trace_cmd=self.safe_plot_drag)
        self.drag_v_var, _ = self.create_entry(ctrl_card, "Velocity (V)", "m/s", row=2, column=0, trace_cmd=self.safe_plot_drag)
        self.drag_a_var, _ = self.create_entry(ctrl_card, "Projected Area (A)", "m²", row=3, column=0, trace_cmd=self.safe_plot_drag)

        self.drag_cd_var.set("0.47") # Sphere
        self.drag_v_var.set("15.0")
        self.drag_a_var.set("0.5")

        self.result_drag = ctk.CTkLabel(ctrl_card, text="F_D = —", text_color=ACCENT, font=("Consolas", 18, "bold"), justify="left")
        self.result_drag.grid(row=4, column=0, sticky="w", pady=(20, 10), padx=10)
        return page

    def _create_page_venturi(self):
        page = ctk.CTkFrame(self.pages_frame, fg_color="transparent")
        ctrl_card = self.create_card(page, title="Venturi Meter", subtitle=r"Q = C_d A_2 \sqrt{2(P_1 - P_2) / \rho(1 - \beta^4)}")
        ctrl_card.columnconfigure(0, weight=1); ctrl_card.columnconfigure(1, weight=1)

        self.ven_a1_var, _ = self.create_entry(ctrl_card, "Inlet Area (A₁)", "m²", row=0, column=0, trace_cmd=self.safe_calc_venturi)
        self.ven_a2_var, _ = self.create_entry(ctrl_card, "Throat Area (A₂)", "m²", row=0, column=1, trace_cmd=self.safe_calc_venturi)
        self.ven_p1_var, _ = self.create_entry(ctrl_card, "Inlet Press (P₁)", "Pa", row=1, column=0, trace_cmd=self.safe_calc_venturi)
        self.ven_p2_var, _ = self.create_entry(ctrl_card, "Throat Press (P₂)", "Pa", row=1, column=1, trace_cmd=self.safe_calc_venturi)
        self.ven_cd_var, _ = self.create_entry(ctrl_card, "Discharge Coeff", "", row=2, column=0, trace_cmd=self.safe_calc_venturi)
        self.ven_rho_var, _ = self.create_entry(ctrl_card, "Density (ρ)", "kg/m³", row=2, column=1, trace_cmd=self.safe_calc_venturi)

        self.ven_a1_var.set("0.05")
        self.ven_a2_var.set("0.02")
        self.ven_p1_var.set("200000")
        self.ven_p2_var.set("180000")
        self.ven_cd_var.set("0.98")

        self.result_ven = ctk.CTkLabel(ctrl_card, text="Q_actual = —", text_color=ACCENT, font=("Consolas", 18, "bold"))
        self.result_ven.grid(row=3, column=0, columnspan=2, sticky="w", pady=(25, 10), padx=10)
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
            if hasattr(self, 'lbl_dash_rho'):
                self.lbl_dash_rho.configure(text=f"{props.get('rho', '--')}")
                self.lbl_dash_mu.configure(text=f"{props.get('mu', '--'):.2e}")

            for var in [getattr(self, 're_rho_var', None), getattr(self, 'bern_rho_var', None), 
                        getattr(self, 'drag_rho_var', None), getattr(self, 'ven_rho_var', None)]:
                if var: var.set(str(props.get("rho", "")))
            if hasattr(self, 're_mu_var'):
                self.re_mu_var.set(str(props.get("mu", "")))

        self.lbl_fluid_badge.configure(text=self._fluid_badge_text())
        self.set_status(f"Fluid changed to: {fluid}")

    # ================== SAFE CALC WRAPPERS ==================
    def safe_calc_reynolds(self):
        try:
            V = self._get_float(self.re_v_var)
            D = self._get_float(self.re_d_var)
            rho = self._get_float(self.re_rho_var)
            mu = self._get_float(self.re_mu_var)
            if mu <= 0: return
            Re, regime = fde.calc_reynolds_number(rho, V, D, mu)
            self.result_re.configure(text=f"Re = {Re:.2f}\nRegime = {regime}")
        except Exception: pass

    def safe_calc_continuity(self):
        try:
            A1 = self._get_float(self.cont_a1_var)
            V1 = self._get_float(self.cont_v1_var)
            A2 = self._get_float(self.cont_a2_var)
            if A2 <= 0: return
            V2, Q = fde.calc_continuity_velocity(A1, V1, A2)
            self.result_cont.configure(text=f"V₂ = {V2:.4f} m/s\nQ = {Q:.4f} m³/s")
        except Exception: pass

    def safe_calc_bernoulli(self):
        try:
            P1 = self._get_float(self.bern_p1_var)
            V1 = self._get_float(self.bern_v1_var)
            z1 = self._get_float(self.bern_z1_var)
            V2 = self._get_float(self.bern_v2_var)
            z2 = self._get_float(self.bern_z2_var)
            rho = self._get_float(self.bern_rho_var)
            P2 = fde.calc_bernoulli_pressure(P1, V1, z1, V2, z2, rho)
            self.result_bern.configure(text=f"P₂ = {P2:.2f} Pa")
        except Exception: pass

    def safe_calc_darcy(self):
        try:
            f = self._get_float(self.dw_f_var)
            L = self._get_float(self.dw_l_var)
            D = self._get_float(self.dw_d_var)
            V = self._get_float(self.dw_v_var)
            if D <= 0: return
            hf = fde.calc_darcy_weisbach_head_loss(f, L, D, V)
            self.result_dw.configure(text=f"h_f = {hf:.4f} m")
        except Exception: pass

    def safe_plot_drag(self):
        try:
            Cd = self._get_float(self.drag_cd_var)
            rho = self._get_float(self.drag_rho_var)
            V = self._get_float(self.drag_v_var)
            A = self._get_float(self.drag_a_var)
            
            Fd = fde.calc_drag_force(Cd, rho, V, A)
            self.result_drag.configure(text=f"F_D = {Fd:.2f} N")
            
            if self.canvas_drag:
                self.canvas_drag.get_tk_widget().destroy()

            fig = Figure(figsize=(5, 5), dpi=100, facecolor=BG_CARD)
            ax = fig.add_subplot(111)
            ax.set_facecolor(BG_MAIN)

            V_range = np.linspace(0, max(V*1.5, 30), 100)
            F_range = 0.5 * rho * (V_range**2) * Cd * A

            ax.plot(V_range, F_range, color=ACCENT, linewidth=2)
            ax.scatter([V], [Fd], color=DANGER, s=50, zorder=5)
            ax.set_xlabel(r"Velocity $V$ (m/s)", color=TEXT_SUB)
            ax.set_ylabel(r"Drag Force $F_D$ (N)", color=TEXT_SUB)
            ax.set_title("Drag Profile (Square Law)", color=TEXT_MAIN, pad=15)
            
            ax.tick_params(colors=TEXT_SUB)
            ax.grid(True, linestyle="--", alpha=0.3, color=CARD_BORDER)
            for spine in ax.spines.values(): spine.set_edgecolor(CARD_BORDER)

            self.canvas_drag = FigureCanvasTkAgg(fig, master=self.drag_plot_frame)
            self.canvas_drag.draw()
            self.canvas_drag.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        except Exception: pass

    def safe_calc_venturi(self):
        try:
            A1 = self._get_float(self.ven_a1_var)
            A2 = self._get_float(self.ven_a2_var)
            P1 = self._get_float(self.ven_p1_var)
            P2 = self._get_float(self.ven_p2_var)
            Cd = self._get_float(self.ven_cd_var)
            rho = self._get_float(self.ven_rho_var)
            
            if P1 <= P2 or A1 <= A2:
                self.result_ven.configure(text="Error: P1>P2 and A1>A2 required.")
                return
                
            Q = fde.calc_venturi_flow_rate(A1, A2, P1, P2, rho, Cd)
            self.result_ven.configure(text=f"Q_actual = {Q:.5f} m³/s")
        except Exception: pass

if __name__ == "__main__":
    app = FluidDynamicsApp()
    app.mainloop()
