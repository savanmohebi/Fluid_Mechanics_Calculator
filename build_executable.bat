@echo off
REM Build Script for Fluid Mechanics Calculator v1.1
REM Creates standalone Windows executable

echo ========================================
echo Fluid Mechanics Calculator v1.1
echo Build Script
echo ========================================
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo [ERROR] PyInstaller not found!
    echo Installing PyInstaller...
    pip install pyinstaller
    echo.
)

echo [1/4] Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del /q *.spec
echo Done.
echo.

echo [2/4] Building executable...
pyinstaller --onefile --windowed ^
    --name "FluidMechanicsCalculator_v1.1" ^
    --add-data "FLUID_PROPERTIES_GUI.py;." ^
    --add-data "fluid_statics_gui.py;." ^
    --add-data "fluid_dynamic_gui.py;." ^
    --add-data "DIMENSIONAL_ANALYSIS_GUI.py;." ^
    --add-data "FLUID_PROPERTIES_ENGINE.py;." ^
    --add-data "fluid_statics_engine.py;." ^
    --add-data "FLUID_DYNAMICS_ENGINE.py;." ^
    --add-data "DIMENSIONAL_ANALYSIS_ENGINE.py;." ^
    --icon=NONE ^
    Fluid_Mechanics_Calculator_v1.1_Enhanced.py

if errorlevel 1 (
    echo [ERROR] Build failed!
    pause
    exit /b 1
)
echo Done.
echo.

echo [3/4] Verifying build...
if exist "dist\FluidMechanicsCalculator_v1.1.exe" (
    echo ✓ Executable created successfully!
    echo Location: dist\FluidMechanicsCalculator_v1.1.exe
) else (
    echo [ERROR] Executable not found!
    pause
    exit /b 1
)
echo.

echo [4/4] Creating release package...
if not exist "release" mkdir release
copy "dist\FluidMechanicsCalculator_v1.1.exe" "release\" >nul
copy "README_v1.1.md" "release\README.md" >nul
copy "QUICK_START.md" "release\" >nul
copy "USER_GUIDE.md" "release\" >nul
copy "CHANGELOG.md" "release\" >nul
echo Done.
echo.

echo ========================================
echo BUILD COMPLETE!
echo ========================================
echo.
echo Executable: release\FluidMechanicsCalculator_v1.1.exe
echo Documentation: release\*.md
echo.
echo You can now distribute the 'release' folder!
echo.
pause
