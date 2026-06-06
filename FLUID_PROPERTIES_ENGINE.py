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
