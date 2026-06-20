#!/bin/bash
# Build Script for Fluid Mechanics Calculator v1.1
# Creates standalone executable for Linux/Mac

echo "========================================"
echo "Fluid Mechanics Calculator v1.1"
echo "Build Script"
echo "========================================"
echo ""

# Check if PyInstaller is installed
if ! python3 -c "import PyInstaller" 2>/dev/null; then
    echo "[ERROR] PyInstaller not found!"
    echo "Installing PyInstaller..."
    pip3 install pyinstaller
    echo ""
fi

echo "[1/4] Cleaning previous builds..."
rm -rf build dist *.spec
echo "Done."
echo ""

echo "[2/4] Building executable..."
pyinstaller --onefile --windowed \
    --name "FluidMechanicsCalculator_v1.1" \
    --add-data "FLUID_PROPERTIES_GUI.py:." \
    --add-data "fluid_statics_gui.py:." \
    --add-data "fluid_dynamic_gui.py:." \
    --add-data "DIMENSIONAL_ANALYSIS_GUI.py:." \
    --add-data "FLUID_PROPERTIES_ENGINE.py:." \
    --add-data "fluid_statics_engine.py:." \
    --add-data "FLUID_DYNAMICS_ENGINE.py:." \
    --add-data "DIMENSIONAL_ANALYSIS_ENGINE.py:." \
    Fluid_Mechanics_Calculator_v1.1_Enhanced.py

if [ $? -ne 0 ]; then
    echo "[ERROR] Build failed!"
    exit 1
fi
echo "Done."
echo ""

echo "[3/4] Verifying build..."
if [ -f "dist/FluidMechanicsCalculator_v1.1" ]; then
    echo "✓ Executable created successfully!"
    echo "Location: dist/FluidMechanicsCalculator_v1.1"
    chmod +x "dist/FluidMechanicsCalculator_v1.1"
else
    echo "[ERROR] Executable not found!"
    exit 1
fi
echo ""

echo "[4/4] Creating release package..."
mkdir -p release
cp "dist/FluidMechanicsCalculator_v1.1" "release/"
cp "README_v1.1.md" "release/README.md"
cp "QUICK_START.md" "release/"
cp "USER_GUIDE.md" "release/"
cp "CHANGELOG.md" "release/"
echo "Done."
echo ""

echo "========================================"
echo "BUILD COMPLETE!"
echo "========================================"
echo ""
echo "Executable: release/FluidMechanicsCalculator_v1.1"
echo "Documentation: release/*.md"
echo ""
echo "You can now distribute the 'release' folder!"
echo ""
