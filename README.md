# Fluid Mechanics Calculator v1.1

A desktop engineering calculator for common Fluid Mechanics coursework and civil engineering analysis. Version 1.1 provides a modern CustomTkinter dashboard and launches focused calculators for fluid properties, statics, dynamics, and dimensional analysis.

## Features

- Modern v1.1 dashboard with dark/light theme support.
- Fluid Properties calculator for viscosity, surface tension, vapor pressure, compressibility, and related properties.
- Fluid Statics calculator for pressure, hydrostatic force, buoyancy, stability, and rigid-body fluid motion.
- Fluid Dynamics calculator for continuity, Bernoulli, Reynolds number, Darcy-Weisbach losses, drag, and Venturi flow.
- Dimensional Analysis calculator for Reynolds, Froude, Weber, Mach, Euler numbers, and similitude problems.
- Matplotlib visualizations embedded in module windows.
- Clean package-style source layout with stable imports.

## Project Structure

```text
v1.1/
├── main.py
├── requirements.txt
├── README.md
├── CHANGELOG.md
├── USER_GUIDE.md
├── assets/
└── src/
    ├── __init__.py
    ├── engines/
    │   ├── __init__.py
    │   ├── dimensional_analysis_engine.py
    │   ├── fluid_dynamics_engine.py
    │   ├── fluid_properties_engine.py
    │   └── fluid_statics_engine.py
    ├── gui/
    │   ├── __init__.py
    │   ├── dimensional_analysis_gui.py
    │   ├── fluid_dynamics_gui.py
    │   ├── fluid_properties_gui.py
    │   ├── fluid_statics_gui.py
    │   └── splash_screen.py
    └── utils/
        └── __init__.py
```

Older or uncertain files were moved to `legacy_or_old_versions/` at the repository root.

## Installation

Use Python 3.8 or newer. A virtual environment is recommended.

```bash
cd "C:\Users\savan\Desktop\AUT\Fluid mechanics\calc\v1.1"
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

On Linux or WSL:

```bash
cd "/mnt/c/Users/savan/Desktop/AUT/Fluid mechanics/calc/v1.1"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running the App

From inside the `v1.1` folder, run:

```bash
python main.py
```

On systems where Python 3 is invoked as `python3`, run:

```bash
python3 main.py
```

## Dependencies

- `customtkinter` for the modern GUI.
- `numpy` for numerical calculations and plotted data ranges.
- `matplotlib` for embedded charts.
- `Pillow` as an optional image support dependency used by CustomTkinter assets.

`tkinter` is not listed in `requirements.txt` because it is part of the Python standard library on most installations. If `tkinter` is missing on Linux, install your distribution's Tk package, for example `python3-tk` on Debian/Ubuntu.

## Troubleshooting

- `ModuleNotFoundError: customtkinter`: run `pip install -r requirements.txt` from the `v1.1` folder.
- `No module named src`: make sure you start the app with `python main.py` from inside `v1.1`. The dashboard also launches modules with the project root as the working directory.
- GUI does not appear on Linux/WSL: confirm an X/Wayland display is available and `tkinter` is installed.
- Module buttons do nothing: start the app from a terminal so launch errors are visible, then confirm all dependencies are installed.

## What Changed From Previous Versions

- The latest enhanced v1.1 entry point was standardized as `main.py`.
- Uppercase and inconsistent filenames were renamed to Python-safe lowercase module names.
- Engines and GUI files were separated into `src/engines` and `src/gui`.
- Fragile subprocess launches using old root filenames were replaced with package module launches.
- Legacy files and build outputs were separated from the active v1.1 source tree.
