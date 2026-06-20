# DIMENSIONAL_ANALYSIS_GUI.py
import math
import customtkinter as ctk
from src.engines import dimensional_analysis_engine as da_engine

# تنظیمات تم مشابه کد مرجع شما
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG_MAIN        = "#020817"   
BG_SIDEBAR     = "#020617"   
BG_CARD        = "#0a1128"   
CARD_BORDER    = "#1e293b"
ACCENT         = "#0ea5e9"   
TEXT_MAIN      = "#f8fafc"
TEXT_SUB       = "#94a3b8"

class DimensionalAnalysisApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("FLUIDPROP STUDIO - Dimensional Analysis & Similitude")
        self.geometry("1100x700")
        self.configure(fg_color=BG_MAIN)
        
        self.current_page = None
        self._build_ui()

    def _build_ui(self):
        # Sidebar
        self.sidebar = ctk.CTkFrame(self, fg_color=BG_SIDEBAR, width=260, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        ctk.CTkLabel(self.sidebar, text="CHAPTER 4", text_color=ACCENT, font=("Segoe UI Black", 18)).pack(pady=(25, 5))
        ctk.CTkLabel(self.sidebar, text="Dimensional Analysis", text_color=TEXT_SUB, font=("Segoe UI", 12, "bold")).pack(pady=(0, 20))

        self.nav_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.nav_frame.pack(fill="both", expand=True, padx=10)

        self.nav_buttons = {}
        self._add_nav("🔢", "Dimensionless Groups", "groups")
        self._add_nav("🚢", "Froude Similitude", "froude")
        self._add_nav("✈️", "Reynolds Similitude", "reynolds")

        # Content Area
        self.content = ctk.CTkFrame(self, fg_color=BG_MAIN, corner_radius=0)
        self.content.pack(side="right", fill="both", expand=True)

        self.header = ctk.CTkFrame(self.content, fg_color=BG_MAIN, height=60, corner_radius=0)
        self.header.pack(fill="x", padx=20, pady=20)
        ctk.CTkLabel(self.header, text="Dimensional Analysis & Dynamic Similitude", font=("Segoe UI", 24, "bold"), text_color=TEXT_MAIN).pack(anchor="w")

        self.pages_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        self.pages_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.pages = {}
        self._create_pages()
        self.show_page("groups")

    def _add_nav(self, icon, text, key):
        btn = ctk.CTkButton(
            self.nav_frame, text=f"  {icon}   {text}", anchor="w",
            fg_color="transparent", text_color=TEXT_SUB, hover_color=BG_CARD,
            font=("Segoe UI", 13, "bold"), height=40, command=lambda: self.show_page(key)
        )
        btn.pack(fill="x", pady=2)
        self.nav_buttons[key] = btn

    def show_page(self, key):
        if self.current_page: self.pages[self.current_page].pack_forget()
        self.pages[key].pack(fill="both", expand=True)
        self.current_page = key
        for k, btn in self.nav_buttons.items():
            btn.configure(fg_color=BG_CARD if k == key else "transparent", text_color=ACCENT if k == key else TEXT_SUB)

    def create_card(self, parent, title, subtitle):
        card = ctk.CTkFrame(parent, fg_color=BG_CARD, corner_radius=10, border_width=1, border_color=CARD_BORDER)
        card.pack(fill="x", pady=10)
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=20, pady=20)
        ctk.CTkLabel(inner, text=title, font=("Segoe UI", 18, "bold"), text_color=TEXT_MAIN).pack(anchor="w")
        ctk.CTkLabel(inner, text=subtitle, font=("Consolas", 13, "italic"), text_color=ACCENT).pack(anchor="w", pady=(2, 15))
        content = ctk.CTkFrame(inner, fg_color="transparent")
        content.pack(fill="both", expand=True)
        return content

    def create_entry(self, parent, label, unit, row, col, trace_cmd):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=row, column=col, sticky="ew", padx=10, pady=10)
        frame.columnconfigure(1, weight=1)
        ctk.CTkLabel(frame, text=label, text_color=TEXT_MAIN).grid(row=0, column=0, sticky="w", padx=(0, 10))
        var = ctk.StringVar(value="0.0")
        var.trace_add("write", lambda *a: trace_cmd())
        ctk.CTkEntry(frame, textvariable=var, width=100, fg_color=BG_MAIN).grid(row=0, column=1, sticky="ew", padx=(0, 10))
        ctk.CTkLabel(frame, text=unit, text_color=TEXT_SUB).grid(row=0, column=2, sticky="w")
        return var

    def _get_float(self, var):
        try: return float(var.get())
        except ValueError: return 0.0

    def _create_pages(self):
        # 1. Dimensionless Groups Page
        p1 = ctk.CTkFrame(self.pages_frame, fg_color="transparent")
        c1 = self.create_card(p1, "Buckingham Pi / Important Groups", "Re, Fr, We, Ma, Eu")
        c1.columnconfigure((0,1), weight=1)

        self.p1_rho = self.create_entry(c1, "Density (ρ)", "kg/m³", 0, 0, self.calc_groups)
        self.p1_V   = self.create_entry(c1, "Velocity (V)", "m/s", 0, 1, self.calc_groups)
        self.p1_L   = self.create_entry(c1, "Char. Length (L)", "m", 1, 0, self.calc_groups)
        self.p1_mu  = self.create_entry(c1, "Viscosity (μ)", "Pa.s", 1, 1, self.calc_groups)
        self.p1_g   = self.create_entry(c1, "Gravity (g)", "m/s²", 2, 0, self.calc_groups)
        self.p1_sig = self.create_entry(c1, "Surf. Tension (σ)", "N/m", 2, 1, self.calc_groups)
        self.p1_c   = self.create_entry(c1, "Speed of Sound (c)", "m/s", 3, 0, self.calc_groups)
        self.p1_dP  = self.create_entry(c1, "Pressure Diff (ΔP)", "Pa", 3, 1, self.calc_groups)

        # مقادیر اولیه برای تست
        self.p1_rho.set("1000"); self.p1_V.set("5"); self.p1_L.set("0.5"); self.p1_mu.set("0.001")
        self.p1_g.set("9.81"); self.p1_sig.set("0.073"); self.p1_c.set("1480"); self.p1_dP.set("50000")

        self.lbl_groups_res = ctk.CTkLabel(c1, text="Results...", text_color=ACCENT, font=("Consolas", 16, "bold"), justify="left")
        self.lbl_groups_res.grid(row=4, column=0, columnspan=2, sticky="w", pady=20, padx=10)
        self.pages["groups"] = p1

        # 2. Froude Similitude Page
        p2 = ctk.CTkFrame(self.pages_frame, fg_color="transparent")
        c2 = self.create_card(p2, "Froude Similitude (Open Channels / Ship Models)", "Fr_m = Fr_p")
        c2.columnconfigure((0,1), weight=1)

        self.p2_Lm = self.create_entry(c2, "Model Length (L_m)", "m", 0, 0, self.calc_froude_sim)
        self.p2_Lp = self.create_entry(c2, "Proto Length (L_p)", "m", 0, 1, self.calc_froude_sim)
        self.p2_Vm = self.create_entry(c2, "Model Velocity (V_m)", "m/s", 1, 0, self.calc_froude_sim)
        self.p2_Fm = self.create_entry(c2, "Model Force (F_m)", "N", 1, 1, self.calc_froude_sim)
        self.p2_rhom = self.create_entry(c2, "Model Density (ρ_m)", "kg/m³", 2, 0, self.calc_froude_sim)
        self.p2_rhop = self.create_entry(c2, "Proto Density (ρ_p)", "kg/m³", 2, 1, self.calc_froude_sim)
        
        self.p2_Lm.set("1.0"); self.p2_Lp.set("25.0"); self.p2_Vm.set("2.0")
        self.p2_Fm.set("15.0"); self.p2_rhom.set("1000"); self.p2_rhop.set("1025")

        self.lbl_froude_res = ctk.CTkLabel(c2, text="Prototype V: -- \nPrototype F: --", text_color=ACCENT, font=("Consolas", 16, "bold"), justify="left")
        self.lbl_froude_res.grid(row=3, column=0, columnspan=2, sticky="w", pady=20, padx=10)
        self.pages["froude"] = p2

        # 3. Reynolds Similitude Page
        p3 = ctk.CTkFrame(self.pages_frame, fg_color="transparent")
        c3 = self.create_card(p3, "Reynolds Similitude (Closed Conduits / Submarines)", "Re_m = Re_p")
        c3.columnconfigure((0,1), weight=1)

        self.p3_Lm = self.create_entry(c3, "Model Length (L_m)", "m", 0, 0, self.calc_rey_sim)
        self.p3_Lp = self.create_entry(c3, "Proto Length (L_p)", "m", 0, 1, self.calc_rey_sim)
        self.p3_Vm = self.create_entry(c3, "Model Velocity (V_m)", "m/s", 1, 0, self.calc_rey_sim)
        self.p3_num = self.create_entry(c3, "Model Kin. Visc (ν_m)", "m²/s", 2, 0, self.calc_rey_sim)
        self.p3_nup = self.create_entry(c3, "Proto Kin. Visc (ν_p)", "m²/s", 2, 1, self.calc_rey_sim)
        
        self.p3_Lm.set("1.0"); self.p3_Lp.set("10.0"); self.p3_Vm.set("50.0")
        self.p3_num.set("1.5e-5"); self.p3_nup.set("1.0e-6")

        self.lbl_rey_res = ctk.CTkLabel(c3, text="Prototype V: --", text_color=ACCENT, font=("Consolas", 16, "bold"), justify="left")
        self.lbl_rey_res.grid(row=3, column=0, columnspan=2, sticky="w", pady=20, padx=10)
        self.pages["reynolds"] = p3

    # ================== محاسبات بلادرنگ (Real-Time Tracing) ==================
    def calc_groups(self):
        rho = self._get_float(self.p1_rho); V = self._get_float(self.p1_V)
        L = self._get_float(self.p1_L); mu = self._get_float(self.p1_mu)
        g = self._get_float(self.p1_g); sig = self._get_float(self.p1_sig)
        c = self._get_float(self.p1_c); dP = self._get_float(self.p1_dP)

        Re = da_engine.calc_reynolds(rho, V, L, mu)
        Fr = da_engine.calc_froude(V, g, L)
        We = da_engine.calc_weber(rho, V, L, sig)
        Ma = da_engine.calc_mach(V, c)
        Eu = da_engine.calc_euler(dP, rho, V)

        res_text = (f"Reynolds (Re) = {Re:.2e}   |   Froude (Fr) = {Fr:.4f}\n"
                    f"Weber    (We) = {We:.2e}   |   Mach   (Ma) = {Ma:.4f}\n"
                    f"Euler    (Eu) = {Eu:.4f}")
        self.lbl_groups_res.configure(text=res_text)

    def calc_froude_sim(self):
        Lm = self._get_float(self.p2_Lm); Lp = self._get_float(self.p2_Lp)
        Vm = self._get_float(self.p2_Vm); Fm = self._get_float(self.p2_Fm)
        rhom = self._get_float(self.p2_rhom); rhop = self._get_float(self.p2_rhop)

        V_p, F_p = da_engine.froude_similitude(Lm, Lp, Vm, Fm, rhom, rhop)
        self.lbl_froude_res.configure(text=f"Prototype Velocity (V_p) = {V_p:.3f} m/s\nPrototype Force (F_p) = {F_p:.2f} N")

    def calc_rey_sim(self):
        Lm = self._get_float(self.p3_Lm); Lp = self._get_float(self.p3_Lp)
        Vm = self._get_float(self.p3_Vm)
        num = self._get_float(self.p3_num); nup = self._get_float(self.p3_nup)

        V_p = da_engine.reynolds_similitude(Lm, Lp, Vm, num, nup)
        self.lbl_rey_res.configure(text=f"Prototype Velocity (V_p) = {V_p:.3f} m/s")

if __name__ == "__main__":
    app = DimensionalAnalysisApp()
    app.mainloop()
