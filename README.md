# 🌊 Fluid Mechanics Calculator

A comprehensive, GUI-based computational tool designed for mechanical and civil engineers, researchers, and students to seamlessly solve and visualize fundamental fluid mechanics problems.

## 📌 Project Overview
The **Fluid Mechanics Calculator** is a desktop application developed to bridge the gap between theoretical fluid dynamics and practical engineering computation. By utilizing a modern graphical user interface and robust numerical backend, this software allows users to analyze fluid systems with high precision. The application supports 3D data visualization to provide deep insights into parameter relations, such as pressure distributions and dynamic flow behaviors.

## ⚙️ Key Features & Modules
This application is modularized into four core engineering categories:

1. **Fluid Properties (خواص سیالات):**
   - Calculation of fundamental properties such as density ($\rho$), specific weight ($\gamma$), dynamic viscosity ($\mu$), and kinematic viscosity ($\nu$).
   - Ideal gas law implementations: $$P = \rho R T$$

2. **Fluid Statics (استاتیک سیالات):**
   - Hydrostatic pressure distribution calculations: $$\Delta P = \rho g \Delta h$$
   - Manometry, buoyancy forces, and pressure on submerged surfaces.

3. **Fluid Dynamics (دینامیک سیالات):**
   - Analysis of incompressible fluid flow.
   - Implementation of the Bernoulli Equation: $$P_1 + \frac{1}{2}\rho v_1^2 + \rho g z_1 = P_2 + \frac{1}{2}\rho v_2^2 + \rho g z_2$$
   - Continuity equation solvers and pipe flow analysis.

4. **Dimensional Analysis (آنالیز ابعادی):**
   - Identification and calculation of dimensionless parameters (Reynolds Number, Froude Number, Mach Number, etc.).
   - Support for Buckingham Pi theorem applications.

5. **Advanced 3D Visualization:**
   - Integrated 3D plots to visualize complex multi-variable relationships in fluid systems.

## 🛠️ Technology Stack
- **Core Language:** `Python 3.x`
- **User Interface:** `customtkinter` (Modern UI elements)
- **Mathematical Computation:** `numpy`
- **Data Visualization:** `matplotlib` (including `mpl_toolkits.mplot3d`)
- **Deployment:** `PyInstaller` (for standalone executable generation)

## 🚀 Installation & Usage

### Option 1: Using the Portable Version (For End-Users & Engineers)
If you just want to use the software without dealing with Python dependencies:
1. Go to the [Releases](../../releases) section of this repository.
2. Download the latest `Fluid_Mechanics_Calculator.zip` file.
3. Extract the folder and run `Fluid_Mechanics_Calculator.exe`. No installation is required.

### Option 2: Running from Source (For Developers)
To run the code or contribute to the project:

1. Clone the repository:
```bash
   git clone https://github.com/YOUR_USERNAME/Fluid_Mechanics_Calculator.git
   cd Fluid_Mechanics_Calculator
   
