import math

class FluidStaticsEngine:
    """
    موتور محاسباتی استاتیک سیالات.
    شامل متدهایی برای محاسبه فشار هیدروستاتیک، شناوری، حرکت جسم صلب و نیروهای روی سطوح غوطه‌ور.
    """
    g: float = 9.81  # شتاب گرانش (m/s^2)

    @classmethod
    def calc_pressure(cls, P0: float, rho: float, h: float) -> float:
        """
        محاسبه فشار هیدروستاتیک در یک عمق مشخص.
        فرمول: P = P_0 + rho * g * h
        """
        return P0 + (rho * cls.g * h)

    @classmethod
    def calc_buoyancy(cls, rho_fluid: float, volume_submerged: float) -> float:
        """
        محاسبه نیروی شناوری (اصل ارشمیدس).
        فرمول: F_b = rho * g * V
        """
        return rho_fluid * cls.g * volume_submerged

    @staticmethod
    def calc_rigid_body_motion(a_x: float, omega: float, r: float):
        """
        محاسبه زاویه انحراف و ارتفاع سهمی‌گون در حرکت جسم صلب.
        """
        g = 9.81
        theta_rad = math.atan(a_x / g)
        theta_deg = math.degrees(theta_rad)
        z_max = (omega**2 * r**2) / (2 * g)
        return theta_deg, z_max

    # --- متدهای جدید اضافه شده برای سطوح غوطه‌ور ---

    @classmethod
    def calc_hydrostatic_force_plane(cls, rho: float, h_c: float, area: float) -> float:
        """
        محاسبه نیروی هیدروستاتیک برآیند وارد بر یک سطح تخت غوطه‌ور.
        فرمول: F_R = rho * g * h_c * A
        
        پارامترها:
            rho (float): چگالی سیال (kg/m^3) - برای آب معمولاً 1000 یا 998 است.
            h_c (float): فاصله عمودی از سطح آزاد سیال تا مرکز سطح (m)
            area (float): مساحت سطح غوطه‌ور (m^2)
            
        خروجی:
            float: نیروی برآیند (N)
        """
        return rho * cls.g * h_c * area

    @staticmethod
    def calc_center_of_pressure_y(y_c: float, area: float, I_xc: float) -> float:
        """
        محاسبه مکان مرکز فشار در امتداد محور y (محور مایل روی سطح).
        فرمول: y_R = y_c + (I_xc / (y_c * A))
        
        پارامترها:
            y_c (float): فاصله از سطح آزاد تا مرکز سطح در امتداد محور مایل (m)
            area (float): مساحت سطح (m^2)
            I_xc (float): ممان اینرسی سطح حول محور x گذرنده از مرکز (m^4)
            
        خروجی:
            float: مکان مرکز فشار y_R در امتداد محور مایل (m)
        """
        if y_c == 0 or area == 0:
            raise ValueError("y_c and area must be greater than 0.")
        
        return y_c + (I_xc / (y_c * area))
"""
FLUID PROPERTIES ENGINE
ماژول محاسبات ریاضی و فیزیکی آزمایشگاه مکانیک سیالات
"""
import math

# ثابت‌های فیزیکی
g = 9.81  # شتاب گرانش [m/s²]

def calc_kinematic_viscosity(mu, rho):
    """
    محاسبه لزجت سینماتیکی
    """
    return mu / rho

def calc_capillarity(sigma, theta_deg, rho, R):
    """
    محاسبه صعود یا نزول مویینگی
    """
    theta_rad = math.radians(theta_deg)
    return (2 * sigma * math.cos(theta_rad)) / (rho * g * R)

def calc_rot_viscometer(Ri, Ro, L, omega, mu):
    """
    محاسبه گشتاور و توان ویسکومتر چرخشی (جریان کوئت)
    """
    T = (4 * math.pi * mu * L * (Ri**3) * omega) / (Ro - Ri)
    P = T * omega
    return T, P

def calc_flywheel_viscosity(W, k, omega0, alpha, d, L, c):
    """
    محاسبه لزجت دینامیکی از روی آزمایش چرخ‌طیار (کاهش سرعت)
    """
    I = (W / g) * (k**2)  # ممان اینرسی
    mu = (4 * c * I * alpha) / (math.pi * (d**3) * L * omega0)
    return mu
def calc_bulk_modulus_pressure(K_Pa, delta_v_percent):
    """
    محاسبه فشار مورد نیاز برای درصد مشخصی کاهش حجم (تراکم پذیری)
    ورودی ها:
      K_Pa: مدول بالک بر حسب پاسکال (Pa)
      delta_v_percent: درصد کاهش حجم (مثلاً 0.5 برای نیم درصد)
    خروجی:
      تغییرات فشار (Delta P) بر حسب پاسکال (Pa)
    """
    # تبدیل درصد به نسبت اعشاری
    strain = abs(delta_v_percent) / 100.0
    
    # فرمول: dP = K * (dV/V)
    delta_P = K_Pa * strain
    return delta_P

def calc_droplet_pressure(P_out_Pa, sigma, D_m):
    """
    محاسبه فشار مطلق داخل قطره به دلیل کشش سطحی
    ورودی ها:
      P_out_Pa: فشار محیط بیرون بر حسب پاسکال (Pa)
      sigma: ضریب کشش سطحی بر حسب نیوتون بر متر (N/m)
      D_m: قطر قطره بر حسب متر (m)
    خروجی:
      فشار داخل قطره بر حسب پاسکال (Pa)
    """
    # محاسبه اختلاف فشار لاپلاس
    delta_P = (4 * sigma) / D_m
    
    # فشار مطلق داخل
    P_in = P_out_Pa + delta_P
    return P_in
def calc_shaft_power_narrow_gap(D, L, t, rpm, mu, pi_val=math.pi):
    """
    محاسبه گشتاور و توان مورد نیاز برای چرخش شفت در داخل یک غلاف
    (با فرض تقریب فاصله بسیار کم و پروفیل سرعت خطی)
    
    ورودی‌ها:
      D: قطر شفت بر حسب متر (m)
      L: طول شفت بر حسب متر (m)
      t: فاصله (لقی) بین شفت و غلاف بر حسب متر (m)
      rpm: سرعت دوران شفت (دور بر دقیقه - rev/min)
      mu: لزجت دینامیکی سیال بر حسب (kg/m.s یا Pa.s)
      pi_val: مقدار عدد پی (پیش‌فرض math.pi است، اما برای حل برخی سوالات می‌توان آن را 3 قرار داد)
      
    خروجی‌ها:
      T: گشتاور بر حسب نیوتون‌متر (N.m)
      P: توان مصرفی بر حسب وات (W)
    """
    # 1. تبدیل سرعت زاویه‌ای از دور بر دقیقه به رادیان بر ثانیه
    omega = rpm * (2 * pi_val) / 60.0
    
    # 2. محاسبه شعاع شفت
    R = D / 2.0
    
    # 3. محاسبه گشتاور بر اساس فرمول: T = (2 * pi * mu * R^3 * omega * L) / t
    T = (2 * pi_val * mu * (R**3) * omega * L) / t
    
    # 4. محاسبه توان: P = T * omega
    P = T * omega
    
    return T, P
