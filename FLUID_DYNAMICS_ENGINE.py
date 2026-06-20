"""
FLUID DYNAMICS ENGINE
ماژول محاسبات دینامیک و سینماتیک سیالات 
آزمایشگاه و مبانی مکانیک سیالات
"""
import math

# ثابت‌های فیزیکی
g = 9.81  # شتاب گرانش [m/s²]

def calc_reynolds_number(rho, V, D, mu):
    """
    محاسبه عدد بی‌بعد رینولدز برای تشخیص رژیم جریان (آرام یا درهم)
    رابطه: $Re = \frac{\rho V D}{\mu}$
    
    ورودی‌ها:
      rho: چگالی سیال [kg/m³]
      V: سرعت متوسط جریان [m/s]
      D: طول مشخصه (مثلاً قطر داخلی لوله) [m]
      mu: لزجت دینامیکی [Pa.s]
      
    خروجی:
      Re: عدد رینولدز (بدون بعد)
      flow_regime: نوع رژیم جریان (Laminar, Transient, Turbulent)
    """
    Re = (rho * V * D) / mu
    
    if Re < 2300:
        regime = "Laminar"
    elif 2300 <= Re <= 4000:
        regime = "Transient"
    else:
        regime = "Turbulent"
        
    return Re, regime

def calc_continuity_velocity(A1, V1, A2):
    """
    محاسبه سرعت در مقطع دوم بر اساس معادله پیوستگی برای سیال تراکم‌ناپذیر
    رابطه: $A_1 V_1 = A_2 V_2 = Q$
    
    ورودی‌ها:
      A1, A2: مساحت مقاطع اول و دوم [m²]
      V1: سرعت در مقطع اول [m/s]
      
    خروجی:
      V2: سرعت در مقطع دوم [m/s]
      Q: دبی حجمی جریان [m³/s]
    """
    Q = A1 * V1
    V2 = Q / A2
    return V2, Q

def calc_bernoulli_pressure(P1, V1, z1, V2, z2, rho):
    """
    محاسبه فشار در مقطع دوم با استفاده از معادله برنولی (بدون افت انرژی)
    رابطه: $P_1 + \frac{1}{2}\rho V_1^2 + \rho g z_1 = P_2 + \frac{1}{2}\rho V_2^2 + \rho g z_2$
    
    ورودی‌ها:
      P1: فشار مقطع اول [Pa]
      V1, V2: سرعت جریان در مقاطع اول و دوم [m/s]
      z1, z2: ارتفاع مقاطع از سطح مبنا [m]
      rho: چگالی سیال [kg/m³]
      
    خروجی:
      P2: فشار مقطع دوم [Pa]
    """
    # محاسبه هد کل در مقطع اول (به فرم فشار)
    total_energy_1 = P1 + 0.5 * rho * (V1**2) + rho * g * z1
    
    # استخراج فشار مقطع دوم
    P2 = total_energy_1 - (0.5 * rho * (V2**2) + rho * g * z2)
    return P2

def calc_darcy_weisbach_head_loss(f, L, D, V):
    """
    محاسبه افت هد اصطکاکی در لوله‌ها با استفاده از رابطه دارسی-وایسباخ
    رابطه: $h_f = f \frac{L}{D} \frac{V^2}{2g}$
    
    ورودی‌ها:
      f: ضریب اصطکاک دارسی (به دست آمده از نمودار مودی یا معادلات کولبروک)
      L: طول لوله [m]
      D: قطر داخلی لوله [m]
      V: سرعت متوسط جریان [m/s]
      
    خروجی:
      hf: افت هد اصطکاکی [m]
    """
    hf = f * (L / D) * ((V**2) / (2 * g))
    return hf

def calc_drag_force(C_d, rho, V, A):
    """
    محاسبه نیروی پسا (درگ) وارد بر یک جسم غوطه‌ور در جریان سیال
    رابطه: $F_D = \frac{1}{2} \rho V^2 C_D A$
    
    ورودی‌ها:
      C_d: ضریب درگ (بدون بعد)
      rho: چگالی سیال [kg/m³]
      V: سرعت نسبی جریان [m/s]
      A: مساحت تصویر شده (Projected Area) جسم در جهت جریان [m²]
      
    خروجی:
      F_d: نیروی درگ [N]
    """
    F_d = 0.5 * rho * (V**2) * C_d * A
    return F_d

def calc_venturi_flow_rate(A1, A2, P1, P2, rho, C_d=0.98):
    """
    محاسبه دبی حجمی واقعی در یک لوله ونتوری با در نظر گرفتن ضریب تخلیه
    رابطه تئوری بر اساس ترکیب معادله پیوستگی و برنولی.
    
    ورودی‌ها:
      A1: مساحت مقطع ورودی [m²]
      A2: مساحت مقطع گلوگاه [m²]
      P1, P2: فشار در مقطع ورودی و گلوگاه [Pa]
      rho: چگالی سیال [kg/m³]
      C_d: ضریب تخلیه (Discharge Coefficient) ونتوری‌متر (معمولاً بین 0.95 تا 0.99)
      
    خروجی:
      Q_actual: دبی حجمی واقعی [m³/s]
    """
    # اختلاف فشار
    delta_P = P1 - P2
    
    if delta_P < 0:
        raise ValueError("فشار مقطع اول باید بزرگتر از گلوگاه باشد (P1 > P2).")
        
    # مخرج کسر در رابطه ونتوری: sqrt(1 - (A2/A1)^2)
    beta_ratio_sq = (A2 / A1)**2
    denominator = math.sqrt(1 - beta_ratio_sq)
    
    # سرعت تئوری در گلوگاه
    V2_ideal = math.sqrt((2 * delta_P) / rho) / denominator
    
    # دبی واقعی
    Q_actual = C_d * A2 * V2_ideal
    return Q_actual
