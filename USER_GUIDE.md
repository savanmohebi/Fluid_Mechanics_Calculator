# Fluid Mechanics Calculator v1.1 - User Guide

## 📖 Table of Contents
1. [Getting Started](#getting-started)
2. [Main Dashboard](#main-dashboard)
3. [Module Guides](#module-guides)
4. [Features Overview](#features-overview)
5. [Tips & Tricks](#tips--tricks)
6. [Troubleshooting](#troubleshooting)

---

## 🚀 Getting Started

### First Time Setup

1. **Install Python** (if not already installed)
   - Download Python 3.8 or higher from [python.org](https://python.org)
   - During installation, check "Add Python to PATH"

2. **Install Required Libraries**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the Application**
   ```bash
   python Fluid_Mechanics_Calculator_v1.1_Enhanced.py
   ```

### First Launch Experience

When you first launch the application, you'll see:
- **Splash Screen**: An animated loading screen showing initialization progress
- **Main Dashboard**: The central hub for accessing all calculation modules

---

## 🏠 Main Dashboard

### Interface Overview

#### Header Section
- **Title**: "🌊 Fluid Mechanics Calculator" with version information
- **Theme Toggle Button** (🌙/☀️): Switch between dark and light themes
- **About Button** (ℹ️): View application information and developer details

#### Module Cards
Four interactive cards representing each chapter:

1. **💧 Fluid Properties (Chapter 1)** - Blue
2. **⚖️ Fluid Statics (Chapter 2)** - Purple
3. **🌀 Fluid Dynamics (Chapter 3)** - Green
4. **📐 Dimensional Analysis (Chapter 4)** - Amber

Each card displays:
- Icon and chapter number
- Module title
- Brief description
- "Open Module →" button

#### Footer Section
- **Developer Information**: Credits and institution
- **System Status**: Real-time operational status

---

## 📚 Module Guides

### Chapter 1: Fluid Properties 💧

**Purpose**: Calculate fundamental fluid properties

**Features**:
- Density calculations
- Dynamic and kinematic viscosity
- Surface tension analysis
- Fluid database with common fluids (Water, Oil, Glycerin, Air)
- Temperature-dependent properties

**Common Use Cases**:
- Determining fluid type for analysis
- Property lookup for engineering calculations
- Viscosity comparisons
- Surface tension effects

**How to Use**:
1. Click the "Fluid Properties" card
2. Select a fluid from the dropdown or enter custom values
3. Input temperature if applicable
4. View calculated properties in real-time
5. Use the visualization tools for graphical representation

---

### Chapter 2: Fluid Statics ⚖️

**Purpose**: Analyze fluids at rest and pressure distributions

**Features**:
- Hydrostatic pressure calculations
- Pressure at depth
- Buoyancy and flotation analysis
- Manometer problems
- Forces on submerged surfaces (plane and curved)
- Center of pressure calculations

**Common Use Cases**:
- Dam design and analysis
- Underwater structure forces
- Buoyancy calculations for floating objects
- Manometer reading interpretation
- Tank and reservoir analysis

**How to Use**:
1. Click the "Fluid Statics" card
2. Select the problem type from the navigation menu
3. Enter the known parameters:
   - Fluid density
   - Depths/heights
   - Areas
   - Angles (if applicable)
4. Click "Calculate" to see results
5. View force diagrams and center of pressure locations

---

### Chapter 3: Fluid Dynamics 🌀

**Purpose**: Analyze fluids in motion

**Features**:
- Bernoulli's equation applications
- Energy equation calculations
- Flow rate and velocity analysis
- Continuity equation
- Pipe flow problems
- Head loss calculations
- Discharge through orifices and nozzles

**Common Use Cases**:
- Pipe system design
- Pump selection and analysis
- Flow measurement
- Energy analysis in flow systems
- Venturi meter calculations
- Orifice discharge calculations

**How to Use**:
1. Click the "Fluid Dynamics" card
2. Choose the analysis type (Bernoulli, Energy, Flow Rate, etc.)
3. Input parameters:
   - Pressures at different points
   - Velocities
   - Elevations
   - Pipe diameters
   - Fluid properties
4. Calculate results
5. Review energy grade line and hydraulic grade line visualizations

---

### Chapter 4: Dimensional Analysis 📐

**Purpose**: Apply dimensional analysis and similitude principles

**Features**:
- Dimensionless number calculations
  - Reynolds number (Re)
  - Froude number (Fr)
  - Weber number (We)
  - Mach number (Ma)
- Buckingham Pi theorem applications
- Dynamic similitude analysis
- Model-prototype scaling
- Froude and Reynolds similitude

**Common Use Cases**:
- Scale model design
- Wind tunnel testing
- Hydraulic model studies
- Flow regime identification
- Similarity analysis between systems

**How to Use**:
1. Click the "Dimensional Analysis" card
2. Select the similitude type or dimensionless group
3. For dimensionless numbers:
   - Enter velocity, length, density, viscosity
   - Calculate the number
   - Interpret the result (laminar/turbulent, etc.)
4. For similitude problems:
   - Input prototype dimensions
   - Specify scale ratio
   - Calculate model parameters
5. Review scaling relationships

---

## ✨ Features Overview

### Theme System

**Dark Theme** (Default)
- Easy on the eyes for extended use
- Professional appearance
- High contrast for better readability
- Ideal for low-light environments

**Light Theme**
- Clean, modern appearance
- Better for bright environments
- High visibility
- Print-friendly

**How to Switch**:
- Click the 🌙 (moon) or ☀️ (sun) icon in the header
- Theme changes instantly across the entire interface

### Interactive Elements

**Hover Effects**:
- Module cards highlight when you hover over them
- Border color changes to match the chapter color
- Buttons show hover states for better feedback

**Responsive Design**:
- Window can be resized
- Minimum size enforced for usability (850x700)
- Elements scale proportionally

### Navigation

**Module Access**:
- Click any module card to open that chapter
- Each module opens in a separate window
- Main dashboard remains accessible
- Can run multiple modules simultaneously

**Return to Dashboard**:
- Close individual module windows
- Dashboard stays open as the control center

---

## 💡 Tips & Tricks

### Workflow Optimization

1. **Keep Dashboard Open**: Leave the main dashboard open while working in modules
2. **Multiple Modules**: Open multiple modules simultaneously for complex problems
3. **Theme Preference**: Choose your preferred theme at the start of your session
4. **Unit Consistency**: Always use SI units unless otherwise specified

### Best Practices

**For Students**:
- Start with simpler problems in each chapter
- Use the built-in fluid database before custom inputs
- Compare calculated results with theoretical values
- Export or screenshot results for reports

**For Professionals**:
- Verify critical calculations with manual methods
- Use appropriate significant figures
- Document assumptions made in calculations
- Cross-reference with engineering handbooks

### Calculation Tips

**Fluid Properties**:
- Use standard fluids from database for consistency
- Account for temperature effects
- Check viscosity units (dynamic vs kinematic)

**Fluid Statics**:
- Always define your datum level clearly
- Watch sign conventions for pressure
- Verify depth measurements from free surface

**Fluid Dynamics**:
- Check if flow is laminar or turbulent first
- Account for all energy losses
- Verify continuity equation satisfaction

**Dimensional Analysis**:
- Double-check unit consistency
- Understand the physical meaning of dimensionless numbers
- Consider all relevant variables in Pi theorem

---

## 🔧 Troubleshooting

### Common Issues

**Problem**: Application won't start
- **Solution**: 
  - Verify Python 3.8+ is installed
  - Check all dependencies are installed: `pip install -r requirements.txt`
  - Try running from command line to see error messages

**Problem**: Module doesn't open when clicked
- **Solution**:
  - Ensure all module files are in the same directory
  - Check file names match exactly (case-sensitive)
  - Look for error message dialogs

**Problem**: Graphics/plots not displaying
- **Solution**:
  - Install matplotlib: `pip install matplotlib`
  - Check if numpy is installed: `pip install numpy`
  - Restart the application

**Problem**: Theme toggle not working
- **Solution**:
  - Allow a second for the interface to rebuild
  - Close and reopen the application
  - Check customtkinter is up to date

**Problem**: Calculation results seem incorrect
- **Solution**:
  - Verify all input units are SI
  - Check input values are in valid ranges
  - Review problem setup and assumptions
  - Compare with manual calculation

### Performance Issues

**Slow Startup**:
- First launch may be slower while Python compiles modules
- Subsequent launches will be faster
- Consider creating an executable for better startup time

**Laggy Interface**:
- Close unused modules
- Reduce window size if on low-end hardware
- Update graphics drivers
- Close other resource-intensive applications

### Installation Issues

**ImportError for customtkinter**:
```bash
pip install customtkinter --upgrade
```

**ImportError for PIL/Pillow**:
```bash
pip install Pillow
```

**Module not found errors**:
- Ensure you're running from the correct directory
- All .py files should be in the same folder
- Check file permissions

---

## 📞 Getting Help

### Resources

1. **README.md**: Overview and installation instructions
2. **CHANGELOG.md**: Version history and updates
3. **This Guide**: Comprehensive usage instructions

### Contact

For academic support or bug reports:
- Contact through university channels
- Email: Through AUT Civil Engineering department

### Reporting Issues

When reporting an issue, please include:
1. Python version (`python --version`)
2. Operating system
3. Steps to reproduce the problem
4. Error messages (if any)
5. Screenshots (if applicable)

---

## 🎓 Educational Use

This software is designed for:
- Engineering students learning fluid mechanics
- Homework and assignment calculations
- Lab report preparation
- Exam preparation and practice
- Research and design projects

**Academic Integrity**: 
- Understand the underlying principles
- Show your work in submissions
- Use as a verification tool, not a replacement for learning

---

## 🔄 Updates and Versions

**Current Version**: 1.1
**Release Date**: June 2024

**Checking for Updates**:
- Check the About dialog for version number
- Compare with CHANGELOG.md
- Look for new files in the project directory

---

## 📝 Keyboard Shortcuts (Future Feature)

Coming in v1.2:
- `Ctrl+1` to `Ctrl+4`: Quick module access
- `Ctrl+T`: Toggle theme
- `Ctrl+Q`: Quit application
- `F1`: Open help

---

**Happy Calculating! 🌊**

*Developed with ❤️ by Savan Mohebbi*  
*Amirkabir University of Technology - Civil Engineering*
