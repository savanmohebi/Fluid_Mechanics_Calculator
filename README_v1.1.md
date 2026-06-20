# Fluid Mechanics Calculator v1.1

![Version](https://img.shields.io/badge/version-1.1-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-Educational-orange)

## 🌊 Overview

A comprehensive, professional-grade fluid mechanics calculator designed for engineering students and professionals. This application provides computational tools for analyzing fluid properties, statics, dynamics, and dimensional analysis.

## ✨ What's New in v1.1

### Enhanced User Interface
- **🎨 Modern Design**: Completely redesigned dashboard with card-based layout
- **🌓 Theme Support**: Toggle between dark and light modes
- **🎯 Improved Navigation**: Intuitive module cards with icons and descriptions
- **💫 Interactive Elements**: Hover effects and smooth transitions
- **📱 Responsive Layout**: Better scaling and minimum size constraints

### New Features
- **Theme Toggle**: Switch between dark and light themes instantly
- **About Dialog**: Detailed information about the application and developer
- **Status Indicators**: Real-time system status in footer
- **Enhanced Typography**: Better fonts and text hierarchy
- **Color-Coded Modules**: Each chapter has its own distinctive color
- **Professional Branding**: Improved header with version information

### Technical Improvements
- Better error handling for missing modules
- Improved window sizing and constraints
- Enhanced color schemes with better contrast
- Cleaner code structure and documentation
- Optimized performance and responsiveness

## 📦 Modules

### Chapter 1: Fluid Properties 💧
- Density calculations
- Viscosity analysis
- Surface tension
- Fluid database with common fluids
- Temperature-dependent properties

### Chapter 2: Fluid Statics ⚖️
- Pressure calculations
- Hydrostatic forces
- Buoyancy analysis
- Manometer problems
- Force on submerged surfaces

### Chapter 3: Fluid Dynamics 🌀
- Bernoulli's equation
- Energy equation
- Flow analysis
- Velocity and discharge
- Pipe flow calculations

### Chapter 4: Dimensional Analysis 📐
- Dimensionless groups
- Froude similitude
- Reynolds similitude
- Pi theorem applications
- Scale model analysis

## 🚀 Installation

### Prerequisites
```bash
Python 3.8 or higher
```

### Required Libraries
```bash
pip install customtkinter
pip install pillow
pip install numpy
pip install matplotlib
```

### Quick Start
1. Clone or download the repository
2. Install dependencies
3. Run the main application:
```bash
python Fluid_Mechanics_Calculator_v1.1.py
```

## 🎯 Usage

1. **Launch Application**: Run the main Python file
2. **Select Module**: Click on any of the four module cards
3. **Perform Calculations**: Use the module-specific interface
4. **Toggle Theme**: Click the moon/sun icon in the header
5. **View Info**: Click the info icon for application details

## 🛠️ Building Executable

To create a standalone executable using PyInstaller:

```bash
pyinstaller --onefile --windowed --name "FluidMechanicsCalc" Fluid_Mechanics_Calculator_v1.1.py
```

For including all modules:
```bash
pyinstaller --onefile --windowed ^
    --add-data "FLUID_PROPERTIES_GUI.py;." ^
    --add-data "fluid_statics_gui.py;." ^
    --add-data "fluid_dynamic_gui.py;." ^
    --add-data "DIMENSIONAL_ANALYSIS_GUI.py;." ^
    --add-data "FLUID_PROPERTIES_ENGINE.py;." ^
    --add-data "fluid_statics_engine.py;." ^
    --add-data "FLUID_DYNAMICS_ENGINE.py;." ^
    --add-data "DIMENSIONAL_ANALYSIS_ENGINE.py;." ^
    --name "FluidMechanicsCalculator_v1.1" ^
    Fluid_Mechanics_Calculator_v1.1.py
```

## 📁 Project Structure

```
calc/
├── Fluid_Mechanics_Calculator_v1.1.py    # Main dashboard (NEW)
├── Fluid_Mechanics_Calculator.py         # Legacy version
├── FLUID_PROPERTIES_GUI.py               # Chapter 1 GUI
├── FLUID_PROPERTIES_ENGINE.py            # Chapter 1 Engine
├── fluid_statics_gui.py                  # Chapter 2 GUI
├── fluid_statics_engine.py               # Chapter 2 Engine
├── fluid_dynamic_gui.py                  # Chapter 3 GUI
├── FLUID_DYNAMICS_ENGINE.py              # Chapter 3 Engine
├── DIMENSIONAL_ANALYSIS_GUI.py           # Chapter 4 GUI
├── DIMENSIONAL_ANALYSIS_ENGINE.py        # Chapter 4 Engine
├── README_v1.1.md                        # This file (NEW)
└── CHANGELOG.md                          # Version history (NEW)
```

## 🎨 Design Philosophy

The v1.1 redesign focuses on:
- **Professional Appearance**: Clean, modern interface suitable for engineering work
- **User Experience**: Intuitive navigation and clear visual hierarchy
- **Accessibility**: High contrast ratios and readable typography
- **Flexibility**: Theme options to suit different preferences
- **Scalability**: Modular architecture for easy expansion

## 🔧 Technical Details

### Technologies Used
- **GUI Framework**: CustomTkinter (modern tkinter wrapper)
- **Graphics**: PIL/Pillow for image processing
- **Calculations**: NumPy for numerical operations
- **Plotting**: Matplotlib for visualization
- **Packaging**: PyInstaller for executable creation

### System Requirements
- **OS**: Windows 10/11, Linux, macOS
- **RAM**: 4GB minimum, 8GB recommended
- **Display**: 1280x720 minimum resolution
- **Python**: 3.8 or higher

## 👨‍💻 Developer

**Savan Mohebbi**
- Institution: Amirkabir University of Technology (Tehran Polytechnic)
- Department: Civil Engineering
- Course: Fluid Mechanics

## 📄 License

This project is developed for educational purposes as part of the Fluid Mechanics course at Amirkabir University of Technology.

## 🤝 Contributing

This is an academic project. For suggestions or bug reports, please contact the developer.

## 📞 Support

For questions or issues, please contact through university channels.

## 🙏 Acknowledgments

- Amirkabir University of Technology
- Fluid Mechanics Course Instructors
- Civil Engineering Department

## 📝 Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed version history.

---

**Made with 💙 by Savan Mohebbi**  
*Amirkabir University of Technology - Civil Engineering*
