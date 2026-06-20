# DIMENSIONAL_ANALYSIS_ENGINE.py
import math

# ==========================================
# 1. Dimensionless Numbers (گروه‌های بدون بعد)
# ==========================================

def calc_reynolds(rho: float, V: float, L: float, mu: float) -> float:
    """محاسبه عدد رینولدز (نیروی اینرسی به نیروی لزجت)"""
    if mu <= 0: return 0.0
    return (rho * V * L) / mu

def calc_froude(V: float, g: float, L: float) -> float:
    """محاسبه عدد فرود (نیروی اینرسی به نیروی گرانش)"""
    if g <= 0 or L <= 0: return 0.0
    return V / math.sqrt(g * L)

def calc_weber(rho: float, V: float, L: float, sigma: float) -> float:
    """محاسبه عدد وبر (نیروی اینرسی به کشش سطحی)"""
    if sigma <= 0: return 0.0
    return (rho * (V ** 2) * L) / sigma

def calc_mach(V: float, c: float) -> float:
    """محاسبه عدد ماخ (سرعت سیال به سرعت صوت)"""
    if c <= 0: return 0.0
    return V / c

def calc_euler(delta_P: float, rho: float, V: float) -> float:
    """محاسبه عدد اویلر (نیروی فشار به نیروی اینرسی)"""
    if rho <= 0 or V <= 0: return 0.0
    return delta_P / (rho * (V ** 2))

# ==========================================
# 2. Similitude & Model Studies (تشابه و مطالعه مدل‌ها)
# ==========================================

def froude_similitude(L_m: float, L_p: float, V_m: float, F_m: float, rho_m: float, rho_p: float):
    """
    محاسبه پارامترهای پروتوتایپ بر اساس تشابه فرود (معمولاً در جریان‌های سطح آزاد)
    L_r = L_m / L_p (مقیاس طولی)
    """
    if L_p <= 0 or L_m <= 0: return 0.0, 0.0
    
    L_r = L_m / L_p
    rho_r = rho_m / rho_p
    
    # مقیاس سرعت: V_r = sqrt(L_r)
    V_r = math.sqrt(L_r)
    V_p = V_m / V_r if V_r > 0 else 0.0
    
    # مقیاس نیرو: F_r = rho_r * (L_r ** 3)
    F_r = rho_r * (L_r ** 3)
    F_p = F_m / F_r if F_r > 0 else 0.0
    
    return V_p, F_p

def reynolds_similitude(L_m: float, L_p: float, V_m: float, nu_m: float, nu_p: float):
    """
    محاسبه سرعت پروتوتایپ بر اساس تشابه رینولدز (معمولاً در جریان‌های بسته مانند لوله‌ها و تونل باد)
    """
    if L_p <= 0 or L_m <= 0 or nu_m <= 0: return 0.0
    
    L_r = L_m / L_p
    nu_r = nu_m / nu_p
    
    # مقیاس سرعت در تشابه رینولدز: V_r = nu_r / L_r
    V_r = nu_r / L_r
    V_p = V_m / V_r if V_r > 0 else 0.0
    
    return V_p
