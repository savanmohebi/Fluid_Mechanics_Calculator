import unittest
import math
from fluid_statics_engine import FluidStaticsEngine

class TestFluidStatics(unittest.TestCase):
    
    def test_calc_pressure(self):
        """تست محاسبه فشار هیدروستاتیک آب در عمق 10 متری"""
        P0 = 101325.0  # فشار اتمسفر
        rho = 998.0    # چگالی آب
        h = 10.0       # عمق
        
        expected_pressure = 199228.8
        calculated_pressure = FluidStaticsEngine.calc_pressure(P0, rho, h)
        self.assertAlmostEqual(calculated_pressure, expected_pressure, places=2)

    def test_calc_buoyancy(self):
        """تست نیروی شناوری برای 2 متر مکعب آب جابجا شده"""
        rho = 998.0
        v = 2.0
        
        expected_force = 19580.76
        calculated_force = FluidStaticsEngine.calc_buoyancy(rho, v)
        self.assertAlmostEqual(calculated_force, expected_force, places=2)

    def test_elliptical_gate_slide_problem(self):
        """تست حل مسئله دریچه بیضی از اسلاید استاد"""
        # 1. داده‌های اولیه مسئله
        gamma = 9800.0                # N/m^3 (وزن مخصوص داده شده در اسلاید)
        g = 9.81
        rho = gamma / g               # چگالی معادل: kg/m^3
        
        a = 2.5  # متر
        b = 2.0  # متر
        area = math.pi * a * b        # مساحت بیضی
        
        h_c = 10.0                    # متر (عمق مرکز ثقل از سطح آب)
        
        # 2. تست محاسبه نیروی برآیند (F_R)
        F_R_calculated = FluidStaticsEngine.calc_hydrostatic_force_plane(rho, h_c, area)
        F_R_expected = 1539380.40     # معادل 1.54 مگانیوتن در اسلاید
        
        # بررسی اینکه نیرو با تقریب خوبی (خطای کمتر از 1 نیوتن) محاسبه می‌شود
        self.assertAlmostEqual(F_R_calculated, F_R_expected, delta=1.0)
        
        # 3. تست محاسبه مرکز فشار (y_R)
        # زاویه شیب بر اساس لوله 4 متری و دریچه 5 متری (2*2.5): sin(theta) = 4/5 = 0.8
        sin_theta = 0.8
        y_c = h_c / sin_theta         # فاصله مایل تا مرکز ثقل: 12.5 متر
        I_xc = (math.pi * (a**3) * b) / 4.0 # ممان اینرسی بیضی: ~ 24.54
        
        y_R_calculated = FluidStaticsEngine.calc_center_of_pressure_y(y_c, area, I_xc)
        
        # فرمول تئوری: y_R = y_c + (I_xc / (y_c * A)) -> 12.5 + (24.54 / (12.5 * 15.7)) = 12.625
        y_R_expected = 12.625 
        
        self.assertAlmostEqual(y_R_calculated, y_R_expected, places=3)

if __name__ == '__main__':
    unittest.main()
